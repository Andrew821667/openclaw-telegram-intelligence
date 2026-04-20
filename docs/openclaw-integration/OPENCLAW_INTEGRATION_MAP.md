# OPENCLAW INTEGRATION MAP

## Bots and agents
- assistant_bot -> assistant
- legal_bot -> legal

## Assistant agent skills
- shared_core
- inbox_triage
- telegram_memory_tool

## Legal agent skills
- shared_core
- legal_risk_check
- legal_sources_memory

## Current behavior
assistant_bot:
- общий assistant
- memory / ops / общие контуры

legal_bot:
- юридический анализ
- external legal memory:
  - legal_cases
  - legal_law_updates
  - legal_commentary

## Tool bridge
OpenClaw agents используют локальный telegram-memory tool через exec.
