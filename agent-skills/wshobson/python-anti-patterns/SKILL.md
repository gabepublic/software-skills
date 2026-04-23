---
name: python-anti-patterns
description: Use this skill when reviewing Python code for common anti-patterns to avoid. HTTP examples use HTTPX (aligned with the FastAPI toolchain). Use as a checklist when reviewing code, before finalizing implementations, or when debugging issues that might stem from known bad practices.
---

# Python Anti-Patterns Checklist

A reference checklist of common mistakes and anti-patterns in Python code. Review this before finalizing implementations to catch issues early.

## When to Use This Skill

- Reviewing code before merge
- Debugging mysterious issues
- Teaching or learning Python best practices
- Establishing team coding standards
- Refactoring legacy code

**Note:** This skill focuses on what to avoid. For guidance on positive patterns and architecture, see [python-design-patterns](../python-design-patterns/SKILL.md).

**With design & code-style skills:** Turning on **Ruff, ty, tests, Pydantic, repositories, and clear layers** ([python-code-style](../python-code-style/SKILL.md)) is **not** premature abstraction—those are **quality gates** everyone pays once. The **rule of three** in design patterns applies to **deduplicating business logic**, not to postponing linters or boundaries. Prefer duplication over a **wrong shared** primitive; avoid duplication **across public API surfaces** when it hides inconsistent validation.

**HTTP clients:** Prefer **HTTPX** for sync and async HTTP—the same default as the [Official FastAPI skill](../fastapi/SKILL.md) and [FastAPI other-tools](../fastapi/references/other-tools.md) (HTTPX over Requests). Examples below use HTTPX so they stay consistent with [python-testing-patterns](../python-testing-patterns/SKILL.md).

## Infrastructure Anti-Patterns

### Scattered Timeout/Retry Logic

```python
# BAD: Timeout logic duplicated everywhere
import httpx

def fetch_user(client: httpx.Client, user_id: str) -> httpx.Response | None:
    try:
        return client.get(f"/users/{user_id}", timeout=30.0)
    except httpx.TimeoutException:
        logger.warning("Timeout fetching user")
        return None

def fetch_orders(client: httpx.Client, user_id: str) -> httpx.Response | None:
    try:
        return client.get(f"/users/{user_id}/orders", timeout=30.0)
    except httpx.TimeoutException:
        logger.warning("Timeout fetching orders")
        return None
```

**Fix:** Centralize in decorators or client wrappers.

```python
# GOOD: Centralized retry logic on a pooled client (HTTPX + tenacity)
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

client = httpx.Client(base_url="https://api.example.com", timeout=30.0)

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def http_get(path: str) -> httpx.Response:
    response = client.get(path)
    response.raise_for_status()
    return response
```

### Double Retry

```python
# BAD: Retrying at multiple layers
@retry(max_attempts=3)  # Application retry
def call_service():
    return client.request()  # Client also has retry configured!
```

**Fix:** Retry at one layer only. Know your infrastructure's retry behavior.

### Hard-Coded Configuration

```python
# BAD: Secrets and config in code
DB_HOST = "prod-db.example.com"
API_KEY = "sk-12345"

def connect():
    return psycopg.connect(f"host={DB_HOST}...")
```

**Fix:** Use environment variables with typed settings.

```python
# GOOD
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = Field(alias="DB_HOST")
    api_key: str = Field(alias="API_KEY")

settings = Settings()
```

## Architecture Anti-Patterns

### Exposed Internal Types

```python
# BAD: Leaking the SQLModel table to the API
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):  # table model — internal
    id: str = Field(primary_key=True)
    email: str
    password_hash: str  # must never leak

@app.get("/users/{id}")
def get_user(id: str, session: SessionDep) -> User:  # leaks password_hash
    return session.get(User, id)
```

**Fix:** Use DTOs / response models.

```python
# GOOD: public schema built from the table instance (Pydantic v2 + SQLModel)
from pydantic import ConfigDict
from sqlmodel import SQLModel

class UserPublic(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str

@app.get("/users/{id}")
def get_user(id: str, session: SessionDep) -> UserPublic:
    user = session.get(User, id)
    return UserPublic.model_validate(user)
```

