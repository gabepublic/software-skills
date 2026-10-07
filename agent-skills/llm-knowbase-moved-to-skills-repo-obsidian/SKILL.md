---
name: llm-knowbase
description: Gathers facts from the llm-brain Obsidian vault (Knowledge Base or KB) and constructs sourced answers from its memory notes. Use when the user asks to search, answer from, summarize, update, or organize the listed Obsidian vault.
---

# LLM Knowledge Base

## Vault Contract

Use `C:\zObsidian\llm-brain\` as `vault_root`.

If `vault_root` cannot be found, stop and warn the user with `Vault missing!`.

Expected structure:

```text
vault_root/raw/               # source documents; immutable once added
vault_root/memories/          # agent-maintained markdown memory pages
vault_root/memories/index.md  # table of contents for memory pages
vault_root/memories/log.md    # append-only operation log
```

## Guardrails

- Read from `vault_root/memories/**` and `vault_root/templates/**`.
- Do not read or modify `vault_root/.obsidian/**`, `vault_root/.git/**`, `.gitignore`, or `.gitattributes`.
- Never modify existing files in `vault_root/raw/`; add new raw source files only when the user explicitly asks.
- Never search `vault_root/raw/**` or use raw files to answer questions.
- Write or update `vault_root/memories/**` only when the user asks for a memory change or approves saving a result.
- Preserve Obsidian links as `[[memory-links]]`; do not replace them with Markdown links inside memory pages.

## Answer Workflow

When the user asks a question that should be answered from the vault:

1. Verify `vault_root` exists.
2. Read `vault_root/memories/index.md` first when present.
3. Search `vault_root/memories/**` for relevant concepts, entities, processes, summaries, and Q&A notes.
4. Read the relevant memory pages and follow `[[memory-links]]` to related memory pages when more context is needed.
5. Construct a direct answer from memory-page evidence only.
6. Cite factual claims with the most specific memory page available.
7. Say explicitly when the memory pages do not contain enough evidence.

Prefer concise answers. Include only the amount of source detail needed for the user's request.

## Evidence Rules

- Treat memory pages as the only evidence source for answers.
- Do not present uncited vault-derived facts as certain.
- If sources conflict, state the contradiction and cite each side.
- If a useful claim is plausible but unsupported by the vault, mark it as needing verification.
- Do not treat the user's question as factual evidence.

## Memory Updates

When the user approves saving or updating memory:

1. Create or update a page in `vault_root/memories/`, not `raw/`.
2. Use one durable topic per page and a lowercase-hyphen `.md` filename.
3. Include YAML frontmatter, source paths, a short summary, notes, and related pages.
4. Use `type: qa` only for saved question-answer results.
5. Record the originating question under `## Origin` for Q&A pages.
6. Append a brief entry to `vault_root/memories/log.md` describing the change.
7. Update `vault_root/memories/index.md` if a page is added, renamed, or materially reclassified.

See [REFERENCE.md](REFERENCE.md) for the memory schema, page template, graph model, and citation format.
