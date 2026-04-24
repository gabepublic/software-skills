---
workflowType: architecture
project_name: baseline
user_name: Architect
date: '2026-04-24'
---

When generating stories from this architecture, you must ALSO first read the `.agents/skills/` directory. Each story's 'Acceptance Criteria' should include a check for compliance with the relevant skill in `.agents/skills/`.


## Implementation Standards & Skills

This project utilizes standardized Agent Skills. All generated stories and code implementations MUST adhere to the patterns defined in the `.agents/skills/`.

- **Constraint:** Do not use default LLM patterns if they conflict with the "rules" defined in the skills listed above.

- **Precedence:** If the listed Agent Skills disagree with each other, use the following order of precedence over conflicting skill guidance:
  - FastAPI Config-01 (`.agents/skills/fastapi-config-01`)
  - FastAPI (`.agents/skills/fastapi`)
  - The rest of the Python Skills (`.agents/skills/python-*` and `.agents/skills/async-python-patterns`)

