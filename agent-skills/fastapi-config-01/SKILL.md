---
name: fastapi-config-01
description: Opinionated FastAPI project conventions (SQLModel, Alembic, pytest, Docker). Use with the [Official FastAPI skill](../fastapi/SKILL.md) when building or refactoring REST APIs in Python. Covers layout, async DB sessions, repositories, services, auth, and tests.
---

# FastAPI Config-01

Project specific FastAPI skill to align with the project specifications and configurations that are listed below.

Apply this skill in conjunction with:

- The [Official FastAPI skill](../fastapi/SKILL.md). To refresh from upstream: `npx skills add https://github.com/fastapi/fastapi --skill fastapi`, or see [skills.sh/fastapi](https://skills.sh/fastapi/fastapi/fastapi). 

- Other Python skills under `../`.

Where **this skill** or [Patterns](references/patterns.md) are silent, follow the [Official FastAPI skill](../fastapi/SKILL.md); **this skill** does not define alternate FastAPI or Pydantic framework rules.


## When to Use This Skill

- Starting new FastAPI projects from scratch
- Implementing REST APIs with Python
- Building performant web services
- Setting up API projects with proper structure and testing


## Project Stack (fixed choices)

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | FastAPI |
| Data validation and serialization | Pydantic |
| Database ORM and Modeling | SQLModel |
| Database - development | SQLite |
| Database - production | PostgreSQL |
| Database migration tool | Alembic |
| Authentication | authlib, python-jose[cryptography] |
| Encryption | passlib, bcrypt |
| HTTP Communication | HTTPX |
| Testing | pytest, pytest-cov |


## Project Structure

**Recommended Layout:**

```
api-app/
├── app/
|    ├── adapters/               # Adapters
|    ├── api/                    # API routes
|    │   ├── v1/
|    │   │   ├── endpoints/
|    │   │   │   ├── users.py
|    │   │   │   ├── auth.py
|    │   │   │   └── items.py
|    │   │   └── router.py
|    │   └── dependencies.py     # Shared dependencies
|    ├── core/                   # Core configuration
|    │   ├── config.py
|    │   ├── security.py
|    │   └── database.py
|    ├── models/                 # Database models
|    │   ├── user.py
|    │   └── item.py
|    ├── schemas/                # Pydantic schemas
|    │   ├── user.py
|    │   └── item.py
|    ├── services/               # Business logic
|    │   ├── user_service.py
|    │   └── auth_service.py
|    ├── repositories/           # Data access
|    │   ├── user_repository.py
|    │   └── item_repository.py
|    └── main.py                 # Application entry
├── tests                        # tests folder
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Nesting and Versioning Policy

Use extra depth under app/api/v1/endpoints/ as the default versioning mechanism for HTTP contracts, so you can add v2/, v3/, etc. beside v1/ without reshuffling unrelated code.

Outside app/api/, keep packages shallow and flat by default—especially core/, models/, schemas/, services/, and repositories/ (one package per concern, files grouped by domain, no gratuitous impl//internal/ chains).

A versioned subtree outside api/ is allowed when there is a clear, durable contract difference tied to API versions (for example, materially different request/response shapes, orchestration rules, or adapter behavior). In those cases, use focused versioned namespaces such as schemas/v1, services/v1, or adapters/v1, and keep the rest of the package flat.

Do not introduce version folders preemptively. Add them only when:

differences are substantial (not minor field drift),
parallel support for multiple API versions is required, and
the version boundary improves clarity more than it increases navigation cost.
This follows python-project-structure: prefer flat hierarchies, and add depth only for a clear architectural reason.

## Non-functional requirements

- **Release**: create the `Dockerfile` that is commonly used for deployment.

## Testing

- **New HTTP behavior**: When you add or change a route, dependency, or response contract, add or update tests under `tests/` so the behavior is locked in. Prefer one focused test module per area (e.g. `tests/test_v1_version.py` for `GET /v1/version`) or group related routes in a single file if they stay small.
- **How to test**: Follow [python-testing-patterns](../python-testing-patterns/SKILL.md) (pytest, meaningful coverage). For FastAPI apps, the [Testing Pattern](references/patterns.md) shows `httpx.AsyncClient` with `ASGITransport`; synchronous `fastapi.testclient.TestClient` is also fine for simple routes without async fixtures.
- **CI mindset**: Run `uv run pytest` (and optionally `uv run pytest --cov=app`) before considering the change done.

## Patterns

Use the patterns as the default templates whenever you generate, extend, or refactor application code for this project. See [Patterns](references/patterns.md) for detailed patterns.


## Choosing `def` vs `async def`

When implementing FastAPI routes, dependencies, or background work that touches asyncio, thread pools, or blocking I/O, consult the [Choosing `def` vs `async def`](references/def-vs-async-def.md).

## Required Fields in Pydantic Models (Skill Conformance)

To stay aligned with the **Official FastAPI** skill, do not use ellipsis (...) to mark required fields in Pydantic models.

Use plain type annotations for requiredness, and use `Field()` only for constraints/metadata when needed.

Do this:
```
from pydantic import BaseModel, Field
class CreateResponseRequest(BaseModel):
    model: str
    reasoning_effort: str = Field(description="Reasoning level, e.g. low/medium/high")
    instructions: str
    input: str
    max_token_limit: int = Field(gt=0, description="Maximum output token budget")
```

Avoid this:
```
from pydantic import BaseModel, Field
class CreateResponseRequest(BaseModel):
    model: str = Field(..., description="Target model")
    reasoning_effort: str = Field(..., description="Reasoning level")
    instructions: str = Field(..., description="System instructions")
```

Use `Field(...)` ellipsis only if a framework edge case truly requires it; otherwise treat it as a conformance violation in this project.

Review check: reject or refactor any schema using `Field(...)` ellipsis for required fields.
