#!/usr/bin/env python3
"""
Read Inbox Primary mail (Gmail API, OAuth 2.0).

Use a Desktop OAuth client JSON as credentials.json (or GOOGLE_CLIENT_SECRET_FILE).
That Cloud project user is unrelated to which mailbox you read: each mailbox
authorizes once. Tokens: --account EMAIL or GMAIL_ACCOUNT / GMAIL_ADDRESS →
<project root>/tokens/<sanitized-email>.json; if no account is set →
<project root>/token.json; GMAIL_TOKEN_PATH overrides the path. While the OAuth
app is in Testing, add each mailbox as a test user.

Lists Inbox Primary (INBOX + CATEGORY_PERSONAL). Env: GMAIL_LIMIT, GMAIL_UNREAD_ONLY,
GMAIL_ACCOUNT, GMAIL_ADDRESS, GMAIL_TOKEN_PATH. .env is loaded with override=True.
`python scripts/read_gmail.py --debug` logs labelIds per message on stderr.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import os
import sys
from email.header import decode_header
from pathlib import Path
from textwrap import indent

try:
    from dotenv import load_dotenv
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ModuleNotFoundError as exc:
    missing = exc.name or "required package"
    print(
        f"Missing Python module: {missing}\n"
        "Install this skill's dependencies from the skill root with:\n"
        "  python -m pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

_SKILL_ROOT = Path(__file__).resolve().parent.parent


def _infer_project_root(skill_root: Path) -> Path:
    if (
        skill_root.parent.name == "skills"
        and skill_root.parent.parent.name == ".agents"
    ):
        return skill_root.parent.parent.parent.resolve()
    return Path.cwd().resolve()


_PROJECT_ROOT = _infer_project_root(_SKILL_ROOT)
load_dotenv(_SKILL_ROOT / ".env", override=True)

# Read-only access is enough to list subjects and headers.
_SCOPES = ("https://www.googleapis.com/auth/gmail.readonly",)

# Gmail UI “Primary” tab: threads in Inbox with the Personal category label.
_INBOX_PRIMARY_LABEL_IDS: tuple[str, ...] = ("INBOX", "CATEGORY_PERSONAL")
_UNREAD_INBOX_PRIMARY_REQUIRED: frozenset[str] = frozenset(
    ("UNREAD", "INBOX", "CATEGORY_PERSONAL")
)


def _env_bool(name: str, *, default: bool = False) -> bool:
    """Parse a truthy/falsy environment variable (unknown values use `default`)."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    s = str(raw).strip()
    s = s.lstrip("\ufeff").strip().strip("'\"")
    s = s.lower()
    if s in ("1", "true", "yes", "on"):
        return True
    if s in ("0", "false", "no", "off", ""):
        return False
    return default


def _decode_mime_header(value: str | None) -> str:
    if not value:
        return ""
    parts: list[str] = []
    for chunk, enc in decode_header(value):
        if isinstance(chunk, bytes):
            parts.append(chunk.decode(enc or "utf-8", errors="replace"))
        else:
            parts.append(chunk)
    return "".join(parts)


def _decode_body_data(data: str) -> str:
    """Decode Gmail API body.data (URL-safe base64, padding optional)."""
    try:
        padded = data + "=" * (-len(data) % 4)
        raw = base64.urlsafe_b64decode(padded)
        return raw.decode("utf-8", errors="replace")
    except (ValueError, binascii.Error):
        return ""


def _collect_text_bodies(payload: dict | None) -> tuple[str, str]:
    """Walk a message payload; return (text/plain, text/html) if found."""
    if not isinstance(payload, dict):
        return "", ""

    plain, html = "", ""
    mime = (payload.get("mimeType") or "").lower()
    body = payload.get("body") or {}
    data = body.get("data")
    if isinstance(data, str) and data:
        decoded = _decode_body_data(data)
        if mime == "text/plain":
            plain = decoded
        elif mime == "text/html":
            html = decoded

    for part in payload.get("parts") or []:
        if isinstance(part, dict):
            p_plain, p_html = _collect_text_bodies(part)
            plain = plain or p_plain
            html = html or p_html

    return plain, html


def _message_body_text(payload: dict | None) -> str:
    """Prefer plain text; fall back to HTML if that is all there is."""
    plain, html = _collect_text_bodies(payload)
    text = (plain or html or "").strip()
    if not plain and html:
        return f"(HTML only)\n{html}"
    return text


def _message_has_all_labels(msg: dict, required: frozenset[str]) -> bool:
    labels = msg.get("labelIds")
    if not isinstance(labels, list):
        return False
    return required.issubset({str(x) for x in labels})


