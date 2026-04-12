# software-skills
Modular software skills that enhance AI agent capabilities while enforcing structured, intent-aligned execution.

## SETUP

- Use `skill-creator` to help creating the skill
```
npx skills add https://github.com/anthropics/skills --skill skill-creator
```

## SKILL: Next.js CONFIG-01

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

- TBD