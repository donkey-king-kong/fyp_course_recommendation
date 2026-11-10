# Open-Source Agent Observability Tools

Research date: 2026-11-10

## Scope and decision

This review targets observation of coding subagents: parent-child hierarchy,
tool calls, status, timelines, traces, and live dashboards. Claims below use
official repositories and product documentation. "TRAE fit" is an integration
assessment, not a vendor claim: TRAE has no verified native telemetry stream in
this workspace, so any fit depends on cooperative events, readable local logs,
or custom OpenTelemetry (OTel) spans.

**Recommendation:** keep **Agent Flow** as the immediate live topology view and
trial **OpenLIT** as the local durable trace/dashboard layer. The existing
metadata-only adapter already maps TRAE parent, child, lifecycle, and broad tool
events into Agent Flow's small JSONL contract. OpenLIT is the closest
Apache-2.0 local alternative with an explicit coding-agent product surface,
OTLP ingestion, tool-call traces, timelines, analytics, and a trace-derived
agent DAG. It does not document native TRAE support, so a TRAE-to-OTLP adapter
would still be required.

Use **Phoenix** when trace debugging, querying, and coding-agent MCP access
matter more than an exact live parent-child graph. Use **Opik** instead when an
OSI-approved full-platform license is required. Do not deploy Langfuse or
AgentOps solely for the current cooperative state feed; their richer
LLM-observability stacks add more infrastructure and content-handling surface
than this metadata-only use case needs. OpenLLMetry is useful as instrumentation
but is not a dashboard by itself.

## Comparison

