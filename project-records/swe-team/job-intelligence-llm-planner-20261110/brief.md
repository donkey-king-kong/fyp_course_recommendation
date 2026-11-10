# Product Brief: Grounded Course Assistant and Job-Market Intelligence

**Flow ID:** `swe-product-manager`  
**Parent:** parent orchestrator  
**Status:** planning proposal only; not product, legal, privacy, security, source, or release approval  
**Scope:** (A) a grounded assistant for course recommendations and (B) evidence-backed job intelligence  
**Evidence cutoff:** research supplied for this planning run, verified on 2026-11-10

## 1. Executive Decision

Build **B as a staged companion capability within the course-recommendation
product**, not as a user-visible separate service and not as part of the LLM
itself.

- A and B share one user journey and one canonical skill bridge.
- B has a separate governed evidence pipeline, source-policy boundary, versioned
  snapshots, and kill switch.
- In the current FastAPI monolith, B should begin as a bounded domain/service.
  A separately deployed ingestion worker becomes warranted only when live,
  scheduled, or rendered-source ingestion is authorized and operational
  isolation is needed.
- B is **read-only context in the first user release**. It may explain how
  observed job skills relate to existing recommendations, but it does not
  change eligibility, prerequisite results, exact-slot assignment, or ranking.
- Any later market-informed ranking must be deterministic, independently
  evaluated, reversible to the static mapping, and outside LLM authority.

**LinkedIn-first decision:** LinkedIn is a business-development track, not an
MVP data source. Creating a developer app provides the documented self-service
Open Permissions; job-search inventory retrieval is not among those
permissions. The Job Posting API documentation describes outbound posting and
does not document a read/search endpoint; Apply Connect documentation describes
an ATS posting-and-application workflow and does not document a general
job-search feed. LinkedIn also prohibits unauthorized scraping and automated
collection. [V: LA005, LA008, LA011, LA017, LA019-LA022, LA027-LA031]

The product must not scrape LinkedIn, automate logged-in sessions, buy
LinkedIn-derived scraped datasets, or ingest LinkedIn content indirectly.
Reconsider only after written authorization covers this product's collection,
storage, derived skills, model processing, display, retention, and deletion.

**Compliant MVP fallback:**

1. Use version-pinned O*NET and/or ESCO occupational reference data for role
   exploration; these sources expose occupational/classification data, not
   live-vacancy feeds. [V: LA040-LA043, EO019-EO024]
2. Accept a user-supplied job description only for private, on-demand analysis
   when the user confirms they may provide it and it is not identified as
   LinkedIn-derived; do not fetch its URL, republish its text, or train on it.
3. Add live advertisements only after a provider agreement expressly permits
   the intended commercial use, retention, attribution, derivatives, LLM
   inference, and deletion. Adzuna offers authenticated search; USAJOBS offers
   U.S. federal job search; employer-scoped Greenhouse and Lever endpoints can
   supply published jobs within their documented scope. [V: LA033-LA039]
4. If no provider grants the necessary rights, ship taxonomy-backed role
   context and rights-checked supplied-posting analysis without claims about
   current market frequency or trends.

## 2. Problem, Users, and JTBD

### Primary persona

An NTU computing student who has uploaded a curriculum/transcript, selected a
career goal, and received deterministic course recommendations, but cannot
readily understand:

- why a course was assigned to a particular slot;
- which prerequisites or standing rules matter;
- what evidence supports the recommendation;
- how two choices trade off;
- how a target role or job posting relates to the recommended pathway.

### Secondary persona

A prospective or returning student exploring the catalog without a complete
profile, who needs course and prerequisite explanations but must not receive
personalized claims unsupported by profile data.

### Jobs to be done

1. **When I see a recommendation,** explain why it was selected, what would
   change it, and what limitations apply so I can make an informed choice.
2. **When a course is locked or a prerequisite is proposed,** show the exact
   dependency and distinguish planning readiness from registration eligibility.
3. **When comparing courses,** separate catalog facts, backend recommendation
   evidence, and generated interpretation.
4. **When I have a role target or job posting,** identify explicit required and
   preferred skills, preserve the evidence, and show which reviewed course-skill
   links may address them.
5. **When evidence is missing or contradictory,** say what is unknown and give
   the next useful action instead of guessing.

## 3. Product Promise

> Explain the student's current course recommendations and roadmap using the
> product's own deterministic evidence, then contextualize them against a
> rights-permitted role or job posting without inventing course facts, job
> requirements, mastery, eligibility, or outcomes.

The model may summarize, compare, translate, and explain supplied evidence. It
may not create facts, treat occupational norms as employer requirements, alter
the deterministic recommendation result, waive prerequisites, or claim that a
student is employable or registration-eligible.

## 4. Evidence and Assumptions

### Repository evidence

The current product already exposes deterministic curriculum, transcript,
roadmap, readiness, recommendation, open-slot, score-component, and career
evidence data. It has a narrow Software Engineer/Data Engineer course-skill
preview covering seven courses and six stable skill IDs. It does not have a job
pipeline, assistant endpoint, conversation store, authenticated student entity,
or model evaluation harness. Browser profile and transcript state is
user-controlled prototype data. [Repository analysis: `repo-analysis.md`]

