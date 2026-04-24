---
name: fastapi-config-01
description: Opinionated FastAPI project conventions (SQLModel, Alembic, pytest, Docker). Use with the [Official FastAPI skill](../fastapi/SKILL.md) when building or refactoring REST APIs in Python. Covers layout, async DB sessions, repositories, services, auth, and tests.
---

# FastAPI

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

### Nesting under `app/api/` only (versioning)

The extra depth under **`app/api/v1/endpoints/`** is **not** a general “prefer deep trees” rule. It applies **only** to the HTTP API package so you can add **`v2/`**, **`v3/`**, etc. beside `v1/` without reshuffling the rest of the codebase.

Everywhere else in this layout—**`core/`**, **`models/`**, **`schemas/`**, **`services/`**, **`repositories/`**—stay **shallow and flat** (one package per concern, files grouped by name, no gratuitous `impl/` or `internal/` chains). That matches [python-project-structure](../python-project-structure/SKILL.md): prefer flat hierarchies and add depth **only** for a clear reason; here the reason is **API versioning under `api/`**, not deeper nesting for services or models.

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
