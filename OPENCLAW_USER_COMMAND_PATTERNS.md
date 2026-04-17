# OpenClaw User Command Patterns for Telegram Memory Tool

## Goal
User should interact in natural language, without shell details.

## Supported intent patterns

### Scopes
- какие есть scope
- покажи scope
- какие контуры доступны

### Scope contents
- что входит в legal_ai
- покажи состав openclaw
- какие чаты в project_all

### Sync
- обнови legal_ai
- синкни openclaw
- обнови память по project_all

### Brief
- дай brief по legal_ai за 14 дней
- дай краткую сводку по openclaw за 7 дней
- что главное в legal_ai за неделю

### Digest
- дай digest по legal_ai за 14 дней
- сделай обзор по openclaw за неделю

### Search
- найди в legal_ai всё про Harvey
- найди в openclaw всё про gmail за 14 дней
- где в project_all обсуждали Telegram memory

## Command mapping

### Scopes
telegram-memory-tool scopes

### Scope contents
telegram-memory-tool scope-info --scope <scope>

### Sync
telegram-memory-tool sync --scope <scope>

### Brief
telegram-memory-tool brief --scope <scope> --days <days> --limit 5

### Digest
telegram-memory-tool digest --scope <scope> --days <days> --limit 5

### Search
telegram-memory-tool search --scope <scope> --query "<query>" --days <days> --limit 10

## Important implementation note
For OpenClaw exec-backed tests and integrations, prefer a fresh session id when needed.
