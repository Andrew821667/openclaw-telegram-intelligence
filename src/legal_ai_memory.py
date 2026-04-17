from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timedelta, UTC

from common import get_db
from chat_scopes import SCOPES


def normalize(text: str) -> str:
    text = (text or "").replace("\n", " ").strip().lower()
    text = " ".join(text.split())
    return text[:220]


def looks_english(text: str) -> bool:
    sample = (text or "")[:400]
    latin = sum(1 for ch in sample if ("a" <= ch.lower() <= "z"))
    cyrillic = sum(1 for ch in sample if ("а" <= ch.lower() <= "я") or ch.lower() == "ё")
    return latin > cyrillic


def get_scope_chat_ids(scope: str) -> tuple[int, ...]:
    if scope not in SCOPES:
        available = ", ".join(sorted(SCOPES))
        raise SystemExit(f"Unknown scope: {scope}. Available scopes: {available}")
    return tuple(SCOPES[scope])


def cmd_sync(scope: str, limit: int) -> None:
    chat_ids = get_scope_chat_ids(scope)
    for chat_id in chat_ids:
        print(f"=== SYNC scope={scope} chat_id={chat_id} ===")
        result = subprocess.run(
            [
                sys.executable,
                "src/sync_messages.py",
                "--chat-id",
                str(chat_id),
                "--limit",
                str(limit),
            ]
        )
        if result.returncode != 0:
            raise SystemExit(result.returncode)


def cmd_summary(scope: str, days: int, limit: int, skip_english: bool) -> None:
    chat_ids = get_scope_chat_ids(scope)
    conn = get_db()

    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    placeholders = ",".join("?" for _ in chat_ids)

    sql = f"""
        SELECT
            c.title,
            m.chat_id,
            m.message_id,
            m.date_utc,
            coalesce(m.text, '') as text
        FROM tg_messages m
        JOIN tg_chats c
          ON c.chat_id = m.chat_id
        WHERE m.chat_id IN ({placeholders})
          AND m.date_utc >= ?
        ORDER BY m.date_utc DESC
        LIMIT 300
    """

    rows = conn.execute(sql, (*chat_ids, since)).fetchall()

    seen = set()
    kept = 0

    for title, chat_id, message_id, date_utc, text in rows:
        key = normalize(text)
        if not key or key in seen:
            continue
        if skip_english and looks_english(text):
            continue
        seen.add(key)

        preview = text.replace("\n", " ").strip()[:400]
        lang_mark = "[EN] " if looks_english(text) else ""
        print(f"[{date_utc}] {title} ({chat_id}) msg={message_id}")
        print(f"  {lang_mark}{preview}")
        print()

        kept += 1
        if kept >= limit:
            break

    conn.close()


def cmd_search(scope: str, query: str, days: int, limit: int) -> None:
    chat_ids = get_scope_chat_ids(scope)
    conn = get_db()

    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    placeholders = ",".join("?" for _ in chat_ids)

    sql = f"""
        SELECT
            c.title,
            m.chat_id,
            m.message_id,
            m.date_utc,
            snippet(tg_messages_fts, 2, '[', ']', ' … ', 16) AS snippet
        FROM tg_messages_fts
        JOIN tg_messages m
          ON m.chat_id = tg_messages_fts.chat_id
         AND m.message_id = tg_messages_fts.message_id
        JOIN tg_chats c
          ON c.chat_id = m.chat_id
        WHERE tg_messages_fts MATCH ?
          AND m.chat_id IN ({placeholders})
          AND m.date_utc >= ?
        ORDER BY m.date_utc DESC
        LIMIT ?
    """

    rows = conn.execute(sql, (query, *chat_ids, since, limit)).fetchall()

    for title, chat_id, message_id, date_utc, snippet in rows:
        print(f"[{date_utc}] chat={title} ({chat_id}) msg={message_id}")
        print(f"  {snippet}")
        print()

    conn.close()


def cmd_scopes() -> None:
    for name, chat_ids in SCOPES.items():
        print(f"{name}: {', '.join(str(x) for x in chat_ids)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    scopes_parser = subparsers.add_parser("scopes")

    sync_parser = subparsers.add_parser("sync")
    sync_parser.add_argument("--scope", default="legal_ai")
    sync_parser.add_argument("--limit", type=int, default=500)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--scope", default="legal_ai")
    summary_parser.add_argument("--days", type=int, default=7)
    summary_parser.add_argument("--limit", type=int, default=10)
    summary_parser.add_argument("--skip-english", action="store_true")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--scope", default="legal_ai")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--days", type=int, default=14)
    search_parser.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    if args.command == "scopes":
        cmd_scopes()
    elif args.command == "sync":
        cmd_sync(args.scope, args.limit)
    elif args.command == "summary":
        cmd_summary(args.scope, args.days, args.limit, args.skip_english)
    elif args.command == "search":
        cmd_search(args.scope, args.query, args.days, args.limit)


if __name__ == "__main__":
    main()
