from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, UTC
from pathlib import Path

from common import get_db
from chat_scopes import SCOPES, add_scope, add_to_scope, remove_from_scope, delete_scope


STOPWORDS = {
    "и", "в", "на", "с", "по", "для", "из", "что", "как", "это", "к",
    "о", "об", "от", "до", "за", "под", "при", "или", "а", "но", "не",
    "the", "and", "for", "with", "from", "that", "this", "into", "about",
    "legal", "ai"
}


def normalize(text: str) -> str:
    text = (text or "").replace("\n", " ").strip().lower()
    text = " ".join(text.split())
    return text[:220]


def looks_english(text: str) -> bool:
    sample = (text or "")[:400]
    latin = sum(1 for ch in sample if ("a" <= ch.lower() <= "z"))
    cyrillic = sum(1 for ch in sample if ("а" <= ch.lower() <= "я") or ch.lower() == "ё")
    return latin > cyrillic


def tokenize(text: str) -> list[str]:
    cleaned = []
    for ch in (text or "").lower():
        if ch.isalnum() or ch in ("_", "ё"):
            cleaned.append(ch)
        else:
            cleaned.append(" ")
    words = "".join(cleaned).split()
    return [w for w in words if len(w) >= 4 and w not in STOPWORDS]


def get_scope_chat_ids(scope: str) -> tuple[int, ...]:
    if scope not in SCOPES:
        available = ", ".join(sorted(SCOPES))
        raise SystemExit(f"Unknown scope: {scope}. Available scopes: {available}")
    return tuple(SCOPES[scope])


def emit_output(lines: list[str], output: str | None) -> None:
    content = "\n".join(lines).rstrip() + "\n"
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Saved to {path}")
    else:
        print(content, end="")


def format_record_terminal(header: str, body: str) -> list[str]:
    return [header, f"  {body}", ""]


def format_record_markdown(header: str, body: str) -> list[str]:
    return [f"### {header}", "", body, ""]


def cmd_sync(scope: str, limit: int) -> None:
    chat_ids = get_scope_chat_ids(scope)
    for chat_id in chat_ids:
        print(f"=== SYNC scope={scope} chat_id={chat_id} ===")
        result = subprocess.run(
            [
                sys.executable,
                "src/sync_messages.py",
                "--chat-id",
                str(chat_id),
                "--limit",
                str(limit),
            ]
        )
        if result.returncode != 0:
            raise SystemExit(result.returncode)


def cmd_summary(scope: str, days: int, limit: int, skip_english: bool, fmt: str, output: str | None) -> None:
    chat_ids = get_scope_chat_ids(scope)
    conn = get_db()

    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    placeholders = ",".join("?" for _ in chat_ids)

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
          AND m.date_utc >= ?
        ORDER BY m.date_utc DESC
        LIMIT 300
    """

    rows = conn.execute(sql, (*chat_ids, since)).fetchall()

    seen = set()
    kept = 0
    lines: list[str] = []

    if fmt == "markdown":
        lines.append(f"# Summary for scope `{scope}`")
        lines.append("")
        lines.append(f"- Days: {days}")
        lines.append(f"- Limit: {limit}")
        lines.append("")

    for title, chat_id, message_id, date_utc, text in rows:
        key = normalize(text)
        if not key or key in seen:
            continue
        if skip_english and looks_english(text):
            continue
        seen.add(key)

        preview = text.replace("\n", " ").strip()[:400]
        lang_mark = "[EN] " if looks_english(text) else ""
        header = f"[{date_utc}] {title} ({chat_id}) msg={message_id}"
        body = f"{lang_mark}{preview}"

        if fmt == "markdown":
            lines.extend(format_record_markdown(header, body))
        else:
            lines.extend(format_record_terminal(header, body))

        kept += 1
        if kept >= limit:
            break

    conn.close()
    emit_output(lines, output)


def cmd_search(scope: str, query: str, days: int, limit: int, fmt: str, output: str | None) -> None:
    chat_ids = get_scope_chat_ids(scope)
    conn = get_db()

    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    placeholders = ",".join("?" for _ in chat_ids)

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
          AND m.date_utc >= ?
        ORDER BY m.date_utc DESC
        LIMIT ?
    """

    rows = conn.execute(sql, (query, *chat_ids, since, limit)).fetchall()
    lines: list[str] = []

    if fmt == "markdown":
        lines.append(f"# Search results for `{query}` in scope `{scope}`")
        lines.append("")
        lines.append(f"- Days: {days}")
        lines.append(f"- Limit: {limit}")
        lines.append("")

    for title, chat_id, message_id, date_utc, snippet in rows:
        header = f"[{date_utc}] chat={title} ({chat_id}) msg={message_id}"
        body = snippet

        if fmt == "markdown":
            lines.extend(format_record_markdown(header, body))
        else:
            lines.extend(format_record_terminal(header, body))

    conn.close()
    emit_output(lines, output)


