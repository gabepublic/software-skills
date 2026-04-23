# wshobson

Skills cloned or cloned-and modified skills.

Notes:
- some skills need to be modified due to typos, issues, or conflict with other skills.
- See the "Modified Skills" list below.
- Skills included in this folder BUT not in the modified list means it's only cloned.
- Hopefully, in the future we don't need to clone after better Revision Management.

## Source

Python Skills:
- [Python Project Structure & Module Architecture](https://skills.sh/wshobson/agents/python-project-structure)
- [Python Code Style & Documentation](https://skills.sh/wshobson/agents/python-code-style)
- [Python Design Patterns](https://skills.sh/wshobson/agents/python-design-patterns)
- [Python Error Handling](https://skills.sh/wshobson/agents/python-error-handling)
- [Python Type Safety](https://skills.sh/wshobson/agents/python-type-safety)
- [Python Configuration Management](https://skills.sh/wshobson/agents/python-configuration)
- [Python Observability](https://skills.sh/wshobson/agents/python-observability)
- [Python Resilience Patterns](https://skills.sh/wshobson/agents/python-resilience)
- [Python Resource Management](https://skills.sh/wshobson/agents/python-resource-management)
- [Async Python Patterns](https://skills.sh/wshobson/agents/async-python-patterns)
- [Python Anti-Patterns Checklist](https://skills.sh/wshobson/agents/python-anti-patterns)
- [Python Testing Patterns](https://skills.sh/wshobson/agents/python-testing-patterns)
```
npx skills add https://github.com/wshobson/agents --skill python-project-structure
npx skills add https://github.com/wshobson/agents --skill python-code-style
npx skills add https://github.com/wshobson/agents --skill python-design-patterns
npx skills add https://github.com/wshobson/agents --skill python-error-handling
npx skills add https://github.com/wshobson/agents --skill python-type-safety
npx skills add https://github.com/wshobson/agents --skill python-configuration
npx skills add https://github.com/wshobson/agents --skill python-observability
npx skills add https://github.com/wshobson/agents --skill python-resilience
npx skills add https://github.com/wshobson/agents --skill python-resource-management
npx skills add https://github.com/wshobson/agents --skill async-python-patterns
npx skills add https://github.com/wshobson/agents --skill python-anti-patterns
npx skills add https://github.com/wshobson/agents --skill python-testing-patterns
```

## MODIFIED Skills

- `python-design-patterns`
  - Inconsistency (broken cross-reference, not a doctrine clash)
  - “Related Skills” links to `python-project-setup`, which is no longer in the `wshobson/agents` repo; changed to `python-project-structure` instead. Updating the link to avoid agent confusion.

- `python-error-handling`
  - Pydantic required fields / Field(...) — python-error-handling vs fastapi
  - python-error-handling examples use required fields like email: str = Field(..., min_length=5, ...).
  - fastapi explicitly says not to use ... as defaults for required parameters on models or path operations, and shows Field(gt=0) without ellipsis.
  - Same underlying feature (required + constraints), different house style. Following both blindly produces inconsistent Pydantic style in API code.
  - Resolution hint: For FastAPI work, align examples with fastapi (no ... in Field / Query when the field is already required by type).

- `python-code-style`
  - Type checker / data stack preferences — fastapi vs python-code-style / python-type-safety
  - fastapi defers to a “other tools” reference and emphasizes ty (with uv, Ruff) in that section.
  - `python-code-style` and `python-type-safety` center Ruff + mypy (with pyright as an alternative).
  - Not a logical contradiction, but competing defaults for “what we recommend in this repo.”
  
- `python-type-safety`
  - Type checker / data stack preferences — fastapi vs python-code-style / python-type-safety
  - fastapi defers to a “other tools” reference and emphasizes ty (with uv, Ruff) in that section.
  - `python-code-style` and `python-type-safety` center Ruff + mypy (with pyright as an alternative).
  - Not a logical contradiction, but competing defaults for “what we recommend in this repo.”
  
- `python-project-structure`
  - `fastapi-config-01`: Canonical layout is `api-app/app/...` (application package under `app/`, no `src/` layout shown).
  