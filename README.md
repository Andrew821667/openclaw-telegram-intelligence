# openclaw-telegram-intelligence

MVP локального Telegram intelligence / memory слоя для OpenClaw.

## Что уже умеет
- авторизация через Telegram user-client
- локальная SQLite база
- синхронизация чатов и сообщений
- полнотекстовый поиск
- поиск по теме за период
- dedup summary по Legal AI-контуру

## Основные скрипты
- `src/init_db.py` — инициализация БД
- `src/list_dialog_filters.py` — чтение Telegram folders / filters
- `src/sync_dialogs.py` — синк списка чатов
- `src/sync_messages.py` — синк сообщений по одному чату
- `src/sync_selected_chats.py` — синк набора чатов
- `src/sync_legal_ai.py` — синк Legal AI-контура
- `src/search_messages.py` — общий поиск
- `src/search_messages_in_chat.py` — поиск внутри одного чата
- `src/search_legal_ai_chats.py` — поиск по Legal AI-контуру
- `src/search_legal_ai_topic_days.py` — поиск по теме за период
- `src/summary_legal_ai_recent.py` — последние сообщения
- `src/summary_legal_ai_dedup.py` — dedup summary
- `src/summary_legal_ai_days.py` — summary за период

## Настройка
Создать `.env` на основе `.env.example`.

Пример:
TG_API_ID=
TG_API_HASH=
TG_SESSION_NAME=main
TG_DB_PATH=/Users/openclaw/telegram-memory/data/telegram_memory.sqlite3

## Первый запуск
1. Создать venv
2. Установить зависимости
3. Инициализировать БД
4. Пройти Telegram login
5. Синхронизировать чаты и сообщения

## Полезные команды

### Синк Legal AI-контура
cd ~/telegram-memory && source .venv/bin/activate && unset TG_API_ID TG_API_HASH TG_SESSION_NAME TG_DB_PATH && python src/sync_legal_ai.py

### Поиск по теме за период
cd ~/telegram-memory && source .venv/bin/activate && python src/search_legal_ai_topic_days.py --query "Harvey" --days 14 --limit 10

### Dedup summary
cd ~/telegram-memory && source .venv/bin/activate && python src/summary_legal_ai_dedup.py

## Важно
В репозиторий не коммитятся:
- `.env`
- `data/telegram_memory.sqlite3`
- session-файлы Telethon
- логи
