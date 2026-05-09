---
name: raw-to-obsidian
description: Ingests read-only sources from `daily-raw` and `daily-memory` into interlinked `memories/` pages with enforced YAML metadata, body citations, `memories/index.md`, and append-only `memories/log.md`; stores pending high-risk plans and execution audits as dated files under `plans/`; lints or audits the memory graph. Use when the user invokes raw-to-obsidian, ingests memory from raw/daily notes, updates index or log, uses `plans/` for plan/audit pairs, validates metadata and links, or audits graph health.
---

# raw-to-obsidian

Build and maintain the **memory graph** under `memories/` from immutable sources. Obsidian syntax: [.agents/skills/obsidian-markdown/SKILL.md](../obsidian-markdown/SKILL.md).

## Canonical structure

```text
daily-raw/          # source transcripts — read only, never modify
daily-memory/       # distilled daily notes — read only, never modify
memories/           # agent-maintained memory graph (.md nodes)
memories/index.md   # table of contents for memory pages
memories/log.md     # append-only operation log for memory edits
plans/              # pending plans + post-execution audits (not graph nodes)
plans/YYYY-MM-DD-plan.md
plans/YYYY-MM-DD-audit.md
raw                 # source documents — read only, immutable, never modify
```

## Graph model

- **Node:** one `.md` file in `memories/` = one durable concept, entity, process, source summary, Q&A capture, or index.
- **Edge:** one intentional `[[link]]` to another memory page’s filename stem (treat these as **memory links**; Obsidian resolves by note name).
- **Metadata:** YAML frontmatter on every page (schema below).
- **Backlinks:** use Obsidian backlinks to judge connectivity; reduce orphans per Global rules.

## Modes

| Mode | Writes `memories/`? | Focus |
|------|---------------------|--------|
| **ingest** | Yes (after user alignment) | Sources → summary + concept/entity/process nodes |
| **lint** | No | Memory graph + metadata + format compliance |
| **audit** | No | Same checks as lint, plus contradiction/outdated-risk report |

Confirm **mode**, **source paths**, and (for ingest) **user alignment** on focus before writing.

## Node metadata (required on every `memories/**/*.md`)

| Key | Rule |
|-----|------|
| `id` | Filename stem, `lowercase-hyphen` (e.g. `machine-learning` for `machine-learning.md`) |
| `type` | One of: `concept`, `entity`, `process`, `summary`, `qa`, `index` |
| `tags` | Short topical tags (YAML list) |
| `sources` | List of contributing raw paths and/or memory pages |
| `last_updated` | `YYYY-MM-DD HH:MM:SS` |
| `status` | `draft` or `stable` |

## Global rules

- **Never** modify `daily-raw/**`, `daily-memory/**` or `raw/**`.
- Filenames: `lowercase-hyphen.md` only; **one primary topic** per page; split when mixed.
- Plain language, short sections; meaningful `[[memory-links]]` between pages.
- For **unresolved links:** if the link is important but the content isn't ready, create the file with status: draft and a "STUB" header.
- After **any** memory change: update `memories/index.md` and append `memories/log.md`.
- If categorization is unclear, **ask the user** before writing.
- Factual claims in body: **Citation rules** (below).

## Ingest workflow

**Trigger:** user asks for ingestion.

1. Read the **full** scoped document(s) in `daily-raw/`, `daily-memory/` and `raw/` (read-only).
2. Share **key takeaways** and proposed focus with the user; **align before writing**.
3. Create a **note** page: normalized name from source basename — strip final extension, lowercase, replace `.` and `_` with `-`, collapse duplicate hyphens → `filename-note.md` (e.g. `2026-05-08-raw.md` → `2026-05-08-note.md`).
4. Set or refresh metadata on **every** touched node.
5. Create/update `concept` / `entity` / `process` nodes for major ideas (expect **many** nodes per source, often ~10–15).
   - NOTE: Create new nodes only for distinct concepts that don't yet exist or require significant expansion; otherwise, update existing nodes.
6. Resolve all broken `[[links]]` (stub or unlink).
7. Update `memories/index.md` with new/changed pages and **one-line** descriptions.
8. Append **one** entry to `memories/log.md`: date, source(s), short change summary.

## Citation rules (body text)

- Every factual claim cites a source immediately after: `(source: filename.ext)` (relative path from vault root when needed).
- Conflicting sources: state the contradiction explicitly.
- No evidence: mark as needing verification.
- Keep citations in the body even when paths appear in `sources:` frontmatter.

## Lint / audit workflow (memory pages)

When asked to lint or audit `memories/`:

1. Contradictions across pages.  
2. Orphan pages (no inbound `[[links]]`).  
3. Named concepts lacking a dedicated page.  
4. Likely outdated claims (stale `last_updated`, superseded `sources`).  
5. Metadata schema + Obsidian-format compliance.  
6. Unresolved `[[wikilinks]]`.  
7. Output a **numbered** list with **concrete fixes**.

## Guardrails (summary)

- **Allowed read:** `daily-raw/**`, `daily-memory/**`, `raw/**`, `templates/**`, `memories/**`, `plans/**`  
- **Allowed write:** `memories/**` (ingest/lint fixes); `plans/**` only for `*-plan.md` / `*-audit.md` artifacts per [.agents/skills/raw-to-obsidian/REFERENCE.md](REFERENCE.md#plans-folder)  
- **Forbidden touch:** `.obsidian/**`, `.git/**`, `.gitignore`, `.gitattributes`  
- **High-risk trigger** (deletes, drops, prod-like changes): follow [.agents/skills/raw-to-obsidian/REFERENCE.md](REFERENCE.md#high-risk-change-protocol).
