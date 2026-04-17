from common import get_db

LEGAL_AI_CHAT_IDS = (
    -1003845717308,  # Chat Legal AI PRO
    -1003289517656,  # Legal AI PRO channel
)

def normalize(text: str) -> str:
    text = (text or "").replace("\n", " ").strip().lower()
    text = " ".join(text.split())
    return text[:220]

def main() -> None:
    conn = get_db()

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
        ORDER BY m.date_utc DESC
        LIMIT 100
    """

    rows = conn.execute(sql, LEGAL_AI_CHAT_IDS).fetchall()

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
        if kept >= 10:
            break

    conn.close()

if __name__ == "__main__":
    main()
