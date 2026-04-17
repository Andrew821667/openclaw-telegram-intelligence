from __future__ import annotations

import asyncio
import json
from datetime import datetime, UTC

from telethon.tl.functions.messages import GetDialogFiltersRequest

from common import get_client, get_db


async def main() -> None:
    client = get_client()
    conn = get_db()

    await client.start()
    result = await client(GetDialogFiltersRequest())

    filters = getattr(result, "filters", [])
    synced_at = datetime.now(UTC).isoformat()

    conn.execute("DELETE FROM tg_dialog_filters")

    for item in filters:
        filter_id = getattr(item, "id", None)
        title = getattr(item, "title", None) or f"filter_{filter_id}"
        raw_json = json.dumps(item.to_dict(), ensure_ascii=False, default=str)

        if filter_id is None:
            continue

        conn.execute(
            """
            INSERT INTO tg_dialog_filters(filter_id, title, raw_json, synced_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(filter_id) DO UPDATE SET
                title=excluded.title,
                raw_json=excluded.raw_json,
                synced_at=excluded.synced_at
            """,
            (filter_id, str(title), raw_json, synced_at),
        )

        print(f"[FILTER] id={filter_id} title={title}")

    conn.commit()
    conn.close()
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
