---
name: research-websites
description: >
  Research a topic using user-provided website(s) as the primary evidence, then
  corroborate with credible external sources when needed. Produce a structured
  brief using templates/summary.md.
allowed-tools: 
---

# Research website

## When To Use

Use this skill when the user asks you to research, explain, compare, summarize, or analyze a topic and provides one or more website URLs (or clearly indicates target sites).

Prefer this skill when:
- The user wants conclusions grounded in specific website content.
- The task requires extracting claims, positioning, offerings, policies, or evidence from those sites.
- The user wants a concise brief rather than raw browsing notes.

## Inputs

- Required: at least one target website URL (or a clear instruction identifying the target website(s)).
- Required: research objective/question tied to the target website(s).
- Optional constraints: timeframe, geography, audience level, preferred sources, depth, and output focus.
- Optional focus areas or sub-questions.

If URL(s), scope, or intent are ambiguous, ask one brief clarifying question before deep research.

## Workflow

1. Confirm scope:
   - Restate the target website(s) and research objective.
   - Identify key sub-questions needed for a useful answer.
   - Note any user constraints (time range, region, etc.).

2. Extract first-party evidence from provided website(s):
   - Prioritize official pages (about, product, pricing, docs, policy, blog/newsroom, support, legal pages).
   - Capture factual claims, dates, metrics, and direct statements with page URLs.
   - Distinguish between explicit statements and inference.

3. Corroborate and contextualize with external sources:
   - Validate major claims with credible independent sources where possible.
   - Prefer primary/authoritative sources and recent information when recency matters.
   - Capture disagreements and identify who makes each claim.
   - If external corroboration is unavailable, explicitly state this limitation.

4. Read `templates/summary.md` and produce the final response in that exact structure:
   - Replace each placeholder with concise, source-supported content.
   - Use `Not found in reviewed sources` where evidence is missing.
   - Keep `<EXECUTIVE_SUMMARY>` to 2-4 sentences.
   - Keep findings factual and neutral.
   - Put assumptions, uncertainty, and evidence gaps in caveats.

## Quality Bar

- Use the provided website(s) as primary evidence; do not substitute unrelated sources.
- Use at least 3 distinct sources total when feasible (including target website pages and external corroboration), unless user requests otherwise.
- Prefer high-quality and recent sources for fast-changing topics.
- Cite URLs for major claims, metrics, dates, and contentious points.
- Keep the summary concise and avoid raw dumps.
- Separate observed facts from inference.
- Mention uncertainty when sources disagree or evidence is sparse.
- Do not invent facts, numbers, dates, or citations.

## Edge Cases

- If the user provides multiple websites, compare them explicitly and note alignment vs differences.
- If first-party claims cannot be independently validated, mark confidence lower and explain why.
- If sources strongly conflict, present both sides and explain confidence levels.
- If only low-quality or sparse sources are available, state that limitation clearly.
- If the website is inaccessible or blocked, report it and request replacement URLs.
- If the topic evolves quickly, explicitly include an "as of" date in findings.
