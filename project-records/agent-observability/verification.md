# TRAE Agent Flow Proof of Concept

Date: 2026-11-10

## Outcome

The project-scoped cooperative adapter is implemented and its generated
events pass structural and privacy checks. Agent Flow 0.9.4 has an upstream
JSONL session regression, so the unmodified extension does not display custom
JSONL events reliably after its multi-session changes.

A minimal patch was built and installed into an isolated temporary TRAE
profile. The normal TRAE profile and its installed Agent Flow extension were
not modified.

## Architecture

```text
TRAE parent/subagent instructions
              |
              | cooperative metadata-only CLI calls
              v
project-tools/trae-agent-flow-adapter/adapter.py
              |
              +--> atomic heartbeat JSON
              |
              +--> AgentEvent JSONL
                         |
                         v
             patched Agent Flow 0.9.4
                         |
                         v
                  visual agent graph
```

## Generated Demo

The local demo contains:

- `orchestrator`: working, then completed
- `researcher`: read activity, then completed
- `verifier`: waiting, blocked, then failed

It generated 17 events:

| Event | Count |
|---|---:|
| `agent_spawn` | 3 |
| `agent_complete` | 3 |
| `subagent_dispatch` | 2 |
| `subagent_return` | 2 |
| `message` | 2 |
| `error` | 2 |
| `permission_requested` | 1 |
| `tool_call_start` | 1 |
| `tool_call_end` | 1 |

## Verification

- Adapter unit tests: 4 passed.
- Adapter syntax compilation: passed.
- Agent Flow event shape check: all records contain numeric `time`, string
  `type`, and object `payload`.
- Heartbeat schema check: all records contain agent, status, activity, and
  update time.
- Sensitive-pattern scan: no absolute user/home/tmp paths, email addresses,
  bearer tokens, API-key assignments, password assignments, secret
  assignments, or token assignments found.
- Patched Agent Flow type check: passed.
- Agent Flow extension tests: 78 passed.
- Agent Flow workspace tests: 47 passed.
- Patched VSIX packaging: passed.
- Patched VSIX SHA-256:
  `aead571d8623d38414485d21f265459f736960d96b462c521906914f24b570fb`.
- Patched extension installation into isolated TRAE profile: passed.
- Visual panel confirmation: pending manual interaction in the isolated TRAE
  window because this session has no desktop-control interface.

## Upstream Compatibility Finding

Agent Flow 0.9.4's `JsonlEventSource` correctly reads existing and appended
AgentEvent JSONL records. Its webview now delivers events only for a selected
session. The JSONL connector does not emit a `session-started` message, so no
JSONL session is selected and events remain buffered.

The stored patch:

```text
project-tools/trae-agent-flow-adapter/agent-flow-0.9.4-jsonl-session.patch
```

creates one synthetic session for the selected JSONL file, attaches that
session ID to imported events, and closes the session on disconnect.
The verified VSIX is stored at
`project-tools/trae-agent-flow-adapter/dist/agent-flow-trae-poc-0.9.4.vsix`.

## Isolated Test Profile

Temporary paths:

```text
/tmp/trae-agent-flow-poc-user
/tmp/trae-agent-flow-poc-extensions
/tmp/agent-flow-trae-poc
```

These may be deleted without affecting the normal TRAE profile.

In the isolated TRAE window:

1. Run `Agent Flow: Open Agent Flow`.
2. Choose `Connect`.
3. Choose `Watch JSONL File`.
4. Select
   `project-records/agent-observability/runtime/agent-flow-events.jsonl`.

## Limits

- This is cooperative reporting, not native `spawn_agent` telemetry.
- Missing agent updates cannot be inferred.
- Agent Flow uses approximate event types for waiting, blocked, and failed
  states.
- The redactor is defense in depth; agents must still use generic activity
  labels.
- Runtime telemetry is ignored by Git and can be removed with the adapter's
  `clear --yes` command.
