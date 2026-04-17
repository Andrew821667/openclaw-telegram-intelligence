# Маршрутизация пользовательских запросов для Telegram Memory Tool

## Назначение
Этот файл описывает, как переводить естественные пользовательские запросы в команды `telegram-memory-tool`.

## Важно
Это не исчерпывающий навсегда список всех возможных сценариев.
Это базовый рабочий набор команд для первой интеграции Telegram Memory Tool в OpenClaw.

## Базовые пользовательские сценарии

### 1. Показать доступные контуры
Примеры запросов:
- какие есть контуры
- какие группы чатов доступны
- покажи доступные scope

Команда:
telegram-memory-tool scopes

### 2. Показать состав контура
Примеры запросов:
- что входит в legal_ai
- покажи состав openclaw
- какие чаты входят в project_all

Команда:
telegram-memory-tool scope-info --scope <scope>

### 3. Обновить память по контуру
Примеры запросов:
- обнови legal_ai
- синкни openclaw
- обнови память по project_all

Команда:
telegram-memory-tool sync --scope <scope>

### 4. Дать краткий brief
Примеры запросов:
- дай brief по legal_ai за 14 дней
- дай краткую сводку по openclaw за неделю
- что главное в legal_ai за 7 дней

Команда:
telegram-memory-tool brief --scope <scope> --days <days> --limit 5

### 5. Дать обзорный digest
Примеры запросов:
- дай digest по legal_ai за 14 дней
- сделай обзор по openclaw за неделю

Команда:
telegram-memory-tool digest --scope <scope> --days <days> --limit 5

### 6. Найти тему
Примеры запросов:
- найди в legal_ai всё про Harvey
- найди в openclaw всё про gmail за 14 дней
- где в project_all обсуждали Telegram memory

Команда:
telegram-memory-tool search --scope <scope> --query "<query>" --days <days> --limit 10

### 7. Показать последние записи
Примеры запросов:
- покажи последние записи по legal_ai
- дай summary по openclaw за 7 дней
- что недавно было в project_all

Команда:
telegram-memory-tool summary --scope <scope> --days <days> --limit 10

## Практические замечания
- Для exec-вызовов через OpenClaw лучше использовать свежий session_id при тестах.
- Пользователю не нужно показывать shell, exec, пути к бинарникам и внутреннюю механику.
- В пользовательском ответе лучше возвращать только итоговый результат.
- Список сценариев можно расширять по мере развития интеграции.
