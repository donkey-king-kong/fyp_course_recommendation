# Proposed Technical Plan: Grounded Assistant and Job Intelligence

**Flow ID:** `swe-tech-lead`  
**Parent:** parent orchestrator  
**Date:** 2026-11-10  
**Status:** Proposed buildable architecture; not frame-approved; not shape-ready; not approved for implementation or release  
**Inputs:** `final-plan.md`, `research/repo-analysis.md`, `research/security-constraints.md`, and the source files scoped by `repo-analysis.md`

## 1. Technical Decision

Extend the current FastAPI application with four isolated logical boundaries:

1. a deterministic, read-only assistant over versioned recommendation, roadmap, catalog, and reviewed course-skill evidence;
2. an optional no-tools LLM synthesizer that may only restate validated claims;
3. a separately gated private posting-analysis boundary with one-hour transient storage;
4. a future isolated ingestion worker for authorized shared sources.

The existing recommendation and readiness services remain authoritative. The
assistant, LLM, posting pipeline, skill mapper, source adapters, and scheduler
must never call, write, parameterize, or override recommendation filtering,
readiness, prerequisites, scoring, ranking, or exact-slot assignment.

Stage 2 cannot affect ranking before all Stage 4 graduation gates and authorities
approve a separate deterministic ranking proposal. Enforce this structurally:

- no `job_intelligence` or `assistant` import in
  `backend/services/recommendation_service.py`;
- no recommendation-service import in assistant or posting modules;
- no Stage 2 tables in recommendation queries, views, or database roles;
- no market fields in `RecommendationRequest`;
- `MARKET_RANKING_ENABLED=false`, absent from ordinary runtime configuration
  until a separate approved Stage 4 change;
- a dependency and response-hash regression check fails CI if Stage 1/2 changes
  recommendation outputs for locked baseline inputs.

## 2. Current to Proposed Architecture

```text
CURRENT
React/Zustand localStorage
  -> hard-coded localhost API clients
  -> FastAPI routers
  -> deterministic services
  -> PostgreSQL + checked-in JSON evidence

No auth, assistant, model adapter, job model, scheduler, queue, or migrations.

PROPOSED STAGES 0-2
React assistant/posting UI
  -> typed /assistant/v1 and /job-intelligence/v1 clients
  -> authenticated Principal boundary (production) or explicit offline fixture scope
  -> thin FastAPI routers
     -> IntentRouter
     -> AssistantOrchestrator
        -> intent-specific ContextBuilder
        -> ClaimEvidenceRegistry
        -> DeterministicTemplate
        -> CitationValidator
        -> LlmSynthesizerPort (optional, no tools)
           -> approved ProviderAdapter -> deployer-managed secret
     -> PostingPolicyService
     -> PostingAnalysisStateMachine
        -> isolated document parser
        -> deterministic extractor/validator
        -> bounded LLM extraction (optional)
        -> CanonicalSkillRegistry
        -> PrivateAnalysisStore + ExpiryWorker
  -> PostgreSQL
     - append-only shared evidence/version records
     - tenant-scoped transient private analysis records

PROPOSED STAGE 3, DISABLED UNTIL AUTHORIZED
External scheduler
  -> registered source-policy/query pair event
  -> queue + distributed lease
  -> isolated ingestion worker with restricted egress
     -> SourceAdapter
     -> immutable snapshot/assertion/normalization stores
     -> review/publication service

RecommendationService remains outside every path above.
```

The FastAPI monolith may host Stage 0-2 logical modules. Any network collection,
scheduled ingestion, or hostile remote-content parsing must run in the isolated
worker before activation.

## 3. Component Boundaries

| Component | Owns | Must not own |
| --- | --- | --- |
| `IntentRouter` | Six allowlisted intents, entity checks, one clarification | Semantic free-form routing, actions, retrieval |
| `ContextBuilder` | Minimum typed facts for one intent, deterministic ordering | Raw browser store, raw PDFs, ranking calls |
| `ClaimEvidenceRegistry` | Immutable claim, citation, snapshot, version, resolution | Model prose or mutable source rebinding |
| `DeterministicTemplate` | Complete fallback answer per route | Provider behavior |
| `AssistantOrchestrator` | Route, context, fallback-first flow, validation | Recommendation mutation or hidden recalculation |
| `LlmSynthesizerPort` | Bounded synthesis request/response contract | Tools, retrieval, secrets, writes |
| `PostingPolicyService` | Provenance declaration, role/input/source policy | Legal approval inference |
| `PostingAnalysisStateMachine` | Lifecycle, extraction, validation, deletion request | Shared publication or ranking |
| `CanonicalSkillRegistry` | Versioned IDs, aliases, taxonomy and course links | Prompt-only mappings |
| `SourceAdapter` | One approved source's auth, fields, limits, attribution, deletion hooks | Scheduling, publication, recommendation policy |
| `IngestionService` | Jobs, leases, idempotency, retries, provenance, kill switches | Source-specific interpretation |
| `Scheduler` | Invoke pre-registered policy/query pairs | User cron, URLs, source registration |
| `ReviewPublicationService` | Approval state and immutable publication version | Automatic publication |

## 4. Deterministic Assistant Flow

### 4.1 Request and routing

`POST /assistant/v1/answers` accepts an explicit UI action, optional text, and
opaque references. It never accepts a full Zustand record.

Routing precedence:

1. explicit `intent` from an allowlisted UI entry point;
2. required entity shape and IDs;
3. deterministic keyword/entity rules;
4. if exactly two intents remain, return `clarification_required`;
5. otherwise return `unsupported_intent` and supported actions.

The six intents are exactly:

- `explain_recommendation`
- `explain_readiness_or_prerequisite`
- `compare_current_recommendations`
- `explain_open_slot`
- `show_course_fact`
- `show_reviewed_skill_exposure`

The router cannot invoke the model. Adding an intent requires a new enum value,
builder, template, locked fixtures, and authority review.

### 4.2 Context builder

Each builder implements:

```python
class ContextBuilder(Protocol):
    intent: AssistantIntent
    def build(self, principal: Principal, request: AssistantRequest) -> GroundedContext: ...
```

`GroundedContext` contains only:

- `context_version`, `intent`, `built_at`;
- immutable `recommendation_result_ref` when relevant;
- selected recommendation/slot/course/roadmap IDs;
- typed `claims[]` and `citations[]`;
- freshness and conflict states;
- limitations and permitted next actions;
- a canonical SHA-256 hash over RFC 8785-style canonical JSON.

Builders query authoritative service projections or immutable snapshots and
sort all records by stable ID. They reject unknown, stale, cross-scope, or
unselected entity IDs. They do not accept model-selected IDs.

Current recommendation compatibility requires additive response metadata:
`resultRef`, `resultVersion`, `generatedAt`, and `inputHash`. The recommendations
router captures the already-computed deterministic response as an append-only
snapshot; it does not change the request or ranking call. Existing response
fields remain unchanged. If snapshot capture is unavailable, recommendations
still work, but assistant explanation returns `context_unavailable` rather than
treating browser-replayed JSON as authoritative.

Browser-only curriculum, transcript, completion, and preference fields remain
labelled `user_supplied` or `transcript_derived`; neither `studentId` nor
localStorage establishes identity.

### 4.3 Fallback-first orchestration

For every accepted route:

1. build and validate context;
2. render a complete deterministic answer;
3. bind every factual span to a claim and citation;
4. stop if synthesis is disabled, circuit-open, over budget, or unnecessary;
5. send only bounded claims, limitations, and display labels to the adapter;
6. validate model shape, claim references, prohibited wording, and citations;
7. return synthesis or the prebuilt fallback with
   `model_enhancement_unavailable`.

Raw score components stay out of user-facing context. Builders translate the
existing evidence into qualitative reasons without changing or recomputing it.

## 5. LLM Provider Adapter and Secret

```python
class LlmSynthesizerPort(Protocol):
    def synthesize(self, request: SynthesisRequest) -> SynthesisResult: ...
```

`SynthesisRequest` contains prompt/schema/model versions, intent, bounded claim
records, citation IDs, limitations, locale, and token ceiling. It contains no
secret, raw student document, arbitrary history, URL, tool definition, database
handle, or ranking input.

One `OpenAICompatibleProviderAdapter` is proposed behind the port; provider,
endpoint, region, and model remain authority-deferred. The credential is one
deployer-managed secret per environment/service, injected at runtime from the
approved secret manager. It is never accepted from users or exposed to the
browser, prompts, URLs, cookies, localStorage, logs, traces, error payloads, or
ordinary config.

Startup modes:

- secret missing or model kill switch off: `deterministic_only`;
- provider auth/revocation failure: open circuit immediately, no retry;
- transient failures: proposed breaker of five failures in 60 seconds, open
  five minutes, then one half-open probe;
- one primary call and at most one schema-repair call;
- provider/model/prompt change requires locked shadow replay.

## 6. Claims, Citations, and Evidence Registry

Immutable entities:

