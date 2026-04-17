from common import get_db

PROJECT_CHAT_IDS = (
    -1003845717308,  # Chat Legal AI PRO
    -1003289517656,  # Legal AI PRO channel
    8451229612,      # Andrew Assistant Bot
    8606799512,      # Andrew Legal Bot
)

def main() -> None:
    conn = get_db()

    query = "OpenClaw"
    limit = 20

    placeholders = ",".join("?" for _ in PROJECT_CHAT_IDS)
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
        ORDER BY m.date_utc DESC
        LIMIT ?
    """

    rows = conn.execute(sql, (query, *PROJECT_CHAT_IDS, limit)).fetchall()

    for title, chat_id, message_id, date_utc, snippet in rows:
        print(f"[{date_utc}] chat={title} ({chat_id}) msg={message_id}")
        print(f"  {snippet}")
        print()

    conn.close()

if __name__ == "__main__":
    main()
