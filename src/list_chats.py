from common import get_db

def main() -> None:
    conn = get_db()
    rows = conn.execute(
        """
        SELECT chat_id, archived, chat_type, title, last_message_at
        FROM tg_chats
        ORDER BY COALESCE(last_message_at, '') DESC
        LIMIT 200
        """
    ).fetchall()

    for chat_id, archived, chat_type, title, last_message_at in rows:
        print(f"{chat_id}\tarchived={archived}\ttype={chat_type}\t{title}\t{last_message_at}")

    conn.close()

if __name__ == "__main__":
    main()
