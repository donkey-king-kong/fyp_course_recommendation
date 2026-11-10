# Research Paper Insight Planner — Proposed MVP Technical Plan

**Status:** Proposed Shape input; concrete and buildable, but not approved for implementation, launch, provider use, or authority-gated data handling  
**Run:** `research-paper-insight-planner-20261110`  
**Date:** 2026-11-10  
**Source of invariants:** `final-plan.md`; this document proposes mechanisms and does not weaken or replace product decisions D01–D26.

## 1. Scope, Goals, and Non-goals

### Architecture goals

1. Preserve exact paper/version identity and immutable revision lineage from intake through export.
2. Fail closed: unsupported evidence, wrong-version locators, invalid class labels, unsafe fetches, or overspend cannot become a supported export.
3. Make partial discovery and analysis explicit and reproducible rather than silently retrying into a different corpus.
4. Bound exposure to hostile remote content, source rights, source-byte retention, vendors, and tenant data.
5. Produce deterministic, schema-valid Markdown `1.0.0` from durable structured records, not directly from model prose.
6. Meet the proposed MVP operating envelope: default corpus 8, hard corpus 20, ≤30 displayed candidates, US$3 target, US$8 hard cap, p90 10/20-minute latency targets.

### Quality attributes, in priority order

| Attribute | Proposed mechanism | Observable target |
|---|---|---|
| Integrity | Exact-version foreign keys, immutable revisions, deterministic validators, privileged publish gate | Zero integrity blockers in the predeclared audit |
| Security | SSRF-safe resolver, isolated fetch/parser workers, deny-by-default egress, no credentials, content limits | Zero private-network or access-control bypasses |
| Reproducibility | Append-only snapshots, content/locator hashes, versioned schemas, deterministic IDs/export | Unchanged revision replays byte-stably except declared volatile fields |
| Privacy/retention | Separate transient/durable storage classes, TTLs, deletion ledger, raw-content-free telemetry | Source/cache deletion ≤24h; durable expiry ≤30d, pending A1 |
| Cost control | Preflight reservation, per-stage metering, atomic hard-cap ledger | No revision exceeds US$8; default target ≤US$3 |
| Resilience | Idempotent jobs, bounded retries, partial results, child revisions | Provider/parser failure remains explicit and recoverable |
| Operability | Structured state transitions, redacted metrics/traces, kill switches | Diagnose by IDs/states without source text in logs |
| Portability | Provider/parser adapters and Markdown schema | Replace providers and parsers without changing domain contracts |

### Non-goals

No exhaustive search, systematic review, truth ranking, paywall/authentication bypass, autonomous execution, high-stakes advice, broad library/collaboration support, production recommendation engine, or training on retained content. The authorized-PDF path remains disabled until A1 and security gates approve it.

## 2. System Context

**Actors:** one authenticated applied-ML practitioner; canonical scholarly metadata/content providers; model provider(s); product operators/auditors; privacy/legal and product/finance authorities.

**System boundary:** a multi-tenant web/API service accepts a topic or scholarly URL, creates an immutable revision, discovers or resolves candidates, waits for exact-version corpus confirmation, retrieves lawful content, extracts version-bound evidence, generates typed claims, validates them deterministically, and exports Markdown.

**Trust boundaries:** public ingress; control plane; isolated untrusted-content processing. Remote paper bytes and extracted text are untrusted data, never instructions. Providers do not call internal control-plane APIs.

**Assumed MVP load for sizing, not approval:** low hundreds of concurrent runs, bursty worker demand, 20-paper maximum, one region, no cross-region active/active. Stateless control services may scale horizontally; state transitions serialize per revision.

## 3. Proposed Component Boundaries

| Component | Responsibilities | Must not do |
|---|---|---|
| Web/API ingress | Authentication, tenant context, request schema, topic/URL intake, confirmation, status, export download | Fetch arbitrary URLs, synthesize claims, mutate a sealed revision |
| Safe resolver/fetch broker | Normalize URL, enforce scheme/host/IP/redirect/content policy, issue scoped fetch grants | Accept credentials, follow unrestricted redirects, expose cloud metadata/private networks |
| Run orchestrator | Revision state machine, DAG scheduling, idempotency keys, retries, cancellation, budget reservation/metering, partial state | Interpret paper content or bypass validation |
| Discovery/identity adapters | Provider queries, raw/normalized result snapshots, conservative DOI/repository identity grouping | Treat general web results as canonical identity; auto-merge fuzzy matches |
| Isolated retrieval/parser workers | Use fetch grants, scan/decompress with limits, parse PDF/HTML/metadata, emit normalized document and locators | Reach control-plane databases directly; retain bytes beyond TTL |
| Evidence/claim pipeline | Build evidence candidates, generate class-labelled claims/issues/advice drafts, bind exact evidence IDs | Publish Markdown or mark unsupported material as supported |
| Privileged validation/publish gate | Deterministic identity, locator, quote, entailment, class, citation, advice, schema, budget and deletion-policy checks; atomic publish | Repair claims silently, call models, accept mutable input |
| Storage/export services | Append-only domain store, object classes, outbox/audit ledger, deterministic Markdown rendering and download | Store source bytes in durable records or log raw content |

The architecture diagram groups these capabilities into eight visual components; implementation may split services only after interfaces and ownership remain stable.

## 4. End-to-end Sequences

### 4.1 Topic sequence

1. `POST /v1/runs` records verbatim topic and options under `RUN-* / REV-1`; request validation is synchronous.
2. Orchestrator reserves a discovery budget and enqueues provider query jobs. Each adapter records submitted query, expansion, filters, limit, ranking mode, timestamp and provider result/error snapshot.
3. Identity service normalizes exact DOI/repository relations, proposes visible fuzzy groups only, de-duplicates, merges rank transparently, truncates to 30, and proposes 8 selections.
4. API returns candidate snapshot and partial-provider warnings. The revision remains `awaiting_confirmation`.
5. User confirms 1–20 exact versions with inclusion/exclusion reasons. Confirmation seals the corpus snapshot and timestamp. Any later membership/version edit forks a child revision.
6. Orchestrator reserves remaining budget and fans out retrieval/parser jobs for confirmed versions. Access state is recorded per version.
7. Evidence extraction emits exact-version evidence records; generation emits typed draft blocks. Unsupported/failed papers remain explicit.
8. Privileged gate validates every publishable block and renders a candidate export. It atomically stores validation result, audit event, output hash and Markdown or returns blocked/partial status.

### 4.2 Paper-URL sequence

1. `POST /v1/runs` records the verbatim URL/DOI-like input; syntax checks run synchronously.
2. Safe resolver performs DNS/IP checks for every hop, bounded redirects, TLS/content-type/size policy and canonical-provider resolution. Unsafe, credential-bearing, ambiguous or unsupported input returns a typed error before parsing.
3. Identity adapters present canonical paper/version, publication/access/correction state and unresolved ambiguities.
4. User confirms the exact record/version. No analysis starts before this event.
5. Open lawful content is fetched in isolation; inaccessible content is restricted to permitted abstract/metadata. User-supplied PDFs remain feature-flagged off pending A1/security approval.
6. Parsing, evidence, generation and privileged validation follow the same contracts as topic runs. With one paper, cross-paper sections render `not_applicable: one confirmed paper`.

### 4.3 Revision creation rules

Retry that can change provider results, provider recovery, corpus/version edits, regeneration, schema change, or model/prompt change creates a child revision. A transport retry of the same immutable job input remains within a revision. Prior snapshots and output bytes are never updated.

## 5. Synchronous and Asynchronous Contracts

### Synchronous

- Create run/revision, resolve request syntax, read status/candidates/output, confirm corpus, request deletion.
- Return within normal HTTP timeouts; expensive work returns `202 Accepted` plus revision and operation IDs.
- Confirmation uses optimistic concurrency with `expected_revision_etag`; stale writes return `409 REVISION_STALE`.
- Validation/export lookup never fabricates a pending result; it returns explicit state.

### Asynchronous

- Discovery, canonical resolution requiring providers, retrieval, parsing, extraction, generation, validation, export and deletion execute as durable jobs.
- Queue payloads contain IDs, schema versions, object references, hashes and scoped fetch grants—not raw paper text.
- Every event is at-least-once; consumers are idempotent. Domain commits and event publication use a transactional outbox.
- Ordering is guaranteed only per `revision_id`; workers reject events whose expected state/hash does not match.

## 6. Representative Interfaces

### 6.1 HTTP API

```json
POST /v1/runs
{
  "input": {"type": "topic", "value": "parameter-efficient adaptation"},
  "intent": "choose one non-safety-critical experiment",
  "filters": {"from_year": 2022, "domains": ["machine_learning"]},
  "request_id": "01J..."
}
```

```json
202 Accepted
{
  "run_id": "RUN-7K4...",
  "revision_id": "REV-1",
  "state": "discovering",
  "operation_id": "OP-...",
  "coverage_notice": "Bounded candidate set—not exhaustive coverage."
}
```

```json
POST /v1/runs/RUN-7K4/revisions/REV-1/confirm
{
  "paper_versions": ["V-ARXIV-2401.01234v2"],
  "exclusions": [{"paper_id": "P-...", "reason": "out_of_scope"}],
  "expected_revision_etag": "sha256:..."
}
```

```json
201 Created
{
  "confirmed_revision_id": "REV-1",
  "corpus_status": "user_confirmed",
  "confirmed_at": "2026-11-10T14:00:00Z",
  "analysis_operation_id": "OP-..."
}
```

```json
{
  "error": {
    "code": "URL_PRIVATE_DESTINATION",
    "message": "The URL resolves to a prohibited network destination.",
    "retryable": false,
    "details": {"redirect_hop": 1},
    "correlation_id": "CORR-..."
  }
}
```

Canonical HTTP errors include `INVALID_INPUT` (400), `UNAUTHENTICATED` (401), `TENANT_FORBIDDEN` (403), `URL_UNSAFE`/`URL_PRIVATE_DESTINATION`/`ACCESS_BYPASS_PROHIBITED` (422), `IDENTITY_AMBIGUOUS` (409), `REVISION_STALE` (409), `CORPUS_LIMIT_EXCEEDED` (422), `BUDGET_STOP` (409), `EXPORT_BLOCKED` (409), `NOT_FOUND` (404), `RATE_LIMITED` (429), and `DEPENDENCY_UNAVAILABLE` (503).

### 6.2 Internal adapter contracts

```text
DiscoveryProvider.search(query_revision, cursor?, limit, deadline) ->
  ProviderPage{provider, submitted_query, returned_order[], next_cursor?,
               raw_count?, truncation, request_time, error?}

IdentityProvider.resolve(identifier_or_url, fetch_grant?) ->
  Resolution{paper_record, candidate_versions[], relationships[], ambiguities[]}

ContentProvider.plan(version, access_policy) ->
  RetrievalPlan{canonical_url, expected_media_types[], max_bytes,
                lawful_access_basis, fetch_grant_request}

Parser.parse(source_ref, paper_version_id, limits) ->
  ParsedDocument{document_hash, blocks[], locator_map[], warnings[], parser_version}
```

Adapters return typed errors (`unsupported`, `denied`, `rate_limited`, `timeout`, `invalid_response`, `terms_blocked`) and never coerce them to empty success.

### 6.3 Domain events

```json
{
  "event_id": "EVT-...",
  "type": "paper.parse.completed.v1",
  "occurred_at": "2026-11-10T14:02:00Z",
  "tenant_id": "TEN-...",
  "run_id": "RUN-...",
  "revision_id": "REV-1",
  "job_id": "JOB-...",
  "idempotency_key": "sha256:revision+version+parser+input_hash",
  "payload": {
    "paper_version_id": "V-...",
    "parsed_document_ref": "transient://...",
    "document_hash": "sha256:...",
    "warnings": ["page_text_order_degraded"]
  }
}
```

Event evolution is additive within a major version; incompatible payload changes use a new event suffix. Consumers ignore unknown additive fields but reject unknown major versions.

### 6.4 Publish-gate result

```json
{
  "revision_id": "REV-1",
  "decision": "blocked",
  "validation_version": "1.0.0",
  "violations": [
    {"code": "EVIDENCE_WRONG_VERSION", "claim_id": "C-...", "evidence_id": "E-P-..."},
    {"code": "PRIMARY_CLASS_CARDINALITY", "claim_id": "C-...", "actual": 2}
  ],
  "partial_sections": ["paper_register"],
  "advice": {"status": "insufficient_evidence_for_advice", "gaps": ["weak applicability"]}
}
```

## 7. Canonical Domain and Immutable Data Model

### Core entities

| Entity | Key fields and invariants |
|---|---|
| Tenant | `tenant_id`; all owned rows and object keys include tenant scope |
| Run | `run_id`, tenant, input type/value, created time; stable lineage root |
| RunRevision | `(run_id, revision_no)`, parent, immutable state snapshot hash, schema/generator/model/prompt versions, cost totals |
| QueryRevision | provider-specific submitted query, expansions, filters, ranking, limits, timestamps |
| ProviderSnapshot | returned IDs/order, pagination/truncation, raw/de-duped counts, typed failure, completeness warning |
| PaperRecord | stable product ID, identifiers, bibliographic fingerprint, publication state; no fuzzy auto-merge |
| PaperVersion | version ID/date/source/access state/retrieval time/content hash/correction relationship |
| CorpusSnapshot | candidate list, selected/excluded versions/reasons, confirmation actor/time; sealed before analysis |
| SourceObject | transient object reference, media type, hash, size, access basis, `delete_after` |
| ParsedDocument | parser/version/hash, block map, warnings, transient reference |
| EvidenceItem | exact `paper_version_id`, locator, minimal quote or withheld reason, anchor/hash, access scope, resolution state |
| Claim | exactly one class, statement, support status, evidence references, validation state |
| Issue | proposition, support, contradiction, comparability limits, explanations, alternatives, unresolved status |
| Advice | one bounded experiment or suppression; separate evidence dimensions and reasons |
| ValidationResult | validator version, deterministic violations, input aggregate hash, decision |
| Export | schema version, immutable Markdown object/hash, created time, partial flag |
| CostLedgerEntry | reservation/actual/refund, stage/provider/model, amount, idempotency key |
| DeletionLedgerEntry | object class/reference, deadline, attempt/result/evidence; no raw content |
| AuditEvent | actor/service, action, target IDs/hashes, outcome, correlation ID; append-only |

### Immutable revision design

- Postgres tables for revision-owned entities use immutable primary keys and deny `UPDATE`/`DELETE` to the application role; lifecycle uses status/event rows and expiry tombstones.
- A revision has `draft` orchestration state until its snapshot inputs are sealed, but each emitted snapshot row is append-only. Sealing computes an aggregate hash over ordered canonical JSON.
- Child revisions reference the parent and copy identifiers by reference; changed snapshots receive new IDs. Removed paper versions cannot be referenced by child claims.
- Event/outbox rows commit in the same transaction as state transitions. Duplicate transitions compare idempotency key plus input hash; a mismatched replay fails.
- Durable Markdown is content-addressed and bound to one `validation_result_id`; export cannot point to an unapproved gate result.

## 8. Retrieval and Provider Adapter Boundary

A provider adapter owns provider syntax, pagination, rate limits and response normalization. It does not own identity policy, ranking policy, storage, retries or claim generation. The core supplies deadlines, maximum result counts and a budget token. Adapters disclose every query and failure.

Proposed initial feasibility spike: one canonical metadata provider plus arXiv and PubMed/PMC-style repositories; actual providers and terms remain undecided and authority-dependent. General web search, if retained, can propose candidates only and cannot establish canonical identity.

All content retrieval goes through the fetch broker. Workers receive short-lived, single-destination grants bound to resolved public IPs, scheme, port, redirect limit, byte limit, media types and expiry. Provider SDKs cannot open arbitrary sockets.

## 9. Safe URL Fetch and SSRF Controls

1. Accept only `https` (and normalized DOI-like identifiers); reject user info, fragments for identity, nonstandard ports unless allowlisted, local files and unsupported schemes.
2. Parse with one standards-compliant library; normalize IDNs and reject ambiguous host encodings, numeric/obfuscated IP literals and malformed authorities.
3. Resolve DNS through a controlled resolver. Deny loopback, private, link-local, multicast, reserved, carrier-grade NAT, metadata endpoints and organization internal ranges for IPv4/IPv6.
4. Pin the approved public address set for the connection; re-resolve and re-check every redirect. Deny public-to-private rebinding and mixed-answer sets under the conservative policy.
5. Apply an allowlist for canonical providers/repositories in MVP; generic publisher URLs may resolve metadata but do not authorize restricted content.
6. Disable ambient proxies, cookies, client certificates, credential forwarding and browser automation. Never submit login, CAPTCHA or paywall forms.
7. Enforce TLS verification, connect/read/total deadlines, ≤5 redirects, compressed and decompressed byte ceilings, archive nesting/ratio limits and expected media types.
8. Stream to isolated scanning storage; sniff actual type, scan for malware/active content, strip executable features for parsing, and reject polyglots/unexpected types.
9. Treat robots/provider terms as policy inputs. A denied route produces `denied`/`metadata_only`; no fallback mirror or bypass is attempted.
10. Log only normalized host category, policy rule, byte count and IDs—not full query URLs where they may contain sensitive values.

Blocked private-network and paywall routes terminate at this boundary and are shown in `architecture.html`.

## 10. Parsing and Exact-version Evidence

### Parsing

- Run parsers in ephemeral containers/microVMs with no inbound access, read-only base image, non-root UID, CPU/memory/time/process limits, no control-plane credentials and broker-only egress.
- Store original bytes and full parsed text only in the transient class. Emit a normalized block graph keyed by document hash and parser version.
- PDF blocks carry physical page index, printed label when recoverable, bounding box, reading-order index and normalized text anchor. HTML blocks carry canonical URL, heading path, DOM/paragraph index and text anchor. Metadata/abstract carries provider field and record version.
- Figures/tables/equations use typed locators plus caption/region anchors. Parser warnings propagate to evidence and claim support status.

### Exact-version locator strategy

`EvidenceLocator` is a tagged union:

```json
{
  "type": "pdf_span",
  "paper_version_id": "V-...",
  "document_hash": "sha256:...",
  "page_index": 7,
  "page_label": "6",
  "bbox": [72.0, 144.0, 510.0, 228.0],
  "block_index": 18,
  "text_anchor": {"prefix_hash": "...", "quote_hash": "...", "suffix_hash": "..."}
}
```

- Resolve locators only against the same `paper_version_id`, document hash and parser version used for extraction.
- Store the minimum lawful quotation (default ≤2 sentences or 50 words) or a withheld reason; hash/locator survives when quotation retention is prohibited.
- On replay, re-resolve anchor and compare normalized quotation hash. Ambiguous, absent, changed or wrong-version anchors become `evidence_unavailable`/`parser_degraded`, never support.
- Corrections/retractions create linked version records; locators never migrate automatically.

## 11. Claim Generation and Deterministic Gates

Generation consumes only confirmed-version evidence records and structured paper metadata. It returns JSON conforming to a strict schema; paper text is delimited and tagged as untrusted. The model cannot call tools, fetch URLs, choose corpus membership, write stores or publish.

Every analytical block has exactly one primary class: `PAPER-SPECIFIC`, `CROSS-PAPER SYNTHESIS`, or `GENERATED ADVICE`. Generated prose must reference evidence IDs rather than free-form citations.

The privileged gate executes in this order:

1. Revision/corpus seal and tenant ownership.
2. Paper/version identity, access and publication-state rules.
3. Evidence-key uniqueness and exact-version locator resolution.
4. Quotation hash/length/withholding rules and attribution.
5. Claim schema, exactly-one-class cardinality and support-state consistency.
6. Deterministic lexical/structural checks plus a separately versioned entailment evaluator; evaluator uncertainty blocks `supported` status.
7. Cross-paper source completeness and structured contradiction/incomparability fields.
8. Advice suppression triggers, one-experiment cardinality, applicability and stop/failure criteria.
9. Citation closure: every `[@E-*]` resolves once; removed versions are unreachable.
10. Markdown schema/order/enums/ID grammar/deterministic rendering.
11. Spend ≤US$8 and lifecycle metadata present.

The gate may downgrade a draft to explicit unsupported status only by creating a new generated candidate and validation result; it never mutates the submitted claim. Integrity violations block export. Partial export is permitted only when omissions are prominent and every remaining supported claim passes.

## 12. Markdown Schema and Export Path

