REM Install required skills for the project.
@echo off
uv add --group dev pytest pytest-cov ruff ty

uv add alembic asyncer httpx sqlmodel toml

call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill fastapi
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-project-structure
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-code-style
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-design-patterns
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-error-handling
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-type-safety
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-configuration
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-observability
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-resilience
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-resource-management
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill async-python-patterns
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-anti-patterns
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-testing-patterns
call npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill fastapi-config-01

