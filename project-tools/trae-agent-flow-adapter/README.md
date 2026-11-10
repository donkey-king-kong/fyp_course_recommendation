# TRAE to Agent Flow Adapter

This is a project-scoped proof of concept for visualizing cooperatively
reported TRAE agents in Agent Flow. It does not inspect TRAE internals.

## What It Publishes

- Agent and parent identifiers
- Short, sanitized task and activity labels
- Lifecycle state
- Broad tool category
- Timestamp and sanitized outcome

It intentionally does not publish prompts, responses, tool arguments, file
contents, environment variables, credentials, or token counts.

## Quick Demo

Requirements: Python 3.10+ and Agent Flow. Version 0.9.4 needs the included
`agent-flow-0.9.4-jsonl-session.patch`; see the compatibility note below.

From the workspace root:

```bash
python3 project-tools/trae-agent-flow-adapter/adapter.py demo
```

The command writes:

```text
project-records/agent-observability/runtime/agent-flow-events.jsonl
project-records/agent-observability/runtime/heartbeats/*.json
```

Run `Agent Flow: Open Agent Flow` from the Command Palette. In the panel,
choose `Connect`, then `Watch JSONL File`, and select:

```text
/Users/bytedance/Downloads/SC4001 To study for finals/project-records/agent-observability/runtime/agent-flow-events.jsonl
```

The demo contains an orchestrator, a completed researcher, and a verifier
that waits and then fails.

Agent Flow 0.9.4 advertises an `agentVisualizer.eventLogPath` setting, but its
activation code does not currently read that setting. Use the interactive
`Watch JSONL File` command instead.

It also fails to announce a session when reading custom JSONL, while its
multi-session webview only displays events from an announced session. The
included patch adds that missing lifecycle message. A patched build was tested
in an isolated temporary TRAE profile; it did not replace the normal installed
extension. See
`project-records/agent-observability/verification.md` for the exact evidence
and temporary paths.

The verified patched VSIX is:

```text
project-tools/trae-agent-flow-adapter/dist/agent-flow-trae-poc-0.9.4.vsix
```

To repeat the isolated installation without affecting the normal TRAE
profile:

```bash
trae \
  --user-data-dir /tmp/trae-agent-flow-poc-user \
  --extensions-dir /tmp/trae-agent-flow-poc-extensions \
  --install-extension \
  project-tools/trae-agent-flow-adapter/dist/agent-flow-trae-poc-0.9.4.vsix \
  --force
```

## Cooperative Usage

Initialize one session:

```bash
python3 project-tools/trae-agent-flow-adapter/adapter.py init \
  --session-id local-run-001 \
  --task "Coordinate local checks" \
  --replace
```

Register and update a child:

```bash
python3 project-tools/trae-agent-flow-adapter/adapter.py start \
  --agent researcher \
  --parent orchestrator \
  --task "Inspect the event contract"

python3 project-tools/trae-agent-flow-adapter/adapter.py status \
  --agent researcher \
  --state working \
  --activity "Reviewing metadata fields"

python3 project-tools/trae-agent-flow-adapter/adapter.py tool-start \
  --agent researcher \
  --category Read

python3 project-tools/trae-agent-flow-adapter/adapter.py tool-end \
  --agent researcher \
  --category Read \
  --outcome succeeded

python3 project-tools/trae-agent-flow-adapter/adapter.py complete \
  --agent researcher \
  --parent orchestrator \
  --summary "Event contract reviewed"
```

Supported states are `starting`, `working`, `waiting`, `blocked`,
`completed`, and `failed`. Supported tool categories are `Browser`, `Edit`,
`Read`, `Search`, `Shell`, and `Test`; all other values become `Other`.

For real TRAE subagents, put these commands in the parent prompt and require
each worker to call them at start, meaningful transitions, and completion.
This reporting is cooperative: if an agent does not publish an update, the
visualizer cannot infer one.

## Retention and Removal

Keep only the newest 1,000 events:

```bash
python3 project-tools/trae-agent-flow-adapter/adapter.py prune --max-events 1000
```

Delete all runtime telemetry produced by this adapter:

```bash
python3 project-tools/trae-agent-flow-adapter/adapter.py clear --yes
```

To remove the prototype entirely, delete this adapter directory. No TRAE
settings are changed by the adapter.

## Tests

```bash
python3 -m unittest discover \
  -s project-tools/trae-agent-flow-adapter \
  -p "test_*.py" \
  -v
```

## Limitations

- TRAE does not currently provide a verified native `spawn_agent` event stream
  to this prototype.
- Parent-child relationships and status depend on cooperative reporting.
- Agent Flow may render `waiting`, `blocked`, and `failed` using its closest
  available event types rather than dedicated status badges.
- Redaction is defense in depth, not permission to send sensitive text. Keep
  task and activity labels generic.