- Canonical structured records are the source of truth. A pure renderer maps one validated revision to Markdown `1.0.0` in the exact heading order from `final-plan.md`.
- Front matter and sections are rendered from ordered fields; maps are key-sorted; IDs are stable; timestamps are UTC RFC 3339; money uses fixed decimal strings.
- Required empty sections render controlled `not_applicable` or `unavailable` objects with reasons.
- Pipeline: validated aggregate hash → Markdown render → schema/semantic validator → citation-closure check → byte/hash stability check → immutable output object → `export.published.v1` audit event.
- `schema_version` is pinned per revision. Patch clarifies; minor adds optional fields; major requires an explicit migration/export version and consumer compatibility suite.
- Export download uses a short-lived signed URL or authenticated streaming endpoint and records no raw output body in access logs.

## 13. Storage Classes and Deletion Lifecycle

| Class | Contents | Proposed store | Lifecycle |
|---|---|---|---|
| Transient source | Remote/uploaded bytes, full parsed text, parser scratch, scan quarantine | Encrypted object storage with per-tenant prefix and lifecycle tag | Delete by `run_completed_at + 24h` or earlier; failed/cancelled jobs included |
| Durable minimal metadata | IDs, hashes, access/publication states, locators, withheld/minimal quotes, provenance, cost, validation, audit | Postgres + encrypted object metadata | Expire at 30d unless legal authority approves another rule |
| Durable output | Requested Markdown and validation manifest | Encrypted immutable object storage | Expire at 30d; no source bytes embedded beyond approved minimal quote |
| Queue/cache | ID-only messages; bounded normalization cache | Managed queue/Redis with encryption | Visibility/retry TTL <24h; no raw text |
| Logs/telemetry | IDs, states, counts, durations, rule/error codes | Observability backend | No raw content; retention proposed ≤30d |
| Backups | Encrypted durable records only; transient bucket excluded | Provider backup facility | Logical expiry/tombstone plus bounded backup purge pending A1 |

Deletion flow: expiry scanner emits deletion commands → object/store adapters delete by exact key → verification HEAD/query confirms absence → deletion ledger records hashed key, deadline, attempts and result → daily SLO alert on overdue items. Vendor deletion/no-training evidence is a launch dependency. Legal hold is not proposed for MVP; adding one requires A1 and visible product behavior.

## 14. Job Orchestration, Idempotency, Retries, Partial Results, and Budget

### State machine

`created → discovering/resolving → candidates_available/awaiting_confirmation → ingesting → generating → validating → export_ready`, with explicit `partial`, `blocked`, `failed`, `cost_stop`, `deletion_pending`, `deleted`, `superseded` substates. State transitions are compare-and-set against revision state/version.

### Idempotency and retries

- API idempotency: tenant + endpoint + client request ID, with canonical request hash.
- Job idempotency: revision + stage + paper version + adapter/parser/model version + immutable input hash.
- Retry only typed transient failures: timeout, 429, 5xx, worker loss. Use capped exponential backoff with jitter and provider `Retry-After`; proposed maximum 3 attempts per immutable job.
- Unsafe/denied/ambiguous/schema/integrity/budget errors are not retried.
- Dead-letter entries contain IDs/error codes only. Operator replay forks a child revision if external results could change.

### Partial results

- Provider/page failures produce immutable partial snapshots and completeness warnings.
- Paper failures mark per-paper access/support state. Independent successful papers continue.
- A section may be omitted or `unavailable`; no placeholder becomes support.
- Export is allowed only after the gate proves all included supported claims valid and omissions prominent. Advice suppression is a valid result, not a failure.

### Budget enforcement

1. Estimate discovery, retrieval, parsing, model and storage variable cost before confirmation; expose estimate.
2. On confirmation, atomically reserve stage envelopes from an US$8 revision cap. Default plan targets ≤US$3 and may reduce optional breadth before work starts.
3. Every billable request requires a signed budget token with remaining authorized amount. The ledger writes reservation before dispatch and actual/refund after completion using idempotency keys.
4. Retries consume the same revision cap; they do not reset reservations. The orchestrator checks remaining budget before every page/model batch.
5. At predicted or actual cap, stop undispatched work, cancel cooperative jobs, persist metered actuals, label omissions and attempt a valid partial export. Never weaken evidence/validation gates to save cost.
6. A final database constraint rejects ledger totals above US$8 except a zero-cost correcting entry; provider-side maximum-token/request limits reduce overshoot exposure.

Open issue: currency conversion, taxes and delayed provider billing require Finance policy; MVP should reserve a conservative safety margin within US$8.

## 15. Authentication and Tenant Isolation Assumptions

- Proposed MVP uses OIDC Authorization Code + PKCE and server-side sessions; API service validates issuer, audience, nonce and expiry.
- Every request resolves one `tenant_id` and `user_id`; authorization is resource ownership plus role (`user`, `operator`, `auditor`).
- Postgres row-level security and mandatory tenant predicates protect durable rows. Object keys and queue topics are tenant-prefixed; signed URLs bind tenant/object/expiry.
- Service identities use short-lived workload credentials and least privilege. Parser workers receive only one scoped source object/fetch grant and output destination.
- Cross-tenant deduplication by raw content is prohibited in MVP; hashes may match but references and keys remain tenant-local.
- Operators cannot read source/output by default. Break-glass access, if later allowed, requires named authority, reason, expiry and audit.
- Organization SSO, SCIM, public sharing and anonymous runs are deferred.

## 16. Observability Without Raw Content

