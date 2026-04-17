from __future__ import annotations

import argparse
from datetime import datetime, timedelta, UTC

from common import get_db

LEGAL_AI_CHAT_IDS = (
    -1003845717308,  # Chat Legal AI PRO
    -1003289517656,  # Legal AI PRO channel
)

def main(query: str, days: int, limit: int) -> None:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    main(args.query, args.days, args.limit)