- `evidence_snapshots`
- `evidence_claims`
- `evidence_citations`
- `answer_records` for content-free identity/version metadata only where allowed
- `recommendation_result_snapshots`
- `skill_registry_versions`
- `course_skill_link_versions`
- future `source_policy_versions` and `publication_versions`

Every factual span resolves to:

```json
{
  "claimId": "clm_...",
  "claimClass": "catalog_fact",
  "snapshotId": "snp_...",
  "locator": {"kind": "json_pointer", "value": "/modules/SC4023/description"},
  "contentSha256": "...",
  "sourceVersion": "catalog-2026-...",
  "policyVersion": null,
  "observedAt": "2026-11-10T00:00:00Z",
  "resolution": "active",
  "labels": ["seeded"]
}
```

Claim classes are `catalog_fact`, `deterministic_recommendation_fact`,
`job_evidence`, `normalized_skill_inference`, and `generated_advice`.
Resolution is `active`, `superseded`, `stale`, `withdrawn`, or `unavailable`.
Refresh creates new IDs and versions; old citations are never rebound.

The model may cite only registry IDs included in its request. Application
validation requires every returned factual span to reference an included active
claim and resolvable locator. Generated advice has no factual authority and
must cite each premise.

## 7. Posting Ingestion and Extraction State Machine

Stage 2B accepts one English text or approved text-bearing PDF, within proposed
configured limits, for the two exact pilot roles. It accepts no URL fetch.

Analysis states:

```text
received
  -> provenance_validated
  -> content_isolated
  -> deterministic_parsed
  -> extracting
  -> evidence_validated
  -> normalizing
  -> completed | completed_with_gaps | rejected | abstained
  -> deleting -> deleted

Any nonterminal state -> failed_pending_cleanup -> deleted (within 24h)
```

Item states:

```text
detected
  -> evidence_validated
  -> normalized | ambiguous | unmapped
  -> accepted | rejected

conflicting may be attached before acceptance
```

Deterministic code owns document identity, headings/lists, exact offsets,
quote matching, modality enums, negation, hashes, schema/range/cross-field
validation, policy, and state transitions. The model sees only unresolved,
requirement-bearing spans and may split atomic requirements, interpret local
modality, resolve a local clause, or propose mapping candidates. One schema
repair and one posting-level user clarification are allowed; otherwise abstain.

Only exact evidence with a valid locator and validated modality can be accepted.
Responsibilities and company technologies do not become candidate requirements.

## 8. Source Adapters and Scheduler Separation

Stage 3 remains disabled until source authorization and operational gates pass.

`SourceAdapter` contract:

```python
class SourceAdapter(Protocol):
    source_id: str
    def fetch(self, approved_request: ApprovedSourceRequest) -> FetchArtifact: ...
    def translate(self, artifact: FetchArtifact) -> SourceSnapshotDraft: ...
    def lifecycle(self, artifact: FetchArtifact) -> SourceLifecycleSignal: ...
    def delete(self, source_ref: str) -> DeletionOutcome: ...
```

The scheduler emits only registered `(source_id, policy_version, query_id,
window, scheduled_at)` tuples. The ingestion service verifies policy, obtains a
distributed lease, applies quotas, and dispatches the adapter. Ordinary users
cannot supply hosts, URLs, cron expressions, bulk jobs, or query fan-out.

Source semantics stay in adapters; scheduler and ingestion code contain no
source-specific parsing. Publication requires a named data/source owner and a
new immutable publication version.

## 9. Canonical Skill Registry and Mapping

The initial registry seeds the six existing stable IDs from
`data/student_skill_evidence.json`. A registry version contains canonical ID,
label, status, aliases, role bridges, and pinned O*NET/ESCO/ISCO references.

Every mapping record stores:

- raw mention and exact evidence claim;
- taxonomy and release/version;
- concept ID/URI, preferred label, and locale;
- candidates and scores;
- deterministic/model/reviewer method;
- `exact`, `alias`, `broader`, `narrower`, `ambiguous`, or `unmapped`;
- reviewer, decision time, and mapping version.

Course links separately store course code, source excerpt, depth, scope,
academic reviewer, decision time, and version. Data/domain owners approve
aliases and taxonomy mappings; academic owners approve course links.

Automatic mapping is disabled by category until the locked-set proposed gate of
at least 98% precision and adequate coverage passes. Prompts cannot create an
accepted registry entry or course link.

## 10. Transient Storage and Deletion

For the controlled Stage 2 pilot, keep raw text/PDF bytes and all private
derivatives in tenant-scoped PostgreSQL transient tables so immediate deletion
can occur in one database transaction. Enforce low input limits before insert.
Do not use shared caches or deduplication across principals.