Emit structured metrics/traces/logs containing correlation, tenant surrogate, run/revision/job/provider/parser/model versions, state transition, counts, byte sizes, durations, budget amounts, access/support state, validation/error codes and deletion deadlines/results. Never emit query text, titles, authors, URLs with query strings, paper text, quotations, prompts, model completions, Markdown, credentials or signed URLs.

Use allowlisted logging schemas, serializer redaction, payload-size guards and tests with canary secrets/source phrases. Trace baggage carries opaque IDs only. Dashboards cover queue age, stage latency, provider errors, parser warnings, validation blockers, advice suppression, cost, export status and deletion SLO. Audit events are append-only durable records separate from operational logs.

## 17. Proposed Deployment Topology

- One cloud region and environment-separated accounts/projects.
- Public CDN/WAF/load balancer fronts stateless web/API services in a private application network.
- Private control-plane services: orchestrator, identity/discovery, evidence/generation coordinator, validation/export, Postgres, queue and cache.
- Isolated worker pool in a dedicated network/account: retrieval/parser containers or microVMs, no inbound route, broker-only egress, no database credentials, ephemeral disks.
- Fetch broker/proxy is the only internet egress for paper content and applies DNS/IP/redirect/content policy.
- Managed encrypted object storage uses separate transient and durable buckets, independent IAM and lifecycle rules.
- Model/provider egress uses explicit gateways and eligible no-training contracts; raw-content scope is minimized.
- Kill switches disable a provider, remote fetch, generation, export or all new jobs without deleting audit state.

## 18. Scaling and Failure Modes

| Failure/pressure | Proposed behavior |
|---|---|
| Provider rate limit/outage | Adapter circuit breaker, bounded retry, immutable partial snapshot, visible warning |
| Queue backlog | Per-tenant fair scheduling, concurrency caps, admission control, age alerts; no silent deadline extension |
| Parser bomb/crash | Isolation limits, quarantine/delete, typed parser failure; other papers continue |
| Model timeout/malformed JSON | Bounded retry under same budget; schema failure blocks affected output |
| Database contention | Serialize transitions per revision; partition/event tables later; read replicas for status only |
| Object-store failure | Do not mark stage complete until hash/object commit verifies; retry idempotently |
| Validator unavailable | Export remains blocked; never bypass privileged gate |
| Cost ledger unavailable | Stop new billable work fail-closed |
| Deletion worker failure | Retry until deadline, page before breach, retain evidence; prevent new launch if SLO cannot be proven |
| Worker compromise | One-job credentials, network isolation, rapid revocation, image pinning, audit; assume remote content hostile |
| Hot tenant | Tenant quotas and weighted fair queues protect others |
| Schema/model rollout | Pin versions per revision; canary new versions on locked benchmark; rollback without rewriting revisions |
| Region outage | MVP restores from encrypted durable backup to same region target; stated RTO/RPO remain an operations decision |

Horizontal scaling units are API replicas and queue consumers. Scale retrieval/parser separately from generation. Partition by tenant/revision only when measured load requires it; preserve per-revision ordering and budget serialization.

## 19. Recommended Stack and Tradeoffs

| Area | Recommendation | Alternatives and tradeoffs |
|---|---|---|
| API/domain | Python 3.13 + FastAPI + Pydantic | TypeScript/NestJS improves full-stack type sharing; Python better aligns with scholarly parsing/ML libraries |
| Durable DB | PostgreSQL 17, JSONB only for versioned payload edges | DynamoDB scales easily but complicates relational integrity, RLS and audit queries |
| Orchestration | Temporal Cloud/self-hosted Temporal | Celery is simpler but weaker for long-lived durable workflows/idempotent history; cloud queues + state machine increase custom code |
| Queue/outbox | Temporal task queues plus Postgres outbox for domain events | Kafka is unnecessary for MVP volume and raises deletion/operations burden |
| Object storage | S3-compatible separate transient/durable buckets with object lock only for short audit manifests | Database blobs simplify transactions but worsen size, lifecycle and parser isolation |
| Cache/rate limits | Redis-compatible managed cache, ID-only | Postgres advisory locks reduce components but are weaker for distributed quotas |
| Parsing | GROBID for scholarly structure plus PyMuPDF fallback, both pinned and isolated | Unstructured/Tika broaden formats but add variability; managed parsers add vendor/privacy dependencies |
| Validation | JSON Schema/Pydantic + custom pure validators; optional independently versioned entailment model | LLM-only review is nondeterministic and cannot be the privileged gate |
| Identity | DOI/Crossref-style metadata plus repository-native version IDs | Fuzzy bibliographic matching remains suggestion-only |
| Frontend | TypeScript + React/Next.js, server API boundary | Static SPA is simpler but authentication/status streaming is less cohesive |
| Infra | Terraform, OCI images, Kubernetes only if existing platform support exists; otherwise managed container jobs/services | Kubernetes offers isolation/scaling but is operationally costly for an MVP |
| Observability | OpenTelemetry + metrics/log backend with allowlisted attributes | Vendor agents must be configured to avoid body capture |
| Secrets | Cloud KMS/secrets manager + workload identity | Static environment secrets increase rotation and worker exposure risk |

Recommendation is conditional on concierge success and platform availability; no stack is approved by this plan.

## 20. Future Work Packages and File Ownership

The repository has no product implementation tree yet. The following proposed layout freezes ownership before parallel implementation. Shared schema changes route through the integration owner; parallel owners do not edit the same files.

