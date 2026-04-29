---
name: summarize-emails
description: >
  Reads the user's Gmail Inbox Primary (recent threads via OAuth) and produces
  short summaries. Use when the user asks to summarize email, check inbox,
  list recent mail, recap messages, or describe what came in. Not for sending
  mail or changing labels—read and summarize only.
compatibility: >
  Python 3 with dependencies in requirements.txt. Gmail OAuth (credentials /
  tokens per scripts/read_gmail.py). Network access to Gmail API. Run commands
  from this skill's root directory (the folder that contains SKILL.md) so .env
  and paths resolve correctly.
metadata:
  version: "1.0"
---

## When to use

Activate for requests like: summarize my email, what’s in my inbox, recap recent Gmail, unread summary, brief me on the last N messages.

## Before you run

1. **Working directory**: Use the directory containing this `SKILL.md` as the current working directory when invoking Python (same folder as `scripts/`).
2. **Dependencies**: In a fresh environment, install this skill's bundled Python dependencies before running the script:

   ```bash
   python -m pip install -r requirements.txt
   ```

   If the script reports missing Python modules, run the same command from the skill root and retry.
3. **Credentials**: If the script exits with errors about missing files or auth, follow the docstring in `scripts/read_gmail.py` (Desktop OAuth client, tokens, optional `.env` beside `SKILL.md`).

## Steps

1. Choose `--limit` from the user’s request (e.g. “last 3” → `3`). If they give no number, use `10` (or `5` for a very short recap).
2. Add `--unread-only` only if they explicitly want unread mail only.
3. Run:

   ```bash
   python scripts/read_gmail.py --limit <N>
   ```

   Example: `python scripts/read_gmail.py --limit 5`

4. Treat stdout as **EMAIL_MESSAGES**. If the process exits non-zero, read stderr, explain the failure to the user, and do not invent message content.
5. Summarize **EMAIL_MESSAGES** for the user:
   - One or two sentences per message: sender, subject, and the main point or action (if the body is present).
   - Keep chronological order as printed unless the user asks otherwise.
   - If output says `No messages matched`, say so clearly; do not fabricate emails.

## Output quality

- Prefer neutral, factual wording; call out deadlines, questions directed at the user, or obvious action items.
- Do not dump full bodies unless the user asks for verbatim content.

## Example (shape of your reply)

**User:** “Summarize my last two emails.”

**Agent:** After a successful run with `--limit 2`, reply in prose like:

- **From / Subject:** One-sentence gist.
- **From / Subject:** One-sentence gist.

## Edge cases

| Situation | What to do |
|-----------|------------|
| Exit code 1, FileNotFoundError / credentials | Tell the user what is missing; point them to `scripts/read_gmail.py` header comments. |
| Exit code 2, Gmail API error | Quote or paraphrase the error; suggest token refresh or Google account status. |
| Token mailbox mismatch (ValueError text in stderr) | Explain that the saved token is for a different address; suggest deleting the token file and re-authorizing. |
| Empty inbox / no matches | Report no matching messages; offer to retry with `--no-unread-only` if they used unread-only and might have no unread mail. |

Optional flags are documented in the script: `--account EMAIL`, `--debug` (label diagnostics on stderr).
