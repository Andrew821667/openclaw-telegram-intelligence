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


def save_scopes(scopes: dict[str, tuple[int, ...] | list[int]]) -> None:
    data = {name: [int(x) for x in values] for name, values in scopes.items()}
    SCOPES_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def add_scope(name: str, chat_ids: list[int]) -> None:
    scopes = {k: list(v) for k, v in load_scopes().items()}
    if name in scopes:
        raise SystemExit(f"Scope already exists: {name}")
    scopes[name] = list(dict.fromkeys(int(x) for x in chat_ids))
    save_scopes(scopes)


def add_to_scope(name: str, chat_ids: list[int]) -> None:
    scopes = {k: list(v) for k, v in load_scopes().items()}
    if name not in scopes:
        raise SystemExit(f"Unknown scope: {name}")
    merged = scopes[name] + [int(x) for x in chat_ids]
    scopes[name] = list(dict.fromkeys(merged))
    save_scopes(scopes)


def remove_from_scope(name: str, chat_ids: list[int]) -> None:
    scopes = {k: list(v) for k, v in load_scopes().items()}
    if name not in scopes:
        raise SystemExit(f"Unknown scope: {name}")
    remove_set = {int(x) for x in chat_ids}
    scopes[name] = [x for x in scopes[name] if x not in remove_set]
    save_scopes(scopes)


def delete_scope(name: str) -> None:
    scopes = {k: list(v) for k, v in load_scopes().items()}
    if name not in scopes:
        raise SystemExit(f"Unknown scope: {name}")
    del scopes[name]
    save_scopes(scopes)


SCOPES = load_scopes()
