# Final Product Plan: Grounded Course Assistant and Job Intelligence

**Flow ID:** `swe-product-manager`
**Parent:** parent orchestrator
**Status:** Planning complete; not frame-approved; not shape-ready; not implemented; not released
**Evidence cutoff:** 2026-11-10
**Authority:** Authoritative standalone product plan for this planning run

## 1. Executive Decision

Build one course-recommendation product with separately gated capabilities:

1. A grounded, deterministic-first assistant that explains the student's
   existing roadmap and recommendation evidence.
2. A read-only job-context companion with two independent modes:
   taxonomy-backed role context and ephemeral supplied-posting analysis.
3. A separately governed job-evidence pipeline only after source authorization.
4. Market-informed deterministic ranking only through a later proposal after
   read-only value, source, mapping, coverage, and regression gates pass.

The assistant and job context share the student journey and canonical skill
bridge. They do not share authority:

- The existing backend remains the sole authority for prerequisites, readiness,
  filtering, scoring, ranking, and exact-slot assignment.
- The model may explain, compare, translate, and suggest a bounded next step.
- The model receives no mutation, eligibility, ranking, source-policy, admin,
  network, database, shell, or arbitrary tool authority.
- Job ingestion, source policy, private-record lifecycle, publication, and
  ranking influence have separate controls and kill switches.
- Stage 1 and Stage 2 are read-only. Neither changes a recommendation.

The current FastAPI monolith may host the initial logical boundaries. Authorized
network collection or scheduling requires an isolated ingestion worker before
activation.

## 2. Persona and JTBD

**Primary persona:** an NTU computing student with a generated roadmap or
deterministic recommendation who needs to understand why it was produced before
making a course decision.

**Primary JTBD:**

> When I receive a course recommendation, help me understand its evidence,
> prerequisites, tradeoffs, uncertainty, and what could change it, without
> overstating academic eligibility or career outcomes.

**Secondary JTBD:** relate an existing recommendation to a supported role target
or an authorized supplied posting while preserving the difference between
employer evidence, taxonomy context, reviewed course exposure, and unknowns.

Prospective-student catalog chat and generalized career advice are outside the
initial release.

## 3. Capability Stages

| Stage | Capability | Product boundary | Exit condition |
|---|---|---|---|
| 0 | Contract and fixtures | Six intents, claim/citation schemas, canonical skill seeds, deterministic templates, synthetic or legally retained fixtures only | Contract, authority, fallback, and adversarial checks pass |
| 1A | Deterministic grounded assistant | Six allowlisted routes; no model dependency | Each route has valid grounding, fallback, limitations, and abstention |
| 1B | Optional model synthesis | One provider adapter; rephrases bounded claims only | Grounding, comprehension, cost, latency, privacy, and safety gates pass |
| 2A | `role_target` | Pinned O*NET/ESCO context for the narrow pilot; no employer-demand claim | Independent user-value and calibrated-trust gate passes |
| 2B | `supplied_posting` | Private, declaration-gated, non-LinkedIn, no-fetch, one-hour maximum result lifetime | Independent extraction, citation, deletion, user-value, and trust gates pass |
| 3 | Authorized shared snapshots | One written-authorized source; scheduled shared evidence; no ranking effect | Source, policy, quality, coverage, freshness, operations, and publication approvals pass |
| 4 | Deterministic market-informed ranking | Separate candidate policy in shadow mode; no LLM scoring | Ranking graduation gates and release authority approval pass |

Stages are independently releasable and independently killable. Later-stage
capabilities must not be marketed as present earlier.

## 4. Feature Boundary

### Grounded recommendation assistant

Owns:

- deterministic intent routing;
- bounded context assembly from existing backend records;
- deterministic answer templates;
- optional synthesis over supplied claims;
- answer validation, citations, limitations, and fallback;
- explanation of existing results only.

Does not own:

- course filtering, readiness, prerequisites, scoring, ranking, or slots;
- preference changes, profile mutation, registration actions, or waivers;
- job-source access, extraction publication, or market weights.

### Separately governed job-evidence pipeline

Owns:

- posting provenance and source-policy decisions;
- private posting extraction and lifecycle;
- future authorized retrieval, scheduling, quotas, deduplication, and freshness;
- immutable snapshots, raw assertions, normalized entities, mappings, review,
  publication, and selective purge.

Does not own:

- recommendation policy;
- direct user-facing ranking changes;
- source-rights interpretation outside named authority approval;
- model-generated facts or prompt-only mappings.

The common contract is a versioned canonical skill registry and immutable
claim/citation interface. The pipeline cannot publish into student-visible
context until its policy, evidence, and quality gates pass.

## 5. Stage 1 Contract

### Exact intents

| Intent | Required context | Supported output |
|---|---|---|
| `explain_recommendation` | Current recommendation and slot IDs | Existing reason, source, readiness, prerequisites, qualitative evidence |
| `explain_readiness_or_prerequisite` | Course/roadmap ID and current readiness snapshot | Implemented prerequisite/standing branch and material limitations |
| `compare_current_recommendations` | Two or more IDs in the current result | Evidence-backed comparison without declaring a universal optimum |
| `explain_open_slot` | Current open-slot ID | Existing `no-supported-match` or `limit-reached` reason |
| `show_course_fact` | Course code | Versioned catalog facts, with seeded/live limitations |
| `show_reviewed_skill_exposure` | Supported role and submitted course codes | Reviewed likely exposure and explicit unknowns, never mastery |

