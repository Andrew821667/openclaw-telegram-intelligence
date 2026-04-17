# Telegram Memory Tool

## Purpose
Local Telegram intelligence tool for:
- sync
- search
- summary
- digest
- brief

Works on top of local SQLite memory populated from Telegram user-client data.

## Stable command entrypoint
Use:

telegram-memory-tool

Do not call internal python files directly unless debugging is required.

## Main commands

### Show scopes
telegram-memory-tool scopes

### Show chats inside scope
telegram-memory-tool scope-info --scope legal_ai

### Sync scope
telegram-memory-tool sync --scope legal_ai

### Search by topic
telegram-memory-tool search --scope legal_ai --query "Harvey" --days 14 --limit 5

### Summary
telegram-memory-tool summary --scope legal_ai --days 14 --limit 5

### Digest
telegram-memory-tool digest --scope legal_ai --days 14 --limit 5

### Brief
telegram-memory-tool brief --scope legal_ai --days 14 --limit 5

### Markdown export
telegram-memory-tool brief --scope legal_ai --days 14 --limit 5 --format markdown --output outputs/legal_ai_brief.md

## Existing scopes
- legal_ai
- openclaw
- project_all

## Scope management
### Add scope
telegram-memory-tool add-scope --scope my_scope --chat-id 8451229612

### Add chat to scope
telegram-memory-tool add-to-scope --scope my_scope --chat-id 8606799512

### Remove chat from scope
telegram-memory-tool remove-from-scope --scope my_scope --chat-id 8451229612

### Delete scope
telegram-memory-tool delete-scope --scope my_scope

## Notes
- Tool is local-only.
- Data is stored in local SQLite.
- Telegram auth/session is already configured under the current user.
- Use sync before analytical commands if fresh data is needed.
- Prefer brief/digest for human-facing answers.
- Prefer search for targeted recall.