Aligned with [fastapi-config-01](../fastapi-config-01/SKILL.md) and [fastapi/other-tools](../fastapi/references/other-tools.md) — prefer SQLModel over SQLAlchemy, and keep table models (`table=True`) out of response signatures.

### Mixed I/O and Business Logic

```python
# BAD: SQL embedded in business logic
from sqlmodel import select

async def calculate_discount(user_id: str, session: AsyncSession) -> float:
    user = await session.get(User, user_id)
    orders = (await session.exec(select(Order).where(Order.user_id == user_id))).all()
    # Business logic mixed with data access
    if len(orders) > 10:
        return 0.15
    return 0.0
```

**Fix:** Repository pattern. Keep business logic pure.

```python
# GOOD
def calculate_discount(user: User, orders: list[Order]) -> float:
    # Pure business logic, easily testable
    if len(orders) > 10:
        return 0.15
    return 0.0
```

## Error Handling Anti-Patterns

### Bare Exception Handling

**Scope:** The anti-pattern is *silent* broad catches — `except Exception: pass` (or `except:` with no re-raise, no log, no typed outcome). Three **intentional** uses of `except Exception` are **not** covered by this rule:

1. **Transaction / cleanup context managers** that roll back and then `raise` — see [python-resource-management](../python-resource-management/SKILL.md) *Pattern 3*.
2. **Batch processors** that capture per-item failures into a `BatchResult` — see [python-error-handling](../python-error-handling/SKILL.md) *Pattern 7* and the *Ignored Partial Failures* section below.
3. **`fail_safe` decorators** that log and return a default for non-critical, degradable paths — see [python-resilience](../python-resilience/SKILL.md) *Pattern 9*.

In all three, the catch is broad **on purpose** and every failure is either re-raised, captured, or logged. What this rule forbids is swallowing without a trace.

```python
# BAD: Swallowing all exceptions
try:
    process()
except Exception:
    pass  # Silent failure - bugs hidden forever
```

**Fix:** Catch specific exceptions. Log or handle appropriately.

```python
# GOOD
try:
    process()
except ConnectionError as e:
    logger.warning("Connection failed, will retry", error=str(e))
    raise
except ValueError as e:
    logger.error("Invalid input", error=str(e))
    raise BadRequestError(str(e))
```

### Ignored Partial Failures

```python
# BAD: Stops on first error
def process_batch(items):
    results = []
    for item in items:
        result = process(item)  # Raises on error - batch aborted
        results.append(result)
    return results
```

**Fix:** Capture both successes and failures. Use the generic `BatchResult[T]` shape defined in [python-error-handling](../python-error-handling/SKILL.md) *Pattern 7* so both skills return the same type.

```python
# GOOD
from python_error_handling import BatchResult  # same shape as python-error-handling

def process_batch(items: list[Item]) -> BatchResult[ProcessedItem]:
    succeeded: dict[int, ProcessedItem] = {}
    failed: dict[int, Exception] = {}
    for idx, item in enumerate(items):
        try:
            succeeded[idx] = process(item)
        except Exception as e:
            failed[idx] = e
    return BatchResult(succeeded=succeeded, failed=failed)
```

### Missing Input Validation

```python
# BAD: No validation
def create_user(data: dict):
    return User(**data)  # Crashes deep in code on bad input
```

**Fix:** Validate early at API boundaries.

```python
# GOOD
def create_user(data: dict) -> User:
    validated = CreateUserInput.model_validate(data)
    return User.from_input(validated)
```

## Resource Anti-Patterns

### Unclosed Resources

```python
# BAD: File never closed
def read_file(path):
    f = open(path)
    return f.read()  # What if this raises?
```

**Fix:** Use context managers.

```python
# GOOD
def read_file(path):
    with open(path) as f:
        return f.read()
```

### Blocking in Async

