from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def get_client() -> TelegramClient:
    api_id = int(require_env("TG_API_ID"))
    api_hash = require_env("TG_API_HASH")
    session_name = os.getenv("TG_SESSION_NAME", "main")

    sessions_dir = BASE_DIR / "data" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    return TelegramClient(str(sessions_dir / session_name), api_id, api_hash)


def get_db() -> sqlite3.Connection:
    db_path = Path(
        os.getenv(
            "TG_DB_PATH",
            str(BASE_DIR / "data" / "telegram_memory.sqlite3"),
        )
    )
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn
