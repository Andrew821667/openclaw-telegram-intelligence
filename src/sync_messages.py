from __future__ import annotations

import argparse
import asyncio
import json

from common import get_client, get_db


async def main(chat_id: int, limit: int) -> None:
    client = get_client()
    conn = get_db()

    await client.start()

    conn.execute("DELETE FROM tg_messages WHERE chat_id = ?", (chat_id,))
    conn.execute("DELETE FROM tg_messages_fts WHERE chat_id = ?", (chat_id,))

    inserted = 0

    async for msg in client.iter_messages(chat_id, limit=limit):
        raw_json = json.dumps(msg.to_dict(), ensure_ascii=False, default=str)
        text = msg.message or ""
        media_type = type(msg.media).__name__ if msg.media else None

        conn.execute(
            """
            INSERT OR REPLACE INTO tg_messages(
                chat_id, message_id, date_utc, sender_id, sender_name, text,
                reply_to_message_id, has_media, media_type, raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chat_id,
                msg.id,
                msg.date.isoformat(),
                msg.sender_id,
                None,
                text,
                getattr(msg, "reply_to_msg_id", None),
                1 if msg.media else 0,
                media_type,
                raw_json,
            ),
        )

        conn.execute(
            """
            INSERT INTO tg_messages_fts(chat_id, message_id, text)
            VALUES (?, ?, ?)
            """,
            (chat_id, msg.id, text),
        )
        inserted += 1

    conn.commit()
    conn.close()
    await client.disconnect()
    print(f"Inserted {inserted} messages for chat_id={chat_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat-id", type=int, required=True)
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()

    asyncio.run(main(args.chat_id, args.limit))
