# Research Paper Insight Planner — Final Product Plan

**Status:** Authoritative implementation-planning artifact; decision-ready, not approved for launch  
**Date:** 2026-11-10  
**Product owner:** Unassigned  
**Decision deadline:** Unassigned; must be dated before Shape exit  
**Launch authority still required:** Privacy/legal and product/finance, as listed in the decision ledger

## 1. Executive Decision

Proceed only to concierge validation and Shape for an MVP serving **one launch persona: applied ML practitioners planning non-safety-critical experiments**. The product starts from a research topic or paper URL, forms a bounded and user-confirmed corpus, and produces a versioned Markdown brief that traces claims to exact analyzed paper versions and evidence locations. Its promise is **“traceable decision support over a corpus you confirm.”**

Do not commit to broad provider integrations or production architecture until concierge validation passes. Release requires zero observed integrity failures in the predeclared audit, not an average accuracy threshold. Production scale additionally requires sustainable economics. Privacy/legal approval remains mandatory for source rights, deletion, retention, vendor handling, and no-training controls; product/finance approval remains mandatory for pricing or any scale-margin threshold change.

## 2. Inputs, Evidence, and Unknowns

| Item | Current position | Planning treatment |
|---|---|---|
| Problem/opportunity | Supplied through product intent and draft brief | Treat fragmented discovery, provenance loss, and ungrounded advice as the core problem. |
| Launch user | Settled | Applied ML practitioner planning a bounded, non-safety-critical experiment. |
| Desired outcome | Settled for validation | A useful next-experiment decision from a confirmed corpus, with inspectable evidence and explicit uncertainty. |
| Constraints | Partly settled | Lawful access, exact-version evidence, immutable revisions, Markdown output, hard integrity and spend controls. |
| Available evidence | Product intent and two grilling rounds only | Demand, provider coverage, accuracy baseline, pricing, and legal feasibility remain assumptions. |
| Stakeholders | Roles known; accountable people missing | Product owner, privacy/legal, finance, design, tech lead, QA, and DevOps/Security must be named before Shape exit. |
| Decision deadline | Missing | Orchestrator must assign a date before Shape exit. |

**Evidence:** The requested product must support topic discovery, URL ingestion, source inspection, evidence-grounded synthesis, implementation guidance, and portable Markdown. No user research, provider agreement, benchmark result, pricing evidence, legal approval, or production accuracy result has been supplied.

**Key assumptions to test:** Practitioners will accept corpus confirmation and visible caveats; lawful sources provide enough useful coverage; the evidence model is understandable; the Markdown contract works across papers; exact grounding can meet utility, latency, and cost ceilings.

## 3. Problem, Persona, and JTBD

**Problem statement:** Applied ML practitioners currently move among search tools, publisher pages, PDFs, notes, and generators. They cannot reliably tell which paper version supports a claim, how the corpus was selected, where synthesis differs from author findings, or when implementation advice exceeds the evidence. The result is slow review, citation errors, false consensus, and poorly bounded experiments.

**Launch persona:** An applied ML practitioner evaluating research for a non-safety-critical experiment. Researchers, students, educators, and product leads may inform discovery research but are not launch personas or acceptance-test populations.

**Primary JTBD:** “When I need to choose my next ML experiment, help me form and confirm a bounded research corpus, inspect what the exact paper versions support, and produce one evidence-linked experiment proposal so I can decide what to test without mistaking generated advice for published findings.”

**User outcomes:**

- Understand how candidates were found, ranked, truncated, and selected.
- Trace every supported claim to an exact paper version and resolvable evidence location.
- See disagreement, incomparability, access gaps, and uncertainty without manufactured consensus.
- Receive at most one bounded next experiment with assumptions, metrics, stop conditions, and failure modes.
- Export a stable, machine-checkable Markdown record suitable for further review.

## 4. Product Promise and Non-goals

**Promise:** Traceable decision support over a corpus the user confirms. Every run states that retrieval is bounded, the user controls corpus membership, and generated advice requires validation.

**Goals:**

- Support both topic and paper-URL starting points while preserving provenance.
- Make corpus composition, provider behavior, access scope, and run revision explicit.
- Separate paper-specific claims, cross-paper synthesis, and generated advice exactly.
- Produce inspectable, versioned Markdown that survives provider-link decay where lawful.
- Fail closed when exact evidence, applicability, or safe experiment framing is inadequate.

**Non-goals:**

- No exhaustive search, systematic-review claim, meta-analysis, truth ranking, scientific authority, or peer-review-quality judgment.
- No paywall, authentication, proxy, CAPTCHA, DRM, robots, rate-limit, or provider-term bypass.
- No recommendations for clinical, legal, public-safety, or other high-stakes decisions.
- No autonomous code execution, training, deployment, purchasing, policy action, or production change.
- No roadmap or production decision disguised as advice; generated advice is limited to one next experiment.
- No broad document library, reference-manager sync, collaboration, native mobile app, or full citation-style editor in MVP.

## 5. Workflows

### 5.1 Topic Workflow

