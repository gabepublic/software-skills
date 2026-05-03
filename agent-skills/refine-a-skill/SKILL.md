---
name: refine-a-skill
description: Reviews and improves existing agent skills for clear triggers, reliable workflows, progressive disclosure, and useful supporting files. Use when the user asks to review, refine, polish, improve, audit, or restructure an existing SKILL.md or skill folder.
---

# Refine a Skill

## Process

1. **Read the whole skill folder**
   - Inspect `SKILL.md` first, then any linked references, examples, assets, and scripts.
   - Identify the skill's domain, target users, triggering language, workflow, and outputs.
   - Note whether the skill is instruction-only or includes executable helpers.

2. **Diagnose the current state**
   - Check whether the description clearly says what the skill does and when to use it.
   - Verify the workflow is actionable without requiring hidden context.
   - Look for stale, duplicated, overly broad, or time-sensitive guidance.
   - Confirm terminology, file names, and examples match the actual skill contents.
   - Flag any missing validation steps, safety constraints, or bundled resources.

3. **Outline the edit plan**
   - Summarize the main issues before editing.
   - Propose concrete changes in order, including any files to add, split, or remove.
   - Keep the plan scoped to the user's requested refinement unless a structural issue blocks quality.

4. **Refine the skill**
   - Make `SKILL.md` concise and immediately usable.
   - Prefer imperative, step-by-step instructions over background explanation.
   - Move rarely needed details into one-level-deep reference files such as `REFERENCE.md` or `EXAMPLES.md`.
   - Add scripts only for deterministic, repeatable operations that benefit from explicit error handling.
   - Preserve useful existing behavior; remove vague guidance and obsolete compatibility notes.

5. **Validate the result**
   - Re-read changed files for clarity, trigger accuracy, and broken links.
   - Confirm `SKILL.md` is ideally under 100 lines.
   - Ensure the frontmatter is valid and the description stays under 1024 characters.
   - Report the refinement summary, any files changed, and remaining risks or follow-ups.

## Review Checklist

- [ ] Frontmatter has `name` and a third-person `description`.
- [ ] Description includes specific "Use when..." triggers.
- [ ] `SKILL.md` is concise, preferably under 100 lines.
- [ ] Workflow steps are actionable and ordered.
- [ ] Supporting details are split into one-level-deep files when helpful.
- [ ] Examples are concrete and relevant.
- [ ] Scripts are justified by repeatability or reliability.
- [ ] No avoidable time-sensitive claims or inconsistent terminology remain.

## Reference

Use [REFERENCE.md](REFERENCE.md) for skill structure, description guidance, and splitting criteria.
