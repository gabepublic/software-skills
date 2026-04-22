# Patterns

Use the patterns below as the default templates whenever you generate, extend, or refactor application code for this project. Each pattern is a canonical slice of the agreed stack, follow them so stay consistent across the codebase. When a detail is not specified here, follow [Official FastAPI skill](.agents/skills/fastapi/SKILL.md) for framework-level FastAPI and Pydantic conventions.

## Implementation Patterns

### Pattern 1: Complete FastAPI Application

```python
# app/main.py
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan events."""
    # Startup: e.g. create DB tables, warm caches, open external clients
    yield
    # Shutdown: close connections and clients

app = FastAPI(title="API Template", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

# app/api/v1/router.py
from fastapi import APIRouter
api_router = APIRouter(prefix="/api/v1", tags=["api"])

# app/core/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_V1_STR: str = "/api/v1"

@lru_cache
def get_settings() -> Settings:
    return Settings()

# app/core/database.py
from collections.abc import AsyncIterator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from app.core.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Models should inherit SQLModel with table=True; metadata is SQLModel.metadata.
async def get_db() -> AsyncIterator[AsyncSession]:
    """Dependency for database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
SessionDep = Annotated[AsyncSession, Depends(get_db)]

# app/api/v1/endpoints/examples.py
from fastapi import APIRouter
from app.core.database import SessionDep

router = APIRouter()

@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/example-async-db")
async def example(session: SessionDep) -> dict[str, str]:
    # Only use async def when everything awaited here is truly async/non-blocking.
    ...

# GET /api/v1/example-async-db
```

### Pattern 2: CRUD Repository Pattern

```python
# repositories/base_repository.py
from typing import Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
IdType = TypeVar("IdType")

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType, IdType]):
    """Base repository for CRUD operations."""
    def __init__(self, model: type[ModelType], pk_field: str = "id") -> None:
        self.model = model
        self.pk_field = pk_field

    async def get(self, db: AsyncSession, id_value: IdType) -> ModelType | None:
        pk_col = getattr(self.model, self.pk_field)
        result = await db.execute(select(self.model).where(pk_col == id_value))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id_value: IdType) -> bool:
        obj = await self.get(db, id)
        if obj is None:
            return False
        await db.delete(obj)
        return True

# repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate, int]):
    """User-specific repository."""
    def __init__(self) -> None:
        super().__init__(User, pk_field="id")

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

user_repository = UserRepository()

# app/models/user.py
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    is_active: bool = True
    # ...

# app/schemas/user.py
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    email: str
    password: str  # public input

class UserCreateDB(SQLModel):
    email: str
    hashed_password: str  # internal write schema

class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None  # public update input

class UserUpdateDB(SQLModel):
    email: str | None = None
    hashed_password: str | None = None
    is_active: bool | None = None
    
# services/user_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserCreateDB, UserUpdate, UserUpdateDB

class UserService:
    async def create_user(self, db: AsyncSession, user_in: UserCreate):
        existing = await user_repository.get_by_email(db, user_in.email)
        if existing:
            raise ValueError("Email already registered")

        to_db = UserCreateDB(email=user_in.email, hashed_password=get_password_hash(user_in.password))
        return await user_repository.create(db, to_db)

    async def update_user(self, db: AsyncSession, user_id: int, user_in: UserUpdate):
        user = await user_repository.get(db, user_id)
        if user is None:
            return None
        data = user_in.model_dump(exclude_unset=True)
        password = data.pop("password", None)
        if password:
            data["hashed_password"] = get_password_hash(password)
        return await user_repository.update(db, user, UserUpdateDB.model_validate(data))
```

**Service layer:** Implement services as in **Pattern 2** (repository + `UserService` + separate public vs DB schemas). The endpoint section below shows how to expose `UserServiceDep` on routes. Avoid duplicating a second, conflicting `UserService` definition in the same codebase.

## Pattern 3: API Endpoints with Dependencies

```python
# api/v1/endpoints/users.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.api.dependencies import get_current_user
from app.core.database import SessionDep
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_service import UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])
CurrentUserDep = Annotated[User, Depends(get_current_user)]

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: SessionDep, svc: UserServiceDep) -> User:
    try:
        return await svc.create_user(db, user_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get("/me", response_model=User)
def read_current_user(current_user: CurrentUserDep) -> User:
    return current_user

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: Annotated[int, Path(ge=1)], db: SessionDep, current_user: CurrentUserDep, svc: UserServiceDep) -> User:
    user = await svc.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: Annotated[int, Path(ge=1)], user_in: UserUpdate, db: SessionDep, current_user: CurrentUserDep, svc: UserServiceDep) -> User:
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = await svc.update_user(db, user_id, user_in)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: Annotated[int, Path(ge=1)], db: SessionDep, current_user: CurrentUserDep, svc: UserServiceDep) -> None:
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    deleted = await svc.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
```

## Pattern 4: Authentication & Authorization

```python
# core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)

# api/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import get_settings
from app.core.database import SessionDep
from app.core.security import ALGORITHM
from app.schemas.user import User
from app.services.user_service import UserServiceDep

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(db: SessionDep, token: Annotated[str, Depends(oauth2_scheme)], svc: UserServiceDep) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await svc.get_user(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user
```

## Testing Pattern

```python
# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.main import app
from app.core.database import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```