1. User enters a topic and optional intent, date range, domain, and use case.
2. System preserves the verbatim query and records every provider-specific submitted query, expansion, filter, result limit, ranking mode, returned count, and failure state.
3. System returns no more than **30 de-duplicated candidates**, disclosing raw and de-duplicated counts, truncation, ranking factors, provider failures, and access mix with “bounded candidate set—not exhaustive coverage.”
4. Product may apply a visible merge rank using normalized relevance, recency, and method/domain diversity; no hidden boost may change the candidate set. Users can inspect, disable, or revise expansions and rerun.
5. System proposes a default corpus of **8 papers**; the user may select up to a **hard cap of 20**.
6. User confirms at least one exact paper/version. Synthesis cannot begin beforehand.
7. System preserves candidates, inclusions, exclusions, exclusion reasons, and confirmation timestamp in an immutable run revision.
8. System retrieves only lawful content, shows per-paper access state, extracts inspectable evidence, and exposes failures.
9. System generates labelled analysis and, only if allowed by the fail-closed rules, one bounded experiment.
10. Any membership or version change creates a new revision and requires renewed confirmation; removed papers cannot remain cited.

### 5.2 Paper URL Workflow

1. User enters a DOI-like value or supported DOI, arXiv, PubMed/PMC, publisher, repository, or direct-PDF URL.
2. System validates the request safely, resolves redirects, and identifies a conservative canonical record/version or returns a specific unsafe, unsupported, ambiguous, or access error.
3. System displays identity, analyzed version, publication state, access scope, correction/retraction signal, and any duplicate/version ambiguity.
4. User confirms the exact record/version before analysis.
5. Open-access full text may be processed. A narrowly gated user-supplied PDF may be processed only after the user attests authorization and upload security/legal gates pass. Credentials, proxy access, bypass, and unauthorized mirrors are prohibited.
6. If full text is unavailable, analysis is limited to permitted metadata/abstract and every affected output is marked `abstract-only` or `metadata-only`.
7. Single-paper output keeps cross-paper sections with `not_applicable: one confirmed paper`.
8. Related-paper expansion, if later offered, returns to the topic candidate-and-confirmation workflow; it never silently changes the corpus.

### 5.3 Required Product States

Start/empty; resolving; candidates available; no results; candidate truncation; provider partial failure; unsafe/unsupported URL; identity ambiguity; possible duplicate/version conflict; awaiting confirmation; ingesting; full-text; mixed access; abstract-only; metadata-only; denied; failed; corrected; retracted; parser degraded; evidence unavailable; contradiction; incomparable; advice suppressed; generation partial; export blocked; export ready; stale revision; superseded revision; deletion pending; deletion confirmed; cost stop.

## 6. Lawful Access and Corpus Controls

- Full text is processed only when open access or supplied by a user who attests authorization; source rights and quotation rules require privacy/legal approval before launch.
- The product never accepts credentials or attempts paywall, proxy, CAPTCHA, DRM, robots, rate-limit, or access-control bypass.
- URL handling rejects unsupported schemes, local files, credential-bearing URLs, loopback, private/link-local destinations, redirect-to-private targets, oversized content, and unexpected content types.
- General web search may locate a candidate but cannot establish canonical identity by itself. Canonical scholarly providers and repositories are preferred.
- Auto-merge is allowed only for exact normalized DOI matches or an explicit repository-version relationship from a canonical provider.
- Repository IDs, bibliographic fingerprints, and title/author/year similarity may only propose a visible group. Conflicting metadata stays separate until the user confirms the relationship.
- Inaccessible records remain visible with `metadata-only`, `abstract-only`, `denied`, or `failed`; they cannot support full-text claims.
- Retracted papers are visible but excluded from synthesis and advice by default. Explicit historical/methodological inclusion carries a warning and can never be the sole support for advice.
- Corrections remain linked to the affected version with status and date; evidence never silently migrates across versions.
- Every provider failure produces an immutable partial discovery snapshot containing provider/query revision, request time, returned IDs/order, pagination/truncation, error class, and completeness warning.
- Pending privacy/legal approval, source bytes and derived full-text caches are deleted within 24 hours of run completion; only minimal identifiers, access state, locators/hashes, quoted evidence, provenance, and requested outputs are retained for 30 days.

## 7. Trust and Evidence Model

### 7.1 Immutable Entities

- **Run:** Stable identifier for an input and its revision lineage.
- **Run revision:** Immutable snapshot of query/provider state, candidate set, confirmed corpus, access state, output, spend, and schema version. Retry, recovery, corpus change, version change, or regeneration creates a child revision; no prior revision is overwritten.
- **Paper record:** Conservative scholarly identity with stable paper ID, canonical identifiers, publication state, and separate version records.
- **Paper version:** Exact analyzed artifact with version ID/date, access scope, source, retrieval time, and content hash where lawful.
- **Evidence item:** Stable evidence ID bound to one exact paper version and one locator/content anchor.
- **Claim:** An analytical block with exactly one primary class, support status, evidence references, and validation state.
- **Issue:** Structured disagreement record with proposition, supporting evidence, contradicting evidence, comparability limits, plausible explanations, alternatives, and unresolved status.

### 7.2 Primary Claim Classes

