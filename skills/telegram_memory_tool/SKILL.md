---
name: telegram_memory_tool
description: Используй локальный инструмент telegram-memory-tool для контуров Telegram-памяти: scopes, scope-info, sync, summary, digest, brief, search.
---

# Telegram Memory Tool

## Когда использовать
Используй этот skill, когда пользователь просит:

- показать доступные контуры / scope
- показать состав контура
- обновить память по контуру
- дать brief / digest / summary по контуру
- найти тему в Telegram-памяти

## Важное правило
Не рассуждай про "историю сессий", "доступ к Telegram API", "файлы сессий", "входящие сообщения" и другие обходные пути, если задача относится к Telegram Memory Tool.

Вместо этого используй локальную команду:

`/Users/openclaw/telegram-memory/bin/telegram-memory-tool`

через exec tool.

## Доступные команды

### Показать контуры
`/Users/openclaw/telegram-memory/bin/telegram-memory-tool scopes`

### Показать состав контура
`/Users/openclaw/telegram-memory/bin/telegram-memory-tool scope-info --scope <scope>`

### Обновить память по контуру
`/Users/openclaw/telegram-memory/bin/telegram-memory-tool sync --scope <scope>`

### Краткая сводка
`/Users/openclaw/telegram-memory/bin/telegram-memory-tool brief --scope <scope> --days <days> --limit 5`

### Обзор
`/Users/openclaw/telegram-memory/bin/telegram-memory-tool digest --scope <scope> --days <days> --limit 5`

### Последние записи
`/Users/openclaw/telegram-memory/bin/telegram-memory-tool summary --scope <scope> --days <days> --limit 10`

### Поиск
`/Users/openclaw/telegram-memory/bin/telegram-memory-tool search --scope <scope> --query "<query>" --days <days> --limit 10`

## Сопоставление пользовательских фраз

### Контуры
- "какие есть контуры"
- "какие есть scope"
- "покажи контуры"

=> используй `scopes`

### Состав контура
- "что входит в legal_ai"
- "покажи состав openclaw"

=> используй `scope-info --scope ...`

### Обновление
- "обнови legal_ai"
- "синкни openclaw"

=> используй `sync --scope ...`

### Brief
- "дай brief по legal_ai за 14 дней"
- "что главное в legal_ai за неделю"

=> используй `brief --scope ... --days ... --limit 5`

### Digest
- "дай digest по legal_ai"
- "сделай обзор по openclaw"

=> используй `digest --scope ... --days ... --limit 5`

### Summary
- "покажи последние записи по legal_ai"
- "дай summary по openclaw за 7 дней"

=> используй `summary --scope ... --days ... --limit 10`

### Search
- "найди в legal_ai всё про Harvey"
- "найди в openclaw всё про gmail"

=> используй `search --scope ... --query ... --days ... --limit 10`

## Как отвечать
После вызова команды верни пользователю только итоговый полезный результат, без технических деталей про shell, exec, пути, session files, API и внутренние инструменты.
