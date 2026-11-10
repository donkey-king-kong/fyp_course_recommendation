# Custom Local Agent Visualizer: Stack Research

Date: 2026-11-10
Scope: research only; no implementation or shared-file changes

## Decision

Use a small loopback web application:

- **Transport and file adapter:** Python 3 standard library
  (`http.server.ThreadingHTTPServer`, JSON parsing, polling, and SSE).
- **Visualization:** plain HTML/CSS/JavaScript plus vendored **D3 7.9.2**.
- **Views:** one SVG parent-child tree and one SVG event timeline. Use CSS and
  D3 transitions for state changes.
- **Storage:** none. Replay the existing JSONL and heartbeat files into an
  in-memory reducer on startup.

This is the smallest practical stack that covers all requested behavior with
one runtime process and one browser dependency. D3 directly supplies a tidy
tree layout, data joins, transitions, time scales, axes, and zoom. A native-SVG
implementation would remove the dependency but would require hand-written
layout, keyed joins, interpolation, axes, and navigation. Cytoscape.js is a
good fallback if graph editing or richer graph algorithms become more
important than the timeline. PixiJS should remain an optional second view,
not part of the first release.

## Local Input Contract

The existing adapter writes:

- append-only `runtime/agent-flow-events.jsonl`;
- atomically replaced `runtime/heartbeats/<agent>.json`; and
- `runtime/session.json`.

Events have numeric `time`, string `type`, object `payload`, and usually a
`sessionId`. Heartbeats contain `agent_id`, optional `parent_id`, `task`,
`status`, `activity`, `outputs`, `blocker`, and `updated_at`. Supported states
are `starting`, `working`, `waiting`, `blocked`, `completed`, and `failed`.
The adapter publishes sanitized metadata, not prompts, responses, tool
arguments, file contents, environment variables, credentials, or token
counts. These are local project facts from
[`adapter.py`](../../../project-tools/trae-agent-flow-adapter/adapter.py) and
its [README](../../../project-tools/trae-agent-flow-adapter/README.md).

## Recommended Architecture

```text
agent-flow-events.jsonl ---- append/tail ----+
                                             |
heartbeats/*.json -------- poll snapshots ---+--> Python state reducer
                                             |      |
session.json ------------- reset boundary ---+      +--> GET /api/snapshot
                                                    +--> GET /events (SSE)
                                                    +--> static local assets
                                                               |
                                                        EventSource + D3
                                                               |
                                             tree | status animation | timeline
```

### Gateway

Bind only to `127.0.0.1` (and optionally `::1`) and serve:

- `GET /`: static, vendored UI;
- `GET /api/snapshot`: complete current session for first load/recovery;
- `GET /events`: `text/event-stream` deltas with monotonic `id` values; and
- optionally `GET /health`: input paths, parser state, and last update time,
  without event content.

`ThreadingHTTPServer` is sufficient for a local tool with a static page and a
small number of long-lived SSE clients. Python documents that it handles
requests in threads, while also warning that `http.server` is not recommended
for production. That warning is acceptable only because this service is
loopback-only, reads an allowlisted directory, exposes no mutation endpoint,
and is not a general network server.[S1]

The JSONL tailer should retain a byte offset, buffer an incomplete final line,
and reset on truncation, inode replacement, or session-ID change. Poll
heartbeats by directory scan and modification metadata; atomic replacement
means treating each file as a new snapshot is safer than attempting in-place
tailing. A malformed line or heartbeat should generate a visible diagnostic
without discarding the last valid state.

### State reducer

Maintain normalized maps for sessions, agents, edges, and event rows.

- Create directed `parent -> child` edges from `subagent_dispatch`,
  `agent_spawn.payload.parent`, and heartbeat `parent_id`.
- Treat heartbeat status as the authoritative current state; use JSONL events
  for history and transitions.
- Keep unknown event types in the timeline instead of dropping them.
- Key JSONL deltas by session plus byte offset; key heartbeat deltas by agent
  plus `updated_at`.
- On reconnect, use the SSE `Last-Event-ID` mechanism when retained deltas are
  available; otherwise send a reset instruction and fetch a fresh snapshot.

SSE is a good fit because updates are one-way. The HTML standard defines
`EventSource`, `text/event-stream`, event IDs, reconnection behavior, and
`Last-Event-ID`; WebSockets would add a bidirectional protocol that this
read-only visualizer does not need.[S2]

### Browser views

1. **Agent tree:** use `d3.hierarchy`/`d3.stratify` and `d3.tree` for stable
   parent-child placement. D3's tree layout assigns coordinates to every
   descendant and is specifically intended for node-link trees.[S3]
2. **State animation:** keyed joins retain node identity. Transition fill,
   halo, opacity, and position when a state changes. Use a restrained pulse
   for `working`, a pause glyph for `waiting`, a fixed warning treatment for
   `blocked`/`failed`, and a settled treatment for `completed`. Respect
   `prefers-reduced-motion`.
