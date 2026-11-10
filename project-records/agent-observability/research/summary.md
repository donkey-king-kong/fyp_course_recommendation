# Agent Visualization Research Synthesis

Date: 2026-11-10

## Recommendation

Keep the current cooperative Agent Flow bridge for live TRAE hierarchy and
status. If animated characters are the priority, build a small local frontend
over the same sanitized heartbeat and JSONL files rather than trying to make a
Claude-specific product infer TRAE internals.

Recommended progression:

1. **Now:** Agent Flow plus the existing cooperative JSONL adapter.
2. **Animated view:** loopback Python SSE server, vendored D3 tree/timeline,
   and plain HTML/CSS character animation.
3. **Durable history later:** optional metadata-only OTLP export to OpenLIT.
4. **Alternative integration experiment:** an Office Sim adapter, if its 3D
   office is preferred over a purpose-built interface.

## Ranked Options

| Rank | Option | Best use | TRAE-native status |
|---:|---|---|---|
| 1 | Existing Agent Flow bridge | Live hierarchy, states, timeline | Tested cooperatively in this workspace |
| 2 | Custom local visualizer | Animated characters with our privacy boundary | Feasible from existing JSONL and heartbeats |
| 3 | Office Sim adapter | Existing 3D office and multi-runtime architecture | Adapter not implemented |
| 4 | OpenLIT alongside Agent Flow | Durable local traces, analytics, aggregate DAG | OTLP adapter not implemented |
| 5 | Original Pixel Agents | Polished pixel office for Claude Code | Does not observe TRAE-native agents |

## Verification Report

**Mode:** Search verification against owning primary sources.

| Claim | Status | Finding |
|---|---|---|
| No reviewed tool natively observes TRAE built-in subagents | Qualified | No reviewed source claims this support, but this is not a registry-wide nonexistence proof. |
| Original Pixel Agents is the strongest maintained pixel option | Interpretation | Its Claude-specific subagent UI and current official project are verified; “strongest” is the comparison's judgment. |
| Office Sim has the best adapter boundary for a new runtime | Interpretation | Its documented adapter/event contract and supported runtimes are verified; “best” is an engineering judgment. |
| Agent Flow plus the cooperative bridge is directly tested here | Verified | The local event stream, patched extension, tests, and live visual confirmation provide direct evidence. |
| OpenLIT is the strongest durable complement | Interpretation | OTLP ingestion, coding-agent support, dashboards, and trace-derived DAG are verified; ranking is a judgment. |
| Python SSE plus D3 is the smallest practical custom stack | Interpretation | The required standard-library server, SSE, and tree-layout capabilities are verified; “smallest practical” reflects the compared designs. |
| TRAE hooks do not expose `spawn_agent` or parent-child IDs | Verified | Official TRAE docs list six hook events and their schemas without a delegation lifecycle or parent-child identifiers. |

## Primary Evidence

- [TRAE hooks](https://docs.trae.ai/ide/automate-actions-with-hooks?_lang=en)
- [TRAE hook reference](https://docs.trae.ai/ide/hook-configuration-reference?_lang=en)
- [TRAE subagents](https://docs.trae.ai/ide/subagents?_lang=en)
- [Pixel Agents](https://github.com/pixel-agents-hq/pixel-agents)
- [Office Sim](https://github.com/WahyzMaster/office-sim)
- [Office Sim contract](https://github.com/WahyzMaster/office-sim/blob/master/docs/CONTRACT.md)
- [Agent Flow](https://github.com/patoles/agent-flow)
- [OpenLIT coding-agent observability](https://docs.openlit.io/latest/openlit/coding-agents/overview)
- [OpenLIT agent graph](https://docs.openlit.io/latest/openlit/observability/agents/overview)
- [WHATWG server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [Python `http.server`](https://docs.python.org/3/library/http.server.html)
- [D3 tree layout](https://d3js.org/d3-hierarchy/tree)

## Detailed Reports

- `pixel-tools.md`
- `observability-tools.md`
- `trae-integration.md`
- `custom-visualizer.md`