Routing occurs before synthesis from explicit UI context, entity IDs, and
deterministic rules. If exactly two routes remain plausible, ask one
clarification. Otherwise return `unsupported_intent` and the nearest supported
actions. Each intent has its own context builder, deterministic template,
limitations, and abstention tests.

### Unsupported behavior

Stage 1 does not provide anonymous catalog chat, general career advice,
unreturned course alternatives, persistent conversation, preference mutation,
registration eligibility, degree audit, timetable/vacancy checks, employability,
salary/demand claims, mastery claims, or model-selected retrieval. Score
components may be translated into qualitative reasons; raw numeric components
remain hidden.

## 6. Authority and Non-Goals

The assistant may:

- explain and compare validated claims;
- translate evidence into plain language;
- identify uncertainty and conflicts;
- suggest a bounded source, advisor, or user action.

The assistant may not:

- invent course content, prerequisites, employer requirements, quantities, or
  proficiency;
- infer employer intent, geography, work authorization, degree equivalence, or
  mastery;
- claim registration eligibility, employability, hiring probability, optimal
  choice, current demand, frequency, or trend;
- override or trigger hidden recalculation;
- convert taxonomy norms into employer statements;
- browse, fetch URLs, expose secrets, or use embedded content as instructions.

Non-goals through Stage 3 include LinkedIn collection, general web search,
salary prediction, autonomous course actions, persistent chat, BYOK, model
training on user/provider content, aggregate skills-gap/fit/coverage scores, and
any ranking effect.

## 7. Model Credential and Deterministic Fallback

The promised pilot API token is an environment-scoped, deployer-managed server
secret, not tenant BYOK.

- Inject one credential per environment/service from an approved secret
  manager.
- Never expose it to the browser or place it in chat, URLs, cookies,
  localStorage, analytics, logs, repositories, prompts, or ordinary
  configuration.
- Apply provider/model allowlists, access audit, spend limits, redaction tests,
  rotation, and immediate revocation.
- Missing configuration starts the app in `deterministic_only`.
- Authentication/revocation failures open the circuit immediately and require
  operator rotation; they are not retried.
- Provisional transient breaker: five failures in 60 seconds, open for five
  minutes, then one half-open probe.
- Every supported route builds fallback before a model call. Provider failure,
  timeout, validation failure, rate limit, or budget exhaustion returns that
  answer with `model_enhancement_unavailable`; users are never asked for a key.