- successful result: `expires_at <= created_at + 1 hour`;
- explicit delete: lock analysis, delete raw, claims, mappings, answer, and
  private citations in one transaction, then return `204`;
- failed/interrupted: no result and cleanup deadline within 24 hours;
- content-free operational metadata: opaque analysis ID, versions, timestamps,
  states, counts, and deletion outcome for at most 30 days;
- no prompt, source text, answer, student identifier, or secret in operational
  metadata;
- no history, save, share, export, or durable replay.

An expiry worker uses `FOR UPDATE SKIP LOCKED`, idempotent delete operations,
and a content-free deletion tombstone. Database backup and PITR policy must be
approved for the one-hour promise; otherwise Stage 2B remains blocked.

## 11. API Contracts and Errors

### Assistant

```json
POST /assistant/v1/answers
{
  "requestId": "uuid",
  "intent": "explain_recommendation",
  "message": "Why was this recommended?",
  "recommendationResultRef": "rrs_...",
  "entityIds": ["year3-sem1-slot2", "SC4023"]
}
```

```json
{
  "answerVersion": "assistant-answer/v1",
  "answer": "...",
  "intent": "explain_recommendation",
  "claims": [{"claimId": "clm_...", "class": "deterministic_recommendation_fact"}],
  "citations": [{"citationId": "cit_...", "claimId": "clm_...", "display": "..."}],
  "limitations": ["Planning readiness is not registration eligibility."],
  "freshness": {"state": "active", "observedAt": "..."},
  "fallbackAnswer": "...",
  "generated": false,
  "warnings": []
}
```

### Private posting

```json
POST /job-intelligence/v1/analyses
Idempotency-Key: uuid
{
  "inputKind": "text",
  "text": "...",
  "declaredOrigin": "direct_employer",
  "confirmedNotLinkedInDerived": true,
  "roleTarget": "software_engineer"
}
```

Returns `202` with `analysisId`, state, and `expiresAt`. `GET
/job-intelligence/v1/analyses/{id}` returns item-level evidence only. `DELETE
/job-intelligence/v1/analyses/{id}` performs immediate scoped deletion.

### Role context

`GET /job-intelligence/v1/role-context/{role}?version=...` returns pinned,
labelled taxonomy context and never employer demand.

### Error envelope

```json
{
  "error": {
    "code": "citation_validation_failed",
    "message": "The generated enhancement could not be validated.",
    "requestId": "uuid",
    "retryable": false,
    "fallbackAvailable": true
  }
}
```

Representative codes: `unsupported_intent`, `clarification_required`,
`context_unavailable`, `stale_context`, `unsupported_role`,
`provenance_required`, `source_policy_rejected`, `linkedin_origin_rejected`,
`input_too_large`, `unsupported_media`, `malicious_content_rejected`,
`analysis_expired`, `analysis_not_found`, `citation_validation_failed`,
`provider_unavailable`, `budget_exhausted`, `rate_limited`, and
`tenant_scope_denied`. Cross-tenant lookup returns the same `404` shape as an
unknown ID.

### Internal events

Use versioned envelopes with event ID, type, version, occurred time,
correlation ID, opaque tenant scope, aggregate ID, and content-free payload
references:

- `posting.analysis.requested.v1`
- `posting.analysis.expiry_due.v1`
- `posting.analysis.deleted.v1`
- `source.ingestion.scheduled.v1`
- `source.snapshot.created.v1`
- `source.publication.approved.v1`

Consumers deduplicate by event ID. Private source text is never in an event.

## 12. Immutability, Versioning, and Idempotency

Append-only IDs use server-generated UUIDv7/opaque prefixes. Mutable lifecycle
rows may point to immutable versions but cannot rewrite snapshot content.

Version independently:

- source snapshot and policy;
- parser, extraction prompt, schema, model, and adapter;
- mapper, taxonomy, canonical registry, and course-skill ledger;
- recommendation result and service revision;
- answer template and answer;
- publication.

Canonical JSON plus SHA-256 identifies content. Database constraints enforce
unique `(snapshot_id, claim_id)`, immutable content hashes, and state-transition
compare-and-set.

HTTP creation requires `Idempotency-Key`. Scope keys by authenticated principal,
endpoint, and normalized request hash. Same key/same hash replays the prior
status; same key/different hash returns `409 idempotency_conflict`. Scheduled
ingestion keys are `(source, policy_version, query_id, window, scheduled_at)`.
Retries never create new snapshots for identical source bytes and versions.

## 13. SSRF and Content Isolation

