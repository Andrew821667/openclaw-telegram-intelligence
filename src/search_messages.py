from __future__ import annotations

import argparse

from common import get_db


def main(query: str, limit: int) -> None:
    conn = get_db()

    rows = conn.execute(
        """
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
        ORDER BY m.date_utc DESC
        LIMIT ?
        """,
        (query, limit),
    ).fetchall()

    for row in rows:
        title, chat_id, message_id, date_utc, snippet = row
        print(f"[{date_utc}] chat={title} ({chat_id}) msg={message_id}")
        print(f"  {snippet}")
        print()

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    main(args.query, args.limit)
