# OpenClaw Integration Checklist

- [x] Local Telegram intelligence tool implemented
- [x] Unified CLI implemented
- [x] Global command `telegram-memory` works
- [x] Stable tool entrypoint `telegram-memory-tool` works
- [x] Tool usage doc created
- [x] Confirm OpenClaw shell/exec invocation path
- [x] Confirm exec/bash permissions for target agent
- [x] Test `telegram-memory-tool scopes` from OpenClaw path
- [x] Test `telegram-memory-tool brief --scope legal_ai --days 14 --limit 5`
- [ ] Define user-facing command patterns
- [ ] Commit integration notes and results

## Proven working pattern
Use a fresh session id for exec-backed agent tests, for example:
- exec-test-001
- tgtool-scopes-001
- tgtool-brief-001
