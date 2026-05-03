# Skill Refinement Reference

Official Skill Specification: `https://agentskills.io/specification`

## Recommended Structure

```text
skill-name/
|-- SKILL.md      # Main instructions, required
|-- REFERENCE.md  # Detailed guidance, optional
|-- EXAMPLES.md   # Usage examples, optional
`-- scripts/      # Utility scripts, optional
    `-- helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick Start

[Minimal working guidance]

## Workflow

[Step-by-step process for the core task]

## Reference

See [REFERENCE.md](REFERENCE.md) for detailed or rarely needed guidance.
```

## Description Requirements

The description is the main signal the agent sees when deciding whether to load the skill.

Good descriptions:

- Stay under 1024 characters.
- Use third person.
- Start with what the skill does.
- Include a second sentence beginning with "Use when..."
- Mention specific triggers such as user intents, file types, keywords, or contexts.

Good example:

```text
Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, document extraction, or document assembly.
```

Weak example:

```text
Helps with documents.
```

The weak example is too broad to distinguish from other document-related skills.

## When to Split Files

Split content out of `SKILL.md` when:

- `SKILL.md` is over 100 lines.
- Details are useful only after the skill has been selected.
- Content covers distinct reference areas, examples, or schemas.
- The main workflow is harder to scan because of background material.

Keep references one level deep from `SKILL.md` so the agent can find them reliably.

## When to Add Scripts

Add utility scripts when:

- The operation is deterministic, such as validation or formatting.
- The same code would otherwise be generated repeatedly.
- Failure modes need explicit handling.
- A script improves reliability more than prose instructions would.

Prefer simple, documented scripts with clear inputs, outputs, and error behavior.