Stages 0-2 have no URL fetch path. Store a supplied URL only as inert provenance
text. Reject LinkedIn URLs and declared or reliably detected LinkedIn-derived
content.

For future approved adapters:

- registry allowlist of `https` host/path/port and policy version;
- reject credentials, fragments, literals, ambiguous encodings, nonstandard
  schemes, and unapproved ports;
- resolve and block loopback, private, link-local, multicast, reserved,
  metadata, and internal IPv4/IPv6 ranges;
- pin connection-time validation; revalidate each DNS answer and redirect;
- no redirects by default; bounded policy-approved redirects only;
- strict connect/read/total, byte, decompression, content-type, and retry caps;
- worker egress cannot reach databases, metadata, control plane, internal DNS,
  or application network;
- disposable worker has no provider secret, student data, session, shared
  filesystem, or browser cookies;
- static parsing only by default; no scripts, macros, active documents, or
  embedded resource fetches;
- source HTML is never directly rendered; UI accepts escaped plain text and
  structured citations only.

## 14. Prompt-Injection and Output Controls

Treat posting text, PDFs, HTML, prior text, model output, and citations as
untrusted data. Trusted instructions and untrusted spans occupy separate
structured fields with explicit delimiters and length bounds.

The model has no tools, network, secrets, shell, code execution, database,
filesystem, admin endpoint, mutation API, or arbitrary retrieval. Use a
versioned prompt and JSON Schema with closed enums, bounded strings/arrays,
`additionalProperties: false`, refusal/error variants, and one repair attempt.

Application checks:

- exact quote and byte/page/line locator match;
- claim and citation IDs belong to the supplied context;
- no new facts, links, images, HTML, tool arguments, or hidden actions;
- no registration, mastery, employability, demand, frequency, trend, optimum,
  ranking, or unsupported quantity wording;
- no system-prompt or secret-like content in output;
- escaped text rendering and CSP; model-generated remote resources never load.

Adversarial fixtures cover direct/indirect/encoded instructions, Markdown/HTML
exfiltration, citation spoofing, poisoned structured fields, cross-tenant IDs,
system-prompt requests, and secret patterns.

## 15. Authorization and Tenant Assumptions

Production private analysis and model personalization are blocked until
authenticated server identity exists. The proposed production principal is
derived from a validated Azure tenant and stable `oid`; the server derives
tenant/user scope and ignores body-supplied tenant IDs. Browser `studentId`,
email, and matriculation number are never authorization keys.

Until then:

- offline fixtures may run without external model/network calls;
- deterministic Stage 1 may run only in an explicitly controlled single-user
  pilot scope;
- Stage 2B cannot serve unauthenticated general traffic.

Service and data-access methods require `Principal`, and every private row,
cache key, event, job, and deletion is scoped from it. Shared snapshots can be
global only when source rights permit reuse and they contain no student data.
Admin/source/provider/faculty/kill-switch operations require separate roles and
are never model tools.

## 16. Proposed Cost and Latency Budgets

These are release targets, not measured results, at ten concurrent pilot
requests:

- deterministic fallback p95: at most 1 second;
- assisted answer p50/p95: at most 4/8 seconds;
- end-to-end timeout: 10 seconds, then fallback;
- one primary and one repair call maximum;
- 8,000 input and 1,000 output tokens maximum per call;
- USD 0.03 variable cost maximum per completed assisted answer;
- USD 100 monthly pilot hard stop;
- queue and concurrency caps per principal, tenant, model, source, and global;
- reject before provider call when budget or input bounds fail.

Stage 2 parsing runs asynchronously. Proposed pilot targets are `202` within 500
ms and completed text analysis p95 within 15 seconds, subject to fixture
measurement before a release gate is fixed.

## 17. Content-Free Observability

Structured telemetry allowlists only:

- request/correlation/opaque principal IDs;
- intent, state, claim counts, citation counts, validation outcome;
- component and version IDs;
- provider request ID, model, latency, token counts, cost, finish/refusal/error
  class;
- source/policy/query IDs, HTTP status class, bytes, queue/lease/retry counts;
- deletion deadline/outcome and kill-switch state.

Never log request/response bodies, prompts, answers, excerpts, source HTML,
uploads, student identifiers, secrets, authorization/cookies, signed URLs,
database URLs, or dead-letter payload content. Redact at ingress and every
export sink. Metrics labels must be bounded and content-free.

Alerts cover auth/tenant denial spikes, secret access anomalies, provider
auth/failure/latency/cost, citation validation, deletion overdue, stale
publication, source `403/429`, queue growth, and breaker/kill-switch changes.

