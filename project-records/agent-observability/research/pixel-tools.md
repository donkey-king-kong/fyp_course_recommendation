# Animated Agent and Office Interfaces

Research date: 2026-11-10

## Scope and Method

This review covers animated-character and office-style interfaces for coding
agents, with emphasis on Pixel Agents variants, Claude Alive, Office Sim, and
alternatives that improve runtime breadth, subagent fidelity, or privacy.

Only primary sources were used: project repositories, package registries,
official extension listings, and this workspace's direct TRAE compatibility
test record. "TRAE compatible" is split into two questions:

1. Can the UI or extension run in the installed TRAE build?
2. Can it observe TRAE's own parent agents, subagents, and tools?

Those are not equivalent. The installed `trae --version` reports VS Code API
`1.107.1`. A compatible extension manifest is evidence only that TRAE can load
the extension; it is not evidence that the extension understands TRAE agent
telemetry.

## Bottom Line

- **Best polished Pixel Agents option:** original Pixel Agents. It is the most
  actively maintained Pixel branch, has both extension and browser/CLI forms,
  and shows Claude subagents and Agent Teams. It remains Claude Code-specific.
- **Best broad local observer:** Office Sim. It supports Claude Code, Codex,
  Grok, and Antigravity, has a documented adapter contract, scrubs browser
  events, and does not depend on an editor extension. It has no TRAE adapter.
- **Best minimal-data Claude hierarchy view:** Agent Desk. Its hook bridge
  records only session ID, project path, event kind, and timestamp while still
  rendering parent/child agents. It is Claude Code-only.
- **Best Copilot-oriented Pixel variant:** Copilot Pixel Agents. It supports
  Copilot Agent Mode and Claude Code hooks, keeps detailed task capture off by
  default, and can accept custom local POST events. No TRAE hook integration is
  documented.
- **Not currently loadable in this TRAE build:** Hootbu Pixel Agents declares
  VS Code `^1.109.0`, above TRAE's `1.107.1`.
- **No reviewed product natively observes TRAE agents.** The workspace's
  cooperative TRAE adapter plus patched Agent Flow remains the only directly
  tested route. It publishes sanitized metadata rather than reading TRAE
  internals.

## Comparison

