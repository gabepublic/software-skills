# Craft Persona Reference

## Obsidian Graph Model

- Node: one Markdown file in `vault_root/memories/` representing one durable concept, entity, process, source summary, or saved Q&A.
- Edge: one semantic connection created by `[[memory-links]]` between memory pages.
- Metadata: YAML frontmatter describing node identity, type, provenance, freshness, and status.
- Backlinks: reverse edges provided by Obsidian from inbound `[[memory-links]]`; consider them when checking graph connectivity.

## Memory Metadata

Every page in `vault_root/memories/` must include YAML frontmatter with:

- `id`: filename stem in lowercase hyphen form.
- `type`: one of `concept`, `entity`, `process`, `summary`, `qa`, or `index`.
- `tags`: short topical tags.
- `sources`: raw files and/or memory pages used.
- `last_updated`: `YYYY-MM-DD HH:MM:SS`.
- `status`: `draft` or `stable`.

## Memory Page Template

```markdown
---
id: memory-page-title
type: concept
tags: [tag-1, tag-2]
sources:
  - raw/source-file.ext
last_updated: YYYY-MM-DD HH:MM:SS
status: draft
---

# Memory Page Title

**Summary**: One to two sentences describing this page.

## Notes

Main content using clear headings and short paragraphs.
Use `[[memory-links]]` to connect related concepts.

## Related pages

- [[related-concept-1]]
- [[related-concept-2]]
```

## Q&A Page Additions

For saved Q&A pages:

- Use `qa-YYYY-MM-DD-short-topic.md`.
- Set `type: qa`.
- Add `## Origin` with the date and exact user question.
- In `sources`, list the memory pages used to derive the answer.

## Citation Format

- Cite memory evidence as `(source: memories/page-name.md)`.
- Treat memory pages as the answer evidence layer.
- Cite approved raw resume files only when the user explicitly asks, approves them, or provides a specific file path.
- Place citations immediately after the factual claim or sentence they support.
- Mark unsupported claims with `(needs verification)`.
- End answers with `Sources used: memories/example-page.md; memories/another-page.md`.
- If approved raw resume files were used, also include `Approved raw files used: raw/resume-name.pdf`.