| Class | Definition | Mandatory conditions |
|---|---|---|
| `PAPER-SPECIFIC` | Statement attributable to one exact paper version | Exact identity/version, access scope, attribution, locator, evidence key, and entailment. |
| `CROSS-PAPER SYNTHESIS` | Comparison or inference across at least two confirmed papers | Every necessary source, agreement/conflict treatment, comparability limits, and synthesis wording. |
| `GENERATED ADVICE` | Product-generated next-experiment proposal not directly claimed by papers | Evidence links, assumptions, multidimensional evidence status, bounded experiment, uncertainty, failure modes, and stop criteria. |

Every analytical paragraph, list group, or table row has **exactly one** primary class. Missing, multiple, or invalid labels block export and release. A block may consume evidence from several classes but cannot inherit several primary classes.

### 7.3 Access and Support Status

Access enum: `full_text`, `partial_text`, `abstract_only`, `metadata_only`, `denied`, `failed`.

Support enum: `supported`, `unsupported`, `evidence_unavailable`, `parser_degraded`, `not_applicable`.

A claim is `supported` only when its evidence key resolves to the exact analyzed version and the cited evidence entails the claim under its class-specific rubric. Limited-access records may support only statements present in the accessible material. Absence from an abstract is never evidence of absence from the paper.

### 7.4 Portable Evidence Record

Each evidence record contains:

- Stable evidence ID and stable paper/version IDs.
- Locator type and value: quoted span/passage plus page and section when available, or figure, table, equation, paragraph, or abstract field.
- Content anchor or checksum, access scope, retrieval timestamp, and lawful canonical URL.
- Minimum exact text required for verification: by default no more than two sentences or 50 words, subject to stricter source terms.
- If text retention is not lawful, locator and hash remain without the quote.
- Resolution state and parser warning; unresolved/wrong-version locators cannot be presented as support.

### 7.5 Integrity Blockers

Any fabricated source, false-supported citation, wrong-version citation, fabricated or inaccurate quotation, unresolved evidence key presented as support, or missing/multiple/invalid class label blocks export and release. Explicit partial output is allowed only when failed papers or sections are omitted or marked unavailable, all remaining supported claims pass validation, and omissions are prominent.

For this plan, **false-supported citation** means a citation presented as support where identity/version, locator, attribution, quotation accuracy, access scope, or entailment fails, or where a synthesis/advice claim omits evidence necessary to justify it.

### 7.6 Contradictions and Advice

- Material issues retain support, contradiction, comparability limits, plausible explanations, alternatives, and unresolved status; no majority-vote conclusion is manufactured.
- Differences in dataset, population, method, endpoint, or version are `incomparable` when they do not establish contradiction.
- Generated advice proposes one next bounded experiment containing hypothesis, smallest intervention, comparator, dataset/population, success metrics, stop metrics, effort estimate, failure modes, and the result that would change the decision.
- Evidence dimensions remain separate: source access, directness, consistency, applicability, and reproducibility, each `strong`, `mixed`, `weak`, or `unknown` with a reason. No aggregate confidence score is shown.
- Advice is suppressed when any required claim lacks resolved exact-version evidence; method-dependent support is only abstract/metadata; a material contradiction is unresolved; applicability is `weak` or `unknown`; sole support is retracted; or no safe measurable experiment can be framed.
- Suppression returns `insufficient evidence for advice`, the blocking gaps, and the smallest evidence-gathering action—never generic filler.

## 8. Versioned Markdown Output Contract

**Initial normative version:** `1.0.0`.

- Patch versions clarify without changing meaning.
- Minor versions add backward-compatible optional fields.
- Major versions may break consumers.
- Each export declares `schema_version` and `generator_version`; a run revision never silently changes schema version.
- Required headings remain present in order. Empty content uses controlled `not_applicable` or `unavailable` states with reasons.
- ID grammar: run `RUN-<opaque>`; revision `REV-<positive integer>`; paper `P-<stable opaque>`; version `V-<stable opaque>`; evidence `E-<paper-id>-<stable opaque>`; claim `C-<stable opaque>`; issue `I-<stable opaque>`.
- Citation grammar: `[@<evidence-id>]`; every key resolves exactly once in the evidence map.
- Deterministic replay of an unchanged revision preserves section order, IDs, labels, and provenance except documented volatile fields such as export timestamp.

### 8.1 Representative Skeleton