### Verified external evidence used

- JSON-LD can contain arrays, graphs, and context-dependent terms; extraction
  cannot assume one flat object. Schema.org defines job fields but does not
  require publishers to populate or type them. [V: EO005-EO010, EO016-EO018]
- Structured outputs can constrain response shape; application and evidence
  validation are still required. [V: EO014-EO015, EO030-EO032]
- Remote content can carry indirect prompt injection; it must remain untrusted,
  separated from instructions, validated at tool boundaries, and handled with
  least privilege. [V: EO033-EO034]
- O*NET, ESCO, and ISCO provide distinct occupation/skill classification roles
  and versioned identifiers. [V: EO019-EO027]
- Provenance, canonical hashing, conditional requests, and source lifecycle
  signals have standards support. [V: EO036-EO048, EO056-EO057]
- API keys should stay out of clients and repositories; secret handling should
  use centralized, least-privilege controls with monitoring and rotation.
  [V: EO074-EO075]

`citation-verification.md` is authoritative. No claim blocked by that report is
used as external fact. All numeric targets below are proposed product gates,
not measured performance or source claims.

### Assumptions requiring validation

- The pilot remains focused on Software Engineer and Data Engineer pathways.
- Users value explanation and evidence before market-informed reranking.
- A provider and model processor can be found with acceptable commercial,
  privacy, retention, and derivative-use terms.
- The current course-skill ledger can be expert-reviewed and expanded without
  weakening evidence quality.
- A useful assistant can operate on reduced structured profile facts rather
  than raw curriculum/transcript files.

## 5. Information Classes and Authority

Every answer and API object must classify claims into one of these types:

| Class | Definition | Authority | Required presentation |
|---|---|---|---|
| `catalog_fact` | Course code, title, AU, description, level, prerequisites, seeded offering metadata | Catalog/database snapshot | Source, version/freshness, exact field; qualify seeded offerings as non-live |
| `deterministic_recommendation_fact` | Assigned slot, source, readiness, score component, evidence path, open-slot reason | Existing backend response | Name the deterministic service/result version; model cannot modify |
| `job_evidence` | Exact employer/provider statement from a permitted snapshot | Source snapshot | Exact quote/locator, source, observed time, required/preferred/unclear |
| `normalized_skill_inference` | Mapping from a source mention to a canonical skill | Versioned mapper/taxonomy | Preserve raw mention, mapping status, taxonomy/version, confidence reason |
| `generated_advice` | Model synthesis, comparison, questions, or suggested next step | No factual authority | Label as generated; cite every factual premise; never presented as a source fact |

Additional distinctions:

- Browser-entered preferences and completion checks are **user-supplied**.
- Transcript parser outputs are **transcript-derived**, not verified records.
- Course-skill links indicate reviewed **likely exposure**, not mastery.
- Roadmap `available` and recommendation `ready` are **implemented planning
  checks**, not registration permission.
- O*NET/ESCO occupation data is **external enrichment**, never evidence that an
  individual employer required a skill.

Conflict rule: deterministic source records remain visible even when generated
advice disagrees. The assistant must retract or refuse the generated claim; it
must never rewrite the source record.

## 6. Scope and Staging

### Stage 0: Contract and deterministic assistant stub

- Define the claim/citation contract and supported intents.
- Build fixture-based context assembly and deterministic response templates.
- Review the canonical skill registry and existing course-skill evidence.
- No external model, live fetch, scheduled ingestion, or BYOK.

### Stage 1: Grounded assistant MVP (A)

- Read-only explanations of current recommendations, roadmap readiness,
  prerequisites, open slots, catalog facts, and supported pilot skills.
- Comparison of already-returned recommendations.
- Model synthesis only over bounded structured context.
- Deterministic fallback for every supported intent.
- No persistent conversation, mutations, ranking changes, or raw-document
  transfer to the model.

### Stage 2: Job-context companion MVP (B)

- Structured role target backed by pinned O*NET/ESCO data.
- Rights-checked pasted/text-file posting analysis, excluding LinkedIn-derived
  content and arbitrary URL fetching.
- Explicit requirement extraction, normalized skill candidates, course-skill
  bridge, and evidence-backed contextual explanation.
- No live market frequency/trend claims and no recommendation reranking.

### Stage 3: Permitted shared market snapshots

- One contract-approved source and tightly bounded role/geography/seniority
  query.
- Scheduled, versioned shared snapshots with source-specific retention,
  attribution, deletion, freshness, deduplication, and kill switches.
- Read-only market context alongside unchanged recommendations.

### Stage 4: Evaluated deterministic market integration

- Market evidence may modify deterministic role-skill weights only after a
  separate product decision, offline comparison, regression review across
  existing careers, user-facing change explanation, and static fallback.
- The LLM remains an explainer, not a ranker.

### Non-goals

