---
workflowType: architecture
project_name: baseline
user_name: Architect
date: '2026-04-03'
---

When generating stories from this architecture, you must ALSO first read the `.agents/skills/` directory. Each story's 'Acceptance Criteria' should include a check for compliance with the relevant skill in `.agents/skills/`.


## Implementation Standards & Skills

This project utilizes standardized Agent Skills. All generated stories and code implementations MUST adhere to the patterns defined in:

- **Next.js:** 
  - [Next.js Best Practices](.agents/skills/next-best-practices/) — focused reference (RSC boundaries, data patterns, route handlers, metadata, bundling, etc.)
  - [Next.js Project-specific Architecture](.agents/skills/nextjs-config-01) — Next.js project specific rules for any feature work, scaffolding, or reviews.
  - Additional Project-specific Next.js rules are summarized below; defer to these skills and convention for full detail to avoid drift or duplicate rules.

- **Constraint:** Do not use default LLM patterns if they conflict with the "rules" defined in the skills listed above.

- **Precedence:** If the listed Agent Skills disagree with each other, use the following order of precedence over conflicting skill guidance:
  - Additional Project-specific Next.js rules
  - Next.js Project-specific Architecture
  - Next.js Best Practices