```markdown
---
schema_version: "1.0.0"
generator_version: "<version>"
run_id: "RUN-<opaque>"
revision_id: "REV-<n>"
parent_revision_id: null
created_at: "<ISO-8601>"
input_type: "topic | paper_url"
input_value: "<verbatim user input>"
corpus_status: "user_confirmed"
corpus_confirmed_at: "<ISO-8601>"
candidate_count_raw: 0
candidate_count_deduplicated: 0
candidate_count_shown: 0
candidate_truncated: false
analysis_scope: "full_text | mixed_access | abstract_only | metadata_only"
partial_run: false
providers: ["<provider>"]
direct_variable_cost_usd: 0.00
---

# Research Insight Brief

## Decision Context
- Launch persona: Applied ML practitioner
- Intended decision: <one bounded non-safety-critical experiment>
- Coverage notice: Bounded candidate set—not exhaustive coverage.

## Scope and Provenance
- Verbatim query: <value>
- Provider query revisions, expansions, filters, ranking modes, failures
- Included and excluded paper versions with reasons
- Retrieval and confirmation timestamps

## Paper Register
### [P-<id> / V-<id>] <title>
- Authors, date, venue/repository, DOI/identifiers
- Publication state: published | preprint | corrected | retracted | unknown
- Access scope: full_text | partial_text | abstract_only | metadata_only | denied | failed
- Canonical URL and retrieval timestamp
- Duplicate/version status and warnings

## Paper-Specific Analysis
### [P-<id> / V-<id>] <title>
#### Overview
- Claim ID: C-<id>
- Class: PAPER-SPECIFIC
- Support: supported | unsupported | evidence_unavailable | parser_degraded
- Statement with citation [@E-<paper-id>-<id>]
#### Research Question
#### Methods
#### Data and Evaluation
#### Findings
#### Limitations
#### Reproducibility and Artifacts

## Cross-Paper Synthesis
### Agreements
### Contradictions, Incomparability, and Alternatives
- Issue ID: I-<id>
- Class: CROSS-PAPER SYNTHESIS
- Proposition, support, contradiction, comparability limits, explanations, alternatives, status
### Evidence Gaps

## Next Bounded Experiment
- Class: GENERATED ADVICE
- Status: proposed | insufficient_evidence_for_advice
- Hypothesis:
- Smallest intervention and comparator:
- Dataset/population:
- Success and stop metrics:
- Estimated effort:
- Failure modes:
- Decision-changing result:
- Assumptions and evidence [@E-...]
- Evidence dimensions:
  - Source access: strong | mixed | weak | unknown — <reason>
  - Directness: strong | mixed | weak | unknown — <reason>
  - Consistency: strong | mixed | weak | unknown — <reason>
  - Applicability: strong | mixed | weak | unknown — <reason>
  - Reproducibility: strong | mixed | weak | unknown — <reason>

## Uncertainties and Omitted Material
- Unsupported claims, unavailable evidence, parser warnings, failed papers/providers, advice blockers

## References and Evidence Map
### [E-<paper-id>-<id>]
- Paper/version: P-<id> / V-<id>
- Locator: <type and value>
- Access scope: <enum>
- Content anchor/checksum: <value>
- Minimal quotation: <text or withheld with reason>
- Canonical URL: <lawful URL>
- Retrieved at: <ISO-8601>

## Run Ledger
- Immutable candidate snapshot and corpus confirmation
- Revision lineage, cost ledger, partial-state details
- Schema/generator versions and validation result
```

## 9. Prioritized Requirements and Acceptance Criteria

| ID | Priority | Requirement and trace | Independently testable acceptance criterion |
|---|---|---|---|
| R1 | Must | Preserve verbatim and provider-specific discovery behavior; solves hidden retrieval bias. | A topic run records all provider queries, expansions, filters, limits, ranking modes, counts, failures, timestamp, raw/de-duplicated counts, and truncation before confirmation. |
| R2 | Must | Bound discovery at 30 candidates, default-select 8, cap at 20; supports reviewability and ceilings. | No run displays over 30 de-duplicated candidates, initializes over 8 selected papers, or confirms over 20 papers. |
| R3 | Must | Require exact-version corpus confirmation; prevents hidden evidence selection. | No synthesis starts before confirmation; provenance includes candidates, included/excluded versions, reasons, and confirmation timestamp. |
| R4 | Must | Resolve identity conservatively; prevents wrong-work evidence. | Only exact DOI or canonical repository relationships auto-merge; conflicts remain separate and visible until confirmed. |
| R5 | Must | Make all revisions immutable; preserves reproducibility. | Retry, provider recovery, corpus/version change, or regeneration creates a linked child revision; prior candidate, corpus, and output bytes remain unchanged. |
| R6 | Must | Enforce lawful access and secure input boundaries; limits legal/security exposure. | Prohibited URLs/access paths fail before content analysis; inaccessible papers remain limited and labelled; no bypass attempt occurs. |
| R7 | Must | Record exact access and publication states; prevents overclaiming. | Every paper has exactly one access state and applicable correction/retraction state; limited-access content cannot yield full-text claims. |
| R8 | Must | Bind evidence to exact versions and portable locators; enables inspection. | Every supported paper-specific claim resolves to the analyzed version and most specific lawful locator, or changes to a non-supported status. |
| R9 | Must | Apply exactly one primary class to each analytical block; prevents category blending. | Export validation returns zero missing, multiple, or invalid class labels; any occurrence blocks export. |
| R10 | Must | Represent disagreement and incomparability without false consensus. | Each material issue contains the required structured fields; non-comparable evidence is labelled `incomparable`, not reduced to a vote. |
| R11 | Must | Fail closed on unsupported advice; protects the launch decision. | Every trigger in Section 7.6 suppresses advice independently and returns blocking gaps plus a smallest evidence-gathering action. |
| R12 | Must | Export schema-valid Markdown `1.0.0`; supports portability. | Validator confirms front matter, required heading order, enums, ID grammar, citation resolution, null behavior, and deterministic fields. |
| R13 | Must | Produce honest partial outputs; avoids brittle all-or-nothing behavior. | Failed sources/sections are prominent, remaining claims pass validation, and partial output never claims completeness. |
| R14 | Must | Enforce retention and no-training invariants, pending authority approval. | Test evidence shows source-byte/cache deletion within 24 hours, 30-day expiry for minimal run/output records, no raw-text logs, auditable deletion, and eligible vendor controls. |
| R15 | Must | Enforce spend ceilings without weakening integrity. | Preflight reservation and metering keep every run at or below US$8; default runs target US$3; ceiling returns labelled partial output and cost ledger. |
| R16 | Should | Expose corrections/retractions and user-confirmed historical inclusion. | Retracted content is excluded by default, warned when included, and never solely supports advice. |
| R17 | Should | Support narrowly gated authorized PDF supply. | Supply path is unavailable until authorization attestation, legal approval, and security tests pass; supplied bytes follow deletion rules. |
| R18 | Could | Expand a confirmed paper into related candidates. | Expansion creates a bounded candidate set and requires new confirmation; it never mutates the current revision. |
| R19 | Won't | Claim exhaustive coverage, rank truth, bypass restrictions, or act autonomously. | Product copy, tests, and output contain no such claim or behavior. |