## 18. Failure and Fallback Behavior

| Failure | Behavior |
| --- | --- |
| Missing/revoked provider secret | Deterministic-only; auth failure opens circuit immediately |
| Provider timeout/rate/budget/circuit | Return prebuilt fallback with warning |
| Invalid model schema/citation/claim | One repair, then fallback; do not expose invalid prose |
| Context missing/stale/cross-scope | Fail closed with bounded source-refresh action |
| Catalog/database unavailable | Existing endpoints retain current `503`; assistant does not invent |
| Posting policy/origin uncertain | One provenance clarification, then reject |
| Unsupported/malicious/oversized file | Reject before model; schedule content cleanup |
| Extraction ambiguity/conflict | Preserve item state, show exact evidence, or abstain |
| Expired/deleted analysis | Uniform `404 analysis_not_found`; no recreation |
| Expiry worker delayed | Alert, stop new Stage 2 analyses, run idempotent cleanup |
| Source policy expires/withdraws | Stop new fetch/publication; mark dependent evidence unavailable and selectively purge |
| Ingestion/provider outage | No effect on recommendation service; static behavior continues |
| Bad prompt/model/publication | Capability-specific kill switch and last approved version |

No fallback may silently use stale evidence as current.

## 19. Migrations and Compatibility

Introduce Alembic before feature tables; stop extending the current
`create_all`/manual column-ensure pattern for new domains.

Migration sequence:

1. migration framework and baseline of existing tables;
2. recommendation snapshot and evidence registry tables;
3. canonical skill registry and reviewed course-link tables;
4. transient posting-analysis tables with cascade/delete constraints;
5. source-policy, ingestion, snapshot, review, and publication tables only
   after Stage 3 authorization.

Compatibility rules:

- existing `/recommendations`, roadmap, module, transcript, and student-skills
  request fields and behavior remain unchanged;
- recommendation metadata is additive and optional during rollout;
- new endpoints are namespaced `/assistant/v1` and `/job-intelligence/v1`;
- frontend reads `VITE_API_BASE_URL`, defaulting to current local development
  origin;
- `data/student_skill_evidence.json` remains the seed source until the reviewed
  registry migration is accepted; compare seeded DB output to the JSON hash;
- no raw transcript/curriculum migration and no chat-history migration;
- rollback disables new routers/workers and drops only unreferenced feature
  tables after retention/deletion proof;
- Stage 1/2 deploy and rollback do not modify recommendation formulas or static
  career mappings.

## 20. Exact Future File Ownership

One owner edits each path. The integration owner alone edits shared composition
files after owner handoffs.

### Backend owner

```text
backend/schemas/assistant.py
backend/schemas/evidence.py
backend/schemas/job_intelligence.py
backend/models/evidence.py
backend/models/recommendation_snapshot.py
backend/models/skill_registry.py
backend/models/posting_analysis.py
backend/models/source_ingestion.py
backend/routers/assistant.py
backend/routers/job_intelligence.py
backend/services/assistant/__init__.py
backend/services/assistant/intent_router.py
backend/services/assistant/context_builders.py
backend/services/assistant/templates.py
backend/services/assistant/orchestrator.py
backend/services/assistant/citation_validator.py
backend/services/assistant/provider_port.py
backend/clients/llm_provider.py
backend/services/evidence_registry.py
backend/services/recommendation_snapshot_service.py
backend/services/job_intelligence/policy.py
backend/services/job_intelligence/state_machine.py
backend/services/job_intelligence/extraction.py
backend/services/job_intelligence/skill_registry.py
backend/services/job_intelligence/lifecycle.py
backend/services/ingestion/service.py
backend/services/ingestion/publication.py
backend/clients/job_sources/base.py
backend/clients/job_sources/<approved_source>.py
backend/workers/private_expiry.py
backend/workers/source_ingestion.py
```

Contract: implements read-only assistant and governed evidence services; may not
edit recommendation ranking/readiness services.

### Frontend owner

```text
frontend/src/types/assistant.ts
frontend/src/types/jobIntelligence.ts
frontend/src/api/assistantApi.ts
frontend/src/api/jobIntelligenceApi.ts
frontend/src/components/assistant/AssistantPanel.tsx
frontend/src/components/assistant/AnswerEvidence.tsx
frontend/src/components/assistant/AssistantStates.tsx
frontend/src/components/job-intelligence/PostingInput.tsx
frontend/src/components/job-intelligence/PostingResult.tsx
frontend/src/components/job-intelligence/ExpiryAndDelete.tsx
frontend/src/components/job-intelligence/ProvenanceDeclaration.tsx
frontend/src/styles/assistant.css
frontend/src/styles/job-intelligence.css
```