| Package / owner | Proposed files | Contract | Dependencies | Verification | Handoff target |
|---|---|---|---|---|---|
| Domain/contracts — Tech Lead integration owner | `app/domain/**`, `schemas/http/**`, `schemas/events/**`, `schemas/markdown/1.0.0/**` | IDs, enums, immutable aggregates, API/events/schema compatibility | Product invariants; A1 fields | Unit/property/schema compatibility tests | All owners |
| API/auth — Backend engineer | `app/api/**`, `app/auth/**` | Tenant-scoped synchronous contracts; no direct fetch/model calls | Domain contracts, identity provider choice | API contract, authz and tenant-isolation tests | Orchestration owner |
| Orchestration/budget — Platform backend engineer | `app/workflows/**`, `app/budget/**`, `app/outbox/**` | Revision state machine, idempotency, retries, US$8 cap | Domain/events, provider stage estimates | Workflow replay, retry, concurrency and budget tests | Integration owner |
| Retrieval/security — Security engineer | `app/fetch/**`, `deploy/egress/**`, `tests/security/fetch/**` | Grant-only egress and SSRF/content controls | Provider allowlist; A1 terms | DNS rebinding, redirects, IPv4/6, content-bomb suites | Parser owner, DevOps |
| Providers/identity — Retrieval engineer | `app/providers/**`, `app/identity/**` | Adapter protocol, transparent snapshots, conservative merge | Provider choices/terms | Recorded-fixture contract and ambiguity tests | Orchestration owner |
| Parsing/evidence — Document engineer | `workers/parser/**`, `app/evidence/**` | Normalized blocks, typed locators, exact-version anchors | Fetch grants, parser selection | Golden PDF/HTML locator and degraded-parser tests | Generation owner |
| Generation/validation/export — ML/backend engineer | `app/generation/**`, `app/validation/**`, `app/export/**` | Typed drafts; deterministic privileged gate; Markdown renderer | Evidence and schemas; model policy | Locked claim audit, suppression, deterministic export tests | Integration owner, QA |
| Storage/lifecycle — Data engineer | `app/storage/**`, `app/deletion/**`, `migrations/**` | Append-only durable rows, storage classes, TTL/deletion ledger | A1 deletion semantics | Migration, immutability, TTL, backup/deletion tests | DevOps/Security |
| Deployment/observability — DevOps/Security | `deploy/**`, `observability/**` | Isolated topology, workload identity, raw-content-free telemetry, kill switches | Cloud/platform and vendor decisions | IaC policy, egress, secret, log-redaction, restore tests | Integration owner |
| QA/release — QA owner | `tests/acceptance/**`, `tests/fixtures/**`, `benchmarks/locked/**` | 20 tasks, ≥100 claims, independent review evidence, zero-tolerance gates | Locked concierge/audit artifacts | Full release command and signed report | Product owner/orchestrator |

### Engineering handoff requirements

Each owner must report scope/files, contracts preserved/changed, assumptions, exact commands/results, risks/gaps, and next owner/action. The integration owner rejects handoffs without fixture evidence or compatibility impact. Named people and repository path approval remain A3 dependencies.

## 21. Integration Order

1. Freeze domain IDs/enums, API errors, event envelopes, Markdown schema and immutability rules.
2. Build storage/migrations and append-only/outbox primitives against contract tests.
3. Integrate API/auth and revision state machine with stub adapters; prove no analysis before confirmation.
4. Integrate budget ledger and fail-closed billable-work tokens.
5. Integrate safe fetch broker and provider/identity adapters with hostile fixtures.
6. Integrate isolated parser and exact-version locator goldens.
7. Integrate generation as typed drafts, then deterministic validation and advice suppression.
8. Integrate Markdown renderer/export only behind privileged gate.
9. Integrate lifecycle deletion, observability and kill switches across all components.
10. Run locked end-to-end topic/URL, edge-case, cost, deletion and independent claim-audit suites before any pilot.

No provider broadening, upload enablement or scale topology precedes passing the relevant gate.

## 22. Migrations and Compatibility

- Use expand/migrate/contract database changes. Old workers/readers remain compatible during rollout; contract removal waits until queues drain and all active revisions pin a compatible version.
- Every revision records domain schema, event, parser, model/prompt, validator, generator and Markdown versions.
- Existing immutable revisions are never backfilled in place. Reprocessing creates a child revision with explicit reason.
- Event consumers support current and previous major during rolling deploy or deployment is coordinated to avoid mixed majors.
- Markdown `1.x` readers must tolerate optional minor fields; major changes require a separate renderer and golden compatibility suite.
- Deterministic ID algorithm changes require a major domain contract and cannot rewrite old IDs.
- Provider/adapter changes create new query revisions and child run revisions when outputs can differ.

## 23. Verification Strategy and Proposed Commands

Commands are proposed for the future implementation; they are not claimed as present or passing now.

```bash
uv run ruff check app workers tests
uv run mypy app workers
uv run pytest tests/unit tests/contracts -q
uv run pytest tests/integration -q
uv run pytest tests/security/fetch -q
uv run pytest tests/acceptance/identity tests/acceptance/evidence -q
uv run pytest tests/acceptance/advice tests/acceptance/markdown -q
uv run pytest tests/acceptance/budget tests/acceptance/deletion -q
uv run pytest benchmarks/locked --audit-manifest benchmarks/locked/claims.json
terraform fmt -check -recursive deploy
tflint --recursive deploy
checkov -d deploy
```

