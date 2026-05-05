---
name: review-prompt
description: Use this skill when the user asks to review, improve, debug, rewrite, sharpen, or stress-test a prompt. Guide the user through the 4-D framework: Destination, Definition, Doubt, and Done. Ask one targeted question at a time, recommend a default answer, and produce a concise revised prompt when the finish line is clear.
---

# Review Prompt

## Goal

Improve a user's prompt by making the intended result, success criteria, evidence rules, and stopping point explicit. Use the 4-D framework:

- Destination: What result should the model produce?
- Definition: What makes the result successful and usable?
- Doubt: What evidence, citations, uncertainty handling, or source limits are required?
- Done: When should the model stop working and deliver the answer?

## Workflow

1. Read the user's draft prompt and infer the likely task, audience, constraints, and output.
2. Identify the highest-risk gap across Destination, Definition, Doubt, and Done.
3. Ask exactly one question about that gap.
4. Include your recommended answer after the question so the user can accept, edit, or reject it.
5. After the user answers, repeat steps 2-4 until the prompt has enough clarity to draft safely.
6. When the remaining gaps are minor, stop interviewing and produce the revised prompt.

Use this question format:

```markdown
Question: [one focused question]

Recommended answer: [specific default, written as if it could be inserted into the prompt]
```

## Interview Rules

- Walk decision branches in dependency order: Destination first, then Definition, then Doubt, then Done, unless another gap is clearly blocking.
- Prefer precise defaults over broad menus. If multiple options are plausible, recommend the most useful default and briefly name the tradeoff.
- Do not ask compound questions. Split multi-part uncertainty into separate turns.
- Do not over-interview. If a reasonable default would not change the final prompt materially, choose it and move on.
- Preserve the user's intent, voice, domain, and constraints. Improve clarity without changing the underlying ask.
- For factual, legal, medical, financial, or research prompts, make Doubt explicit with source, citation, recency, and uncertainty rules.

## Revision Template

When ready, provide:

```markdown
## Revised Prompt

[Prompt text with clear Destination, Definition, Doubt, and Done.]

## What Changed

- Destination: [brief note]
- Definition: [brief note]
- Doubt: [brief note]
- Done: [brief note]
```

If the user asks only for the final prompt, omit `What Changed`.

## Strong Patterns

- Destination: "Turn this transcript into a client-ready follow-up email."
- Definition: "Success means the email states decisions, open questions, and next actions for each owner."
- Doubt: "Use only details supported by the transcript. Put unclear items under Open Questions."
- Done: "When the checklist is met, provide the final email."

Combined pattern:

```markdown
Turn this transcript into a client-ready follow-up email. Success means the email clearly states what was decided, what is still open, and the next action for each person. Use only decisions directly supported by the transcript. Put unclear items under Open Questions. When the checklist is met, provide the final email.
```

## Examples

Use these examples as patterns, not fixed wording:

| 4-D type | Weak | Strong |
| --- | --- | --- |
| Destination | Summarize this meeting transcript. | Turn this meeting transcript into a follow-up email I can send to the customer. |
| Destination | Make a table from this spreadsheet. | Find the three problems in this spreadsheet that would change my decision. |
| Definition | Rewrite this email. | Rewrite this email so it is clear, calm, and direct. Keep the same facts, keep it under 200 words, and put the ask in the first three sentences. |
| Doubt | Do not make things up. | After every factual claim, cite the source inline, such as `[Source: report, p. 4]`. |
| Doubt | Do not hallucinate. | When you are not sure, write `unverified` or leave the field blank. I would rather see a gap than a guess. |
| Done | Be exhaustive. Think deeply. Research everything. | Stop once you can answer the main question with enough evidence. |
| Done | Cover every angle. | When the output meets the checklist, provide the final version. |

**Weak combined prompt:**

```markdown
Act as a world-class business strategist.
- First, read the following transcript. 
- Identify all key themes.
- Extract action items. 
- Write a client email.
- Make sure the tone is friendly and professional.
- Double-check everything.
- Make a table.
- Finally, give me a recommendation. Be concise and detailed.
```

**Strong combined prompt:**

```markdown
Turn this transcript into a client-ready follow-up email. Success means the email clearly states what we decided, what is still open, and the next action for each person. Use only decisions directly supported by the transcript. Put unclear items under Open Questions. When the checklist is met, provide the final email.
```