Contract: sends bounded references, renders all evidence/limitation states,
never stores posting content/history, and never auto-fetches generated URLs.

### Integration owner

```text
backend/main.py
backend/requirements.txt
backend/models/__init__.py
backend/database/connection.py
backend/routers/recommendations.py
backend/schemas/recommendation.py
backend/services/recommendation_service.py
frontend/src/App.tsx
frontend/src/store/useProfileStore.ts
frontend/src/config/api.ts
frontend/package.json
alembic.ini
backend/database/migrations/env.py
backend/database/migrations/versions/<revision>_*.py
```

Contract: composes routers/config/migrations, adds snapshot metadata without
changing deterministic recommendation behavior, and rejects any Stage 1/2
ranking diff. `recommendation_service.py` should receive no functional edit;
ownership is reserved to resolve imports or prove a zero-diff review.

### QA owner

```text
data/assistant_fixtures/*.json
data/posting_analysis_fixtures/*.json
data/security_fixtures/*
scripts/run_assistant_contract_checks.py
scripts/run_posting_extraction_checks.py
scripts/run_prompt_injection_checks.py
scripts/run_tenant_isolation_checks.py
scripts/run_deletion_lifecycle_checks.py
scripts/run_recommendation_noninterference.py
scripts/run_llm_shadow_replay.py
scripts/run_source_adapter_contract.py
```

Contract: owns locked fixtures, expected outcomes, regression evidence, and
content-free reports; does not tune implementation against held-out labels.

### DevOps/security owner

```text
.env.example
deploy/api.yaml
deploy/private-expiry-worker.yaml
deploy/source-ingestion-worker.yaml
deploy/scheduler.yaml
deploy/network-policies.yaml
deploy/secrets.md
deploy/runbooks/llm-provider.md
deploy/runbooks/private-data-deletion.md
deploy/runbooks/source-withdrawal.md
deploy/runbooks/kill-switches.md
```

Contract: secret injection, worker isolation, egress, schedules, budgets,
alerts, kill switches, retention, and drills. Source worker/scheduler manifests
remain disabled until Stage 3 approval.

## 21. Integration Order and Handoffs

1. **P0 contracts:** Backend schemas, authority tests, fixtures, and migration
   baseline. Freeze API/error/state/version contracts.
2. **P0 evidence foundation:** immutable recommendation snapshots, claim and
   citation registry, registry seeds, and citation validator.
3. **P0 deterministic Stage 1:** intent router, six builders, templates,
   orchestrator, API, and deterministic frontend states.
4. **P0 noninterference gate:** locked recommendation captures and dependency
   checks must show no Stage 1/2 ranking/readiness/prerequisite/slot effect.
5. **P0 optional synthesis:** provider port, deployer secret, breaker, budgets,
   shadow replay, then independently gated frontend generated/fallback state.
6. **P0 role target:** pinned taxonomy projections and reviewed registry only.
7. **P0 supplied posting:** authenticated principal, provenance flow, transient
   store, extraction state machine, delete/expiry worker, hostile-file controls.
8. **P1 authorized ingestion:** source policy registry, one adapter, isolated
   worker, scheduler, review/publication, selective purge; disabled by default.
9. **Later separate proposal:** deterministic market-ranking shadow work only
   after every graduation and authority gate. No LLM scoring.

Each handoff records files, contracts, assumptions, verification output, gaps,
next owner, and requested action. Interface freeze occurs after steps 1 and 7;
shared-file integration begins only after owner handoffs.

## 22. Proposed Verification Commands

These are proposed commands for the future implementation; they are not current
passing evidence.

```bash
python3 -m compileall backend scripts
python3 -m alembic check
python3 -m alembic upgrade head
python3 scripts/run_assistant_contract_checks.py
python3 scripts/run_posting_extraction_checks.py
python3 scripts/run_prompt_injection_checks.py
python3 scripts/run_tenant_isolation_checks.py
python3 scripts/run_deletion_lifecycle_checks.py
python3 scripts/run_recommendation_noninterference.py
python3 scripts/run_llm_shadow_replay.py --deterministic-only
python3 scripts/run_source_adapter_contract.py --fixtures-only
python3 scripts/validate_recommendation_mappings.py
python3 scripts/evaluate_recommendation_benchmark.py
python3 scripts/run_counterfactual_sensitivity.py
python3 scripts/run_coverage_audit.py
npm --prefix frontend run lint
npm --prefix frontend run build
```

Release evidence must additionally prove:

- 100% factual spans resolve to class/source/version/locator;
- zero Stage 1/2 change to locked recommendation outputs;
- no assistant/posting dependency path into recommendation mutation;
- no raw academic document or student identifier reaches the model;
- cross-tenant direct-ID/cache/job/delete attempts fail;
- immediate, one-hour, and interrupted cleanup deadlines hold;
- provider secret/redaction/rotation and kill-switch drills pass;
- SSRF, redirect/DNS, hostile-content, egress, and selective-purge checks pass
  before Stage 3.

## 23. Proposed ADRs

| ADR | Decision | Alternatives rejected/deferred |
| --- | --- | --- |
| ADR-001 | Logical modules in current FastAPI app for Stages 0-2 | Separate AI service adds operational cost before scale/isolation evidence |
| ADR-002 | Deterministic fallback built before every model call | Model-only responses violate availability and authority requirements |
| ADR-003 | LLM is a no-tools synthesis/extraction adapter | Agentic retrieval/actions create ranking, SSRF, and exfiltration paths |
| ADR-004 | Append-only claim/snapshot identity; no citation rebinding | Mutable source pointers make old answers unauditable |
| ADR-005 | Capture recommendation response snapshots additively | Recomputing from assistant input could drift or hide changed parameters |
| ADR-006 | Canonical registry bridges job, taxonomy, course, and existing tags | Prompt-only aliases are unreviewed and non-repeatable |
| ADR-007 | Private pilot content in tenant-scoped transient PostgreSQL | Browser/localStorage, shared cache, or durable history cannot meet scope/deletion |
| ADR-008 | Network ingestion in isolated worker; scheduler only emits registered pairs | In-process/general URL fetch exposes application network and policy bypass |
| ADR-009 | Stage 2 data plane cannot be queried by recommender | Feature flags alone do not prevent accidental ranking influence |
| ADR-010 | Alembic for all new tables | Continuing ad hoc `create_all`/column ensures is not reversible or auditable |
| ADR-011 | Content-free general telemetry | Prompt/response logging conflicts with private lifecycle and secret controls |
| ADR-012 | Stage 4 is a separate deterministic proposal with static fallback | LLM scoring or direct Stage 2 weighting violates graduation gates |

All ADRs remain proposed until the responsible authority accepts them.

## 24. Authority Dependencies and Stops

| Authority | Required decision/evidence | Blocks |
| --- | --- | --- |
| Product/frame | Accept capability boundaries, six intents, and independent Stage 2 modes | Shape and implementation |
| Tech lead | Interface freeze, module boundaries, migration and noninterference evidence | Each technical cohort |
| Legal/source | Written source rights, terms/robots, derivatives, LLM use, display, retention/deletion | Any live Stage 3 source or LinkedIn exception |
| Privacy/security | Provider/endpoint/region, minimum payload, identity, tenant isolation, deletion, hostile-content controls | Stage 1B, 2B, 3 |
| DevOps/security | Secret manager, rotation, worker egress/isolation, kill switches, runbooks | External model and workers |
| Finance/product sponsor | Provider and spend ceiling | Stage 1B onward |
| Academic/recommendation | Course-skill links; any later formula/tolerance | Stage 2 course claims and Stage 4 |
| Data/domain/source | Aliases, taxonomy mappings, publication and coverage | Stages 2-4 |
| Research/evaluation | Locked sets, annotation/adjudication, study protocol | Cohort progression |
| Accessibility | Keyboard/screen-reader evidence and defect disposition | User-facing release |
| Release authority | Capability-specific go/no-go and rollback acceptance | Any production release |

Non-waivable stops are source authorization, authenticated tenant isolation for
private multi-user data, selective deletion, secret safety, deterministic
fallback, and zero critical security failures. Production remains blocked.

## 25. Residual Risks

- Current browser state is editable and unauthenticated; it cannot support a
  production private assistant without server identity.
- Recommendation snapshots add storage and transaction behavior to a currently
  read-only response path; rollout needs fail-open compatibility for
  recommendations and fail-closed behavior for explanations.
- PostgreSQL backup/PITR behavior may conflict with the one-hour content promise;
  privacy and operations must approve deletion semantics before Stage 2B.
- The seven-course skill ledger is too sparse for broad gaps or mastery claims.
- Provider, endpoint, region, source, queue, scheduler, and infrastructure are
  intentionally undecided.
- Exact future deployment paths are ownership proposals, not evidence that
  those directories or platforms are approved.

This plan defines an executable decomposition only. It does not confer frame,
shape, legal, privacy, security, academic, source, finance, accessibility, or
release approval.
