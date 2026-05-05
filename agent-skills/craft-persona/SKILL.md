---
name: craft-persona
description: Creates role-targeted personas, summaries, bios, credential positioning, and resume-vault Q&A from the user's Obsidian resume vault. Use when asked to summarize, tailor, position, or answer experience questions for AI, product, consulting, or technical leadership roles.
---

# Craft Persona

## Purpose

Turn the user's resume vault, credentials, project history, career notes, and approved personal source material into concise, accurate positioning or answers for a target role or opportunity.

## Vault Contract

- Default resume `vault_root`: `C:\zObsidian\llm-resume\`.
- Read `memories/index.md` first when present, then search `memories/**` for relevant evidence.
- Use the `templates/**` when instructed.
- Do not read or modify `.obsidian/**`, `.git/**`, `.gitignore`, or `.gitattributes`.
- Do not modify existing files in `raw/**`.
- Only inspect `raw/**` resumes or source documents when the user explicitly asks, approves it, or provides a specific file path.
- If the resume vault is missing or evidence is thin, say so and ask for the missing resume, target posting, questions, or clarification.
- Preserve Obsidian links as `[[memory-links]]`; do not replace them with Markdown links inside memory pages.

## Intake

Before drafting or answering, identify:

1. Target role or audience, such as AI architect, AI engineer, AI product manager, executive stakeholder, recruiter, hiring manager, conference organizer, or client.
2. Output type, such as resume summary, LinkedIn About, short bio, executive bio, cover-letter positioning, interview answers, questionnaire responses, capability statement, or role-fit matrix.
3. Tone and length constraints, such as technical, executive, concise, warm, founder-like, first person, third person, 50 words, or 3 bullets.
4. Required facts, exclusions, or sensitivities, such as credentials to emphasize, industries to downplay, confidential employers, dates, or compensation-related details.

If the user provides a target job description, treat it as role context, not as evidence about the user.

## Workflow

1. Verify the resume vault exists.
2. Read `memories/index.md` when available and search for resume, career, credential, education, project, leadership, product, AI, architecture, engineering, consulting, and domain-specific evidence.
3. Gather only the evidence needed for the requested persona, summary, or questions.
4. Extract reusable proof points: roles, scope, AI/data/software/product work, leadership, credentials, industries, tools, and measurable outcomes.
5. Map proof points to the target role's likely buying criteria or the user's specific questions.
6. Draft the persona, summary, or answers in the requested format.
7. Add a short evidence note listing the source memory pages or approved files used.
8. Clearly mark unsupported but plausible claims as `Needs verification`.

## Resume Q&A

Use this skill for questions that should be answered from the resume vault, including screening questions, application prompts, interview prep, RFP/profile questions, and "based on my resume" requests.

- Answer directly from sourced resume-vault evidence.
- If a question asks for a yes/no answer, give the answer first, then a concise supporting explanation.
- If the evidence is partial, say what is supported and what still needs confirmation.
- If the question targets a role or job description, tailor the answer to that context without inventing experience.
- When useful, provide both a short response and a stronger polished version.

## Evidence Rules

- Treat memory pages as the only evidence source for answers unless the user approves specific raw files.
- Do not present uncited vault-derived facts as certain.
- If sources conflict, state the contradiction and cite each side.
- If a useful claim is plausible but unsupported by the vault, mark it as `Needs verification`.
- Do not treat the user's question as factual evidence.

## Role Lenses

Use these lenses to decide what to emphasize:

- AI architect: enterprise architecture, solution design, governance, model integration, data platforms, security, scalability, tradeoffs, stakeholder alignment.
- AI engineer: implementation depth, model/application integration, evaluation, tooling, data pipelines, APIs, software quality, deployment, observability.
- AI product manager: customer problem framing, roadmap judgment, AI product strategy, discovery, metrics, cross-functional leadership, launch execution, risk management.
- AI consultant/advisor: diagnosis, executive communication, transformation strategy, operating models, workshops, recommendations, client outcomes.
- Technical leader: team leadership, mentoring, delivery accountability, architecture standards, decision-making, communication across technical and business groups.

## Output Standards

- Make claims specific, defensible, and sourced.
- Prefer concrete evidence over generic adjectives.
- Keep the user's voice credible and grounded; avoid hype, inflated seniority, or unverifiable metrics.
- Tailor vocabulary to the target audience while preserving factual accuracy.
- Separate finished copy from reasoning notes.
- When useful, provide two or three variants with different positioning angles.

## Useful Output Patterns

- Executive summary: 3-5 sentences focused on strongest role fit, scope, and differentiators.
- Role-fit bullets: 4-7 bullets pairing target-role requirements with evidence.
- Persona brief: Positioning, best-fit roles, differentiators, proof points, watchouts, and ready-to-use draft copy.
- Resume profile: compact paragraph plus optional keyword line. Avoid first person unless requested.

See [REFERENCE.md](REFERENCE.md) for the memory schema, page template, graph model, and citation format.