def _internal_date_ms(msg: dict) -> int:
    """Gmail internalDate: milliseconds since epoch (string or int in JSON)."""
    raw = msg.get("internalDate")
    if raw is None:
        return 0
    try:
        return int(raw)
    except (TypeError, ValueError):
        return 0


def _message_id_to_fetch_for_thread(thread: dict, *, unread_only: bool) -> str | None:
    """Message to show for a thread: newest in thread; if unread_only, newest that is unread Primary."""
    msgs = [m for m in (thread.get("messages") or []) if isinstance(m, dict)]
    if not msgs:
        return None
    msgs.sort(key=_internal_date_ms, reverse=True)
    if unread_only:
        for m in msgs:
            if not _message_has_all_labels(m, _UNREAD_INBOX_PRIMARY_REQUIRED):
                continue
            mid = m.get("id")
            if isinstance(mid, str) and mid:
                return mid
        return None
    m0 = msgs[0]
    mid = m0.get("id")
    return mid if isinstance(mid, str) and mid else None


def _row_from_full_message(
    msg: dict, *, unread_only: bool, debug: bool
) -> tuple[int, tuple[str, str, str, str]] | None:
    """Turn a messages.get(full) dict into (internalDate_ms, row) or None if filtered out."""
    if not isinstance(msg, dict):
        return None
    if unread_only and not _message_has_all_labels(msg, _UNREAD_INBOX_PRIMARY_REQUIRED):
        labels = msg.get("labelIds")
        label_set = {str(x) for x in labels} if isinstance(labels, list) else set()
        if debug:
            need = ",".join(sorted(_UNREAD_INBOX_PRIMARY_REQUIRED))
            mid = msg.get("id", "?")
            print(
                f"[debug] skip {mid} labels={sorted(label_set)} need={need}",
                file=sys.stderr,
            )
        return None
    if debug:
        labels = msg.get("labelIds")
        label_set = {str(x) for x in labels} if isinstance(labels, list) else set()
        mid = msg.get("id", "?")
        print(f"[debug] keep {mid} labels={sorted(label_set)}", file=sys.stderr)
    payload = msg.get("payload")
    if not isinstance(payload, dict):
        payload = {}
    headers = {
        h["name"]: h["value"]
        for h in payload.get("headers", [])
        if isinstance(h, dict) and "name" in h and "value" in h
    }
    subject = _decode_mime_header(headers.get("Subject"))
    from_ = _decode_mime_header(headers.get("From"))
    body = _message_body_text(payload)
    row = (str(msg.get("id") or ""), subject, from_, body)
    if not row[0]:
        return None
    return (_internal_date_ms(msg), row)


def _credentials_path() -> Path:
    raw = os.environ.get("GOOGLE_CLIENT_SECRET_FILE", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (_SKILL_ROOT / "credentials.json").resolve()


def _safe_token_filename(email: str) -> str:
    s = email.strip().lower()
    out = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in s)
    out = out.strip("._") or "account"
    while "__" in out:
        out = out.replace("__", "_")
    return out


