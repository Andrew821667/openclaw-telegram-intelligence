import subprocess
import sys

LEGAL_AI_CHAT_IDS = (
    -1003845717308,  # Chat Legal AI PRO
    -1003289517656,  # Legal AI PRO channel
)

def main() -> None:
    for chat_id in LEGAL_AI_CHAT_IDS:
        print(f"=== SYNC legal_ai chat_id={chat_id} ===")
        result = subprocess.run(
            [
                sys.executable,
                "src/sync_messages.py",
                "--chat-id",
                str(chat_id),
                "--limit",
                "500",
            ]
        )
        if result.returncode != 0:
            raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