- LinkedIn scraping, browser automation, or LinkedIn-derived third-party data.
- Salary prediction, hiring probability, employability score, or guaranteed
  career outcome.
- Autonomous course selection, profile mutation, prerequisite waiver, or
  registration action.
- Full degree audit, timetable/vacancy checks, live offering guarantees, or
  undocumented eligibility inference.
- Inferring mastery from completion or course descriptions.
- General web search, unrestricted URL ingestion, or a model-operated browser.
- Market trends without authorized longitudinal data and publishability gates.
- Model training/fine-tuning on student or provider content.
- BYOK in the initial release.

## 7. Input Modes

| Mode | MVP stage | Inputs | Boundary |
|---|---:|---|---|
| Current recommendation question | 1 | Message plus bounded current result IDs/snapshot | Current deterministic result only |
| Roadmap/prerequisite question | 1 | Message plus roadmap/readiness snapshot | Planning status, not registration eligibility |
| Course/catalog question | 1 | Course code(s), optional anonymous mode | Catalog snapshot only |
| Recommendation comparison | 1 | Two or more returned recommendation IDs | No unreturned alternative invented |
| Role target | 2 | Pilot role, geography, seniority, optional preferences | Pinned taxonomy context; no live-market claim |
| Supplied posting | 2 | Pasted text or text/PDF upload, provenance declaration | No URL fetch; reject known LinkedIn origin; private analysis |
| Approved source record | 3 | Provider/source record ID | Shared permitted snapshot only |
| URL refresh | Later | Allowlisted source URL | Same governed pipeline; never arbitrary or LLM-selected |

Raw transcript/curriculum PDFs, student ID, recruiter/member data, unrelated
browser state, credentials, and full conversation history are excluded from
model input by default.

## 8. End-to-End Flows

### Flow A1: Explain a recommendation

1. User selects a current recommendation and asks “Why this course?”
2. Backend resolves the current deterministic recommendation snapshot.
3. Context builder selects assignment, source (`career`/`interest`), slot,
   reason, readiness, prerequisites, top evidence path, catalog facts, and
   freshness.
4. Policy layer marks each field by information class.
5. Deterministic template creates a fallback answer.
6. Model may transform that evidence into plain language.
7. Validator checks that all factual sentences resolve to supplied claim IDs.
8. UI renders answer, inline citations, fact-type labels, limitations, and
   fallback if validation/model call fails.

### Flow A2: Explain readiness or prerequisites

1. User asks why a course is locked/available or what must come first.
2. Backend reads roadmap readiness and prerequisite edges/text.
3. It distinguishes completed, earlier planned, missing, standing-related, and
   unknown requirements.
4. Assistant explains the implemented branch and states that co-requisites,
   live offerings, timetable, vacancies, cohort rules, and registration
   permission may be outside coverage.
5. Conflicting or unparsable prerequisite evidence produces “uncertain” and a
   catalog/advisor next step, never a waiver.

### Flow A3: Compare recommendations

1. User chooses existing recommendations.
2. Backend returns a comparison matrix of slots, prerequisites, readiness,
   source, reviewed skill links, and catalog facts.
3. Model summarizes explicit tradeoffs without declaring a universally best
   course.
4. The answer identifies which preference or constraint would change the
   decision but does not change it.

### Flow B1: Explore a role target

1. User chooses a supported role, geography, and seniority band.
2. System resolves a pinned occupation/taxonomy version and shows the match or
   ambiguity.
3. It retrieves taxonomy skill relationships as external enrichment.
4. Skill bridge maps canonical skills to reviewed course-skill evidence.
5. Assistant explains possible pathway relevance, explicitly stating that the
   taxonomy is not a live posting and does not establish employer demand.

### Flow B2: Analyze a supplied posting

1. User supplies text/file and declares source/provision rights.
2. System rejects known LinkedIn origin and unsupported/binary/oversized input.
3. Malware/content checks and deterministic parsing run first.
4. Parser extracts typed fields, headings, lists, explicit requirement spans,
   and source offsets.
5. Bounded LLM extraction handles only unresolved requirement-bearing prose.
6. Application validates schema, evidence quotes/offsets, modality, negation,
   candidate-facing status, and conflicts.
7. Mapper proposes canonical skill candidates while preserving raw mentions.
8. Low-confidence or conflicting items remain ambiguous/unmapped.
9. Skill bridge shows reviewed course links and gaps.
10. Assistant contextualizes current recommendations without reranking them.
11. Raw input expires under the private-analysis retention policy; the user can
    delete it immediately.

### Flow B3: Use an approved live source

1. Scheduler or user request creates an idempotent ingestion job for an
   allowlisted policy/query.
2. Source policy is checked before network access.
3. Authorized feed/API is preferred; fetch runs with source quotas and
   isolation.
4. Snapshot, assertions, normalized entities, provenance, dedup cluster, and
   lifecycle state are versioned separately.
5. Shared role snapshot is published only if quality and sample gates pass.
6. Assistant cites the published snapshot version and observation window.
7. If stale, withdrawn, or disabled, UI falls back to the last permitted static
   role evidence or says current market evidence is unavailable.