def _resolve_token_file(account: str | None) -> Path:
    raw = os.environ.get("GMAIL_TOKEN_PATH", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    acc = (account or "").strip()
    if acc:
        d = _PROJECT_ROOT / "tokens"
        d.mkdir(parents=True, exist_ok=True)
        return (d / f"{_safe_token_filename(acc)}.json").resolve()
    return (_PROJECT_ROOT / "token.json").resolve()


def _default_gmail_account() -> str | None:
    v = (
        os.environ.get("GMAIL_ACCOUNT") or os.environ.get("GMAIL_ADDRESS") or ""
    ).strip()
    return v or None


def load_credentials(account: str | None) -> Credentials:
    """Load or refresh OAuth credentials for one mailbox; write token to disk."""
    token_file = _resolve_token_file(account)
    secrets_file = _credentials_path()

    creds: Credentials | None = None
    if token_file.is_file():
        creds = Credentials.from_authorized_user_file(str(token_file), _SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not secrets_file.is_file():
                raise FileNotFoundError(
                    f"OAuth client secrets not found: {secrets_file}\n"
                    "Create a Desktop OAuth client in Google Cloud Console, download JSON, "
                    "save as credentials.json in the skill root or set GOOGLE_CLIENT_SECRET_FILE."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets_file), _SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    return creds


def fetch_recent(
    service,
    limit: int = 10,
    unread_only: bool = False,
    *,
    debug: bool = False,
) -> list[tuple[str, str, str, str]]:
    """Up to `limit` Inbox Primary rows (id, subject, from, body).

    Uses **threads** (same as the Gmail inbox): one row per conversation, ordered
    like the client. The body/subject/from are taken from the **newest** message
    in each thread. Plain ``messages.list`` would interleave older messages from
    the same thread, which does not match the web UI order.
    """
    limit = max(1, limit)
    staged: list[tuple[int, tuple[str, str, str, str]]] = []

    def _try_add_message_id(mid: str) -> bool:
        """Fetch full message by id; append to staged if under limit and not filtered."""
        nonlocal staged
        if len(staged) >= limit:
            return False
        msg = (
            service.users().messages().get(userId="me", id=mid, format="full").execute()
        )
        built = _row_from_full_message(msg, unread_only=unread_only, debug=debug)
        if built is None:
            return False
        staged.append(built)
        return True

    def _process_thread_stub(stub: dict) -> None:
        nonlocal staged
        if len(staged) >= limit:
            return
        tid = stub.get("id")
        if not isinstance(tid, str) or not tid:
            return
        thread = (
            service.users()
            .threads()
            .get(userId="me", id=tid, format="metadata")
            .execute()
        )
        if not isinstance(thread, dict):
            return
        mid = _message_id_to_fetch_for_thread(thread, unread_only=unread_only)
        if mid:
            _try_add_message_id(mid)

    if unread_only:
        page_token: str | None = None
        while len(staged) < limit:
            list_kwargs: dict = {
                "userId": "me",
                "maxResults": min(100, max(20, (limit - len(staged)) * 5)),
                "q": "in:inbox category:primary is:unread",
            }
            if page_token:
                list_kwargs["pageToken"] = page_token
            resp = service.users().threads().list(**list_kwargs).execute()
            batch = resp.get("threads") or []
            page_token = resp.get("nextPageToken")
            if not batch:
                break
            for stub in batch:
                if len(staged) >= limit:
                    break
                _process_thread_stub(stub)
            if not page_token:
                break
    else:
        resp = (
            service.users()
            .threads()
            .list(
                userId="me",
                labelIds=list(_INBOX_PRIMARY_LABEL_IDS),
                maxResults=limit,
            )
            .execute()
        )
        for stub in resp.get("threads") or []:
            if len(staged) >= limit:
                break
            _process_thread_stub(stub)

    staged.sort(key=lambda item: item[0], reverse=True)
    return [row for _, row in staged]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read Inbox Primary Gmail (OAuth 2.0); mailbox may differ from Cloud project owner.",
    )
    parser.add_argument(
        "--account",
        metavar="EMAIL",
        default=_default_gmail_account(),
        help="Mailbox (default GMAIL_ACCOUNT or GMAIL_ADDRESS). Token: <project root>/tokens/<email>.json unless GMAIL_TOKEN_PATH.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=int(os.environ.get("GMAIL_LIMIT", "10")),
        help="Max messages (default GMAIL_LIMIT, 10).",
    )
    parser.add_argument(
        "--unread-only",
        action=argparse.BooleanOptionalAction,
        default=_env_bool("GMAIL_UNREAD_ONLY"),
        help="Unread only (default GMAIL_UNREAD_ONLY). --no-unread-only includes read.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Log token path, mailbox, unread_only, and each message labelIds on stderr.",
    )
    args = parser.parse_args()
    account = (args.account or "").strip() or None

    try:
        creds = load_credentials(account)
        service = build("gmail", "v1", credentials=creds, cache_discovery=False)
        profile = service.users().getProfile(userId="me").execute()
        addr = (profile.get("emailAddress") or "").strip() or "?"
        want = (account or "").strip()
        if want and addr.lower() != want.lower():
            raise ValueError(
                f"Token {_resolve_token_file(account)} is for {addr!r}, not {want!r}. "
                "Delete that token file and sign in as the requested mailbox."
            )
        if args.debug:
            print(
                f"[debug] token={_resolve_token_file(account)} mailbox={addr!r} "
                f"requested={want!r} unread_only={args.unread_only}",
                file=sys.stderr,
            )
        # else:
        #    print(f"Mailbox: {addr}", file=sys.stderr)
        rows = fetch_recent(
            service,
            limit=max(1, args.limit),
            unread_only=args.unread_only,
            debug=args.debug,
        )
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        return 2

    if not rows:
        print("No messages matched.")
        return 0

    for mid, subject, from_, body in rows:
        print(f"Message ID {mid}")
        print(f"  From:    {from_}")
        print(f"  Subject: {subject}")
        if body:
            print("  Body:")
            print(indent(body, "    "))
        else:
            print("  Body:    (empty or non-text parts only)")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