| Product | License and cost | Runtime and install | Subagent visualization | Telemetry source | Privacy and data surface | Maintenance evidence | TRAE compatibility evidence |
|---|---|---|---|---|---|---|---|
| **Pixel Agents (original)** | MIT. Marketplace listing and public npm package are free; donations are optional. | Claude Code on macOS, Linux, and Windows. VS Code `^1.105.0` extension, or Node `>=20` via `npx pixel-agents`. | Yes. Subagents and persistent Agent Teams appear as separate characters with roles and lifecycle changes. | Claude hooks (`SessionStart`, `PreToolUse`, `PermissionRequest`, `Stop`, etc.); fallback and enrichment from `~/.claude/projects/*.jsonl`. | Local server defaults to `127.0.0.1`; standalone control uses a bearer token. It reads Claude transcripts and can expose an embedded terminal, so local access is broad. LAN/Tailscale use requires deliberate exposure and token handling. | v1.6.0 released and published 2026-11-10; repository not archived. | Manifest floor is below TRAE `1.107.1`, so loading is plausible. It only documents Claude telemetry, not TRAE events; it would visualize Claude Code launched in TRAE, not TRAE-native agents. |
| **Pixel Agents - Hootbu** | MIT; Marketplace extension is free. A full source build requires a separately purchased furniture tileset that is excluded from the repository. | Claude Code VS Code extension. Current manifest requires VS Code `^1.109.0`. | Strong explicit support: Task-tool children spawn near the parent, nest in the task panel, show permission bubbles, and auto-despawn. | Polls Claude Code JSONL transcript files; state transitions are heuristic. | Observational and local according to its official listing, but it reads transcripts. The source-build asset license adds a non-code dependency. No separate privacy specification was found. | Marketplace v1.3.0 updated 2026-08-18; repository pushed the same date and is not archived. | **Incompatible with installed TRAE today:** `^1.109.0` is higher than `1.107.1`. It also lacks TRAE telemetry support. |
| **Copilot Pixel Agents** | MIT; Marketplace extension is free. | GitHub Copilot Agent Mode or Claude Code. VS Code `^1.70.0`; Marketplace install, then install/reinstall hooks. Unix hooks require `sh` and `python3`; Windows uses PowerShell. | The event normalizer accepts `SubagentStart` and `SubagentStop`, but the default installer does not register subagent hooks. Actual hierarchy fidelity depends on provider events. | Copilot and Claude hooks POST to a loopback server, initially port 7823. Custom integrations may POST normalized JSON to the active local port. | Loopback-only. Detailed tool input/output/error capture is off by default, memory-only, bounded, and best-effort redacted; arguments can still contain source or private data when enabled. It does not read chat transcripts or model reasoning. | Marketplace v0.7.0 updated 2026-09-14; repository pushed 2026-11-02 and is not archived. | Manifest is loadable on TRAE's API level. No TRAE hook location or event schema is documented. A small adapter could POST cooperative TRAE events, but that integration is unimplemented and untested. |
| **Claude Alive** | MIT and public npm package; no purchase price. | Claude Code only. Node `>=20`; `npm install -g claude-alive`, `claude-alive install`, then `claude-alive start` at localhost:3141. | Yes. Children are smaller characters; an org-chart overlay shows parent-child hierarchy and agent type. | Claude lifecycle hooks over localhost HTTP/WebSocket. On completion it also parses Claude transcript JSONL for token usage and model data. | Documentation says no external calls and localhost-only endpoints. It nevertheless has a browser-accessible PTY terminal and reads transcripts for token accounting, giving it a larger local attack/data surface than a metadata-only viewer. | npm v0.5.9 published 2026-06-15. The registry-linked GitHub repository returned unavailable on 2026-11-10, weakening source auditability and maintenance confidence. | Browser UI is editor-independent, but event ingestion is Claude-specific. It cannot observe TRAE-native agents without a new event adapter; none is documented. |
| **Office Sim** | MIT, free public npm package; sponsorship optional. | Claude Code/Claude Desktop, Codex/ChatGPT Desktop, Grok, and Antigravity. Node `>=22`; `npx office-sim --open`. Browser UI at `127.0.0.1:4317`. | Yes for supported sources. The event contract includes `isSubagent`, `parentSessionId`, and `agentType`; the UI has a dedicated subagent cast slot. | Tails each runtime's local session logs; also accepts low-latency Claude HTTP hooks. A documented adapter registry normalizes sources into one event schema. | Loopback-only with host/origin guards and optional auth. Browser events are scrubbed to tool categories, basenames, URL hosts, and short summaries; raw commands, file contents, credentials, and encrypted conversations are excluded. Without `--auth`, another local process or OS user can read state. | v0.10.2 released and published 2026-11-03; repository is not archived. | Editor-independent, so it runs beside TRAE. It has no TRAE log adapter and does not accept the workspace adapter's AgentEvent JSONL directly. Its documented adapter boundary makes it the strongest candidate for adding TRAE support, but that is an engineering option, not current compatibility. |
| **Agent Desk** | MIT; Marketplace extension is free. | Claude Code, VS Code `>=1.85`. Install `paulerbrt.agent-desk`, open the panel, and approve hook installation. | Excellent Claude-specific hierarchy: each session is a Manager; delegated subagents appear as Employees, work, and leave on completion. | Claude hooks append NDJSON records that the extension tails. It can show sessions started outside its panel. | Strongest minimization claim in this set: records session ID, project path, event kind, and timestamp, not conversations, code, prompts, or tool content. Data stays in `~/.claude/agent-desk/`; event retention is bounded. | Marketplace v0.1.4 updated 2026-07-29. No linked public source repository was exposed by the official listing, so maintenance evidence is limited to Marketplace history. | Manifest floor is compatible with TRAE. Hook source is exclusively Claude Code, so it can show Claude sessions running in TRAE but not TRAE-native agents. |
| **Ctrl/Cubicles** | BUSL-1.1; Marketplace listing is free. | VS Code `>=1.107.0`; Claude Code, Codex CLI, and Augment Code. Optional browser dashboard via `npx @bulletproof-sh/ctrl-daemon@latest`. | Yes. Parent agents and subagents share the office; multi-daemon views combine projects or machines. | Watches supported agents' JSONL transcripts; local daemon streams over WebSocket. | Largest exposure in this comparison: session inspector advertises full conversations, tool calls, code output, and cost data; web sharing and remote observation are features. The daemon package declares `posthog-node`, so absence of product analytics must not be assumed. | Extension v1.2.8 updated 2026-04-02. Registry has stable daemon 0.19.0 and later alpha releases through 2026-04-19. | Engine floor narrowly fits TRAE `1.107.1`. No TRAE source is supported. Its broader runtime list does not include TRAE, and the proprietary license/privacy surface make it a weaker integration base than Office Sim. |