### 9.1 Mandatory Edge Cases

Malformed and unsafe URLs; redirect-to-private target; inaccessible full text; abstract-only and metadata-only records; mixed-access corpus; duplicate ambiguity; wrong-version trap; corrected and retracted papers; parser-degraded locator; direct quotation; provider partial failure and retry; candidate truncation; contradiction versus incomparability; removed paper after regeneration; unresolved evidence key; class-label collision; weak-applicability advice suppression; cost ceiling; deletion across failed jobs and subprocessors.

## 10. Success Measures and Release Gates

| Gate | Threshold | Use |
|---|---:|---|
| Integrity | **Zero observed false-supported citations** and zero fabricated sources, wrong-version citations, fabricated/inaccurate quotations, unresolved support keys, or class-label failures in the predeclared release audit | Hard release gate |
| Diagnostic entailment | 95% sampled entailment | Pilot diagnostic only; never sufficient for release and never offsets a critical failure |
| Citation coverage | 100% of substantive paper-specific claims have resolved support or explicit non-supported status | Hard release gate |
| Label integrity | 100% of analytical blocks have exactly one valid primary class | Hard release gate |
| Utility | At least **70%** of completed pilot tasks produce a useful next-experiment decision without material factual correction, and the user distinguishes advice from findings | Pilot/build gate |
| Cost | Default run target **≤US$3**; every run through 20 papers **≤US$8 hard ceiling** | Build/release gate |
| Latency | p90 ≤10 minutes for default runs and ≤20 minutes for capped runs, from confirmation to reviewable export | Pilot/release gate |
| Reviewer burden | Median ≤10 minutes and p90 ≤15 minutes to confirm corpus and inspect enough evidence to use output | Pilot/release gate |
| Workflow completion | ≥90% of supported benchmark tasks reach a reviewable corpus/export or specific recoverable error | Pilot/release gate |
| Evidence navigation | ≥80% of pilot users open support for a selected claim without assistance in ≤2 actions | Pilot/release gate |
| Access/security | Zero successful access-control bypass or private-network fetch in the security suite | Hard release gate |
| Retention/reuse | 24-hour source-byte deletion, 30-day minimal run/output expiry, deletion audit, no raw-text logs, and no unapproved training/evaluation reuse | Hard release gate pending privacy/legal approval |
| Scale economics | Non-negative contribution margin at p90 cost and **≥60% contribution margin** at expected default-run mix | Hard scale gate, subject only to explicit product/finance change |

**Operating stop rules:** Stop scope expansion on any integrity blocker. If more than 10% of valid runs exceed cost ceilings, more than 20% exceed latency/reviewer ceilings, or utility is below 70%, first reduce corpus size, providers, or output sections. Remove generated advice before weakening evidence or label gates. Re-test the same locked tasks; do not retroactively relax thresholds.

## 11. Concierge Validation Protocol

**Purpose:** Disprove or support the core demand, comprehension, integrity, workflow, and operating assumptions before production architecture or broad integration.

**Participants:** Recruit 10 launch-persona users working on permitted, non-safety-critical ML experiment decisions. Each completes exactly two tasks.

**Task set:** Lock **20 predeclared tasks** before output creation: 10 topic tasks and 10 URL tasks, every task represented once. The set must include open full text, abstract-only, metadata/inaccessible source, malformed/unsafe URL, duplicate/version conflict, corrected paper, retracted paper, mixed access, provider partial failure, parser degradation, contradiction/incomparability, and advice suppression.

**Method:** Use concierge work or a throwaway prototype only. Preserve the verbatim inputs, candidate snapshots, user corpus decisions, evidence records, outputs, timing, cost estimates, observed assistance, corrections, and post-task decision. Do not build broad provider integrations or select production architecture.

**User measures:** Corpus-control comprehension; exact class-label comprehension; evidence opening in ≤2 actions; time to confirmation and sufficient verification; usefulness of the next-experiment decision; material corrections; and reasons for suppression or abandonment.

**Claim audit:**