Verification layers:

- Property tests for ID grammar, one-class cardinality, revision immutability, deterministic serialization and citation closure.
- Adapter contract tests from recorded lawful fixtures, with provider failures/truncation/ranking disclosures.
- Golden PDF/HTML tests for physical pages, sections, figures/tables/equations, parser degradation and wrong-version traps.
- Security suite for URL parsing, DNS rebinding, redirects, private IPv4/IPv6, metadata endpoints, content types, decompression bombs, malware and paywall denial.
- Workflow fault injection for duplicate events, crashes after side effects, queue delay, retries, cancellation, child revisions and partial exports.
- Budget concurrency tests proving reservations/actuals cannot cross US$8.
- Time-controlled lifecycle tests proving transient ≤24h and durable ≤30d deletion, including failed jobs, queues and backup policy evidence.
- Telemetry canary tests proving source phrases/secrets never enter logs/traces.
- Predeclared 20-task/100-claim audit with two independent reviewers and adjudication; report each integrity blocker separately.

## 24. Proposed ADRs

1. **ADR-001:** Append-only run revisions and child-revision triggers.
2. **ADR-002:** Canonical paper/version identity and conservative merge policy.
3. **ADR-003:** Provider adapter protocol and initial provider set.
4. **ADR-004:** Fetch broker, DNS/IP pinning and isolated parser boundary.
5. **ADR-005:** Portable locator union and exact-version resolution semantics.
6. **ADR-006:** Structured generation and privileged deterministic publish gate.
7. **ADR-007:** Per-revision budget reservation/metering and hard-cap behavior.
8. **ADR-008:** Transient/durable storage classes, deletion evidence and backups.
9. **ADR-009:** Markdown `1.0.0` canonical rendering and compatibility policy.
10. **ADR-010:** Tenant/auth model and operator access.
11. **ADR-011:** Temporal versus queue/state-machine orchestration.
12. **ADR-012:** Raw-content-free observability and audit separation.
13. **ADR-013:** Parser stack and degradation policy.
14. **ADR-014:** Model/vendor eligibility, no-training guarantees and prompt-injection boundary.

These ADRs are proposed records for Shape; none is approved here.

## 25. Risks, Unresolved Decisions, and Authority Dependencies

| Decision/risk | Likelihood / impact | Proposed owner | Options and recommendation | Authority / trigger |
|---|---|---|---|---|
| Concierge may fail before build | Medium / Critical | Product owner | Do not commit production architecture; use this as conditional build model | Orchestrator/Product; Shape entry gate |
| Provider terms/coverage unknown | High / Critical | Privacy/legal + retrieval lead | Spike narrow canonical providers; reject providers without required disclosure/no-training/deletion terms | A1 before provider implementation/launch |
| Quote/locator retention legality | Medium / Critical | Privacy/legal | Prefer minimal quote or withheld hash; final rule requires source-by-source matrix | A1 before launch |
| Exact 24h/30d semantics and backups | Medium / Critical | Privacy/legal + Security | Separate stores and prove deletion; decide backup purge/tombstone semantics | A1 before storage policy approval |
| Model/vendor data reuse | Medium / Critical | Privacy/legal + Security | Eligible no-training vendor or self-hosted model; no vendor until contract/control evidence | A1 before sending content |
| Initial provider/parser set | High / High | Tech Lead + Product | Narrow to formats that pass locked locator tests; reduce coverage rather than integrity | Concierge evidence; provider feasibility |
| Entailment validator mechanism | Medium / Critical | QA + ML lead | Deterministic checks plus independently versioned evaluator; human audit remains release gate | QA standard before implementation |
| Authorized PDF uploads | Medium / Critical | Security + Legal | Keep disabled in MVP until attestation, scanning, rights and deletion gates pass | A1/security explicit approval |
| Currency/delayed billing margin | Medium / High | Product/Finance | Reserve conservative buffer inside US$8 and cap provider requests | A2 before cost implementation |
| Pricing/margin threshold | High / High | Product/Finance | Preserve US$3/US$8 now; scale only after approved economics | A2 before scale |
| Named owners/deadline absent | Certain / High | Orchestrator | Assign product, legal, finance, design, tech, QA, DevOps/Security owners and date | A3 before Shape exit |
| Cloud/RTO/RPO/region choice | Medium / Medium | DevOps/Security | Single-region MVP with tested restore; set explicit RTO/RPO in Shape | Platform owner before deployment |
| Tenant model at launch | Medium / High | Product/Security | Private tenant per organization; no public sharing | Product/Security before auth build |
| Audit destination immutability | Low / High | Security/Legal | Append-only DB/object manifest; decide whether regulated WORM is required | A1/Security before launch |

### Explicit escalation

Observed facts: frame approval, named owners, decision deadline, provider/legal approvals, locked concierge tasks and locked claim audit are absent. Affected work: implementation assignment, provider selection, retention semantics, upload path, vendor/model use and launch. Viable options are (1) remain at architecture planning/concierge setup, recommended; (2) approve only narrow technical spikes using synthetic/public fixtures; or (3) prematurely implement production paths, not recommended. The orchestrator must resolve A3 and schedule A1/A2 before Shape exit. This plan must not be treated as shape-ready or implementation approval.
