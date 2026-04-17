from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timedelta, UTC

from common import get_db

LEGAL_AI_CHAT_IDS = (
    -1003845717308,  # Chat Legal AI PRO
    -1003289517656,  # Legal AI PRO channel
)


def normalize(text: str) -> str:
    text = (text or "").replace("\n", " ").strip().lower()
    text = " ".join(text.split())
    return text[:220]


def cmd_sync(limit: int) -> None:
    for chat_id in LEGAL_AI_CHAT_IDS:
        print(f"=== SYNC legal_ai chat_id={chat_id} ===")
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


def cmd_summary(days: int, limit: int) -> None:
    conn = get_db()

    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    placeholders = ",".join("?" for _ in LEGAL_AI_CHAT_IDS)

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

    rows = conn.execute(sql, (*LEGAL_AI_CHAT_IDS, since)).fetchall()

    seen = set()
    kept = 0

    for title, chat_id, message_id, date_utc, text in rows:
        key = normalize(text)
        if not key or key in seen:
            continue
        seen.add(key)

        preview = text.replace("\n", " ").strip()[:400]
        print(f"[{date_utc}] {title} ({chat_id}) msg={message_id}")
        print(f"  {preview}")
        print()

        kept += 1
        if kept >= limit:
            break

    conn.close()


def cmd_search(query: str, days: int, limit: int) -> None:
    conn = get_db()

    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    placeholders = ",".join("?" for _ in LEGAL_AI_CHAT_IDS)

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

    rows = conn.execute(sql, (query, *LEGAL_AI_CHAT_IDS, since, limit)).fetchall()

    for title, chat_id, message_id, date_utc, snippet in rows:
        print(f"[{date_utc}] chat={title} ({chat_id}) msg={message_id}")
        print(f"  {snippet}")
        print()

    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync")
    sync_parser.add_argument("--limit", type=int, default=500)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--days", type=int, default=7)
    summary_parser.add_argument("--limit", type=int, default=10)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--days", type=int, default=14)
    search_parser.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    if args.command == "sync":
        cmd_sync(args.limit)
    elif args.command == "summary":
        cmd_summary(args.days, args.limit)
    elif args.command == "search":
        cmd_search(args.query, args.days, args.limit)


if __name__ == "__main__":
    main()