**Scope:** This rule is about blocking calls **inside an `async def`**. It does **not** say you must make every FastAPI path operation `async`. The [Official FastAPI skill](../fastapi/SKILL.md) (*Async vs Sync path operations*) explicitly recommends plain `def` by default — FastAPI runs it in a threadpool, so blocking libraries are safe there. Only once a function is `async def` does the anti-pattern below apply.

```python
# BAD: Blocks the entire event loop
import time
import httpx

async def fetch_data(url: str):
    time.sleep(1)  # Blocks everything!
    httpx.get(url, timeout=30.0)  # sync HTTP in async def — also blocks!
```

**Fix (preferred in FastAPI projects): use `async def` with async-native libraries.**

```python
# GOOD
import asyncio
import httpx

async def fetch_data(url: str):
    await asyncio.sleep(1)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
```

**Fix (when a blocking library is unavoidable): bridge with Asyncer.** Per [fastapi/other-tools](../fastapi/references/other-tools.md), prefer **Asyncer** (`asyncify` / `syncify`) over AnyIO or raw `asyncio` for crossing the sync/async boundary.

```python
from asyncer import asyncify

async def fetch_via_blocking_lib(url: str) -> dict:
    return await asyncify(blocking_lib.get)(url)
```

If Asyncer isn't a dependency, fall back to `asyncio.to_thread(...)` (see [async-python-patterns](../async-python-patterns/SKILL.md)).

## Type Safety Anti-Patterns

### Missing Type Hints

```python
# BAD: No types
def process(data):
    return data["value"] * 2
```

**Fix:** Annotate all public functions.

```python
# GOOD
def process(data: dict[str, int]) -> int:
    return data["value"] * 2
```

### Untyped Collections

```python
# BAD: Generic list without type parameter
def get_users() -> list:
    ...
```

**Fix:** Use type parameters.

```python
# GOOD
def get_users() -> list[User]:
    ...
```

## Testing Anti-Patterns

### Only Testing Happy Paths

```python
# BAD: Only tests success case
def test_create_user():
    user = service.create_user(valid_data)
    assert user.id is not None
```

**Fix:** Test error conditions and edge cases.

```python
# GOOD
def test_create_user_success():
    user = service.create_user(valid_data)
    assert user.id is not None

def test_create_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        service.create_user(invalid_email_data)

def test_create_user_duplicate_email():
    service.create_user(valid_data)
    with pytest.raises(ConflictError):
        service.create_user(valid_data)
```

### Over-Mocking

```python
# BAD: Mocking everything
def test_user_service():
    mock_repo = Mock()
    mock_cache = Mock()
    mock_logger = Mock()
    mock_metrics = Mock()
    # Test doesn't verify real behavior
```

**Fix:** Use integration tests for critical paths. Mock only external services.

## Quick Review Checklist

Before finalizing code, verify:

- [ ] No scattered timeout/retry logic (centralized)
- [ ] No double retry (app + infrastructure)
- [ ] No hard-coded configuration or secrets
- [ ] No exposed internal types (ORM models, protobufs)
- [ ] No mixed I/O and business logic
- [ ] No bare `except Exception: pass`
- [ ] No ignored partial failures in batches
- [ ] No missing input validation
- [ ] No unclosed resources (using context managers)
- [ ] No blocking calls in async code
- [ ] All public functions have type hints
- [ ] Collections have type parameters
- [ ] Error paths are tested
- [ ] Edge cases are covered

## Common Fixes Summary

| Anti-Pattern | Fix |
|-------------|-----|
| Scattered retry logic | Centralized decorators |
| Hard-coded config | Environment variables + pydantic-settings |
| Exposed ORM models | DTO/response schemas |
| Mixed I/O + logic | Repository pattern |
| Bare except | Catch specific exceptions |
| Batch stops on error | Return BatchResult with successes/failures |
| No validation | Validate at boundaries with Pydantic |
| Unclosed resources | Context managers |
| Blocking in async | `httpx.AsyncClient` (or other async-native I/O) |
| Missing types | Type annotations on all public APIs |
| Only happy path tests | Test errors and edge cases |