## 9. Functional Requirements

### P0: Grounded assistant

- `A-R1` Support intents: recommendation explanation, readiness/prerequisite
  explanation, course facts, current-result comparison, open-slot explanation,
  and pilot skill exposure.
- `A-R2` Assemble context server-side from narrow service-owned builders; do
  not submit localStorage wholesale.
- `A-R3` Generate and return deterministic fallback text before any model call.
- `A-R4` Attach stable claim IDs, source type, version, freshness, and locator
  to every factual premise.
- `A-R5` Validate generated factual sentences against supplied claims; on
  failure, serve the fallback and record a sanitized validation event.
- `A-R6` Preserve existing recommendation, readiness, and prerequisite outputs
  exactly. The assistant has no mutation/admin tools.
- `A-R7` Show user-supplied, transcript-derived, seeded, reviewed, normalized,
  and generated labels distinctly.
- `A-R8` Expose limitations relevant to the question, not a generic disclaimer
  wall.
- `A-R9` Treat unknown, stale, conflicting, and unsupported as first-class
  states.
- `A-R10` Require explicit confirmation before any future preference change;
  confirmation triggers the existing deterministic recalculation flow.

### P0: Job-context companion

- `B-R1` Support only approved pilot roles, geographies, seniority bands, and
  source modes.
- `B-R2` Separate immutable source snapshot, raw source assertions, normalized
  entities, derived decisions, and generated advice.
- `B-R3` Require exact evidence text and stable locator for every accepted
  posting requirement.
- `B-R4` Preserve required, preferred, optional, unclear, negated, alternative,
  and conflicting modality.
- `B-R5` Represent absent information as unknown, never “not required.”
- `B-R6` Preserve raw skill mentions; normalization may be exact, alias,
  broader, narrower, ambiguous, or unmapped.
- `B-R7` Pin taxonomy and mapper versions and support replay.
- `B-R8` Connect normalized job skills only to reviewed canonical course-skill
  evidence. No prompt-only mappings.
- `B-R9` Keep market context read-only during MVP; no score/rank/slot changes.
- `B-R10` Reject LinkedIn URLs/content and all unapproved source acquisition.

### P1: Governed live snapshots

- Source-policy registry and pre-fetch decision.
- Authorized API/feed client with source-specific quotas and attribution.
- Idempotent scheduled and on-demand jobs using one pipeline.
- Conditional refresh where supported, lifecycle state, version history,
  conservative deduplication, selective purge, and source kill switch.
- Publishability gates for sample sufficiency, quality, freshness, and
  representativeness.

## 10. Conversation and Refusal Behavior

The assistant should be concise, answer-first, and evidence-forward:

1. Answer the supported part.
2. Cite factual premises at sentence or bullet level.
3. State the material limitation.
4. Offer a bounded next action.

It must refuse or narrow requests that:

- ask it to invent prerequisites, course content, job requirements, salary,
  demand, mastery, employability, or eligibility;
- ask it to override backend ranking, slot assignment, or prerequisite logic;
- request scraping, login automation, access-control bypass, or analysis of
  LinkedIn-derived content;
- request secrets, system prompts, hidden instructions, another user's data,
  or admin/source-policy actions;
- require stale or absent evidence to be presented as current;
- ask for discriminatory ranking or sensitive-trait inference.

Refusal pattern:

> I cannot establish **[claim/action]** from the available evidence. I can
> instead **[supported action]** using **[named source/state]**.

The assistant must not repeat hostile embedded instructions, auto-render remote
images/links, or place untrusted content in citations/tool arguments.

## 11. Grounding and Citation Contract

Each answer returns:

- `answer`;
- `claims[]` with ID, class, exact value, source, locator, version, observed
  time, and confidence reason;
- `citations[]` mapping answer spans to claim IDs;
- `limitations[]`;
- `freshness`;
- `fallbackAnswer`;
- `generated=true|false`;
- optional `proposedAction` with `confirmationRequired=true`.

Citation rules:

- Catalog and deterministic facts cite structured record fields/result IDs.
- Job requirements cite exact quote plus JSON pointer, feed field, page/line,
  or normalized-text offsets.
- Normalized skills cite both raw mention and mapper/taxonomy version.
- Generated advice cites all factual premises and never cites itself.
- Taxonomy enrichment is visually distinct from employer evidence.
- A citation must resolve at display time; inaccessible/expired evidence yields
  an unavailable state, not an unlinked claim.
- Source text may be displayed only where source terms permit it.

## 12. Parser and Model Responsibilities

### Deterministic components own

- source policy, network metadata, and retrieval;
- JSON-LD processing, microdata/RDFa, feed/API fields, headings, list
  boundaries, dates, URLs, quantities, and identifiers;
- evidence offsets and quote matching;
- schema, enum, range, negation, and cross-field validation;
- hashes, dedup candidates, versions, freshness, and lifecycle transitions;
- tenant/policy checks, budgets, tool permissions, and write authorization;
- existing course eligibility, prerequisites, ranking, and slot allocation.

### LLM components may