## Pixel Agents Variant Trade-offs

### Original

The original has overtaken the forks on maintenance and distribution breadth.
Its current release supports a VS Code panel and standalone browser interface
from one codebase, authenticates hook delivery, detects external Claude
sessions, and renders subagents. It is the default choice when the observed
runtime is Claude Code and the user wants an actively maintained product.

For TRAE, the extension can plausibly load because its engine floor is
`^1.105.0`, but its provider layer is Claude-specific. Running `claude` in a
TRAE terminal is a supported-shaped use; observing TRAE's own orchestration is
not.

### Hootbu Fork

Hootbu's fork provides the clearest Task-panel treatment of nested Claude
subagents, permissions, and cleanup. Two concerns outweigh that advantage:

- Current TRAE is below the extension's declared `^1.109.0` engine.
- It relies on transcript heuristics and documents ambiguous state transitions.

It should not be selected for the current TRAE installation without either a
TRAE upgrade or a deliberately rebuilt extension whose API use has been
tested against `1.107.1`.

### Copilot Fork

This fork is materially different rather than a simple skin. Its strongest
features are Copilot hook support, optional bounded task inspection, and a
small local POST event surface. It is the easiest Pixel variant to adapt to a
cooperative event publisher because integrations can send normalized events
without writing Copilot or Claude transcripts.

That potential does not equal present TRAE support. In particular, accepting
`SubagentStart` does not mean the default hook installer subscribes to it.

## Stronger Alternatives

### Office Sim: strongest integration base

Office Sim is stronger than the Pixel family when runtime breadth, source
auditability, and adapter design matter more than 2D office editing. Its
contract separates discovery, source adapters, normalized session state, and
browser events. A future TRAE adapter could consume a sanctioned TRAE event
stream or the cooperative metadata produced by this workspace.

The gap is concrete: Office Sim currently tails known Claude, Codex, Grok, and
Antigravity storage layouts. It does not consume Agent Flow JSONL and should
not be described as TRAE-compatible until such an adapter is built and tested.

### Agent Desk: strongest privacy-minimal viewer

Agent Desk is stronger when the requirement is simply "show Claude parents and
children without exposing content." Its event bridge deliberately excludes
prompts, conversations, code, and tool arguments. It gives up runtime breadth,
task details, and a public repository link in exchange.

### Ctrl/Cubicles: strongest remote spectacle, weakest default fit

Ctrl has broad runtime support, remote/multi-daemon views, sharing, and rich
inspection. Those features also produce the largest privacy and licensing
cost: full conversation/code inspection, a shareable web path, a PostHog
dependency, and BUSL rather than a permissive open-source license. It is a
strong presentation product but not the preferred foundation for sensitive
TRAE observability.

## TRAE Recommendation

For the current workspace:

