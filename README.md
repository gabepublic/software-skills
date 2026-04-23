# software-skills
Modular software skills that enhance AI agent capabilities while enforcing structured, intent-aligned execution.

## SETUP

- Use `skill-creator` to help creating the skill
```
npx skills add https://github.com/anthropics/skills --skill skill-creator
```

- **NOTE:** DO NOT checkin `.agent` folder or otherwise the skills cannot be found by `npx skills add`

- **NOTE:** use `agent-skills` folder for all the skills because when the standard `skills` folder is present, the `npx skills add` will NOT do a *deep scan*; it will just look for the folder immediately in the `skills` folder as the skill name.

## Cloned or Modified Skills

Some skills from different authors can be in conflict when used together.
  


## SKILL: Next.js CONFIG-01

### DEVELOP the Skill

- Depends on Skill: [vercel-labs: Next.js Best Practices](https://github.com/vercel-labs/next-skills)
```
npx skills add https://github.com/vercel-labs/next-skills --skill next-best-practices
```
- Next.js 16: start from template
```
npx create-next-app@latest .
```
- Typescript
- Prisma ORM
- See `skills/nextjs-config-01/SKILL.md` for other tech stack.
- Use the Agent and `skill-creator` skill to create this skill
```
Create a skill (`nextjs-config-01`) using rules and specifications defined in `@generate-skills-artifacts/nextjs-config-01/architecture.md`
 and `@generate-skills-artifacts/nextjs-config-01/convention.md` 
```
- Create the `skills/nextjs-config-01/resources` folder; copy `generate-skills-artifacts/nextjs-config-01/architecture.md` and
  `generate-skills-artifacts/nextjs-config-01/convention.md` to the `resources` folder.
- Install the skill on the actual Next.js project
```
npx skills add https://github.com/gabepublic/software-skills --skill nextjs-config-01
```
- Copy the `_bmad-output/examples/nextjs-config-01/architecture/` to the Next.js project `_bmad-output/planning-artifacts/`
- Copy the `_bmad-output/examples/nextjs-config-01/prd.md` to the Next.js project `_bmad-output/planning-artifacts/` for testing the skills. 

### USING the Skill

- In the new Next.js project:
- Create Next.js project using the template:
```
npx create-next-app@latest .
```
- Required components
```
npx shadcn@latest init
pnpm install react-hook-form @hookform/resolvers
pnpm install zod
pnpm install drizzle-orm
pnpm install iron-session
pnpm install bcryptjs
pnpm install -D vitest @vitest/ui jsdom @vitejs/plugin-react
pnpm install -D @testing-library/jest-dom @testing-library/react
pnpm install -D @playwright/test
npx playwright install
```
- Add to `package.json`
```
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  },
}
```
- Copy files for tests (vitest & playwright):
	- Copy `vitest.config.ts` and `playwright.config.ts`
	- Copy `tests/` folder
- TEST the SETUP
```
pnpm dev
pnpm test
pnpm test:e2e
```
- Install BMAD; choose the IDE; 
```
npx bmad-method install
```
- Add the following Agent Skills; also see `skills-lock.json`:
  - next-best-practices - Next.js Best Practices
```
npx skills add https://github.com/vercel-labs/next-skills --skill next-best-practices
```
- nextjs-config-01 - Next.js project config
```
npx skills add https://github.com/gabepublic/software-skills --skill nextjs-config-01
```
- Copy the `_bmad-output/examples/nextjs-config-01/architecture/` to the Next.js project `_bmad-output/planning-artifacts/`
- [Optional] Copy the `_bmad-output/examples/nextjs-config-01/prd.md` to the Next.js project `_bmad-output/planning-artifacts/` for testing the skills. 
- Do the BMAD Process (`/bmad-create-prd`, `/bmad-create-epics-and-stories`, `/bmad-sprint-planning`, `/bmad-create-story`, and `/bmad-dev-story`)


## SKILL: FastAPI CONFIG-01

### DEVELOP the Skill

- Create a folder, `fastapi-config-01-dev` and install the following Skill dependencies.

- Depends on Python Skills:
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

- Depends on FastAPI Skills:
  - [FastAPI](https://skills.sh/fastapi/fastapi/fastapi)
```
npx skills add https://github.com/fastapi/fastapi --skill fastapi
```

- STAGE-1: use AI agent (for example cursor agent or cursor IDE) to review whether there are conflicts between the skills.

- STAGE-2: develop the `skills/fastapi-config-01` skill.
  - For testing, checkin to github

- STAGE-3: after the `fastapi-config-01` skill is complete, again test it in the `fastapi-config-01-dev` folder by installing the `fastapi-config-01`:
```
npx skills add https://github.com/gabepublic/software-skills --skill fastapi-config-01
```

### USING the Skill

- Install uv - https://docs.astral.sh/uv/getting-started/installation/#pypi
- Check uv
```
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

- Install Skills
```
npx skills add https://github.com/gabepublic/software-skills --skill fastapi

npx skills add https://github.com/gabepublic/software-skills --skill python-project-structure
npx skills add https://github.com/gabepublic/software-skills --skill python-code-style
npx skills add https://github.com/gabepublic/software-skills --skill python-design-patterns
npx skills add https://github.com/gabepublic/software-skills --skill python-error-handling
npx skills add https://github.com/gabepublic/software-skills --skill python-type-safety
npx skills add https://github.com/gabepublic/software-skills --skill python-configuration
npx skills add https://github.com/gabepublic/software-skills --skill python-observability
npx skills add https://github.com/gabepublic/software-skills --skill python-resilience
npx skills add https://github.com/gabepublic/software-skills --skill python-resource-management
npx skills add https://github.com/gabepublic/software-skills --skill async-python-patterns
npx skills add https://github.com/gabepublic/software-skills --skill python-anti-patterns
npx skills add https://github.com/gabepublic/software-skills --skill python-testing-patterns

npx skills add https://github.com/gabepublic/software-skills --skill fastapi-config-01
```

- Manually create baseline files;  ANY template scafolding???

- Install BMAD; choose the IDE; 
```
npx bmad-method install
```

TODO:########
- Copy the `_bmad-output/examples/nextjs-config-01/architecture/` to the Next.js project `_bmad-output/planning-artifacts/`
- [Optional] Copy the `_bmad-output/examples/nextjs-config-01/prd.md` to the Next.js project `_bmad-output/planning-artifacts/` for testing the skills. 
- Do the BMAD Process (`/bmad-create-prd`, `/bmad-create-epics-and-stories`, `/bmad-sprint-planning`, `/bmad-create-story`, and `/bmad-dev-story`)