- Predeclare at least **100 substantive claims**, stratified across all three classes, full-text and limited-access states, providers, formats, paper versions, and agreement/conflict outcomes.
- Include all mandatory edge cases: wrong-version traps, duplicate ambiguity, inaccessible full text, corrected/retracted papers, parser-degraded locators, provider partial failure, direct quotations, contradiction/incomparability, and advice suppression under weak evidence.
- Assign **two independent reviewers per claim** who did not create the outputs. A third reviewer adjudicates disagreements; report agreement and adjudication rather than hiding them.
- Score each class-specific dimension `pass`, `fail`, or `not_applicable` with rationale. Any critical failure fails the claim; aggregate averages cannot offset it.
- `PAPER-SPECIFIC`: identity/version, locator, access scope, attribution, quotation accuracy, entailment.
- `CROSS-PAPER SYNTHESIS`: all paper-specific checks plus every necessary source, faithful agreement/conflict treatment, comparability limits.
- `GENERATED ADVICE`: all applicable checks plus evidence linkage, applicability, bounded experiment, assumptions, uncertainty, failure modes, and stop criteria.

**Concierge pass:** Zero observed integrity blockers, utility ≥70%, label and corpus comprehension pass, workflow/inspection gates pass, and no ceiling/stop-rule breach that remains after a bounded scope reduction. Otherwise iterate or stop; do not proceed by averaging away failures.

## 12. Prioritized MVP Scope

**P0 — Validate before build:** Topic and URL concierge workflows; candidate/corpus confirmation; access and identity states; evidence opening; exact class labels; normative Markdown; advice suppression; two-reviewer audit; cost/latency/burden measurement.

**P1 — MVP build:** Bounded topic discovery; supported URL resolution; conservative identity/versioning; immutable snapshots/revisions; lawful full-text and limited-access processing; exact-version evidence; paper analysis; structured cross-paper issues; one fail-closed bounded experiment; schema validation; secure fetch; deletion/retention controls; hard budget stop; partial export.

**P2 — Conditional:** Narrow authorized PDF supply, only after legal/security gates; visible retraction/correction controls; corpus edit/regenerate with immutable lineage; optional related-paper expansion.

**Deferred:** Broad uploads/libraries, reference-manager sync, collaboration, native mobile, citation graphs, multilingual support, style editing, code generation/execution, model training, deployment, production architecture recommendations, and all high-stakes advice.

## 13. Roadmap and Phase Gates

| Phase | Work | Exit rule |
|---|---|---|
| 0. Validation setup | Name stakeholders; assign deadline; lock 20 tasks, 100-claim sample, rubrics, scripts/content, and measurement plan. | Inputs and audit set frozen before outputs; no architecture commitment. |
| 1. Concierge validation | Run 10 users × 2 tasks; produce traceable outputs manually or with a throwaway prototype; complete two-reviewer audit. | All concierge gates pass, or scope is reduced and the same tasks rerun. |
| 2. Shape | Designer, Tech Lead, QA, and DevOps/Security decide mechanisms and interaction details while preserving invariants; legal/finance authorities evaluate deferred items. | Shape artifacts cover all handoff decisions; authority gates have owners/dates; no invariant is weakened. |
| 3. MVP build | Implement P1 contracts and checks incrementally against the locked benchmark. | Requirements R1–R15 and applicable R16–R17 pass; hard integrity/security/retention/cost gates pass. |
| 4. Pilot | Run launch-persona pilot with instrumented real workflows and independent audit. | Utility ≥70%, ceilings and burden gates pass, zero integrity blockers, authority approvals recorded. |
| 5. Controlled launch | Release to bounded users/providers with monitoring, deletion evidence, and rollback/kill controls. | Sustained release gates; no unresolved critical risk or authority gate. |
| 6. Scale | Model expected and p90 economics including providers/models, storage/egress, moderation/support, audit, and failed runs; report pilot labor separately. | Non-negative margin at p90 and ≥60% at expected default mix, plus all trust/utility/latency gates. |

## 13A. Proposed MVP Architecture

The SWE Team Tech Lead has produced a concrete architecture proposal:

- [Technical architecture and implementation plan](technical-plan.md)
- [Interactive system architecture diagram](architecture.html)

The proposed design uses eight bounded capabilities across public ingress,
private control-plane, and isolated untrusted-content zones:

1. Web/API ingress authenticates users and accepts topic or paper-URL input.
2. A safe resolver and fetch broker enforce lawful access, SSRF controls,
   redirect limits, content limits, and deny-by-default egress.
3. Discovery and identity adapters disclose provider queries and preserve
   conservative paper/version identity.
4. An append-only run orchestrator owns immutable revisions, idempotent jobs,
   retries, partial results, and the per-revision budget ledger.
5. Isolated retrieval/parser workers handle hostile source bytes without
   control-plane database access.
6. The evidence and claim pipeline emits exact-version evidence records and
   typed draft claims, never publishable prose.
7. A privileged deterministic validation gate enforces identity, locator,
   citation, class, advice, schema, lifecycle, and US$8 budget invariants.
8. Separate transient and durable stores enforce the proposed 24-hour source
   deletion and 30-day minimal-output lifecycle before deterministic Markdown
   export and append-only audit.

This architecture is a **proposed Shape input**, not `shape-ready` or
implementation approval. Provider choices, model/vendor eligibility, precise
retention semantics, authorized uploads, cloud topology, and named ownership
remain subject to the authority gates in this plan.

## 14. Shape Handoffs

### 14.1 Product Design

