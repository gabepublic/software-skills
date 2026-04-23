---
name: python-code-style
description: Python code style, linting, formatting, naming conventions, and documentation standards. Prefer uv, Ruff, and ty (aligned with the FastAPI toolchain). Use when writing new code, reviewing style, configuring tools, writing docstrings, or establishing project standards.
---

# Python Code Style & Documentation

Consistent code style and clear documentation make codebases maintainable and collaborative. This skill covers modern Python tooling, naming conventions, and documentation standards.

**Toolchain:** Prefer **uv** (environments and dependencies), **Ruff** (lint + format), and **ty** (type checking), matching the [FastAPI other-tools reference](../fastapi/references/other-tools.md). **mypy** or **pyright** remain valid alternatives if a project already standardizes on them.

**Duplication vs tooling:** Enable **uv, Ruff, ty**, imports policy, and docstring norms **immediately**. Defer **merging similar implementations** until you know they share one contract—the [python-design-patterns](../python-design-patterns/SKILL.md) **rule of three** applies to abstractions, not to whether you add a formatter on day one.

## When to Use This Skill

- Setting up linting and formatting for a new project
- Writing or reviewing docstrings
- Establishing team coding standards
- Configuring uv, Ruff, or ty
- Reviewing code for style consistency
- Creating project documentation

## Core Concepts

### 1. Automated Formatting

Let tools handle formatting debates. Configure once, enforce automatically.

### 2. Consistent Naming

Follow PEP 8 conventions with meaningful, descriptive names.

### 3. Documentation as Code

Docstrings should be maintained alongside the code they describe.

### 4. Type Annotations

Modern Python code should include type hints for all public APIs.

## Quick Start

