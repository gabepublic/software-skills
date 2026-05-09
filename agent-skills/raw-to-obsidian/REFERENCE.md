# raw-to-obsidian — reference

## Summary page naming

Input: source file basename including extensions, e.g. `2026-05-08.raw.md`, `2026-05-08.md`.

1. Remove the **last** extension only once (`.md` → inner name; `.raw.md` → treat as full basename `2026-05-08.raw.md` → stem `2026-05-08.raw` when removing `.md` once).
2. Lowercase the stem.
3. Replace `.` and `_` with `-`; collapse multiple `-` to one; trim leading/trailing `-`.
4. Append `.md`.

Examples:

| Source | Summary filename |
|--------|------------------|
| `2026-05-08.raw.md` | `2026-05-08-raw.md` |
| `2026-05-08.md` | `2026-05-08.md` (already valid stem) |
| `My_Note.raw.md` | `my-note-raw.md` |

If two sources would collide, suffix with `-2`, `-3`, … after user confirmation.

## Plans folder

Store **pending approvals** and **post-execution audit trails** under `plans/`. These files are **not** memory graph nodes: do **not** require memory-node frontmatter unless you later promote content into `memories/`.

**Pairing:** use the same calendar date for a batch, e.g. `plans/2026-05-08-plan.md` and `plans/2026-05-08-audit.md`.

**Multiple batches same day:** after user confirmation, disambiguate with suffixes, e.g. `2026-05-08-plan-2.md` / `2026-05-08-audit-2.md`, or a user-chosen slug before `-plan`.

## `memories/index.md` expectations

- Table (or list) of memory pages with **one-line** purpose.
- Keep `type: index` in frontmatter; link to hub pages and recent summaries.

## `memories/log.md` expectations

- **Append-only.** Never rewrite prior entries; newest entry at bottom.
- Each ingest or batch ends with one line or short block: ISO date, source paths, counts of pages touched, operator (agent).

## High-risk change protocol

**Trigger:** deletes, database drops, production modifications, or any action outside **Allowed write** in `SKILL.md`.

1. Write `plans/YYYY-MM-DD-plan.md` listing every intended path change, rationale, and rollback sketch. Link to the matching audit filename you will use after execution.
2. **Stop** and wait for **explicit human approval** in-thread (or linked ticket).
3. After execution, write or append the outcome to `plans/YYYY-MM-DD-audit.md` (same date stem as the plan unless superseded by a disambiguated pair). Include timestamp, what ran, and diff-style path summary.
4. If approval never arrives, do not execute destructive steps.

Treat `*-audit.md` as the durable record of what happened; keep it readable without Obsidian-specific features if you want repo-friendly diffs.

## Read-only source hygiene (optional)

If the user asks to **validate archives** without mutating them: for `daily-raw`, optionally check `## Interaction` / `### User` / `### Assistant` structure per `AGENTS.md`. **Do not edit** those files; report only.