def cmd_digest(scope: str, days: int, limit: int, fmt: str, output: str | None) -> None:
    chat_ids = get_scope_chat_ids(scope)
    conn = get_db()

    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    placeholders = ",".join("?" for _ in chat_ids)

    sql = f"""
        SELECT
            c.title,
            m.date_utc,
            coalesce(m.text, '') as text
        FROM tg_messages m
        JOIN tg_chats c
          ON c.chat_id = m.chat_id
        WHERE m.chat_id IN ({placeholders})
          AND m.date_utc >= ?
        ORDER BY m.date_utc DESC
        LIMIT 500
    """

    rows = conn.execute(sql, (*chat_ids, since)).fetchall()
    conn.close()

    lines: list[str] = []

    if not rows:
        emit_output(["Нет данных за указанный период."], output)
        return

    topic_counter = Counter()
    chat_counter = Counter()
    unique_previews: list[tuple[str, str, str]] = []
    seen = set()

    for title, date_utc, text in rows:
        chat_counter[title] += 1
        topic_counter.update(tokenize(text))

        norm = " ".join((text or "").replace("\n", " ").split()).strip().lower()[:220]
        if norm and norm not in seen:
            seen.add(norm)
            preview = " ".join((text or "").replace("\n", " ").split()).strip()[:280]
            unique_previews.append((date_utc, title, preview))

    if fmt == "markdown":
        lines.append(f"# Digest for scope `{scope}`")
        lines.append("")
        lines.append(f"- Period: last {days} days")
        lines.append(f"- Messages scanned: {len(rows)}")
        lines.append("")
        lines.append("## Top chats")
        lines.append("")
        for title, count in chat_counter.most_common(5):
            lines.append(f"- {title}: {count}")
        lines.append("")
        lines.append("## Top topics")
        lines.append("")
        for word, count in topic_counter.most_common(12):
            lines.append(f"- {word}: {count}")
        lines.append("")
        lines.append("## Key recent items")
        lines.append("")
        for date_utc, title, preview in unique_previews[:limit]:
            lines.append(f"### [{date_utc}] {title}")
            lines.append("")
            lines.append(preview)
            lines.append("")
    else:
        lines.append(f"Digest for scope: {scope}")
        lines.append(f"Period: last {days} days")
        lines.append(f"Messages scanned: {len(rows)}")
        lines.append("")
        lines.append("Top chats:")
        for title, count in chat_counter.most_common(5):
            lines.append(f"- {title}: {count}")
        lines.append("")
        lines.append("Top topics:")
        for word, count in topic_counter.most_common(12):
            lines.append(f"- {word}: {count}")
        lines.append("")
        lines.append("Key recent items:")
        for date_utc, title, preview in unique_previews[:limit]:
            lines.append(f"- [{date_utc}] {title}")
            lines.append(f"  {preview}")
            lines.append("")

    emit_output(lines, output)


def cmd_scopes() -> None:
    for name, chat_ids in SCOPES.items():
        print(f"{name}: {', '.join(str(x) for x in chat_ids)}")