- classify ambiguous prose sections;
- split prose into atomic candidate-facing requirements;
- interpret required/preferred/unclear modality from local evidence;
- resolve local pronouns/coordinated clauses;
- propose taxonomy candidates;
- explain, summarize, compare, and translate validated claims.

### LLM components may not

- browse or fetch URLs;
- receive credentials or raw student documents;
- infer missing numbers, proficiency, degree equivalence, authorization,
  geography, or employer intent;
- turn responsibilities/company technology into candidate requirements without
  explicit evidence;
- write source records, approve mappings, mutate preferences, or call admin
  endpoints;
- decide course eligibility, prerequisite satisfaction, ranking, or slot
  allocation.

## 13. Missing, Vague, and Non-Actionable Fallback Ladder

Stop at the first level that produces supported, useful output:

1. Return exact deterministic/catalog fact.
2. Return exact job assertion with evidence.
3. Return normalized skill with explicit mapping status.
4. Return raw vague requirement without invented level/quantity.
5. Present conflicting assertions side by side.
6. Ask one targeted clarification when user input can resolve ambiguity.
7. Use pinned taxonomy enrichment, labelled as non-employer context.
8. Show “unmapped” or “no reviewed course link.”
9. Suggest a concrete human/source check.
10. Abstain when no actionable evidence remains.

Examples:

- “Strong Python” remains an explicit text requirement; no proficiency level is
  invented.
- No degree statement becomes “degree requirement unknown,” not “no degree
  required.”
- A skill with no reviewed course mapping remains a market/job gap in the
  evidence graph, not a new course recommendation.
- A course with no reviewed skill evidence remains unknown, not irrelevant.

## 14. Canonical Taxonomy and Current-Repo Mapping

Create one canonical skill registry that bridges:

```text
source mention
  -> canonical skill ID
  -> taxonomy mappings/version
  -> role/job evidence
  -> reviewed course-content evidence/depth
  -> deterministic recommendation tag/skill area
```

Seed, but do not broaden without review, the six stable pilot IDs already used:

- `programming-foundations`
- `software-engineering-practice`
- `software-delivery-management`
- `data-storage`
- `distributed-systems`
- `cloud-service-platforms`

Mapping decisions:

- O*NET-SOC: U.S. occupation anchor.
- ESCO: EU/multilingual occupation and skill concepts.
- ISCO-08: international occupation roll-up.
- Internal canonical registry: vendor/product aliases and the bridge to current
  recommendation tags and course evidence.
- Separate vocabulary: degrees and credentials.

Occupation-level expectations can expand search or provide context only. They
must never be converted into requirements for an individual posting.

## 15. Freshness, Deduplication, and Versioning

### Version every transformation

Record source snapshot hash, source-policy version, parser, prompt, schema,
model, mapper, taxonomy, course-skill ledger, recommendation result, and
publication version. A changed component creates a new derived version; it does
not silently overwrite prior assertions.

### Freshness

- Supplied posting: observed at upload; no claim that it remains open/current.
- Taxonomy: display pinned release/version.
- Live source: display observed time, evidence window, and lifecycle state.
- Stale/unavailable data cannot support “current” or trend wording.
- Proposed starting service targets: refresh active authorized feeds daily,
  accelerate near explicit expiry, and publish a stale warning after the
  source-specific SLA. These are product targets to validate, not sourced
  facts.

### Deduplication

Use source identifiers and requisition keys first, canonical content hash
second, and similarity only to generate review candidates. Never merge solely
on title, canonical URL, or semantic similarity. Retain all source members,
versions, and an unmerge path. Optimize against over-merging.

### Lifecycle

Track discovered, active, possibly stale, expired, unavailable, reactivated,
and tombstoned. Preserve closure reason and last observation. A transient
failure or access denial is not proof of closure.

## 16. On-Demand vs Scheduled Recommendation

Course recommendations remain on-demand through the existing deterministic
endpoint.

- Chat can explain a stored/current result.
- A future confirmed preference change invokes the existing deterministic
  recommendation flow and creates a new result version.
- Chat itself never recalculates with hidden parameters.

Job evidence:

- Supplied-posting analysis is on-demand and private.
- Shared market snapshots are scheduled by approved role/query windows.
- On-demand source refresh, if later enabled, uses the same source policy,
  quotas, parser, provenance, deduplication, and lifecycle logic as scheduled
  ingestion.
- Concurrent requests coalesce; ordinary users cannot create cron expressions,
  bulk URL jobs, or arbitrary query fan-out.

## 17. BYOK UX and Custody

### MVP decision

BYOK is disabled. Use a platform-managed server credential only after provider,
privacy, secret-management, budget, and release gates are met. The browser
never receives the key and never calls the model provider directly.

### Future options, in product preference order

1. Provider delegated authorization/OAuth with revocable narrow scope.
2. Customer-managed vault reference with narrow runtime access.
3. Dedicated backend secret submission, tenant-scoped envelope encryption, and
   immediate delete/replace.
4. Explicit session-only server memory with short expiry and no persistence.

Future UX requirements:

- Secret entry occurs in an isolated credential screen, never chat.
- No analytics, replay, URL, cookie, localStorage, support ticket, or ordinary
  configuration capture.
- Show provider, status, creation time, scope, and non-sensitive fingerprint
  only; never return the key.
- Plainly disclose that a stored key can be decrypted and used by the service;
  encryption at rest is not end-to-end secrecy.
- Provide immediate revoke/replace and a secret-free audit record.

## 18. Source Acquisition and Policy

Source priority:

1. Contract-approved publisher/provider API or feed.
2. Employer-authorized Greenhouse/Lever scope.
3. USAJOBS where U.S. federal coverage fits.
4. O*NET/ESCO/ISCO taxonomy enrichment.
5. Rights-checked supplied text/file for private analysis.
6. Abstain.

Before any live source, the policy registry must record approved host/path,
purpose, owner, terms version, robots result where applicable, authentication,
rate limits, allowed fields, attribution, raw/derived storage, model use,
training prohibition, retention, deletion, and review expiry.

Fail closed when policy is absent, expired, conflicting, or indeterminate.
There is no general-purpose fetcher and no model-selected URL.

## 19. Privacy, Retention, and Deletion

- Minimize model payload to course codes, aggregate AU where needed, explicit
  result facts, and selected evidence. Do not send student ID, raw PDFs,
  grades unless essential, recruiter/member data, or unrelated history.
- Keep conversation persistence off until authenticated server identity,
  tenant scoping, deletion, and export are designed.
- Supplied posting raw text: proposed default is session processing plus
  deletion within 24 hours; offer immediate deletion. Validate against the
  source and processor terms before release.
- Generated answer/model telemetry: retain only sanitized operational metadata
  by default; raw replay requires a separate purpose, access policy, and expiry.
- Shared snapshots: retain only fields and durations permitted by source
  policy; support source-level selective purge and re-derivation.
- Do not train on student, posting, provider, or conversation data.
- Browser data remains user-controlled and must never be represented as an
  authoritative academic record.
- Production personalization requires authenticated server identity and
  server-derived tenant scope; browser `studentId` is not an authorization key.

## 20. Abuse, Security, and Cost Controls

- Treat all external/uploaded text and model output as untrusted.
- No secrets, network, database, shell, write, admin, or arbitrary tools for
  the model.
- Strict input/output size, token, latency, model, tool-step, and retry caps.
- Per-user, tenant, IP, source, model, daily, and monthly budgets before calls.
- Cache only by non-sensitive, tenant-safe keys; never mix student history into
  shared caches.
- One bounded repair for schema-invalid output; unsupported semantics abstain
  rather than retry with leading prompts.
- Sanitized metrics for calls, refusals, cache hits, validation failures,
  tokens, cost, and latency; no prompt/response bodies in general logs.
- Kill switches for model, provider/model version, ingestion, source, schedule,
  on-demand fetch, rendering, BYOK, mutations, and market-informed ranking.
- Deterministic fallback remains available during provider outage, budget
  exhaustion, bad rollout, or source withdrawal.

## 21. Evaluation Plan

### Evaluation sets

- Grounded assistant questions spanning each supported intent and each fact
  class.
- Recommendation/readiness cases with known deterministic outputs.
- Job fixtures stratified by structured data, static prose, PDF, missing,
  vague, conflicting, negated, and malicious content.
- Skill mappings split by source/template/time to avoid leakage.
- Adversarial cases: indirect prompt injection, citation spoofing, hostile
  Markdown, system-prompt requests, cross-user IDs, source poisoning, and
  exfiltration links.

### Measures

- factual claim support and citation resolution;
- contradiction with deterministic state;
- unsupported-claim rate;
- exact requirement span precision/recall;
- required/preferred classification;
- taxonomy mapping precision and abstention quality;
- course-skill bridge coverage with unknowns retained;
- refusal correctness;
- deterministic fallback equivalence;
- user task success and explanation usefulness;
- p50/p95 latency, token use, cost, timeout, and fallback rates;
- freshness, dedup over-merge, deletion propagation, and source-policy
  enforcement for live snapshots.

Human review is primary for usefulness and factual support. Automated
LLM-as-judge metrics may supplement but cannot approve release.

## 22. Measurable Acceptance Criteria

All values are proposed gates to challenge and calibrate; none are measured
results.

1. **Claim provenance:** 100% of displayed factual claims have a valid class,
   source ID, version, and resolvable locator.
2. **Deterministic integrity:** 0 assistant-caused changes to recommendation,
   prerequisite, readiness, score, or slot records across contract tests.
3. **Grounding:** at least 99% factual-claim precision on the locked assistant
   set; unsupported claims trigger fallback.
4. **Citation validity:** at least 99.5% of citations resolve to the exact
   displayed premise.
5. **Eligibility boundary:** 100% of readiness/eligibility answers include the
   relevant planning-vs-registration limitation.
6. **Skill boundary:** 100% of transcript/course skill answers use
   exposure/unknown language and never mastery language.
