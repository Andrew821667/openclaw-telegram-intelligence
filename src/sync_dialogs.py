from __future__ import annotations

import asyncio
import json
from datetime import datetime, UTC

from common import get_client, get_db


def detect_chat_type(dialog) -> str:
    if getattr(dialog, "is_user", False):
        return "user"
    if getattr(dialog, "is_group", False):
        return "group"
    if getattr(dialog, "is_channel", False):
        return "channel"
    return "unknown"


async def sync_folder(folder: int, archived: int) -> int:
    client = get_client()
    conn = get_db()

    await client.start()
    dialogs = await client.get_dialogs(folder=folder)

    synced_at = datetime.now(UTC).isoformat()
    count = 0

    for dialog in dialogs:
        entity = dialog.entity
        raw_json = json.dumps(entity.to_dict(), ensure_ascii=False, default=str)

        conn.execute(
            """
            INSERT INTO tg_chats(
                chat_id, title, username, chat_type, archived, last_message_at, raw_json, synced_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                title=excluded.title,
                username=excluded.username,
                chat_type=excluded.chat_type,
                archived=excluded.archived,
                last_message_at=excluded.last_message_at,
                raw_json=excluded.raw_json,
                synced_at=excluded.synced_at
            """,
            (
                dialog.id,
                dialog.name or str(dialog.id),
                getattr(entity, "username", None),
                detect_chat_type(dialog),
                archived,
                dialog.date.isoformat() if dialog.date else None,
                raw_json,
                synced_at,
            ),
        )
        count += 1
        print(f"[CHAT] archived={archived} id={dialog.id} type={detect_chat_type(dialog)} title={dialog.name}")

    conn.commit()
    conn.close()
    await client.disconnect()
    return count


async def main() -> None:
    normal = await sync_folder(folder=0, archived=0)
    archived = await sync_folder(folder=1, archived=1)
    print(f"Done. normal={normal}, archived={archived}")


if __name__ == "__main__":
    asyncio.run(main())
