from common import get_db

LEGAL_AI_CHAT_IDS = (
    -1003845717308,  # Chat Legal AI PRO
    -1003289517656,  # Legal AI PRO channel
)

def main() -> None:
    conn = get_db()

    placeholders = ",".join("?" for _ in LEGAL_AI_CHAT_IDS)
    sql = f"""
        SELECT
            c.title,
            m.date_utc,
            m.message_id,
            substr(replace(coalesce(m.text, ''), char(10), ' '), 1, 300) as preview
        FROM tg_messages m
        JOIN tg_chats c
          ON c.chat_id = m.chat_id
        WHERE m.chat_id IN ({placeholders})
        ORDER BY m.date_utc DESC
        LIMIT 20
    """

    rows = conn.execute(sql, LEGAL_AI_CHAT_IDS).fetchall()

    for title, date_utc, message_id, preview in rows:
        print(f"[{date_utc}] {title} msg={message_id}")
        print(f"  {preview}")
        print()

    conn.close()

if __name__ == "__main__":
    main()