3. **Timeline:** render one lane per agent and one mark or interval per event.
   `d3.scaleUtc` provides predictable temporal positioning and ticks;
   `d3-axis` renders and updates a time axis; D3 transitions interpolate DOM
   attributes and styles.[S4][S5][S6]
4. **Interaction:** selection, keyboard focus, pan/zoom, state filtering, and
   a details panel containing only already-sanitized metadata.

## Graph Library Comparison

Artifact sizes below were measured from the named projects' published npm
tarballs on 2026-11-10. “Min” is the shipped minified browser file; “gzip” is
that exact file compressed with `gzip -9`. These are reproducible artifact
measurements, not tree-shaken application estimates.

| Option | License | Published browser artifact | Fit | Cost/complexity |
|---|---|---:|---|---|
| **D3 7.9.2** | ISC | 280,622 B min / 92,535 B gzip | Best overall fit. `d3-hierarchy` handles the tree; selections/transitions handle state changes; scales/axes handle the timeline; zoom handles navigation.[S3-S7] | D3 is a visualization toolkit, not a ready-made graph widget, so accessibility, styling, and the reducer remain application code. Modular imports can reduce the shipped application below the full-bundle figure, but no unmeasured estimate is claimed here. |
| **Cytoscape.js 3.34.4** | MIT | 435,649 B / 136,466 B | Strong graph-first alternative: graph model, Canvas renderer, events, animations, styling, built-in layouts, and no external dependencies.[S8] | Faster for rich graph interactions, but a timeline still needs custom SVG/Canvas code. More graph machinery than a small agent tree requires. |
| **Sigma 4.0.5 + Graphology 0.26.0** | MIT | 467,375 B / 117,632 B combined | Best when thousands of graph elements require WebGL. Sigma explicitly targets large graph rendering and requires Graphology.[S9][S10] | Nodes need coordinates or a separate layout step, the data model is a second dependency, and the timeline remains separate. This workload is too small to justify the WebGL pipeline. |
| **Native SVG/DOM** | Web standard | 0 library bytes | Absolute minimum transfer size and fully local. | Not the smallest engineering stack: tree layout, joins, zoom, interpolation, and axes all become maintained project code. |

React Flow and similar node-editor frameworks were not shortlisted: this is
a read-only visualizer, so adopting React plus an editor-oriented component
model would increase runtime and architectural surface without satisfying the
timeline or file transport.

## Animated 2D and Pixel-Scene Options

| Option | License | Published browser artifact | Strength | Why it is not in the minimum stack |
|---|---|---:|---|---|
| **Konva 10.9.1** | MIT | 197,594 B min / 58,821 B gzip | Smallest compared scene library. Canvas scene graph, pointer handling, shapes, and `Konva.Animation` frame updates.[S11][S12] | No graph layout or timeline semantics. Good for an interactive office/map scene, but sprite-sheet behavior would be application code. |
| **PixiJS 8.22.0** | MIT | 840,663 B / 236,766 B | Best optional pixel-art renderer. Its application ticker supplies frame-based updates and lifecycle control; GPU rendering suits many animated sprites.[S13][S14] | Adds a second rendering model and substantial bytes while D3/CSS already covers status animation. Use only if animated agents moving through a scene is a required view. |
| **Phaser 4.2.1** | MIT | 1,375,976 B / 352,441 B | Full 2D game framework with scenes, assets, input, sprite sheets, and an animation manager.[S15][S16] | Most capability is unrelated to observability. It is appropriate for a game-like simulation, not the smallest dashboard. |
| **Native Canvas/CSS sprites** | Web standard | 0 library bytes | Lowest bytes for a fixed, tiny sprite set. | Requires custom scene graph, hit testing, animation lifecycle, and accessibility mirroring. Prefer it only for a deliberately tiny decorative scene. |

If a pixel view is later approved, add **PixiJS as an isolated optional panel**
fed by the same normalized browser store. Do not encode event parsing or agent
state in the scene engine. This keeps the D3 tree and timeline as the
accessible operational views and makes the scene removable.

## Privacy and Locality

- Bind to loopback, reject non-loopback host assumptions, and print the exact
  local URL at startup.
- Allowlist only the adapter runtime directory. Do not accept an arbitrary
  path through a query parameter or request body.
- Vendor JavaScript, CSS, fonts, and any sprite assets. Use no CDN, analytics,
  telemetry, remote images, or external source maps.
- Set a restrictive Content Security Policy such as `default-src 'self'`;
  narrow `connect-src` to the local origin.
- Expose read-only `GET` routes, no upload or command-execution endpoint, and
  no directory listing.
- Preserve the adapter's metadata boundary. The visualizer should not open
  referenced output paths or enrich labels from workspace files.
- Keep state in memory and the existing ignored runtime files. Do not add a
  database, browser persistence, or cloud synchronization by default.