**Must preserve:** One persona/JTBD; explicit corpus confirmation; bounded-coverage disclosure; visible query/provider revisions; exact claim labels; identity ambiguity; access/publication states; contradictions/incomparability; advice suppression; partial and immutable revision states.

**Design decisions:** Interaction and content hierarchy for topic versus URL entry, 30-candidate review, default 8 selection, evidence opening, class-label placement, ambiguity resolution, partial-output hierarchy, stale/superseded revisions, and deletion status. Determine whether users can complete enough verification within the 10-minute median burden without hiding states in tooltips.

**Content constraints:** Never use “comprehensive,” “verified,” “best,” or “recommended” without precise qualification. Generated advice cannot resemble a paper finding. Limited-access and retraction warnings remain in context, not only in a legend.

**Deliverable to QA:** State/workflow map and content rules covering every required state and edge case. Final interface design remains a Design responsibility, not this plan.

### 14.2 Tech Lead

**Hard product contracts:** Conservative paper/version identity; immutable revisions and partial snapshots; exact access state; portable evidence IDs/anchors; one primary claim class; structured disagreement; fail-closed advice; normative Markdown validation; secure authorized supply; TTL/deletion propagation; hard spend stop; deterministic export.

**Shape decisions:** Provider feasibility and terms; safe resolution/redirect mechanism; canonical identity representation; locator fidelity by format; parser isolation; evidence validation boundaries; stage budgeting/metering; deletion/audit mechanism; schema validator and deterministic-ID strategy; observability that excludes raw content. These are architecture mechanisms and remain for Shape.

**Questions to answer:** Which provider set can produce the required disclosures? What locator remains portable across PDF/HTML? How is exact-version resolution proven? How do retries share one revision budget? How do queues, failed jobs, backups, and vendors honor deletion? How does generation fail closed on missing evidence?

### 14.3 QA

**Own before output creation:** Lock 20 tasks, stratified 100-claim sample, two-reviewer assignment, adjudication protocol, class-specific rubrics, and pass/fail evidence format.

**Required suites:** Identity/version traps; citation and quotation integrity; schema/ID/citation grammar; exact class labels; contradiction/incomparability; every advice-suppression trigger; immutable retry/corpus revisions; provider partial snapshots; secure URL/access controls; spend stop; deletion and vendor evidence; partial export; deterministic replay; latency, burden, utility, and evidence navigation.

**Release decision:** Report each zero-tolerance condition separately. Never substitute a 95% aggregate for the zero-observed-failure release gate.

### 14.4 DevOps/Security

**Must preserve:** No restricted-access bypass; untrusted remote content isolation; private-network denial across redirects; content limits; raw-text-free logs; auditable 24-hour source deletion; 30-day minimal-record expiry; no unauthorized training/review; hard per-revision spend stop.

**Shape decisions:** Isolation and egress boundaries; allow/deny controls; malware/content scanning; secret handling; queue/cache/backup TTL enforcement; deletion evidence; vendor eligibility checks; incident kill switch; cost reservation and cutoff; monitoring fields that avoid sensitive text.

**Authority dependencies:** Privacy/legal approves source rights, quotation, deletion semantics, backup treatment, subprocessors, and no-training contracts. Security cannot replace that approval.

## 15. Risk Register

| Risk | Severity | Mitigation and owner | Gate |
|---|---|---|---|
| False-supported or fabricated citation | Critical | Fail closed, exact-version locators, two-reviewer audit; Product/QA | Zero observed failures |
| Wrong identity/version merge | Critical | Conservative auto-merge and visible ambiguity; Tech/QA | Identity edge cases pass |
| Advice exceeds evidence | Critical | Separate class, multidimensional status, suppression triggers; Product/QA | Every trigger passes |
| Copyright/provider-term breach | Critical | Approved lawful sources, minimal quotation, transient bytes; Legal | Explicit approval |
| SSRF/malicious content/prompt injection | Critical | Safe resolver, network denial, isolation, limits, untrusted-content handling; Security | Zero successful exploit |
| Retention or vendor reuse breach | Critical | TTL propagation, raw-text-free logs, deletion audit, eligible contracts; Privacy/Security | Approval and tests |
| Retrieval bias appears exhaustive | High | Bounded disclosure, provider-query transparency, corpus confirmation; Product/Design | Comprehension gate |
| Contradiction becomes false consensus | High | Structured issue model and incomparability state; Product/QA | Audit rubric pass |
| Limited-access overgeneralization | High | Access enforcement and fail-closed method advice; Tech/QA | Edge-case pass |
| Cost overrun | High | Preflight estimate, stage reserves, US$8 hard cutoff; Tech/Finance | Per-run compliance |
| Latency/reviewer burden blocks adoption | High | Instrument and reduce scope before trust controls; Product/Tech | p90/median gates |
| Utility below 70% | High | Narrow output/providers/corpus; remove advice only after testing suppression value; Product | Same-task retest |
| Unsustainable scale economics | High | Full contribution model with p90 and expected mix; Finance | 0% p90 / 60% expected |
| Schema drift breaks consumers | Medium | Semantic versioning and immutable schema per revision; Tech/QA | Compatibility suite |
| Provider outage changes evidence set | Medium | Immutable partial snapshot and child retry revision; Tech/QA | Reproducibility suite |
| Persona drift | Medium | One launch persona and acceptance population; Product | No expansion before gate |