7. **Fallback:** every P0 intent has a deterministic answer or explicit
   evidence-based abstention when the model is unavailable.
8. **Requirement support:** at least 99% precision for required vs preferred
   accepted claims; every accepted item has exact evidence.
9. **Unsupported requirements:** no more than 0.5% on the locked fixture set.
10. **Mapping:** automatic skill mapping is enabled per category only after at
    least 98% precision on its locked set; otherwise ambiguous/unmapped.
11. **LinkedIn control:** 100% of known LinkedIn URLs/origins are rejected; no
    automated LinkedIn request occurs in tests or telemetry.
12. **Prompt injection:** 100% of critical adversarial fixtures fail to alter
    tools, policy, ranking, citations, tenant scope, or instructions.
13. **Secret safety:** 0 full credentials, raw tokens, database URLs, prompt
    bodies, or source payloads in logs/traces/error exports.
14. **Privacy minimization:** 0 raw transcript/curriculum PDFs or student
    identifiers sent to the model in integration tests.
15. **Deletion:** user-supplied posting and derived private records are
    selectively deleted within the stated SLA and become inaccessible.
16. **Dedup:** at least 99.5% pair precision before automatic shared-snapshot
    merge; uncertain pairs remain separate.
17. **Freshness:** 100% of job/taxonomy views show observation/release version
    and stale state.
18. **Cost:** hard budget exhaustion prevents a provider call and serves
    fallback; no retry amplification beyond the configured cap.
19. **Latency:** Stage 1 p95 is at most 8 seconds with model and 1 second for
    deterministic fallback under the agreed pilot load.
20. **Accessibility/content:** citations, limitations, loading, refusal, stale,
    and error states are keyboard- and screen-reader-operable.

## 23. Rollout Gates

### Gate 0: Planning to offline fixture prototype

- Supported intents, fact classes, canonical skill IDs, and deterministic
  authority are signed off by named product/technical owners.
- Only synthetic or legally retained fixtures; no live fetch or real student
  documents.

### Gate 1: Internal deterministic assistant

- Context and citation contracts pass.
- Existing recommendation outputs are unchanged.
- Adversarial and fallback tests pass.

### Gate 2: External model in controlled evaluation

- Provider/privacy assessment, minimum payload, retention behavior, server
  secret handling, budgets, logs, and kill switch are evidenced.
- Locked grounding evaluation meets gates.

### Gate 3: Supplied-posting pilot

- Rights declaration, LinkedIn rejection, upload handling, prompt-injection
  controls, retention, deletion, and private tenant scope pass.
- Canonical mappings and course-skill links have named reviewers.

### Gate 4: Live shared job snapshots

- Written source authorization and policy registry cover acquisition, storage,
  derivatives, LLM use, display, attribution, retention, and deletion.
- Ingestion isolation, quotas, provenance, freshness, dedup, purge, monitoring,
  and source kill switch pass.

### Gate 5: Market-informed deterministic ranking

- Separate product decision and evaluation show benefit without unacceptable
  regressions.
- Change is explainable, versioned, reversible, and does not alter prerequisite
  authority.

No gate implies legal, privacy, security, source, or release approval. Each
requires a named authority and recorded evidence.

## 24. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Unauthorized job source | Legal/operational shutdown | Contract gate, source registry, LinkedIn disabled, fail closed |
| Hallucinated course/job fact | Bad academic decision | Claim classes, exact citations, validator, deterministic fallback |
| LLM overrides eligibility/ranking | Product integrity failure | No relevant tools; backend authority; contract tests |
| Sparse course-skill evidence | False completeness | Pilot scope, unknown state, expert review, no prompt-only mapping |
| Taxonomy mismatch | Misleading skill bridge | Canonical registry, versions, raw mention, abstention |
| Prompt injection/poisoning | Exfiltration or policy bypass | Untrusted-data boundary, no tools/secrets, strict validation |
| Stale/duplicate jobs | Misleading “current” context | Observation windows, lifecycle, conservative dedup, stale labels |
| Browser state treated as verified | Trust/privacy failure | User-supplied labels, server identity before persistence |
| Provider retention/cost | Privacy/budget breach | Minimum payload, contract review, budgets, kill switch, fallback |
| Advice overconfidence | User misinterpretation | Generated label, tradeoffs, no optimality/employability claims |
| Separate pipeline complexity | Delivery delay | Stage B, one role/source first, logical boundary before deployment split |

## 25. Dependencies and Open Decisions

### Dependencies

- Reviewed course-skill ledger and canonical alias registry.
- Stable structured context builders over current backend services.
- Named owners for catalog, recommendation policy, taxonomy, source policy,
  privacy, security, and evaluation.
- Provider/source agreements and processor terms before live use.
- Authenticated server identity and tenant isolation before persistent
  conversations or private records.
- Fixture corpus, annotation guide, adjudication, and locked evaluation sets.
- Secret manager, budgets, audit, deletion workflow, monitoring, and kill
  switches before external calls.

### Open decisions