| Tool | License and cost | Deployment | Ingestion and model | Graph, trace, timeline, and live behavior | Privacy | TRAE fit |
|---|---|---|---|---|---|---|
| **Agent Flow** | Apache-2.0; no product fee for the repository. [S1] | Local `npx` web app, source build, or VS Code-compatible extension. [S1] | Claude hooks, Codex rollout JSONL, or newline-delimited `AgentEvent` objects with numeric `time`, typed `type`, and object `payload`; appended records are tailed. [S1][S2] | Best direct match: live interactive agent-node graph, branches, tool calls, return flows, multi-session tabs, timeline, transcript, and file-attention view. Claude hooks stream through an HTTP relay/SSE; JSONL can be watched live. [S1] | Local extension/source builds send no telemetry. The published `npx` binary has opt-out aggregate telemetry; official docs say prompts, paths, tool calls, user data, and environment variables are excluded. [S1] | **High now.** Existing adapter works cooperatively and sends only sanitized metadata. Limitation: missing TRAE updates cannot be inferred, and local verification found an Agent Flow 0.9.4 custom-JSONL session regression requiring the stored patch. [L1][L2] |
| **AgentOps** | MIT repository, including app; self-hosted software has no license fee. Hosted pricing was not exposed in the official static page retrieved for this review, so verify in the vendor dashboard before procurement. [S3] | Hosted service or self-hosted dashboard/API. Official self-host architecture uses a frontend/API, Supabase or PostgreSQL/auth, ClickHouse, and an OTel Collector; Docker and production deployment guides are provided. [S4] | OTel-based SDK and OTLP/HTTP exporter; default hosted trace endpoint is `/v1/traces`, and self-hosting exposes OTLP gRPC 4317 and HTTP 4318. Sessions contain hierarchical `AGENT`, `WORKFLOW`, `OPERATION/TASK`, `LLM`, and `TOOL` spans. [S5][S6] | Dashboard provides session list, chronological timeline, hierarchical tree, messages, analytics, and session replay. Exports are periodic rather than a documented zero-latency live state channel. [S5][S6] | LLM events include messages by default. Host OS, Python, anonymized hostname, SDK version, and process ID are collected unless environment collection is disabled. [S5][S7] | **Medium.** Strong hierarchy and tool semantics if the adapter emits OTel spans. No documented TRAE integration or generic cooperative JSONL input; heavier than Agent Flow for state-only observation. |
| **Langfuse** | MIT core, except separately licensed `ee` directories. Self-host core is infrastructure-cost only; Cloud pricing at review time: Hobby free, Core USD 29/month, Pro USD 199/month, Enterprise USD 2,499/month, with usage/add-ons described on the pricing page. [S8][S9] | Cloud, local Docker Compose, or production Kubernetes/Helm and cloud templates. Self-host v4 uses web/worker services plus PostgreSQL, ClickHouse, Redis/Valkey, and S3-compatible storage. [S9][S10] | Native Python/JS SDKs, public API, or OTLP. Data is `session -> trace -> nested observation`; observations represent LLM, tool, retrieval, event, and span steps and carry IDs, type, name, latency, metadata, and trace/session attributes. SDK exporters batch in the background. [S11] | Detailed nested traces, sessions, observations, costs, metrics, and dashboards. Near-live after exporter flush, not a dedicated live agent-status/topology surface; short-lived processes must explicitly flush. [S11] | Self-host keeps application data in chosen infrastructure, but OSS sends aggregated deployment telemetry to PostHog by default, including counts and up to 30 user email domains; `TELEMETRY_ENABLED=false` disables it. Raw traces/prompts are not included in that telemetry. [S12] | **Medium.** Generic OTLP makes an adapter feasible and the trace UI is mature, but parent-child agent identity needs conventions in span names/attributes. Infrastructure is comparatively heavy for local observation. |
| **Arize Phoenix** | **Elastic License 2.0, source-available and not OSI open source**; self-hosting is free with no documented feature gates, usage limits, or license fees. ELv2 prohibits offering a substantial hosted/managed version to third parties. [S13][S14] | Single local process (`uvx arize-phoenix serve`), Docker/Compose, Kubernetes/Helm, or cloud templates. [S14][S15] | OTel/OpenInference spans through Python/TypeScript wrappers, auto-instrumentation, or manual spans; projects and sessions organize traces. Phoenix also exposes OpenAPI/REST, GraphQL, CLI, and MCP access. [S15][S16] | Real-time trace UI, nested spans, tool/LLM calls, costs, evaluations, and trace querying. It is a trace tree, not an Agent Flow-style live orchestration graph. [S16] | Self-hosted trace/evaluation/dataset data stays in the operator's infrastructure. Basic UI analytics are on by default and can be disabled; a documented air-gap mode disables telemetry and external resources. [S17] | **Medium-high for durable debugging.** Easy local server, generic OTel, and first-party coding-agent CLI/MCP support. A custom TRAE span adapter is required; lifecycle states and sibling topology need explicit attributes. License may be disqualifying for teams requiring OSI terms. |
| **OpenLLMetry + OpenTelemetry** | OpenLLMetry and OTel core repositories are Apache-2.0; instrumentation is free. Backend storage/UI cost depends on the selected OTel-compatible destination. [S18][S19] | Library/SDK in the observed process, usually exporting OTLP to a local or remote OTel Collector and then to Phoenix, Langfuse, Grafana/Tempo, Jaeger, or another backend. [S18][S20] | Standard OTLP/HTTP spans plus OpenLLMetry annotations for workflows, tasks, agents, and tools; supports automatic and manual instrumentation and many backends. [S18][S20] | No graph, timeline, or dashboard by itself. Live behavior depends on batch processor/export interval and backend refresh. Its value is vendor-neutral instrumentation and routing. | OpenLLMetry logs prompts, completions, and embeddings into span attributes **by default**. Set `TRACELOOP_TRACE_CONTENT=false` or per-workflow controls before using it for metadata-only coding-agent telemetry. [S21] | **Medium as a foundation, low alone.** Good schema/export layer for a new TRAE adapter, but it does not solve visualization. Prefer direct OTel SDKs if no supported library is being auto-instrumented. |
| **OpenLIT** | Apache-2.0; full platform is free to self-host, with operator infrastructure cost. [S22] | Local Docker Compose or Kubernetes/Helm. OTLP defaults to local port 4318 and UI to port 3000 in the official quickstart. [S23] | OTel-native traces and metrics using `gen_ai.*`; Python/TypeScript SDKs plus a CLI that normalizes Claude Code, Cursor, Codex, Windsurf, and OpenCode hooks into `gen_ai.*` and `coding_agent.*` conventions. [S22][S24] | Explicit coding-agent dashboards for sessions, cost, outcomes, tools, users, and conversational drill-down. Agent overview includes a live, trace-derived DAG built from up to 500 recent traces, with call counts, p50 latency, and errors. [S25] | Coding-agent CLI sends only to the configured OpenLIT endpoint. Anonymous product/SDK usage telemetry is on by default and can be disabled with `TELEMETRY_ENABLED=false`; official docs list event counts sent to PostHog. [S24][S26] | **High potential.** Closest local-first durable complement to Agent Flow. TRAE is not listed, so build a small OTLP exporter from the cooperative adapter; keep content capture off and emit sanitized lifecycle/tool spans only. |
| **Opik** | Apache-2.0 full platform; free to self-host. [S27] | Local Docker Compose with data under `~/opik`; Kubernetes/Helm for production; hosted Comet option also exists. [S27][S28] | Python/TypeScript SDKs, REST API, framework integrations, and native OTLP/HTTP at `/api/v1/private/otel/v1/traces`. Model is thread -> trace -> hierarchical span; common spans include LLM, function/tool, data, and external API calls. [S29][S30] | Full trace trees, tool calls, timing, token/cost data, dashboards, online evaluation, and agent-graph logging. Official Claude Code plugin captures turns, tools, and subagents; generic OTel is also supported. [S27][S31] | Self-host can keep data in local infrastructure. Trace concepts include exact inputs/outputs, and official guidance warns against logging PII and points to filtering; metadata-only use therefore requires deliberate filtering. [S29] | **Medium-high.** Strong Apache alternative with coding-agent precedent and OTLP. No documented TRAE integration; custom cooperative spans are needed. Better for stored trace analysis than instantaneous status. |

## Suggested TRAE architecture