1. Keep the cooperative `trae-agent-flow-adapter` plus patched Agent Flow as
   the verified TRAE-native path. Its test record covers event shape,
   heartbeats, sensitive-pattern scanning, patched extension tests, packaging,
   and isolated TRAE installation. Visual confirmation remains pending.
2. Use original Pixel Agents or Agent Desk only when the actual observed
   process is Claude Code running inside TRAE. Do not label that as observation
   of TRAE agents.
3. If a character office is required for native TRAE orchestration, target
   Office Sim's adapter/event boundary first. Map only the existing sanitized
   cooperative fields: agent/parent IDs, lifecycle state, broad tool category,
   timestamp, and outcome. Do not feed prompts, tool arguments, or file
   contents into a transcript-shaped compatibility layer.
4. Do not use the Hootbu build on TRAE `1.107.1` without an engine/API
   compatibility test. Do not enable remote sharing or task-content capture in
   any product until its retention and network boundary are accepted.

## Claim Verification

Two verification passes were applied:

- **Pass 1:** extracted the factual comparison claims for license/cost,
  runtime/install, subagent behavior, telemetry, privacy, maintenance, and TRAE
  compatibility.
- **Pass 2:** checked every included claim against at least one owning primary
  source below. Unsupported native-TRAE claims were removed or labelled as
  unimplemented inference. The Hootbu engine mismatch was checked directly
  against its manifest and the installed TRAE version.

No product was installed or executed. Compatibility statements are therefore
limited to manifest/runtime evidence and the separate tested Agent Flow proof.

## Primary Sources

### Pixel Agents

- [Original repository and README](https://github.com/pixel-agents-hq/pixel-agents)
- [Original VS Code Marketplace listing](https://marketplace.visualstudio.com/items?itemName=pablodelucca.pixel-agents)
- [Original npm registry metadata](https://registry.npmjs.org/pixel-agents/latest)
- [Original v1.6.0 release](https://github.com/pixel-agents-hq/pixel-agents/releases/tag/v1.6.0)
- [Hootbu repository](https://github.com/hootbu/pixel-agents)
- [Hootbu Marketplace listing](https://marketplace.visualstudio.com/items?itemName=hootbu.pixel-agent)
- [Copilot Pixel Agents repository](https://github.com/khalango02/copilot-pixel-agents)
- [Copilot Pixel Agents Marketplace listing](https://marketplace.visualstudio.com/items?itemName=cl-oliveira.copilot-pixel-agents)
- [Copilot Pixel Agents license](https://github.com/khalango02/copilot-pixel-agents/blob/master/LICENSE)

### Other Products

- [Claude Alive npm registry metadata](https://registry.npmjs.org/claude-alive/latest)
- [Office Sim repository and README](https://github.com/WahyzMaster/office-sim)
- [Office Sim npm registry metadata](https://registry.npmjs.org/office-sim/latest)
- [Office Sim event and privacy contract](https://github.com/WahyzMaster/office-sim/blob/master/docs/CONTRACT.md)
- [Agent Desk Marketplace listing](https://marketplace.visualstudio.com/items?itemName=paulerbrt.agent-desk)
- [Ctrl/Cubicles Marketplace listing](https://marketplace.visualstudio.com/items?itemName=bulletproof-sh.ctrl)
- [Ctrl daemon npm registry metadata](https://registry.npmjs.org/%40bulletproof-sh%2Fctrl-daemon/latest)

### TRAE Evidence

- [Workspace TRAE/Agent Flow verification](../verification.md)
- [Workspace cooperative adapter documentation](../../../project-tools/trae-agent-flow-adapter/README.md)
- Installed CLI evidence gathered 2026-11-10: `trae --version` returned
  `1.107.1`, commit `9da5f4f95119514cfc3ace561780174ce3193f23`, arm64.
- Version and publication dates were checked through the official Visual
  Studio Marketplace Gallery API (`/_apis/public/gallery/extensionquery`) and
  npm registry metadata on the research date.
