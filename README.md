# openclaw-telegram-intelligence

Локальный Telegram intelligence / memory backend для OpenClaw.

## Что делает проект
Проект хранит и обслуживает Telegram-контуры памяти и внешних источников для OpenClaw-агентов.

Поддерживает:
- scopes / контуры чатов
- sync сообщений
- brief / summary / search
- legal-контуры для внешней правовой памяти
- интеграцию с OpenClaw через локальные skills и exec bridge

## Текущие контуры

### Общие
- `legal_ai` — legaltech / AI / рынок / новости
- `legal_sources` — общий внешний правовой контур

### Специализированные legal-контуры
- `legal_cases` — судебная практика
- `legal_commentary` — комментарии, обсуждения и прикладные мнения юристов
- `legal_law_updates` — изменения законодательства и правовые новинки
- `legal_memory` — каркас под рабочую правовую память

## Интеграция с OpenClaw

### Bots and agents
- `assistant_bot -> assistant`
- `legal_bot -> legal`

### Skills
#### Assistant
- `shared_core`
- `inbox_triage`
- `telegram_memory_tool`

#### Legal
- `shared_core`
- `legal_risk_check`
- `legal_sources_memory`

### Как это работает
OpenClaw-агенты используют локальный telegram-memory tool через `exec`.
Это позволяет ботам:
- строить brief по нужному контуру
- искать по тематике
- делать summary по источникам

## Уже работающие сценарии
Через `legal_bot` уже протестированы:
- обзор судебной практики за период
- обзор новинок законодательства
- обзор комментариев и обсуждений юристов

## Что хранится в репозитории
- код логики scopes / sync / brief / summary / search
- skills как исходники
- документация по интеграции с OpenClaw
- карта контуров

## Что НЕ хранится в репозитории
- bot tokens
- `~/.openclaw/openclaw.json`
- runtime sessions
- logs
- live message databases
- локальные секреты

## Документация
Смотри:
- `docs/openclaw-integration/SCOPES_MAP.md`
- `docs/openclaw-integration/OPENCLAW_INTEGRATION_MAP.md`
- `docs/openclaw-integration/BOOTSTRAP_OPENCLAW.md`

## Следующий этап
Следующее развитие проекта:
- общий модуль `channel_discovery`
- registry найденных и одобренных каналов
- дальнейшая подготовка к export / vector / RAG layer