```text
TRAE parent and subagents
        |
        | cooperative, sanitized lifecycle/tool updates
        v
project-tools/trae-agent-flow-adapter/adapter.py
        |
        +--> AgentEvent JSONL --> Agent Flow (live hierarchy/status)
        |
        `--> optional OTLP spans --> OpenLIT (durable traces/DAG/analytics)
```

Keep the current privacy boundary in both outputs: agent and parent IDs,
generic activity labels, lifecycle state, broad tool category, timestamps,
and outcomes only. Do not export prompts, responses, tool arguments, file
contents, paths, environment values, credentials, or model content. Use one
OTel trace per orchestrated run, one span per agent lifetime, and nested spans
for broad tool activity. Suggested attributes are:

- `service.name=trae-cooperative-observer`
- `gen_ai.agent.name=<sanitized agent id>`
- `trae.parent_agent=<sanitized parent id>`
- `trae.state=starting|working|waiting|blocked|completed|failed`
- `gen_ai.tool.name=Read|Search|Shell|Edit|Test|Browser|Other`
- `trae.outcome=succeeded|failed`

This dual-output design preserves Agent Flow's immediate graph while avoiding
lock-in for historical traces. It should remain opt-in and cooperative until
TRAE exposes a verified native event stream.

## Sources

- **[S1]** Agent Flow official repository and README:
  <https://github.com/patoles/agent-flow>
- **[S2]** Agent Flow protocol and JSONL event source:
  <https://github.com/patoles/agent-flow/blob/main/extension/src/protocol.ts>,
  <https://github.com/patoles/agent-flow/blob/main/extension/src/event-source.ts>
- **[S3]** AgentOps official repository:
  <https://github.com/AgentOps-AI/agentops>
- **[S4]** AgentOps self-hosting overview:
  <https://docs.agentops.ai/v2/self-hosting/overview>
- **[S5]** AgentOps core concepts:
  <https://docs.agentops.ai/v2/concepts/core-concepts>
- **[S6]** AgentOps SDK reference and exporter implementation:
  <https://docs.agentops.ai/v2/usage/sdk-reference>,
  <https://github.com/AgentOps-AI/agentops/blob/main/agentops/sdk/core.py>
- **[S7]** AgentOps host environment:
  <https://docs.agentops.ai/v2/concepts/host-env>
- **[S8]** Langfuse license:
  <https://github.com/langfuse/langfuse/blob/main/LICENSE>
- **[S9]** Langfuse pricing:
  <https://langfuse.com/pricing>
- **[S10]** Langfuse self-hosting:
  <https://langfuse.com/self-hosting>
- **[S11]** Langfuse data model:
  <https://langfuse.com/docs/observability/data-model>
- **[S12]** Langfuse self-host telemetry:
  <https://langfuse.com/self-hosting/security/telemetry>
- **[S13]** Phoenix license:
  <https://github.com/Arize-ai/phoenix/blob/main/LICENSE>
- **[S14]** Phoenix self-hosting:
  <https://arize.com/docs/phoenix/self-hosting>
- **[S15]** Phoenix tracing setup:
  <https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing>
- **[S16]** Phoenix official repository:
  <https://github.com/Arize-ai/phoenix>
- **[S17]** Phoenix self-host privacy:
  <https://arize.com/docs/phoenix/self-hosting/security/privacy>
- **[S18]** OpenLLMetry official repository:
  <https://github.com/traceloop/openllmetry>
- **[S19]** OpenTelemetry specification repository:
  <https://github.com/open-telemetry/opentelemetry-specification>
- **[S20]** OpenLLMetry OTel Collector integration:
  <https://www.traceloop.com/docs/openllmetry/integrations/otel-collector>
- **[S21]** OpenLLMetry content privacy controls:
  <https://www.traceloop.com/docs/openllmetry/privacy/traces>
- **[S22]** OpenLIT official repository:
  <https://github.com/openlit/openlit>
- **[S23]** OpenLIT quickstart and self-hosting:
  <https://docs.openlit.io/latest/openlit/otlp-receiver>,
  <https://docs.openlit.io/latest/openlit/installation>
- **[S24]** OpenLIT coding-agent overview:
  <https://docs.openlit.io/latest/openlit/coding-agents/overview>
- **[S25]** OpenLIT agent graph:
  <https://docs.openlit.io/latest/openlit/observability/agents/overview>
- **[S26]** OpenLIT anonymous telemetry:
  <https://docs.openlit.io/latest/openlit/developer-resources/anonymous-telemetry>
- **[S27]** Opik official repository:
  <https://github.com/comet-ml/opik>
- **[S28]** Opik local deployment:
  <https://www.comet.com/docs/opik/self-host/local_deployment>
- **[S29]** Opik tracing concepts:
  <https://www.comet.com/docs/opik/tracing/concepts>
- **[S30]** Opik OpenTelemetry ingestion:
  <https://www.comet.com/docs/opik/tracing/opentelemetry/overview>
- **[S31]** Opik Claude Code integration:
  <https://www.comet.com/docs/opik/integrations/claude-code>
- **[L1]** Local adapter contract:
  `project-tools/trae-agent-flow-adapter/README.md`
- **[L2]** Local compatibility verification:
  `project-records/agent-observability/verification.md`