def cmd_scope_info(scope: str) -> None:
    chat_ids = get_scope_chat_ids(scope)
    conn = get_db()

    placeholders = ",".join("?" for _ in chat_ids)
    sql = f"""
        SELECT chat_id, archived, chat_type, title, last_message_at
        FROM tg_chats
        WHERE chat_id IN ({placeholders})
        ORDER BY title
    """

    rows = conn.execute(sql, chat_ids).fetchall()

    for chat_id, archived, chat_type, title, last_message_at in rows:
        print(f"{chat_id}\tarchived={archived}\ttype={chat_type}\t{title}\t{last_message_at}")

    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("scopes")

    scope_info_parser = subparsers.add_parser("scope-info")
    scope_info_parser.add_argument("--scope", default="legal_ai")

    sync_parser = subparsers.add_parser("sync")
    sync_parser.add_argument("--scope", default="legal_ai")
    sync_parser.add_argument("--limit", type=int, default=500)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--scope", default="legal_ai")
    summary_parser.add_argument("--days", type=int, default=7)
    summary_parser.add_argument("--limit", type=int, default=10)
    summary_parser.add_argument("--skip-english", action="store_true")
    summary_parser.add_argument("--format", choices=["terminal", "markdown"], default="terminal")
    summary_parser.add_argument("--output")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--scope", default="legal_ai")
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument("--days", type=int, default=14)
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--format", choices=["terminal", "markdown"], default="terminal")
    search_parser.add_argument("--output")

    digest_parser = subparsers.add_parser("digest")
    digest_parser.add_argument("--scope", default="legal_ai")
    digest_parser.add_argument("--days", type=int, default=14)
    digest_parser.add_argument("--limit", type=int, default=5)
    digest_parser.add_argument("--format", choices=["terminal", "markdown"], default="terminal")
    digest_parser.add_argument("--output")

    add_scope_parser = subparsers.add_parser("add-scope")
    add_scope_parser.add_argument("--scope", required=True)
    add_scope_parser.add_argument("--chat-id", dest="chat_ids", action="append", type=int, required=True)

    add_to_scope_parser = subparsers.add_parser("add-to-scope")
    add_to_scope_parser.add_argument("--scope", required=True)
    add_to_scope_parser.add_argument("--chat-id", dest="chat_ids", action="append", type=int, required=True)

    remove_from_scope_parser = subparsers.add_parser("remove-from-scope")
    remove_from_scope_parser.add_argument("--scope", required=True)
    remove_from_scope_parser.add_argument("--chat-id", dest="chat_ids", action="append", type=int, required=True)

    delete_scope_parser = subparsers.add_parser("delete-scope")
    delete_scope_parser.add_argument("--scope", required=True)

    args = parser.parse_args()

    if args.command == "scopes":
        cmd_scopes()
    elif args.command == "scope-info":
        cmd_scope_info(args.scope)
    elif args.command == "sync":
        cmd_sync(args.scope, args.limit)
    elif args.command == "summary":
        cmd_summary(args.scope, args.days, args.limit, args.skip_english, args.format, args.output)
    elif args.command == "search":
        cmd_search(args.scope, args.query, args.days, args.limit, args.format, args.output)
    elif args.command == "digest":
        cmd_digest(args.scope, args.days, args.limit, args.format, args.output)
    elif args.command == "add-scope":
        add_scope(args.scope, args.chat_ids)
        print(f"Added scope: {args.scope}")
    elif args.command == "add-to-scope":
        add_to_scope(args.scope, args.chat_ids)
        print(f"Updated scope: {args.scope}")
    elif args.command == "remove-from-scope":
        remove_from_scope(args.scope, args.chat_ids)
        print(f"Updated scope: {args.scope}")
    elif args.command == "delete-scope":
        delete_scope(args.scope)
        print(f"Deleted scope: {args.scope}")


if __name__ == "__main__":
    main()