- Surface stale-heartbeat age and parse errors; do not infer activity that was
  not cooperatively published.

Locality is an architectural property here, not a claim that every local
process is trusted. Any process able to read the runtime files can read the
same metadata, and any process able to write them can spoof visualized state.

## Delivery Shape

The proposed implementation would contain:

```text
custom-visualizer/
  server.py             # loopback static/SSE server and file readers
  reducer.py            # validated event -> normalized state
  static/
    index.html
    app.js
    app.css
    vendor/d3.min.js
  tests/
    fixtures/
    test_tail_and_reset.py
    test_reducer.py
    test_privacy_and_binding.py
```

No Node process is required at runtime. A build tool is optional: vendoring
the full D3 artifact is simplest; a pinned build can later bundle only the D3
modules actually imported if reducing browser bytes becomes worthwhile.

## Verification Targets for a Future Implementation

- Replay the existing demonstration: orchestrator plus children, including
  working, waiting, blocked, failed, and completed states.
- Append JSONL in partial writes; rotate/truncate it; atomically replace
  heartbeats; change session ID; reconnect SSE.
- Confirm one edge per parent-child relationship and stable node identity
  across updates.
- Confirm timeline ordering and session-relative time without inventing
  missing transitions.
- Test keyboard navigation and reduced motion.
- Assert loopback binding, no external requests, restrictive response headers,
  allowlisted paths, and absence of mutation routes.
- Re-run the adapter's sensitive-pattern scan against data exposed by both
  snapshot and SSE endpoints.

## Sources

- **S1.** Python Software Foundation,
  [`http.server` documentation](https://docs.python.org/3/library/http.server.html)
  (`ThreadingHTTPServer` and production-security warning).
- **S2.** WHATWG,
  [HTML Living Standard: Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html).
- **S3.** D3,
  [`d3-hierarchy` tree documentation](https://d3js.org/d3-hierarchy/tree).
- **S4.** D3,
  [time-scale documentation](https://d3js.org/d3-scale/time).
- **S5.** D3,
  [axis documentation](https://d3js.org/d3-axis).
- **S6.** D3,
  [transition documentation](https://d3js.org/d3-transition).
- **S7.** D3,
  [official repository and ISC license](https://github.com/d3/d3);
  size input:
  [`d3-7.9.2.tgz`](https://registry.npmjs.org/d3/-/d3-7.9.2.tgz).
- **S8.** Cytoscape Consortium,
  [Cytoscape.js documentation](https://js.cytoscape.org/) and
  [MIT license](https://github.com/cytoscape/cytoscape.js/blob/master/LICENSE);
  size input:
  [`cytoscape-3.34.4.tgz`](https://registry.npmjs.org/cytoscape/-/cytoscape-3.34.4.tgz).
- **S9.** Sigma.js,
  [official documentation](https://www.sigmajs.org/docs/) and
  [browser-bundle documentation](https://www.sigmajs.org/reference/browser-bundle/).
- **S10.** Sigma.js and Graphology published artifacts:
  [`sigma-4.0.5.tgz`](https://registry.npmjs.org/sigma/-/sigma-4.0.5.tgz) and
  [`graphology-0.26.0.tgz`](https://registry.npmjs.org/graphology/-/graphology-0.26.0.tgz);
  [Sigma MIT license](https://github.com/jacomyal/sigma.js/blob/main/LICENSE.txt).
- **S11.** Konva,
  [official overview and license statement](https://konvajs.org/) and
  [MIT license](https://github.com/konvajs/konva/blob/master/LICENSE).
- **S12.** Konva,
  [animation documentation](https://konvajs.org/docs/animations/Create_an_Animation.html);
  size input:
  [`konva-10.9.1.tgz`](https://registry.npmjs.org/konva/-/konva-10.9.1.tgz).
- **S13.** PixiJS,
  [official getting-started guide](https://pixijs.com/8.x/guides/basics/getting-started)
  and
  [ticker documentation](https://pixijs.com/8.x/guides/components/application/ticker-plugin).
- **S14.** PixiJS,
  [MIT license](https://github.com/pixijs/pixijs/blob/dev/LICENSE);
  size input:
  [`pixi.js-8.22.0.tgz`](https://registry.npmjs.org/pixi.js/-/pixi.js-8.22.0.tgz).
- **S15.** Phaser,
  [official framework overview](https://docs.phaser.io/phaser/getting-started/what-is-phaser)
  and [animation documentation](https://docs.phaser.io/phaser/concepts/animations).
- **S16.** Phaser,
  [MIT license](https://github.com/phaserjs/phaser/blob/master/LICENSE.md);
  size input:
  [`phaser-4.2.1.tgz`](https://registry.npmjs.org/phaser/-/phaser-4.2.1.tgz).

All software-license statements above were checked against the projects'
license files or official documentation. Artifact sizes are exact for the
listed versions and files, but they do not predict a future tree-shaken
application bundle.