## 16. Decision Ledger

The two grilling rounds settled **26 product decisions**; a third frontier check found no additional product decision requiring resolution. This does **not** imply user, legal, finance, or launch approval.

| ID | Decision | Status |
|---|---|---|
| D01 | Sole launch persona: applied ML practitioner planning a non-safety-critical experiment | Settled product default |
| D02 | Promise: traceable decision support over a user-confirmed corpus | Settled product default |
| D03 | Synthesis requires explicit exact-version corpus confirmation | Settled invariant |
| D04 | Discovery shows ≤30 candidates; default selected 8; hard corpus cap 20 | Settled pilot default |
| D05 | Open or attested-authorized full text only; narrow supply path is gated | Settled invariant; launch authority dependency |
| D06 | Supported claims require exact analyzed version and specific locator | Settled invariant |
| D07 | Every analytical block has exactly one primary class | Settled invariant |
| D08 | High-stakes advice and autonomous action are excluded | Settled scope |
| D09 | Source bytes deleted within 24h; minimal run/output retained 30 days; no bundled reuse consent | Settled product invariant; privacy/legal approval deferred |
| D10 | Integrity failures block export/release; 95% is diagnostic only | Settled release policy |
| D11 | Concierge validation uses 10 users, 20 tasks, and independent claim audit | Settled validation design |
| D12 | Cost, latency, burden, utility, and stop rules are predeclared | Settled operating policy |
| D13 | Provider queries, expansions, ranking, counts, and failures are visible/revisable | Settled product default |
| D14 | Identity/deduplication is conservative; ambiguity stays visible | Settled invariant |
| D15 | Inaccessible/corrected/retracted records follow explicit inclusion and support rules | Settled invariant |
| D16 | Contradictions, incomparability, and alternatives use structured records | Settled output behavior |
| D17 | Markdown contract is normative and semantically versioned | Settled invariant |
| D18 | Evidence records are portable, minimal, version-bound, and checksum/anchor backed | Settled invariant |
| D19 | Advice is one bounded next experiment with separate evidence dimensions | Settled scope |
| D20 | Advice fails closed and falls back to evidence-gathering action | Settled invariant |
| D21 | Audit is ≥100 stratified claims, two reviewers each, third-reviewer adjudication, mandatory edge cases | Settled release method |
| D22 | Audit rubrics are class-specific and critical failures cannot average out | Settled release method |
| D23 | Provider snapshots and run revisions are immutable | Settled invariant |
| D24 | Deletion/no-training controls extend to queues, failed jobs, backups where feasible, and subprocessors | Settled product invariant; privacy/legal approval deferred |
| D25 | US$3 default-run target and US$8 hard ceiling are enforced per run revision | Settled binding ceiling |
| D26 | Scale requires non-negative p90 margin and ≥60% expected-default contribution margin | Settled default gate; pricing/threshold authority deferred |

**Authority-deferred decisions:**

- **A1 — Privacy/legal:** Approve source rights, limited quotation, exact 24-hour deletion semantics, 30-day minimal retention, backup treatment, deletion audit evidence, vendor/subprocessor terms, and contractual/technical no-training behavior.
- **A2 — Product/finance:** Approve pricing and any contribution-margin threshold different from the 60% default before scale. Any change to US$3/US$8 ceilings also requires explicit product/finance authority.
- **A3 — Orchestrator:** Assign accountable people and a dated decision deadline before Shape exit.

## 17. Go/No-go Rules

**Go to Shape only if:** The 20-task protocol, 100-claim audit, rubrics, participant definition, and measurements are locked; accountable roles and dates exist. Otherwise no-go.

**Go to MVP build only if:** Concierge work shows zero observed integrity blockers, utility ≥70%, class/corpus comprehension, evidence navigation, and operating ceilings pass; unresolved failures have not been averaged away. Otherwise iterate with reduced scope or stop.

**Go to pilot only if:** R1–R15 and applicable gated requirements pass; secure-fetch, deletion, budget-stop, schema, immutable-revision, and fail-closed tests pass; no critical risk lacks an owner. Otherwise no-go.

**Go to controlled launch only if:** The stratified two-reviewer 100-claim audit observes zero false-supported citations and zero other integrity blockers; all release gates pass; privacy/legal has approved A1; pricing supports the binding run ceilings; rollback and deletion evidence exist. A 95% entailment result alone is no-go.

**Go to scale only if:** Controlled-launch gates remain passing, utility remains ≥70%, p90 economics are non-negative, expected default-run contribution margin is ≥60%, and product/finance approves pricing or any threshold change. Otherwise remain bounded, reprice, reduce scope, or stop.

**Immediate no-go/stop:** Any fabricated source/quotation, false-supported or wrong-version citation, unresolved support key presented as support, class-label failure, access-control bypass, prohibited high-stakes advice, source-deletion breach, unapproved vendor reuse, or spend beyond US$8.

## 18. Provenance

This plan reconciles `brief.md` with `planner-responses.md`, using the latter wherever they conflict. Two grilling rounds settled 26 product decisions. A third frontier check was empty. The plan records remaining authority gates explicitly and does not represent user approval, legal approval, finance approval, frame approval, or launch approval.
