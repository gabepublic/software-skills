# HOW-TO build the `api-fastapi-skilled-template`

See the template repo: `https://github.com/gabepublic/api-fastapi-skilled-template`

Future enhancements:
- Create an `npx` app like `npx create-next-app` that will automatically clone the repo, and setup based on the QA with the user. See "npx app" below.

## SETUP to make the skilled fastapi template

- From Github, create a new repo, this repo
- Mark the repo as a template
  - Go to your repository on GitHub:
  - Click Settings
  - Scroll to General
  - Find the checkbox: 👉 “Template repository”
  - Turn it on and save
  - That’s it—that repo is now officially a template.
- Clone this repo; and start setup the template

- If `uv` NOT install, see https://docs.astral.sh/uv/getting-started/installation/#pypi
```
# Window
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS or Linux
$ curl -LsSf https://astral.sh/uv/install.sh | sh

where uv
uv --version
```
- Create a uv project using uv
```
uv init
uv venv
.venv\Scripts\activate
```
- Install FastAPI - https://fastapicloud.com/docs/getting-started/
```
uv add "fastapi[standard]"
```
- Install modules and skills, use `install_skills_modules.bat`, or run the following commands:
```
uv add --group dev pytest pytest-cov ruff ty

uv add alembic asyncer httpx sqlmodel toml

npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill fastapi
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-project-structure
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-code-style
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-design-patterns
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-error-handling
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-type-safety
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-configuration
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-observability
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-resilience
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-resource-management
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill async-python-patterns
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-anti-patterns
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill python-testing-patterns
npx skills add https://github.com/gabepublic/software-skills --yes --agent cursor --skill fastapi-config-01
```
- Manually create baseline files using cursor agent using the following prompt:
```
Setup this fastapi project leveraging on the `.agents/skills` and make sure: to create the folder for the api version 1, `api/v1/` according to the @.agents/skills/fastapi-config-01 - Project Structure. Create an endpoint, `/v1/version` that returns `{"version": "1.0"}` 
```
- Add the `_bmad-output/` folder


## `npx` app

The following is recommended by AI based on the given question.

**QUESTION:**
```
When I start a new Next.js project I used their project starter script, `npx create-next-app@latest`. How does this script work? I want to create a similar starter script BUT for my python fastapi project. Show me how to do it using Node.js, and Python if possible.
```

**RESPONSE:**
`create-next-app` is a CLI (Command Line Interface) tool that acts as a wrapper around a template repository. When you run it, the script prompts you for configuration (TypeScript, ESLint, Tailwind), then downloads the corresponding files, installs dependencies, and initializes a Git repository.

To build a similar experience for a FastAPI project, you can use Node.js (leveraging the vast CLI ecosystem) or Python (using native tools).

1. How the Script Works (The Logic)
Regardless of the language, the "Starter Script" workflow follows these steps:

User Input: Ask the user for the project name and optional features (e.g., "Use PostgreSQL?", "Include Docker?").

Template Fetching: Copy files from a local directory or download them from a GitHub repository.

Variable Injection: Replace placeholders (like {{PROJECT_NAME}}) in README.md or pyproject.toml.

Environment Setup: Create a virtual environment and install dependencies.

2. Using Node.js (The `npx` Style)
If you want your users to run `npx create-fastapi-app`, you can use Prompts for the UI and Degit to clone templates without the Git history.

The Setup
Create a directory and run `npm init`.

Install helper packages: `npm install prompts degit kolors`.

The Script (index.js)