Backend-only secret handling is consistent with the audited primary guidance in
[extraction-and-operations, section 12](research/extraction-and-operations.md#12-safe-handling-of-user-provided-llm-api-tokens):
[OpenAI key safety](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)
and [OWASP secrets management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).

## 8. Grounding and Citation Contract

### Exact claim classes

| Class | Meaning | Authority | Required display |
|---|---|---|---|
| `catalog_fact` | Course code, title, AU, description, prerequisite, level, seeded offering metadata | Versioned catalog/database snapshot | Exact field, source/version, and seeded/non-live qualification |
| `deterministic_recommendation_fact` | Assigned slot, source, readiness, score evidence, prerequisite path, open-slot reason | Existing backend result | Result/service version; immutable and not model-editable |
| `job_evidence` | Exact statement from an authorized posting/snapshot | Source snapshot | Exact quote, locator, observation time, and modality |
| `normalized_skill_inference` | Mapping from raw mention to canonical skill | Versioned mapper/taxonomy | Raw mention, state, taxonomy/version, and confidence reason |
| `generated_advice` | Model synthesis, comparison, or suggested next step | No factual authority | Generated label and citations for every factual premise |

Additional labels are mandatory: `user_supplied`, `transcript_derived`,
`reviewed_course_exposure`, `taxonomy_context`, `seeded`, `stale`,
`conflicting`, `ambiguous`, `unmapped`, `unknown`, and `fallback`.

Each answer returns `answer_version`, `answer`, `claims[]`, `citations[]`,
`limitations[]`, `freshness`, `fallbackAnswer`, `generated`, and optional
`proposedAction` with `confirmationRequired=true`.

Every factual span binds to immutable `snapshot_id`, `claim_id`, locator,
content hash, source/policy version, and observation time. Refresh creates new
snapshot, claim, and answer versions. Old citations are never rebound. Resolution
states are `active`, `superseded`, `stale`, `withdrawn`, or `unavailable`.
Unresolved evidence makes the old answer non-reusable for a new factual
decision. Excerpts display only where source policy permits.

Structured output constrains shape but still requires application and evidence
validation; this constraint is supported by
[extraction-and-operations, sections 1 and 4](research/extraction-and-operations.md#1-what-standards-provide-and-what-they-do-not)
and the audited [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-core.html)
and [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
claims.

## 9. LinkedIn and Compliant Inputs

### LinkedIn authorization-only track

Make no automated LinkedIn request, use no logged-in automation, and accept no
scraped or indirectly sourced LinkedIn dataset. Reject declared LinkedIn origin,
LinkedIn URLs, and reliably detected LinkedIn exports. One provenance
clarification is allowed; unresolved origin is rejected. Detection is not
represented as perfect.

This boundary relies only on audited or corrected claims:

- self-service Open Permissions do not include job-search inventory retrieval
  ([verification LA005 correction](research/citation-verification.md#corrected-claims);
  [LinkedIn access](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access));
- Job Posting API documentation describes outbound posting and does not
  document read/search
  ([LA008 correction](research/citation-verification.md#corrected-claims);
  [API overview](https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/overview));
- Apply Connect documents an ATS posting/application workflow, not a general
  search feed
  ([LA011 correction](research/citation-verification.md#corrected-claims);
  [Apply Connect](https://learn.microsoft.com/en-us/linkedin/talent/apply-connect/apply-connect-overview));
- LinkedIn prohibits the unauthorized automated collection methods considered
  here
  ([linkedin-access, Public job pages](research/linkedin-access.md#public-job-pages-are-not-an-ingestion-license);
  [User Agreement](https://www.linkedin.com/legal/user-agreement),
  [robots.txt](https://www.linkedin.com/robots.txt), and
  [Crawling Terms](https://www.linkedin.com/legal/crawling-terms)).

Reconsider LinkedIn only when written authorization covers collection, storage,
derived skills, model processing, display, attribution, retention, and deletion,
followed by legal, privacy, security, source-owner, and release approval.

### Compliant MVP sources and inputs

1. Pinned O*NET and/or ESCO for labelled occupational taxonomy context, not
   Singapore employer evidence or a live-vacancy/current-demand claim. The
   audited sources expose occupational/classification data rather than a
   documented live-vacancy feed
   ([LA041/LA043 corrections](research/citation-verification.md#corrected-claims);
   [O*NET](https://www.onetcenter.org/database.html);
   [ESCO](https://esco.ec.europa.eu/en/about-esco/what-esco)).
2. Pasted text or approved text/PDF upload for private analysis when the user
   affirms they may provide it, selects `direct_employer`,
   `approved_provider`, or `other_user_authorized`, and confirms it is not
   LinkedIn-derived.
3. No URL fetch. A URL may be stored only as provenance text.
4. Future live sources require written rights. Documented candidates include
   authenticated Adzuna search, employer-scoped Greenhouse/Lever published-job
   endpoints, and USAJOBS for U.S. federal scope
   ([linkedin-access, Feasible source options](research/linkedin-access.md#feasible-source-options);
   [Adzuna](https://developer.adzuna.com/docs/search),
   [Greenhouse](https://developers.greenhouse.io/job-board.html),
   [Lever](https://github.com/lever/postings-api),
   [USAJOBS](https://developer.usajobs.gov/API-Reference/GET-api-Search)).
5. Public API documentation is not procurement approval. Commercial use,
   retention, attribution, derivatives, model inference, display, and deletion
   must be confirmed in writing.

## 10. Stage 2 Pilot and Input Policy

Stage 2 is limited to English-language evidence for Singapore-based NTU
computing students exploring entry-level or graduate:

- `software_engineer`: `software engineer`, `software developer`, and explicit
  `junior` or `graduate` variants;
- `data_engineer`: `data engineer` and explicit `junior` or `graduate`
  variants.

Excluded: internships; frontend, backend, full-stack, analytics engineer,
machine-learning engineer, data scientist, architect, lead, staff, principal,
manager, other specialized/senior titles, and ambiguous titles. Unsupported
titles receive a scope message and are not coerced.

Accepted supplied inputs must be single postings, text-bearing, supported,
unencrypted, within configured byte/page/token limits, malware/content checked,
and provenance-declared. Reject binary, oversized, malicious, bulk,
origin-ambiguous, LinkedIn-derived, or acquisition-workaround inputs.

Stage 2 displays item-level evidence only: explicit posting requirement or
labelled taxonomy concept, modality, raw mention, mapping state/version,
reviewed course-exposure links, and explicit gaps. It omits aggregate skills
gap, fit, coverage, missing-skills ranking, frequency, trend, current demand,
and ranking claims.

`role_target` and `supplied_posting` are separate release units with independent
tasks, value results, comprehension results, defects, operational evidence,
kill switches, rollback paths, and continuation decisions. One cannot satisfy
the other's gate.

## 11. Extraction, Uncertainty, and Fallback

### Extraction state machine

```text
item:
detected
  -> evidence_validated
  -> normalized | ambiguous | unmapped
  -> accepted | rejected

conflicting may occur before acceptance

posting:
completed | completed_with_gaps | rejected | abstained
```

Deterministic code owns structure, typed fields, exact headings/lists, evidence
offsets and quote matching, schema/enum/range/cross-field checks, negation,
hashes, policy, versions, and lifecycle. The model receives only unresolved
requirement-bearing spans and may split atomic requirements, interpret local
modality, resolve local clauses, and propose mapping candidates. It gets one
schema repair. The posting gets one user clarification total, limited to
provenance, document identity, or a material fact the user can know.

Accepted requirements require exact evidence, valid locator, validated
modality, and application-side validation. Schema.org fields may be absent or
free text, so missing values remain unknown
([EO016 correction and EO017](research/citation-verification.md#corrected-claims);
[Schema.org JobPosting](https://schema.org/JobPosting)).

### Missing, vague, and conflicting ladder

Stop at the first supported useful level:

1. Exact deterministic/catalog fact.
2. Exact posting assertion with evidence.
3. Normalized skill with explicit mapping state.
4. Raw vague wording without invented quantity or proficiency.
5. Conflicting assertions side by side.
6. One targeted clarification when the user can resolve it.
7. Pinned taxonomy enrichment, labelled non-employer context.
8. `ambiguous`, `unmapped`, `unknown`, or `no reviewed course link`.
9. Concrete human/source check.
10. Abstention.

Unknown never means not required. A responsibility or company technology does
not become a candidate requirement. A missing reviewed course link does not
mean irrelevance, lack of learning, lack of mastery, or student deficiency.

## 12. Skill Taxonomy and Mapping

Use one internal canonical registry:

```text
raw source mention
  -> canonical skill ID
  -> pinned taxonomy mappings
  -> role/posting evidence
  -> reviewed course-content evidence and depth
  -> existing recommendation tag/skill area
```

Initial seed IDs:

- `programming-foundations`
- `software-engineering-practice`
- `software-delivery-management`
- `data-storage`
- `distributed-systems`
- `cloud-service-platforms`

O*NET anchors U.S. occupation context; ESCO provides European/multilingual
occupation and skill concepts; ISCO-08 provides international occupation
roll-up; an internal registry handles aliases and course/recommendation bridges.
The audited taxonomy roles and versioned identifiers are documented in
[extraction-and-operations, section 3](research/extraction-and-operations.md#3-taxonomy-and-normalization-options)
with primary sources
[O*NET](https://www.onetcenter.org/content.html),
[ESCO](https://ec.europa.eu/esco/api/doc/esco_api_doc.html), and
[ISCO-08](https://isco.ilo.org/en/isco-08/).

Every mapping stores raw mention, taxonomy/version, concept ID/URI, preferred
label, locale, candidates/scores, method, and `exact`, `alias`, `broader`,
`narrower`, `ambiguous`, or `unmapped` state. Automatic mapping is enabled by
category only after proposed locked-set precision of at least 98% with adequate
coverage. Otherwise it abstains.

The academic/domain owner exclusively approves course-to-skill links. The
data/domain owner exclusively approves aliases and taxonomy mappings. Every
accepted course link stores excerpt, depth, scope, reviewer, decision date, and
version. The existing seven-course ledger is author-reviewed seed evidence, not
independent validation.

## 13. Private Lifecycle

Each supplied posting receives a server-generated, server-scoped analysis ID
and visible expiry.

- Successful analysis: raw input, extracted claims, citations, derivatives,
  and rendered result remain available for no more than one hour, then clear
  and delete together.
- User deletion: clear and delete raw and derived private records immediately
  as one operation.
- Failed/interrupted analysis: no user-visible result; all raw and derived
  records deleted within 24 hours.
- Operational metadata: retain for 30 days only as opaque IDs, versions,
  timestamps, states, counts, and deletion outcome; no prompt, source text,
  answer, student identifier, or secret.
- No conversation history, save, share, export, or durable result.
- Revisit requires a new authorized submission and analysis ID.

Until authenticated server identity and tenant isolation exist, private posting
analysis is limited to controlled users under approved server-side scope.
Browser `studentId` is never an authorization key. Durable history requires a
new rights, privacy, tenancy, retention, deletion, and product decision.

## 14. On-Demand and Scheduled Ownership

- Course recommendation remains on demand through the existing deterministic
  endpoint.
- Assistant explanation reads a current/versioned result; chat never
  recalculates with hidden parameters.
- Supplied-posting analysis is private and on demand, with no network fetch.
- Shared market snapshots are scheduled only for registered source-policy/query
  pairs after written authorization.
- Future approved on-demand refresh and scheduled ingestion use the same policy,
  quotas, parser, provenance, deduplication, lifecycle, coalescing, and kill
  switches.
- Ordinary users cannot create cron expressions, bulk URL jobs, source
  registrations, or query fan-out.

A source adapter owns authentication, source-field translation, contract-bound
limits, lifecycle signals, attribution, and deletion hooks. The ingestion
service owns registered jobs, idempotency, leases, queues, retries, provenance,
and kill switches. The scheduler invokes registered pairs only. A named
data/source owner alone approves publication after policy, freshness, quality,
and coverage checks.

## 15. Freshness, Versioning, and Deduplication

Version source snapshot hash, source policy, parser, prompt, schema, model,
adapter, mapper, taxonomy, course-skill ledger, recommendation result, and
publication. Any change creates a new derived version.

Freshness is an evidence property:

- supplied posting: `observed_at_upload`, with no current/open claim;
- taxonomy: pinned release/version;
- authorized live snapshot: observation window, lifecycle, and source-specific
  stale threshold;
- stale or unavailable evidence cannot support current-demand or trend wording.

Future cadence is source-specific. The provisional starting target is a
24-hour active refresh and six-hour refresh near explicit expiry, subject to
contract, rate limits, and observed behavior. This is a product target, not an
external fact.

Lifecycle states are `discovered`, `active`, `possibly_stale`, `expired`,
`unavailable`, `reactivated`, and `tombstoned`. Preserve closure reason and last
observation. A transient failure or access denial is not proof of closure.
HTTP validators and conditional requests support revalidation
([extraction-and-operations, section 8](research/extraction-and-operations.md#8-stale-and-deleted-postings);
[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) and
[RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html)).

Deduplicate by source/requisition identity first, canonical content hash second,
and similarity only for review candidates. Never merge solely by title,
canonical URL, or semantic similarity. Retain every source member/version and
support unmerge. Target at least 99.5% pair precision before automatic shared
merge. Canonical JSON supports repeatable hashing
([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html)); redirects and
canonical links are signals, not proof of semantic identity
([Google canonicalization](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)).

## 16. UX State Requirements

The UI must visibly and accessibly distinguish:

- deterministic fact, employer evidence, taxonomy context, normalized
  inference, and generated advice;
- user-supplied versus transcript-derived versus reviewed course exposure;
- active, superseded, stale, withdrawn, unavailable, and expiring evidence;
- required, preferred, optional, unclear, negated, alternative, conflicting,
  ambiguous, unmapped, and unknown items;
- deterministic fallback and model-enhancement-unavailable states;
- readiness from registration eligibility and exposure from mastery;
- unsupported intent/title/input, refusal, validation failure, deletion, and
  source-policy rejection.

Required interactions include sentence/bullet-level citations, on-demand
evidence detail, visible posting expiry, immediate delete, provenance
declaration, LinkedIn rejection without legal-advice wording, and bounded next
actions. Loading, citation, limitation, refusal, stale, deletion, and error
states must be keyboard and screen-reader operable. The UI must not auto-fetch
model-generated links, images, or remote resources.

## 17. Proposed Component Boundaries

These are Shape inputs, not approved architecture:

```text
Frontend
  AssistantPanel
  Evidence/Citation components
  PostingProvenanceAndExpiry flow
  -> assistant API client

FastAPI router/schema
  -> IntentRouter (deterministic)
  -> ContextBuilders (one per Stage 1 intent)
  -> ClaimRegistry + CitationValidator
  -> DeterministicAnswerTemplates
  -> AssistantOrchestrator
       -> VersionedModelAdapter (optional)

Job evidence boundary
  -> PostingPolicyService
  -> PostingExtractionStateMachine
  -> CanonicalSkillRegistry
  -> CourseSkillEvidenceService
  -> PrivateAnalysisLifecycle

Future authorized pipeline
  SourceAdapter(s)
  -> IngestionService
  -> Snapshot/Assertion/Normalization stores
  -> ReviewAndPublicationService
  -> isolated worker and scheduler
```

Keep router logic thin, policy and orchestration in services, provider/source
semantics in adapters, and ranking in the existing recommendation service.
Assistant and extraction provider contracts are versioned separately.

## 18. Quality and Evaluation

### Locked evaluation

Build versioned sets for all six intents, all claim classes, known deterministic
recommendation/readiness outputs, missing/vague/conflicting/negated postings,
structured and prose inputs, PDFs, mapping states, malicious content, citation
spoofing, cross-user IDs, exfiltration links, and provider failures.

Before reporting release metrics:

- at least 100 locked posting families overall;
- dual annotation of all locked items;
- adjudication of every disagreement;
- at least 20 examples in each critical fallback path;
- splits by source/template/time to reduce leakage.

Measure factual support, citation resolution, deterministic contradiction,
unsupported claims, exact-span extraction, modality, mapping precision and
abstention, refusal correctness, fallback equivalence, deletion, freshness,
dedup over-merge, latency, cost, and user task outcomes. Human review is primary;
LLM-as-judge may supplement but cannot approve release.

### Audit sampling

During pilot, review 100% of new templates, new mapping categories, conflicts,
implicit/uncertain candidates, citation failures, and ranking-change cases.
Randomly review 10% of accepted assistant/extraction outputs per weekly cohort.
Dual-review release samples and adjudicate disagreements. Sampling may reduce
only after four consecutive weekly cohorts meet gates with no critical defect;
a critical incident or material drift restores the prior rate.

### User-study protocol

Run a moderated crossover with at least 20 target users comparing unchanged
recommendations alone with recommendations plus the tested read-only mode.
Evaluate `role_target` and `supplied_posting` independently; do not average.

Proposed continuation gates per mode:

- task success improves by at least 10 percentage points;
- at least 80% correctly distinguish employer evidence from taxonomy context;
- at least 80% correct on each critical distinction: citation support,
  fact/advice, unknown/stale, exposure/mastery, fallback, and
  readiness/registration;
- unsupported takeaways occur in no more than 5% of scored answers;
- median task time worsens by no more than 20%;
- at least 70% rate the context useful for the decision;
- any critical misconception repeated by two participants blocks progression
  until correction and retest.

Include keyboard/screen-reader sessions, interview every participant who forms
an unsupported takeaway, and report confidence intervals and qualitative
causes. These are proposed gates, not measured results.

## 19. Cost, Latency, and Precision Gates

At an agreed pilot load of 10 concurrent requests:

- generate fallback before the model call;
- at most one primary call and one schema-repair call;
- deterministic fallback p95 at most 1 second;
- model-assisted p50 at most 4 seconds and p95 at most 8 seconds;
- 10-second end-to-end timeout, then fallback;
- no more than 8,000 input and 1,000 output tokens per call;
- variable model cost at most USD 0.03 per completed assisted answer;
- monthly pilot model budget USD 100 with hard stop and fallback.

Quality gates:

- 100% displayed factual claims have class, source, version, and resolvable
  locator;
- zero assistant-caused changes to deterministic recommendation records;
- at least 99% factual-claim precision on accepted output;
- at least 99% required/preferred precision;
- at least 99.5% exact citation resolution;
- automatic mapping at least 98% precision per enabled category;
- unsupported accepted requirements no more than 0.5%;
- dedup pair precision at least 99.5%;
- zero critical policy/tool/tenant/secret failures;
- zero raw academic documents or student identifiers sent to the model in
  integration tests.

Thresholds are provisional release targets. They must be fixed before results
are inspected and cannot be silently weakened. Remove synthesis from an intent
if it misses value, latency, or cost gates.

## 20. Rollout and Kill Criteria

| Cohort | Scope | Minimum evidence window |
|---|---|---|
| 0 | Internal staff; synthetic or legally retained fixtures | Offline gates |
| 1 | Supervised target students; deterministic Stage 1 | Five operating days and required tasks |
| 2 | Same controlled scope with model synthesis | Five operating days and required tasks |
| 3A | Independently gated `role_target` | Five operating days, required tasks, and 20-user study |
| 3B | Independently gated `supplied_posting` | Five operating days, required tasks, and 20-user study |
| Later | Authorized shared snapshots | Separate source cohort |
| Later | Ranking shadow and limited rollout | Separate ranking cohort |

Never combine first model use, first private upload, first live source, and first
ranking influence in one cohort. No private posting analysis for unauthenticated
general traffic.

Pause or kill the affected capability when:

- source authorization is absent, expires, conflicts, or is withdrawn;
- tenant isolation, selective deletion, secret safety, or a critical security
  fixture fails;
- unsupported claims or citations miss gates;
- deterministic fallback cannot be restored immediately;
- provider cost/latency or user-value gates fail;
- stale evidence is published as current;
- role-target or supplied-posting mode fails its independent study;
- the operator credential is compromised or the budget hard stop is reached.

Independent audited switches cover all model calls, provider/model version,
each Stage 2 mode, all ingestion, source/policy, schedules, on-demand refresh,
rendering, BYOK, mutations, and market-informed ranking.

## 21. Ranking Graduation Gates

Ranking is not committed scope. Entry to shadow mode requires all of:

1. The read-only crossover gate passes for the relevant evidence mode.
2. Source rights expressly cover ranking derivatives.
3. Both pilot roles meet predeclared publishable coverage.
4. Applicable mappings and course links are approved.
5. No stale, implicit, conflicting, ambiguous, or unmapped evidence enters
   weights.
6. The candidate policy is deterministic and versioned.
7. The recommendation owner approves formula and tolerances.

Shadow exit requires locked-task improvement over the static baseline, no
eligibility or slot-contract change, side-by-side explanations, and no
unacceptable all-six-career, diversity, stability, or fairness regression under
tolerances fixed before results are inspected. There is no LLM scoring and no
second unreviewed market bonus. Ranking has its own kill switch and immediate
static fallback. A failed gate returns the product to read-only context.

## 22. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Unauthorized source use | Written-rights gate, source registry, LinkedIn disabled, fail closed |
| Hallucinated course/job facts | Immutable claims, exact evidence, validator, deterministic fallback |
| Model authority creep | No mutation/ranking tools; backend contract tests |
| Sparse course-skill evidence | Narrow pilot, item-level claims, explicit unknowns, owner review |
| Taxonomy/geography mismatch | Raw mention, pinned versions, external-context label, abstention |
| Prompt injection or exfiltration | Untrusted-data boundary, no model tools/secrets, strict validation |
| Private-data retention | One-hour joint expiry, immediate delete, 24-hour interrupted cleanup |
| Cross-user access | Controlled pilot, server-derived scope, authenticated tenancy before expansion |
| Stale or duplicate evidence | Lifecycle states, observation windows, identity-first conservative dedup |
| Model outage or cost spike | Prebuilt fallback, breaker, budgets, operator recovery |
| User over-trust | Claim-class UX, comprehension gates, no aggregate gap/fit claims |
| Ranking regression | Read-only first, shadow gates, all-six-career checks, static rollback |

## 23. Dependencies

- Reviewed canonical skill registry and course-skill ledger.
- Six deterministic context builders and templates.
- Immutable claim/citation schemas and replay fixtures.
- Named product, technical, academic, data/source, legal, privacy, security,
  finance, research, accessibility, and release owners.
- Approved provider/endpoint/region, processor terms, minimum payload, secret
  manager, budgets, redaction tests, and model kill switch before Stage 1B.
- Controlled server-side identity scope, deletion transaction, and hostile-file
  controls before Stage 2B.
- Written source agreement, policy registry, isolated worker, quotas,
  provenance, dedup, freshness, purge, monitoring, and publication process
  before Stage 3.
- Locked fixtures, annotation guide, adjudication, audit tooling, and
  accessibility protocol before cohort progression.

## 24. Prioritized Roadmap

1. **P0 contract:** freeze schemas, six routes, authority matrix, claim classes,
   templates, fixtures, and acceptance tests.
2. **P0 deterministic Stage 1:** implement bounded context builders, fallback,
   citation resolution, limitations, and unsupported-intent UX.
3. **P0 evaluated synthesis:** add one versioned provider adapter only after
   provider/privacy/secrets approval; run shadow and controlled cohort.
4. **P0 taxonomy mode:** pin role mappings for the exact Stage 2 segment and
   independently evaluate `role_target`.
5. **P0 supplied-posting mode:** implement provenance gate, extraction state
   machine, mapping review, one-hour lifecycle, and independent evaluation.
6. **P1 source authorization:** select one provider and complete rights and
   policy approvals; no acquisition before approval.
7. **P1 shared snapshots:** deploy isolated ingestion, publication, freshness,
   dedup, purge, observability, and kill controls.
8. **Later ranking proposal:** define predeclared coverage/tolerances, shadow
   deterministic policy, and all-six-career evaluation.

Explicitly deferred: durable private records, save/share/export, persistent
chat, anonymous catalog chat, preference mutation, BYOK, broader roles/languages,
aggregate gap/fit/market claims, and LLM-controlled ranking.

## 25. Acceptance Criteria

Planning acceptance for handoff requires:

- all six Stage 1 intents and unsupported behavior are explicit;
- both Stage 2 modes and exact pilot segment are explicit;
- authority, claim classes, citation identity, fallback, and private lifecycle
  are internally consistent;
- all 34 decisions appear in the ledger;
- authority-deferred items are not represented as approved backlog;
- numeric targets are labelled proposed, not measured;
- source-dependent constraints cite audited artifact sections and primary URLs;
- no blocked citation-audit claim is used as an external fact;
- roadmap, rollout, kill, ranking, and Shape handoffs preserve read-only scope.

Release acceptance is capability-specific and additionally requires the quality,
user-study, operational, authority, and cohort gates above. Passing this plan
does not confer legal, privacy, security, source, academic, finance, frame, or
release approval.

## 26. Decision Ledger: 34 Settled Product Decisions

| ID | Decision and concrete default | Owner / non-waivable boundary | Revisit trigger |
|---|---|---|---|
| R1-Q1 | One product, independently gated Stages 0-4; job pipeline separately governed | PM scope; tech architecture | Independent customers, scale, or isolation evidence |
| R1-Q2 | Primary persona has a current roadmap/recommendation; explanation first | PM | Primary journey fails value study |
| R1-Q3 | Stage 2 is read-only and continues only on the 20-user crossover gates | PM + research protocol | Locked study evidence |
| R1-Q4 | Model explains only; backend owns readiness, prerequisites, scoring, ranking, slots; qualitative scores only | PM + recommendation owner; deterministic authority non-waivable | New reviewed product decision |
| R1-Q5 | LinkedIn is authorization-only; use pinned taxonomy and rights-checked postings first | Legal/source authority exclusive for exception | Written LinkedIn authorization |
| R1-Q6 | Text/PDF only, no fetch, provenance declaration, reject LinkedIn/ambiguous origin | PM UX; legal exception exclusive | Approved narrower rights boundary |
| R1-Q7 | Pilot token is deployer-managed server secret; BYOK disabled | DevOps/security; secret safety non-waivable | Validated BYOK need and custody review |
| R1-Q8 | Deterministic parsing/validation first; model only for unresolved prose; one repair | PM behavior + tech integrity | Evidence shows another bounded policy is safer |
| R1-Q9 | Preserve required/preferred/optional/unclear/negated/conflicting/ambiguous/unmapped/unknown; one clarification | PM | Calibrated evidence for a new inference class |
| R1-Q10 | Reviewed internal registry bridges pinned O*NET/ESCO/ISCO and six seed IDs; auto-map at proposed 98% precision | Data/domain and academic owners exclusive in their domains | Reviewed expansion evidence |
| R1-Q11 | Private analysis on demand; shared collection scheduled only after approval; one governed pipeline | Source/legal approval non-waivable | Source contract requires separate handling |
| R1-Q12 | Freshness is explicit; supplied posting observed at upload; source-specific SLA; provisional 24h/6h targets | Data/source owner | Contract, rate limits, or measured behavior |
| R1-Q13 | Fallback first; one call + repair; 1s fallback p95, 4s/8s model p50/p95, 10s timeout, token/cost/budget caps | PM/finance/tech | Provider evidence before results inspection |
| R1-Q14 | Minimum structured payload, no persistent chat; successful private data one hour, interrupted 24h, metadata 30d | Privacy/security; deletion and isolation non-waivable | Approved durable-tenancy design |
| R1-Q15 | Hard provenance/precision/safety/fallback/deletion gates and locked strata; pause on failure | Relevant domain owners; critical stops non-waivable | Predeclared calibrated gate change |
| R2-Q1 | Exact six intents, deterministic routing, one ambiguity clarification, else `unsupported_intent` | PM scope + tech implementation | New evaluated intent decision |
| R2-Q2 | Immutable answer/snapshot/claim/locator/hash identity; no citation rebinding | PM contract + source/privacy retention | No planned relaxation |
| R2-Q3 | Missing/revoked token degrades to deterministic-only; provisional 5-in-60s/5m breaker; operator restores | DevOps/security; fallback non-waivable | Operations evidence supports tuning |
| R2-Q4 | One versioned provider adapter; model/provider/region changes require locked shadow replay | PM/tech/privacy/security/finance/release | Continuity or procurement need |
| R2-Q5 | Posting origin must be allowed category plus non-LinkedIn confirmation; declaration is not legal warranty | PM UX; legal/source exception exclusive | Written exception or provider approval |
| R2-Q6 | Item state machine plus posting terminal state; one repair and one user clarification | PM behavior + tech integrity | Evaluated need without weaker evidence |
| R2-Q7 | Named mapping reviewers, versioned evidence, disclosed denominators; no broad gap summary | Academic/data owners exclusive | Predeclared representative coverage gate |
| R2-Q8 | Server analysis ID; delete successful raw/derived together in one hour, immediate on request, interrupted in 24h | Privacy/security; selective deletion/tenancy non-waivable | Approved persistence design |
| R2-Q9 | Adapter owns source semantics; ingestion owns jobs; scheduler registered pairs only; data/source owner publishes | Tech/data/source/legal | Authorized collection architecture evidence |
| R2-Q10 | Ranking requires separate deterministic shadow proposal and all entry/exit gates; static fallback | Recommendation/legal/release approvals non-waivable | Successful read-only and coverage evidence |
| R2-Q11 | Audit all high-risk/new cases plus provisional 10% random weekly; reduce after four clean cohorts | PM/evaluation/domain/security/privacy | Four clean cohorts or incident/drift |
| R2-Q12 | Test comprehension and over-trust; 80% each critical distinction, 5% max unsupported takeaways, repeat misconception blocks | Research/accessibility + PM continuation | Predeclared protocol revision |
| R2-Q13 | Evidence-bound cohorts, minimum five operating days and task sample; capabilities roll back independently | Release authority exclusive | Applicable cohort evidence |
| R2-Q14 | Content-free telemetry only; named owners/runbooks for auth, budget, circuit, deletion, validation, stale, queue alerts | Operational/domain owners | Separately approved replay store |
| R2-Q15 | Domain-specific approval matrix; no inferred approval or PM override of non-waivable stops | Each named authority | Recorded scoped approval/expiry |
| R3-Q1 | Stage 2 exact English/Singapore/entry-level-graduate/two-role alias allowlist; unsupported titles not coerced | PM scope; data/academic mapping owners | Reviewed alias/scope decision |
| R3-Q2 | Supplied-posting result and evidence expire together in one hour; no history/save/share/export | PM/privacy/legal/security/release | Approved durable rights/tenancy design |
| R3-Q3 | Item-level evidence only; no aggregate gap/fit/coverage/frequency/trend/demand claims | PM claim scope; academic/data/legal boundaries | Predeclared denominators, rights, thresholds, validation |
| R3-Q4 | `role_target` and `supplied_posting` pass, release, pause, and roll back independently | PM + research + release authority | Independent evidence for each mode |

## 27. Authority-Deferred Ledger

These are approvals, not unresolved product decisions. Absence, silence, or
another domain's approval does not imply consent.

| Authority | Deferred decision/evidence | Required record | Dependent capability |
|---|---|---|---|
| Legal/source owner | LinkedIn exception; first live source rights for acquisition, storage, derivatives, model use, display, attribution, retention, deletion | Scope, agreement/terms version, owner, decision time, expiry/revisit trigger | Any LinkedIn use or Stage 3 |
| Privacy/security | Provider/endpoint/region, payload, retention exceptions, authenticated tenancy, deletion proof, hostile-content controls, external-model use | Data flow, controls/tests, versions, decision time, expiry | Stage 1B, 2B, 3 |
| Finance/product sponsor | Provider and final spend ceiling | Pricing basis, budget, owner, decision time, revisit trigger | Stage 1B onward |
| Academic/recommendation owner | Course-skill links; later ranking formula, tolerances, academic-policy impact | Evidence excerpts, review/version; later formula and regression protocol | Stage 2 claims; Stage 4 |
| Data/domain/source owner | Aliases, taxonomy mappings, coverage denominators, snapshot publication | Mapping/publication version, evidence, owner, expiry | Stage 2/3/4 |
| Research/evaluation | Protocol, locked-set adequacy, confidence-aware interpretation | Preregistered tasks, samples, rubrics, analysis plan | Cohort continuation |
| Accessibility owner | Keyboard/screen-reader coverage and defects | Test protocol/results and decision | User-facing release |
| Tech lead/DevOps/security | Architecture, deterministic contracts, worker isolation, breaker tuning, operations proof | Design/tests/runbooks/versions | Each technical cohort |
| Release authority | Cohort progression, production go/no-go, rollback | Applicable approvals, gate evidence, scope, time, expiry | Any release |

Non-waivable release stops are source authorization, authenticated tenant
isolation for private multi-user data, selective deletion, secret safety,
deterministic fallback, and zero critical security failures.

## 28. Shape Handoffs

The next Shape phase may resolve implementation and interaction design only. It
must not broaden inputs, claims, persistence, authority, roles, source access,
model powers, or ranking effect.

### Product/interaction Shape

- Specify the six route entry points, clarification, unsupported-intent, and
  deterministic-fallback interactions.
- Design visual language for all claim/evidence states without hiding
  provenance or overwhelming the student.
- Prototype posting declaration, LinkedIn rejection, expiry/delete, unsupported
  role, non-registration readiness, and exposure-not-mastery copy.
- Define citation detail, unavailable evidence, mode-specific rollback, and
  accessibility behavior.

### Technical Shape

- Decompose request/response, claim/citation, immutable snapshot, extraction
  state, and deletion transaction schemas.
- Place context builders, policy checks, provider adapter, skill registry, and
  future ingestion boundaries within the layered FastAPI architecture.
- Specify deterministic route selection, validation, replay, provider circuit,
  budgets, kill switches, and content-free telemetry.
- Design fixture/annotation/replay tooling and proof for no ranking mutation,
  tenant scope, selective deletion, source publication, and rollback.

### Evaluation and operations Shape

- Preregister per-mode locked tasks, rubrics, strata, sample sizes, critical
  distinctions, and confidence-aware analysis.
- Define dashboards, alert thresholds, responders, runbooks, audit records, and
  capability-specific cohort evidence packages.
- Fix provisional effect-size, non-inferiority, coverage, and ranking tolerances
  before observing candidate results.

## 29. Provenance and Completion Note

This plan reconciles the brief, three grilling rounds, planner responses, Final
Frontier Certificate, repository analysis, extraction/operations research,
LinkedIn access research, security constraints, and citation audit.

- Grilling rounds: **3**
- Settled product decisions: **34**
- Final product frontier: **empty**
- Citation audit: **117 verified**, **10 corrected planner-safe**, **46 blocked**
- Blocked claims used as external facts in this plan: **0**

Planning is complete. This document is **not frame-approved, not shape-ready,
not implemented, and not released**. Shape work begins only after the parent
orchestrator accepts this handoff and preserves the authority boundaries above.