Use **uv** to manage the environment, then add dev tools (see [uv](https://docs.astral.sh/uv/) if needed):

```bash
uv init  # or use an existing project with pyproject.toml
uv add --dev ruff ty
```

Configure **Ruff** and **ty** in `pyproject.toml` (patterns below). Run checks:

```bash
uv run ruff check --fix .
uv run ruff format .
uv run ty check
```

Minimal **ty** fragment (full **Ruff** example in Pattern 1):

```toml
[tool.ty.environment]
python-version = "3.12"  # Optional if ty can infer from requires-python / the venv

[tool.ty.rules]
all = "error"  # Treat enabled diagnostics as errors; tune per-file overrides as needed
```

## Fundamental Patterns

### Pattern 1: Modern Python Tooling (uv + Ruff)

Use **uv** to create/sync virtual environments and lock dependencies. Use **Ruff** as the linter and formatter; it replaces flake8, isort, and black with one fast tool.

When building **FastAPI** apps, add Ruff’s **`FAST`** rules (FastAPI-specific lint checks), as suggested in the [FastAPI other-tools reference](../fastapi/references/other-tools.md).

```toml
# pyproject.toml
[tool.ruff]
line-length = 120
target-version = "py312"  # Adjust based on your project's minimum Python version

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "SIM",  # flake8-simplify
    "FAST", # FastAPI — omit if the project is not FastAPI
]
ignore = ["E501"]  # Line length handled by formatter

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Run with:

```bash
uv run ruff check --fix .  # Lint and auto-fix
uv run ruff format .       # Format code
```

### Pattern 2: Type Checking with ty

Use **ty** for static type checking when it is available—same guidance as the [FastAPI other-tools reference](../fastapi/references/other-tools.md). It reads `[tool.ty]` in `pyproject.toml` (see [ty configuration](https://docs.astral.sh/ty/reference/configuration/)).

```toml
# pyproject.toml
[tool.ty.environment]
python-version = "3.12"  # Optional; ty can infer from requires-python / the active venv

[tool.ty.rules]
all = "error"

# Optional: relax diagnostics for tests (adjust globs to your layout)
# [tool.ty.analysis]
# allowed-unresolved-imports = ["tests.**"]
```

Run:

```bash
uv run ty check
```

Quick ad-hoc runs without adding `ty` to the project:

```bash
uvx ty check
```

**Alternatives:** Teams on **mypy** (`[tool.mypy]`) or **pyright** (`[tool.pyright]`) should keep one checker in CI and match the rest of this skill (strictness, typed public APIs). Prefer **ty** for new FastAPI-aligned projects to stay consistent with the FastAPI skill.

### Pattern 3: Naming Conventions

Follow PEP 8 with emphasis on clarity over brevity.

**Files and Modules:**

```python
# Good: Descriptive snake_case
user_repository.py
order_processing.py
http_client.py

# Avoid: Abbreviations
usr_repo.py
ord_proc.py
http_cli.py
```

**Classes and Functions:**

```python
# Classes: PascalCase
class UserRepository:
    pass

class HTTPClientFactory:  # Acronyms stay uppercase
    pass

# Functions and variables: snake_case
def get_user_by_email(email: str) -> User | None:
    retry_count = 3
    max_connections = 100
```

**Constants:**

```python
# Module-level constants: SCREAMING_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
API_BASE_URL = "https://api.example.com"
```

### Pattern 4: Import Organization

Group imports in a consistent order: standard library, third-party, local.

```python
# Standard library
import os
from collections.abc import Callable
from typing import Any

# Third-party packages
import httpx
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

# Local imports
from myproject.models import User
from myproject.services import UserService
```

In FastAPI projects that follow [fastapi-config-01](../fastapi-config-01/SKILL.md), prefer **SQLModel** (with **Pydantic**) for ORM/table models instead of importing **SQLAlchemy** primitives in new code.

Use absolute imports exclusively:

```python
# Preferred
from myproject.utils import retry_decorator

# Avoid relative imports
from ..utils import retry_decorator
```

## Advanced Patterns

### Pattern 5: Google-Style Docstrings

Write docstrings for all public classes, methods, and functions.

**Simple Function:**

```python
def get_user(user_id: str) -> User:
    """Retrieve a user by their unique identifier."""
    ...
```

**Complex Function:**

```python
def process_batch(
    items: list[Item],
    max_workers: int = 4,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchResult:
    """Process items concurrently using a worker pool.

    Processes each item in the batch using the configured number of
    workers. Progress can be monitored via the optional callback.

    Args:
        items: The items to process. Must not be empty.
        max_workers: Maximum concurrent workers. Defaults to 4.
        on_progress: Optional callback receiving (completed, total) counts.

    Returns:
        BatchResult containing succeeded items and any failures with
        their associated exceptions.

    Raises:
        ValueError: If items is empty.
        ProcessingError: If the batch cannot be processed.

    Example:
        >>> result = process_batch(items, max_workers=8)
        >>> print(f"Processed {len(result.succeeded)} items")
    """
    ...
```

**Class Docstring:**

```python
class UserService:
    """Service for managing user operations.

    Provides methods for creating, retrieving, updating, and
    deleting users with proper validation and error handling.

    Attributes:
        repository: The data access layer for user persistence.
        logger: Logger instance for operation tracking.

    Example:
        >>> service = UserService(repository, logger)
        >>> user = service.create_user(CreateUserInput(...))
    """

    def __init__(self, repository: UserRepository, logger: Logger) -> None:
        """Initialize the user service.

        Args:
            repository: Data access layer for users.
            logger: Logger for tracking operations.
        """
        self.repository = repository
        self.logger = logger
```

### Pattern 6: Line Length and Formatting

Set line length to 120 characters for modern displays while maintaining readability.

```python
# Good: Readable line breaks
def create_user(
    email: str,
    name: str,
    role: UserRole = UserRole.MEMBER,
    notify: bool = True,
) -> User:
    ...

# Good: Chain method calls clearly (use .is_(True) on SQL boolean columns—avoids Ruff E712 on `== True`)
result = (
    db.query(User)
    .filter(User.active.is_(True))
    .order_by(User.created_at.desc())
    .limit(10)
    .all()
)

# Good: Format long strings
error_message = (
    f"Failed to process user {user_id}: "
    f"received status {response.status_code} "
    f"with body {response.text[:100]}"
)
```

### Pattern 7: Project Documentation

**README Structure:**

```markdown
# Project Name

Brief description of what the project does.

## Installation

\`\`\`bash
uv pip install myproject
\`\`\`

## Quick Start

\`\`\`python
from myproject import Client

client = Client(api_key="...")
result = client.process(data)
\`\`\`

## Configuration

Document environment variables and configuration options.

## Development

\`\`\`bash
uv sync --all-extras --dev
uv run pytest
uv run ruff check .
uv run ty check
\`\`\`
```

**CHANGELOG Format (Keep a Changelog):**

```markdown
# Changelog

## [Unreleased]

### Added
- New feature X

### Changed
- Modified behavior of Y

### Fixed
- Bug in Z
```

## Best Practices Summary

1. **Use uv** - Environments, installs, and `uv run` / `uvx` for tools
2. **Use Ruff** - Single tool for linting and formatting; enable FastAPI rules when applicable
3. **Use ty** - Fast type checking aligned with the FastAPI toolchain; mypy/pyright OK for legacy standards
4. **120 character lines** - Modern standard for readability
5. **Descriptive names** - Clarity over brevity
6. **Absolute imports** - More maintainable than relative
7. **Google-style docstrings** - Consistent, readable documentation
8. **Document public APIs** - Every public function needs a docstring
9. **Keep docs updated** - Treat documentation as code
10. **Automate in CI** - Run Ruff and ty on every commit
11. **Target Python 3.10+** - For new projects, Python 3.12+ is recommended for modern language features
