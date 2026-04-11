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
- Install the skill on other project
```
npx skills add https://github.com/gabepublic/software-skills --skill nextjs-config-01
```