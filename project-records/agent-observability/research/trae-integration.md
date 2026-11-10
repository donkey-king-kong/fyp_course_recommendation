# TRAE Native Agent Observability for External Visualizers

Date: 2026-11-10
Role: `trae-integration`, parent `orchestrator`

## Executive finding

TRAE has two documented integration surfaces relevant to observability:

1. Native subagents, configured as Markdown files and invoked automatically by
   the built-in Agent.
2. Command hooks for session, prompt, tool, stop, and notification events.

Neither surface documents a `spawn_agent` event, subagent start/stop callback,
subagent ID, parent ID, or child ID. The installed TRAE 3.6.13 public VS Code
extension API also has no event for observing the built-in Agent or its
subagents. A normal extension can implement its own chat participant and
language-model tools, but it cannot subscribe to TRAE's native delegation
lifecycle through a supported API.

Therefore, a visualizer can reliably consume documented session/tool events,
but a native parent-child graph currently requires cooperative publication by
the parent and workers. A metadata-only JSONL side channel, optionally exposed
as an MCP tool, is the safest practical design. It does not require modifying
TRAE or reading private state.

## Documented native surfaces

### Native subagents

The official subagent documentation states that:

- A subagent is defined by a Markdown file.
- The built-in Agent matches the user's task against subagent descriptions and
  decides whether to invoke one.
- A subagent executes in an independent context with its allowed tools and MCP
  servers, then returns its result to the built-in Agent.
- Project definitions live in `.trae/agents/<name>.md`; the feature must be
  enabled under Settings > Beta > Enable Subagents Directory.
- Frontmatter exposes `name`, `description`, `model`, `tools`,
  `disallowedTools`, and `mcpServers`.

The documented definition contains a logical subagent name, but no runtime
instance ID or parent ID. The invocation sequence describes dispatch and
return semantically, but exposes no callback, event stream, transcript path,
or extension API.

Evidence:

- [TRAE: Subagents](https://docs.trae.ai/ide/subagents?_lang=en), especially
  "How are subagents invoked?", "Write subagent files", and "Available tools".
- [TRAE: Create and manage custom agents](https://docs.trae.ai/ide/agent?_lang=en)
  documents callable custom agents and independent contexts, but no runtime
  lifecycle API.
- [TRAE changelog](https://docs.trae.ai/ide/changelog?_lang=en): subagent
  directory loading was added in 3.5.67 on 2026-06-17. An earlier 3.5.63
  hotfix mentions expandable subagent cards, which establishes a native UI,
  not an external event contract.

### Hooks

TRAE documents exactly six hook events:

| Event | Timing | Useful observable data |
|---|---|---|
| `SessionStart` | Before the first chat in a new session | Session start |
| `UserPromptSubmit` | Before Agent processes a user query | Query boundary |
| `PreToolUse` | Before a tool executes | Tool call ID, standardized/original tool name, input |
| `PostToolUse` | After a tool executes | Same call ID plus response |
| `Stop` | Before Agent ends the current query | Completion attempt and final assistant message |
| `Notification` | Confirmation waits or task completion | Notification type, message, optional tool call ID |

Common stdin fields are `session_id`, `cwd`, `hook_event_name`, and
`workspace_roots`. Tool hooks add `tool_use_id`, `tool_name`,
`llm_tool_name`, and tool input/response. Notification supports
`idle_prompt`, `permission_prompt`, `document_review`, `ask_user_question`,
and `browser_interaction`.

The official standardized tool list is `Read`, `Write`, `Edit`, `Glob`,
`Grep`, `LS`, `RunCommand`, `WebSearch`, `WebFetch`, `AskUserQuestion`,
`Skill`, and `mcp__<server>__<tool>`. It does not list `spawn_agent`,
`Task`, `Agent`, delegation, or another subagent operation.

No hook schema includes `agent_id`, `parent_id`, `child_id`, subagent name, or
subagent role. TRAE does not document `SubagentStart`, `SubagentStop`,
`SessionEnd`, or a general event subscription API. Whether the six hooks also
run inside a subagent context is not specified, so it must not be assumed.

Evidence:

- [TRAE: Automate with hooks](https://docs.trae.ai/ide/automate-actions-with-hooks?_lang=en)
- [TRAE: Hook configuration reference](https://docs.trae.ai/ide/hook-configuration-reference?_lang=en)
- [TRAE changelog](https://docs.trae.ai/ide/changelog?_lang=en): hooks were
  added in 3.5.66 on 2026-06-10.

## Is `spawn_agent` exposed?

No documented TRAE surface reviewed here exposes a `spawn_agent` lifecycle.

| Question | Result |
|---|---|
| Is `spawn_agent` a documented hook event? | No |
| Is it a documented standardized tool hook name? | No |
| Do hook payloads expose runtime subagent IDs? | No |
| Do hook payloads expose parent-child IDs? | No |
| Does the subagent Markdown schema expose runtime IDs? | No |
| Does the installed public extension API expose native Agent lifecycle events? | No |

This is a statement about supported, evidenced interfaces. TRAE necessarily
tracks enough internal state to render subagent cards, but internal state is
not a public contract and was not inspected or modified for this research.

## Can VS Code extensions observe native subagents?

Not through the installed public extension API.

The installed build is TRAE 3.6.13 over VS Code 1.107.1. Its shipped
`vscode.d.ts` provides:

- `chat.createChatParticipant(...)` for an extension's own participant;
- a handler invoked only for requests directed to that participant;
- `onDidReceiveFeedback` for that participant's results;
- `lm.registerTool(...)`, `lm.tools`, and `lm.invokeTool(...)` for registered
  language-model tools;
- `lm.onDidChangeChatModels` for model availability.

There is no `spawn_agent`, subagent, parent/child, built-in chat observer, or
global tool-call event in the declaration. A tool invocation token associates
an extension-owned tool invocation with a chat request, but it is opaque and
does not expose a session or agent graph.

Installed evidence:

- `/Applications/Trae.app/Contents/Resources/app/product.json`
  - `appVersion`: `3.6.13`
  - `vscodeVersion`: `1.107.1`
  - SHA-256:
    `193b0bfbe9f96e6892ef6b25b1e9505df1edb9a8a73173540163594bedf64775`
- `/Applications/Trae.app/Contents/Resources/app/out/vscode-dts/vscode.d.ts`
  - `ChatParticipant`: approximately lines 19711-19746
  - `chat.createChatParticipant`: approximately lines 20038-20050
  - language-model tools: approximately lines 20698-20737
  - SHA-256:
    `563ffbe504c294455060931278855da9807a8b3b0f66f7f7769821c6b080bdf2`

### Bundled `DSL Agent Logs` is not a public lifecycle API

TRAE bundles `cloudide.dsl-agent-logs`, a log viewer fed by an internal
`dsl-agent-logs.addLogEntry` command. Its primary source says a Rust component
pushes records through TRAE TypeScript code into the extension. Records are
grouped by `session_id` and may include `taskId` and `agentName`.

This proves that TRAE can feed a bundled extension through an internal
producer. It does not provide a third-party subscription API, parent-child
relationships, or native subagent start/stop events. VS Code extensions also
have no public command-execution interception event, so another extension
cannot passively observe those command arguments.

Installed evidence:

- `/Applications/Trae.app/Contents/Resources/app/extensions/cloudide.dsl-agent-logs/README.md`
- `/Applications/Trae.app/Contents/Resources/app/extensions/cloudide.dsl-agent-logs/src/types.ts`
- `/Applications/Trae.app/Contents/Resources/app/extensions/cloudide.dsl-agent-logs/package.json`
- Manifest SHA-256:
  `7f7d3fe0fa66994d39ee864cd7903dbec200fba3d293dd78d756588bdcfe31b0`

## Existing tools

### Tools explicitly supporting TRAE subagent definitions

Two primary-source projects explicitly target TRAE's native subagent file
format:

- **Sigil** has a `trae` subagent adapter whose target is
  `.trae/agents/<slug>.md`, cites TRAE's official subagent documentation, and
  warns that Enable Subagents Directory must be on.
  [Source at reviewed commit](https://github.com/dgesteves/sigil/blob/0ae3da25b99539d405d49030b4f640587f35fdf2/packages/sigil/src/compile/formats/subagent.ts#L244-L255)
- **TeamAI CLI** documents delivery to `.trae/agents`, omission of incompatible
  model IDs, and TRAE's beta-setting requirement.
  [Source documentation at reviewed commit](https://github.com/Tencent/teamai-cli/blob/b8c811db0cfe6795fe5bfbd31c094dbb295bcce9/docs/guide/sharing.md)

These tools support authoring/distribution of native subagent definitions.
Neither cited source claims to observe live TRAE subagent instances.

### Visualizer found in the installed environment

**Agent Flow 0.9.4** is installed and can watch generic AgentEvent JSONL. Its
manifest and upstream README explicitly name Claude Code and Codex runtimes,
not TRAE. Its source configures Claude hooks including `SubagentStart` and
`SubagentStop`; those are Claude hook names and are absent from TRAE's
documented hook list.

Accordingly, Agent Flow can visualize TRAE only through an adapter-produced
JSONL stream. It does not natively discover TRAE subagents.

Evidence:

- [Agent Flow README](https://github.com/patoles/agent-flow)
- `~/.trae/extensions/simon-p.agent-flow-0.9.4/package.json`
- `~/.trae/extensions/simon-p.agent-flow-0.9.4/dist/extension.js`
- Installed manifest SHA-256:
  `954322b55bf70164f621a3dfee0455bc7039571c02f43e88685e1d094a627827`

No source or installed extension reviewed claimed runtime observability for
TRAE-native subagents. GitHub code searches for TRAE subagent visualizers,
TRAE agent observability, and `.trae/agents` visualizers returned no such
project before the authenticated search rate limit was reached. This is not an
exhaustive registry-wide nonexistence proof.

## Safe integration options

### 1. Hooks for a flat session/tool timeline

A project hook can append sanitized records for:

- session start;
- pre/post tool use;
- permission waits;
- task completion notification;
- stop attempts.

This path is deterministic for the documented events and can feed JSONL
directly. It cannot produce an evidenced native parent-child graph.

Privacy requirements:

- Do not persist `prompt`, `last_assistant_message`, raw `tool_input`, or raw
  `tool_response`.
- Map tool names to broad categories and retain only generated IDs, status,
  monotonic time, and generic labels.
- Open JSONL with append-only permissions and use one record per write.
- Bound retention and keep the output outside source control.
- Treat `session_id` and `tool_use_id` as pseudonymous metadata.

### 2. Cooperative publisher for a parent-child graph

The parent generates a safe agent ID, passes its own ID and the child ID in
the delegated task, and publishes dispatch before delegation. Each subagent
publishes start, meaningful status transitions, and completion. The parent
publishes return.

The publisher can be:

- a small CLI, such as the existing project adapter; or
- a local MCP server with `start`, `status`, `tool`, and `complete` methods.

MCP is a documented fit because TRAE subagent definitions can allow named MCP
servers and tools. It also makes the observability operation explicit in the
worker's tool list. This remains cooperative: skipped calls, crashes, and
misreported IDs cannot be reconstructed.

The project adapter already implements this model:

```text
project-tools/trae-agent-flow-adapter/adapter.py
```

It writes metadata-only Agent Flow JSONL plus atomic heartbeats under:

```text
project-records/agent-observability/runtime/
```

### 3. Hybrid hooks plus cooperative relationships

Use hooks for objective session/tool timing and cooperative events only for
dispatch, start, return, parent ID, and child ID. Join the streams with a
generated correlation ID passed to the child.

This reduces cooperative reporting volume while keeping relationship claims
explicit. It must not infer that two events are parent and child merely
because their timestamps overlap.

## Recommended minimal JSONL contract

```json
{"schema":"trae-observe/v1","event":"agent.dispatch","session":"opaque","agent":"child-7","parent":"orchestrator","time":"RFC3339"}
{"schema":"trae-observe/v1","event":"agent.state","session":"opaque","agent":"child-7","state":"working","time":"RFC3339"}
{"schema":"trae-observe/v1","event":"tool.end","session":"opaque","agent":"child-7","category":"Read","outcome":"succeeded","time":"RFC3339"}
{"schema":"trae-observe/v1","event":"agent.complete","session":"opaque","agent":"child-7","outcome":"succeeded","time":"RFC3339"}
```

Keep labels optional and generic. Do not include prompts, responses, command
arguments, paths, file contents, environment variables, credentials, or token
values. A visualizer should tolerate missing starts/ends, duplicate records,
out-of-order writes, unknown states, and orphaned children.

## Limitations

- Official documentation was reviewed on 2026-11-10 and can change.
- Installed implementation evidence is specific to TRAE 3.6.13 on macOS
  arm64.
- Absence from public declarations and docs does not prove absence from
  private implementation; private implementation is intentionally out of
  scope.
- No TRAE settings, hooks, binaries, databases, or internal files were
  modified.
- No runtime experiment was performed with a native subagent because this
  session did not expose a callable native subagent tool.
- Hook behavior inside subagent contexts is undocumented and unverified.
- Tool discovery was bounded by installed extensions, official docs, primary
  repositories, and GitHub search availability. The later GitHub searches hit
  an authenticated rate limit.
- Existing Agent Flow verification is separate:
  `project-records/agent-observability/verification.md`.

## Practical conclusion

Build external visualization around a documented, metadata-only side channel,
not TRAE internals. Use native hooks for flat session/tool facts. Use an
explicit CLI or MCP publisher when a parent-child graph is required. Label
cooperative relationships as reported rather than observed, and do not claim
that TRAE currently exposes native `spawn_agent` telemetry.
