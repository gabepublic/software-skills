---
name: review-prompt
description: Reviews and rewrites prompt/"llm instructions" drafts using the 4-D framework (Destination, Definition, Doubt, Done). Use when the user asks to review, improve, debug, sharpen, stress-test, or rewrite the prompt.
---

# Review Prompt

Use this skill to turn vague instructions into clear, testable LLM instructions.

## 4-D Framework

- Destination: What result should the model produce?
- Definition: What makes the result successful and usable?
- Doubt: What evidence, citations, uncertainty handling, or source limits are required?
- Done: When should the model stop working and deliver the answer?

## Workflow (step-by-step)

1. Read the user's current prompt and infer task, audience, constraints, and output shape.
2. Identify the highest-risk gap across Destination, Definition, Doubt, and Done.
3. Ask exactly one question about that gap.
4. Include a recommended default answer the user can accept, edit, or reject.
5. After the user answers, repeat steps 2-4 until the instructions are clear enough to draft safely.
6. When the remaining gaps are minor, stop interviewing and produce the revised instructions.

Use this question format:

```markdown
Question: [one focused question]

Recommended answer: [specific default, written as if it could be inserted into the prompt]
```

## Interview Rules (reliability)

- Walk decision branches in dependency order: Destination first, then Definition, then Doubt, then Done, unless another gap is clearly blocking.
- Prefer precise defaults over broad menus. If multiple options are plausible, recommend one default and briefly note tradeoffs.
- Do not ask compound questions. Split multi-part uncertainty into separate turns.
- Do not over-interview. If a reasonable default would not change the final prompt materially, choose it and move on.
- Preserve the user's intent, voice, domain, and constraints. Improve clarity without changing the underlying ask.
- For factual, legal, medical, financial, or research instructions, make Doubt explicit with source, citation, recency, and uncertainty rules.

## Revision Template

When ready, provide this output:

```markdown
## Revised Prompt

[Prompt text with clear Destination, Definition, Doubt, and Done.]

## What Changed

- Destination: [brief note]
- Definition: [brief note]
- Doubt: [brief note]
- Done: [brief note]
```

If the user asks only for the final prompt:
- the `Revised Prompt` should **NOT** include the text: Destination, Definition, Doubt, and Done.
- omit `What Changed`.

## Pattern Cues (Weak -> Strong)

- Destination (weak -> strong): "Summarize this meeting transcript." -> "Turn this meeting transcript into a follow-up email I can send to the customer."
- Definition (weak -> strong): "Rewrite this email." -> "Rewrite this email so it is clear, calm, and direct; keep facts unchanged, under 200 words, and place the ask in the first three sentences."
- Doubt (weak -> strong): "Do not make things up." -> "After every factual claim, cite the source inline, e.g., `[Source: report, p. 4]`."
- Done (weak -> strong): "Cover every angle." -> "When the output meets the checklist, provide the final version."

**Weak combined instructions:**

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

**Strong combined instructions:**

```markdown
Turn this transcript into a client-ready follow-up email. Success means the email clearly states what was decided, what is still open, and the next action for each person. Use only decisions directly supported by the transcript. Put unclear items under Open Questions. When the checklist is met, provide the final email.
```
