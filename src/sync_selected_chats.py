from __future__ import annotations

import argparse
import subprocess
import sys

def main(chat_ids: list[int], limit: int) -> None:
    for chat_id in chat_ids:
        print(f"=== SYNC chat_id={chat_id} ===")
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
            print(f"FAILED chat_id={chat_id}")
            sys.exit(result.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("chat_ids", nargs="+", type=int)
    args = parser.parse_args()
    main(args.chat_ids, args.limit)
