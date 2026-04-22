---
name: fastapi-config-01
description: Opinionated FastAPI project conventions (SQLModel, Alembic, pytest, Docker). Use with the [Official FastAPI skill](.agents/skills/fastapi/SKILL.md) when building or refactoring REST APIs in Python. Covers layout, async DB sessions, repositories, services, auth, and tests.
---

# FastAPI

Project specific FastAPI skill to align with the project specifications and configurations that are listed below.

Apply this skill in conjunction with:

- The [Official FastAPI skill](.agents/skills/fastapi/SKILL.md). To refresh from upstream: `npx skills add https://github.com/fastapi/fastapi --skill fastapi`, or see [skills.sh/fastapi](https://skills.sh/fastapi/fastapi/fastapi). 

- Other Python skills under `.agents/skills/`.

When instructions conflict, prefer **this file** for project stack and layout; prefer [Official FastAPI skill](.agents/skills/fastapi/SKILL.md) for framework-level FastAPI and Pydantic conventions.


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
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Non-functional requirements

- **Release**: create the `Dockerfile` that is commonly used for deployment.


## Patterns

Use the patterns as the default templates whenever you generate, extend, or refactor application code for this project. See [Patterns](references/patterns.md) for detailed patterns.
