from common import get_db


def main() -> None:
    conn = get_db()

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS app_state (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tg_dialog_filters (
            filter_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            raw_json TEXT NOT NULL,
            synced_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tg_chats (
            chat_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            username TEXT,
            chat_type TEXT NOT NULL,
            archived INTEGER NOT NULL DEFAULT 0,
            last_message_at TEXT,
            raw_json TEXT NOT NULL,
            synced_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tg_messages (
            chat_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            date_utc TEXT NOT NULL,
            sender_id INTEGER,
            sender_name TEXT,
            text TEXT,
            reply_to_message_id INTEGER,
            has_media INTEGER NOT NULL DEFAULT 0,
            media_type TEXT,
            raw_json TEXT NOT NULL,
            PRIMARY KEY (chat_id, message_id)
        );

        CREATE INDEX IF NOT EXISTS idx_tg_messages_chat_date
        ON tg_messages(chat_id, date_utc DESC);

        CREATE VIRTUAL TABLE IF NOT EXISTS tg_messages_fts
        USING fts5(chat_id UNINDEXED, message_id UNINDEXED, text);
        """
    )

    conn.commit()
    conn.close()
    print("DB initialized")

if __name__ == "__main__":
    main()