- Exact pilot geography, seniority, and role aliases.
- Whether supplied postings may persist beyond session processing.
- Which model/provider, endpoint, region, retention mode, and cost ceiling.
- Who reviews course-skill and job-skill mappings and within what SLA.
- Minimum live-snapshot sample/coverage needed for publishable aggregate claims.
- Whether score components may be exposed conversationally or only translated
  into qualitative reasons.
- Whether anonymous catalog chat is in Stage 1.
- The first contract-approved job provider.
- Whether future confirmed preference mutation is worth the added state and
  audit complexity.

## 26. Authority Decisions

| Decision | Product position | Required authority before execution |
|---|---|---|
| LLM role | Explain/transform only | Product + tech lead |
| Recommendation/prerequisite authority | Existing deterministic backend | Product + academic-domain owner |
| B shape | Staged companion with separate governed pipeline | Product + tech lead |
| LinkedIn | Disabled; future written-authorization track | Product/legal/source owner |
| Supplied posting | Private, rights-declared, non-LinkedIn, no fetch | Product/privacy/legal/security |
| Live source | Contract-gated and allowlisted | Product/legal/privacy/security |
| BYOK | Disabled in initial release | Product/security/privacy |
| Conversation persistence | Off initially | Product/privacy/tech lead |
| Market ranking | Off through Stage 3 | Product + recommendation owner |
| Taxonomy auto-map | Precision-gated, otherwise abstain | Data/domain owner |
| Release | Gates require named evidence; no implicit waiver | Designated release authority |

## 27. Decision Ledger

| ID | Decision | Rationale | Revisit trigger |
|---|---|---|---|
| D1 | B is a staged companion, not a standalone product | Shared user journey and skill bridge; separate evidence governance | Independent customers, scale, or isolation needs emerge |
| D2 | B has no ranking effect in MVP | Evidence and ontology are not yet mature; explanation is independently useful | Locked evaluation and explicit product decision |
| D3 | LinkedIn is not an MVP source | Documented permissions do not provide job-search inventory; automation is prohibited | Written LinkedIn authorization for exact use |
| D4 | MVP fallback uses taxonomy plus rights-checked supplied postings | Delivers role/posting context without unauthorized collection | Contract-approved live provider |
| D5 | Reject known LinkedIn-origin supplied content | Avoid indirect ingestion workaround | Written authorization/legal decision |
| D6 | Deterministic backend remains authoritative | Existing product contract and testable behavior | Never delegated to LLM; only backend policy may evolve |
| D7 | Generated advice is a separate claim class | Prevents synthesis from masquerading as evidence | No planned reversal |
| D8 | BYOK is deferred | Avoids premature customer-secret custody | Validated need and separate custody review |
| D9 | No persistent chat initially | No authenticated server student boundary exists | Identity, tenancy, deletion, and export are ready |
| D10 | One canonical skill registry bridges all evidence | Current pilot IDs, tags, taxonomies, and job terms otherwise drift | Registry proves inadequate under reviewed expansion |
| D11 | Exact evidence is required for accepted job requirements | Valid JSON alone does not establish factual support | No planned relaxation |
| D12 | Unknown/ambiguous beats inferred completeness | Reduces unsupported academic and job claims | Metrics support a reviewed bounded inference class |
| D13 | One governed pipeline serves scheduled/on-demand acquisition | Prevents on-demand policy bypass | Source contracts require physically separate handling |
| D14 | Market snapshots are shared, not per-student scrapes | Better provenance, cost, privacy, and comparability | A permitted source requires user-specific access |

## 28. Handoffs

### Designer

Design distinct visual treatment for the five claim classes, user-supplied
state, freshness, unknown/conflict, citations, deterministic fallback,
refusal, stale source, and confirmation. Resolve how much evidence is visible
inline versus on demand, how a user declares posting provenance, and how the UI
rejects LinkedIn without implying legal advice.

### Tech lead

Define bounded context builders, claim/citation schemas, canonical skill
registry, deterministic fallback, source-policy boundary, version model,
private-record tenant scope, and kill switches. Decide when live ingestion
requires a separately deployed isolated worker. Preserve current recommender
contracts and prove no model path can mutate ranking or eligibility.

### Griller: decisions to attack

1. Is rejecting all known LinkedIn-origin supplied text necessary and usable,
   or is there a narrower defensible private-analysis boundary?
2. Does taxonomy-only role context deliver enough value to justify Stage 2
   without live market claims?
3. Is B truly one companion capability, or will source governance and
   operations force a separate service earlier?
4. Are the six current skill IDs too narrow or semantically inconsistent for
   a credible pilot?
5. Can deterministic fallback satisfy every proposed Stage 1 intent without
   becoming a second answer system to maintain?
6. Are exact-evidence and citation gates realistic for vague job prose and
   current course data?
7. Should score components remain hidden to avoid false precision?
8. Is an 8-second p95 acceptable, and does model synthesis add enough value
   over deterministic explanations?
9. Are proposed retention, mapping precision, and unsupported-claim targets
   defensible, measurable, and affordable?
10. What evidence would justify moving market context from read-only display
    into deterministic ranking, and who has authority to make that call?
