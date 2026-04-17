from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCOPES_PATH = BASE_DIR / "config" / "scopes.json"


def load_scopes() -> dict[str, tuple[int, ...]]:
    data = json.loads(SCOPES_PATH.read_text())
    scopes: dict[str, tuple[int, ...]] = {}

    for name, chat_ids in data.items():
        scopes[name] = tuple(int(x) for x in chat_ids)

    return scopes


SCOPES = load_scopes()
