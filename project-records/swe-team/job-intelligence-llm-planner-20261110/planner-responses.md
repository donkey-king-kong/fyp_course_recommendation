# SWE Product Manager: Grilling Round 1 Responses

**Flow ID:** `swe-product-manager`  
**Parent:** parent orchestrator  
**Decision basis:** verified claims and corrected claim wording in the supplied research artifacts. Numeric thresholds below are provisional product gates, not measured performance or external facts.

## Q1 - One product, staged capabilities

**Answer: Yes.**

**Rationale:** The assistant and job context share the student journey and canonical skill bridge, while source authorization, extraction, and market-data operations need independent controls. A separate product would duplicate context; an all-at-once launch would couple unrelated release risks.

**Default:** Use separately releasable Stages 0-4 with independent model, ingestion, source, and market-ranking kill switches. Stage 1 contains no market claim; Stage 2 is read-only job context; market-informed ranking remains a separate later decision.

**Implications:** Marketing and UI must expose only capabilities actually released. The tech lead may begin with a bounded service inside the monolith and split ingestion operationally only when authorized live collection requires isolation.

## Q2 - Primary persona and first job to be done

**Answer: Yes.**

**Rationale:** The repository already provides deterministic recommendations, roadmap readiness, prerequisites, open-slot reasons, and evidence paths. Those facts support a grounded explanation journey now; broad catalog chat and market exploration have weaker profile or source evidence.

**Default:** Primary persona is an NTU computing student with a current roadmap or recommendation. The first task is to understand why a recommendation was made, its prerequisites, tradeoffs, uncertainty, and what could change it. Role/posting context is secondary.

**Implications:** Prioritize explanation, readiness, comparison, and open-slot intents. Anonymous catalog help is P1 and must not imply personalization.

## Q3 - Read-only value hypothesis

**Answer: Modify. Approve read-only context, with a concrete continuation gate.**

**Rationale:** Read-only context can improve understanding without contaminating recommendation policy, but "users find it useful" is not measurable enough. It earns continuation only if it improves a student's ability to identify evidenced role skills, distinguish evidence from unknowns, and compare existing course options.

**Default:** Run a moderated crossover pilot with at least 20 target users and a locked task set, comparing unchanged recommendations alone against recommendations plus read-only context. Continue Stage 2 only if:

- task success improves by at least 10 percentage points;
- at least 80% correctly distinguish employer/posting evidence from taxonomy context;
- unsupported takeaways occur in no more than 5% of scored answers;
- median task time does not worsen by more than 20%; and
- at least 70% rate the context as useful for the decision, not merely interesting.

These are provisional go/no-go thresholds, not expected or measured results.

**Implications:** Failure pauses the job-context capability; it does not justify reranking. Product owns the task rubric. A research owner must approve the study protocol and interpret the small pilot with confidence intervals and qualitative evidence.

## Q4 - Assistant authority and answer boundary

**Answer: Yes.**

**Rationale:** The deterministic backend already owns readiness, prerequisite checks, scoring, ranking, and slot allocation. Giving the model hidden authority would make existing behavior unauditable and would overstate incomplete academic checks.

**Default:** The model may explain, compare, translate, and suggest a bounded next step. It receives no mutation, ranking, eligibility, admin, or source-policy tools. Score components may be translated into qualitative reasons; raw numeric components remain hidden in the pilot unless product and the recommendation owner later approve them.

**Implications:** Every factual statement must resolve to supplied claims. Preference changes, if later supported, require an explicit user action followed by the existing deterministic recalculation flow.

## Q5 - LinkedIn exclusion and source strategy

**Answer: Yes.**

**Rationale:** Verified documentation shows that self-service Open Permissions do not include job-search inventory retrieval, the Job Posting API documentation describes outbound posting without a read/search endpoint, and Apply Connect documentation describes an ATS workflow without a general job-search feed. LinkedIn also prohibits the unauthorized automated collection methods considered here.

**Default:** Preserve "LinkedIn-first" only as an authorization and partnership track. Make no automated LinkedIn request, use no logged-in automation, and accept no scraped or indirectly sourced LinkedIn dataset. Use pinned O*NET/ESCO role context and rights-checked supplied postings first; add a live provider only after written terms cover commercial use, retention, attribution, derivatives, model inference, and deletion.

**Implications:** O*NET and ESCO must be labelled occupational classification context, not live vacancies or current demand. LinkedIn can enter the roadmap only after written source-owner authorization plus legal, privacy, and security approval for the exact use.

## Q6 - User-supplied URL, text, and file behavior

**Answer: Modify. Approve text/file input, but reject known or declared LinkedIn-derived content during the pilot.**

**Rationale:** A user manually copying LinkedIn text does not establish the product's right to process, derive, retain, or display that content and could turn manual input into an acquisition workaround. A narrowly justified private-analysis exception is conceivable, but the supplied evidence does not establish that authority.

**Default:** Accept pasted text and approved text/PDF uploads only when the user declares that they may provide the content and that it is not LinkedIn-derived. Do not fetch URLs. Reject declared LinkedIn origin, LinkedIn URLs, and reliably detected LinkedIn page exports. If origin is ambiguous, ask one provenance clarification; reject if unresolved. Do not attempt broad text fingerprinting or claim perfect origin detection.

**Implications:** Store a provenance declaration and policy result, not a legal warranty. Analysis is private, observed-at-upload, non-training, and non-republished. Legal and the source owner must explicitly approve any future exception for user-directed, transient LinkedIn analysis; until then the product position is rejection.

## Q7 - BYOK timing and token custody

**Answer: Modify. The user's promised API token is an operator/deployer-managed server secret, not tenant BYOK.**

**Rationale:** The request establishes that a token will be available, but does not establish a product requirement for end users to supply credentials. Treating it as BYOK would create unsupported tenant custody, revocation, and support obligations.

**Default:** Inject one platform-managed credential per environment/service from an approved server-side secret manager. The browser never receives it and never calls the provider directly. Apply model allowlists, spend limits, access audit, redaction tests, rotation, and immediate revocation. BYOK is disabled.

**Implications:** No credential may enter chat, URLs, cookies, localStorage, analytics, logs, repositories, or ordinary configuration. DevOps/security must approve secret storage and rotation; finance/product must approve the pilot budget. Tenant BYOK requires a later explicit product decision and separate privacy/security design.

## Q8 - Deterministic versus LLM extraction

**Answer: Yes.**

**Rationale:** Structured output constrains shape but does not prove that a requirement exists or is interpreted correctly. Deterministic parsing provides reproducible structure and evidence locations; a bounded model can handle unresolved prose.

**Default:** Deterministic code owns document structure, typed fields, evidence offsets, quote matching, schema and semantic checks, negation checks, policy, hashes, and versions. Invoke the model only for unresolved requirement-bearing prose. Permit one schema repair for malformed output; unsupported semantics abstain without a leading retry.

**Implications:** Accepted requirements require exact evidence and a stable locator. The extraction model has no browser, credentials, writes, database, ranking authority, or arbitrary tools.

## Q9 - Missing, vague, and conflicting requirements

**Answer: Yes.**

**Rationale:** Completing absent fields with occupational norms would misrepresent employer evidence. Suppressing ambiguity would hide information needed for a responsible decision.

**Default:** Preserve `required`, `preferred`, `optional`, `unclear`, negated, alternative, conflicting, ambiguous, unmapped, and unknown states. Keep vague wording without inventing proficiency or quantities. Ask at most one clarification when the user can resolve the ambiguity; otherwise show evidence, taxonomy context as separate enrichment, or abstain.

**Implications:** Unknown does not mean "not required," and no reviewed course link does not mean "irrelevant." UI and evaluation fixtures must test these states directly.

## Q10 - Taxonomy provenance and canonical skills

**Answer: Yes.**

**Rationale:** O*NET, ESCO, ISCO, the current role mappings, and the six pilot skill IDs have different scopes. No single source is authoritative for employers, courses, and all geographies.

**Default:** Preserve raw mentions; pin taxonomy and mapper versions; use O*NET for U.S. occupation context, ESCO for European/multilingual concepts, ISCO for international roll-up, and a reviewed internal registry for course links and aliases. Treat the six current IDs as provisional seeds. Enable automatic mappings by category only after at least 98% precision on a locked set with adequate category coverage; otherwise mark ambiguous/unmapped.

**Implications:** A named academic/domain reviewer must approve course-skill mappings and a named data/domain owner must approve job-skill aliases. The 98% figure is a conservative release target, not current performance.

## Q11 - On-demand versus scheduled ingestion

**Answer: Yes.**

**Rationale:** Private supplied-posting analysis and shared market ingestion have different rights, tenancy, and lifecycle requirements. Arbitrary user-triggered fetching would bypass source governance.

**Default:** Keep supplied-posting analysis private and on demand. Keep recommendation recalculation in the existing backend. Do not enable scheduled or live URL ingestion until one source is contract-approved. Later scheduled and approved on-demand jobs must share source policy, quotas, provenance, deduplication, lifecycle rules, coalescing, and kill switches.

**Implications:** Ordinary users cannot submit cron expressions, bulk URLs, or query fan-out. The source owner, legal, privacy, and security authorities must approve the first live source and its operating policy.

## Q12 - Freshness promise

**Answer: Yes.**

**Rationale:** The available taxonomies are reference classifications, while supplied postings are only known at upload time. A universal "current jobs" promise would overstate both.

**Default:** Label supplied content "observed at upload" and show the pinned taxonomy release. For a future authorized source, show observation window, lifecycle state, and source-specific stale threshold. As an operational starting point only, refresh active authorized records every 24 hours and accelerate to every 6 hours within seven days of an explicit expiry, unless the contract, rate limits, or measured source behavior require another cadence.

**Implications:** No current-demand or trend wording without authorized longitudinal coverage and a publishability gate. Source policy controls final cadence and stale behavior; expired evidence falls back to static role context or an unavailable state.

## Q13 - Cost and latency envelope

**Answer: Modify. Approve bounded synthesis with explicit pilot budgets.**

**Rationale:** An 8-second p95 alone does not control spend or prove incremental value. The model should remain optional per intent and removable when it does not beat deterministic output.

**Default:** Generate fallback first; make at most one primary model call and one schema-repair call. Under an agreed pilot load of 10 concurrent requests:

- deterministic fallback p95: at most 1 second;
- model-assisted response p50: at most 4 seconds and p95: at most 8 seconds;
- timeout: 10 seconds end to end, then serve fallback;
- variable model cost: at most USD 0.03 per completed model-assisted answer at pilot prices;
- pilot model budget: USD 100 per month, with a hard stop and fallback;
- no more than 8,000 input tokens and 1,000 output tokens per call.

These are operating defaults to validate with the chosen provider, not price or performance claims.

**Implications:** Product/finance must approve the cost ceilings after provider pricing is known; the tech lead sets load methodology. Remove model synthesis from an intent if it misses the latency/cost envelope or fails the Q3 usefulness gate.

## Q14 - Privacy, retention, and conversation state

**Answer: Modify. Approve minimization and no persistent chat; use a shorter default raw-content window.**

**Rationale:** The current product lacks authenticated server identity and tenant isolation. Raw academic documents and persistent conversations therefore create unjustified exposure. A 24-hour maximum is defensible as a ceiling, but most successful synchronous analysis does not need raw posting text that long.

**Default:** Send only bounded structured course/result facts and exclude student identifiers and raw academic documents. Do not persist conversation history. Process supplied postings in a tenant-scoped temporary store, delete raw text within 1 hour after successful analysis or immediately on user request, and enforce an absolute 24-hour cleanup deadline for failed/interrupted jobs. Delete derived private records with the raw input unless the user explicitly saves a result under a later approved persistence design. Retain sanitized operational metadata for 30 days, without prompt/response bodies.

**Implications:** Processor terms or source rules may require shorter periods. Any longer retention or saved history requires authenticated identity, tenant isolation, export, selective deletion, stated purpose, and privacy approval. Privacy/legal must approve the schedule; security must verify deletion and cross-tenant tests.

## Q15 - Evaluation gates and kill criteria

**Answer: Modify. Approve hard evidence and safety gates, with precision measured only on adequately powered locked strata.**

**Rationale:** Demo review and one aggregate score are insufficient. The proposed thresholds are conservative release targets, but they must not imply proven performance or allow tiny categories to pass on misleading percentages.

**Default:** Before each capability release require:

- 100% of displayed factual claims have class, source, version, and resolvable locator;
- zero assistant-caused mutations to ranking, readiness, prerequisites, scores, or slots;
- at least 99% factual-claim precision and at least 99% required/preferred precision on accepted outputs;
- at least 99.5% citation resolution;
- automatic mapping only at at least 98% precision per enabled category;
- zero critical prompt-injection policy breaches, cross-user access, or secret leakage;
- verified deterministic fallback, budget cutoff, source kill switch, selective deletion, and latency behavior;
- at least 100 locked job families overall, dual annotation of locked items, adjudication of disagreements, and at least 20 examples in each critical fallback path before reporting its release metric.

Recall is reported, but missed recall is handled through review/abstention rather than weaker evidence gates.

**Implications:** Pause or kill a capability when authorization is absent or withdrawn, tenant isolation or deletion fails, a critical security fixture fails, unsupported claims exceed the gate, fallback cannot be restored, or Q3/Q13 value gates fail. Threshold changes require a recorded rationale and approval from product plus the relevant evaluation, security, privacy, finance, legal, or source authority; they cannot be silently weakened.

## Authority-Bound Decisions Remaining

Only the following remain outside Product Manager authority:

- **Legal/source owner:** any LinkedIn processing exception and every live-source acquisition, storage, derivative, display, retention, and deletion right.
- **Privacy/security:** processor, region, payload, retention, deletion, identity/tenancy, secret custody, and production external-model approval.
- **Finance/product sponsor:** provider selection and the final spend ceiling.
- **Academic/recommendation owner:** reviewed course-skill mappings and any future market effect on deterministic ranking.
- **Release authority:** production go/no-go after the applicable gates have evidence.

Pilot role aliases, geography, seniority, score-display wording, and anonymous catalog priority are ordinary product decisions to settle during backlog refinement; they do not need user escalation unless they change the stated project objective.

# SWE Product Manager: Grilling Round 2 Responses

**Flow ID:** `swe-product-manager`  
**Parent:** parent orchestrator  
**Decision basis:** Round 1 decisions plus verified claims and corrected wording in `research/citation-verification.md`. Numeric operating values below are provisional product targets unless identified as existing constraints; they are not measured results or external facts.

## Q1 - Exact assistant intents and deterministic routing

**Answer: Yes.**

**Rationale:** The six routes match deterministic facts already available in the repository. A broader or model-selected route would make unsupported behavior provider-dependent.

**Concrete default:** Allow only `explain_recommendation`, `explain_readiness_or_prerequisite`, `compare_current_recommendations`, `explain_open_slot`, `show_course_fact`, and `show_reviewed_skill_exposure`. Route from explicit UI context, entity IDs, and deterministic rules before synthesis. Ask one clarification only when two allowlisted routes remain plausible. Otherwise return `unsupported_intent` with the nearest supported actions. Anonymous catalog chat, preference mutation, unreturned alternatives, and general career advice are excluded.

**Implications:** Each intent needs a separate input contract, context builder, deterministic template, limitation set, and abstention test. The model may rephrase the selected route but cannot reroute, widen retrieval, or invent entities.

**Authority flag:** `PM-OWNED SCOPE`; tech lead owns routing implementation. Expansion requires a new product decision and evaluation evidence.

## Q2 - Immutable snapshots and citation semantics

**Answer: Yes.**

**Rationale:** Mutable citations would let old answers silently acquire new premises. Immutable identity preserves what the user actually saw and supports replay and audit.

**Concrete default:** Bind every factual answer span to `answer_version`, immutable `snapshot_id`, `claim_id`, locator, content hash, source/policy version, and observation time. Refreshes create new snapshots, claims, and answer versions. Never substitute current evidence into an old citation. Resolve status as `active`, `superseded`, `stale`, `withdrawn`, or `unavailable`. Display excerpts only where policy permits; a purged or withdrawn premise remains visibly unavailable.

**Implications:** An answer with an unresolved factual citation cannot be reused for a new factual decision and must be regenerated from currently permitted evidence. Storage and deletion designs must preserve non-content tombstones without retaining prohibited source text.

**Authority flag:** `PM-OWNED PRODUCT CONTRACT`; data/source owner approves snapshot publication and retention, legal/source owner controls reproduction rights, and privacy controls private-record retention.

## Q3 - Operator token failure and deterministic fallback

**Answer: Modify. Approve deterministic-only readiness, with measurable breaker defaults owned by operations.**

**Rationale:** The promised token is an environment-scoped operator secret, not a user credential. Model failure must degrade answer style, not remove supported deterministic functions or trigger credential collection.

**Concrete default:** Validate configuration at startup with a secret-free health state. Missing configuration starts as `deterministic_only`. Authentication or revoked-key failure opens the provider circuit immediately and requires revoke/rotate; it is not retried. For transient provider failures, use a provisional breaker of five failures within 60 seconds, open for five minutes, then permit one half-open probe. Honor provider retry guidance for rate limits and make at most the Round 1 call budget. Users receive the prebuilt fallback plus `model_enhancement_unavailable`; no token fragments, prompts, or payloads enter errors or logs.

**Implications:** Alert on authentication failure, spend cutoff, rate-limit saturation, and circuit transitions. Restoring synthesis is an operator action; deterministic routes remain available throughout.

**Authority flag:** `SHARED`; PM owns fallback UX and capability priority, DevOps/security own secret handling and breaker tuning, finance owns spend restoration. Secret safety and deterministic fallback are `NON-WAIVABLE`.

## Q4 - Versioned provider adapter and shadow evaluation

**Answer: Yes.**

**Rationale:** A narrow adapter limits SDK coupling, but providers and model versions are not behaviorally interchangeable. Replacement requires comparative evidence.

**Concrete default:** Support one pilot provider behind separate versioned synthesis and extraction contracts. Normalize request ID, usage, refusal, timeout, finish state, and error class; record provider, endpoint, region, model snapshot, prompt, schema, and adapter version in provenance. Before any provider, endpoint, region, or model change, replay the locked set in shadow mode with no user-visible effect. Graduation requires the existing grounding and citation gates, zero deterministic-contract regressions, zero new critical safety failures, and no material latency or cost regression beyond approved envelopes. These are provisional release gates, not measured performance.

**Implications:** Keep the incumbent path and deterministic fallback until the candidate passes. Add a second adapter only for evidenced continuity or procurement need; do not promise drop-in equivalence.

**Authority flag:** `SHARED`; PM approves user-value tradeoffs, tech lead approves the adapter contract, privacy/security approve provider data flow, finance approves cost, and release authority approves the switch.

## Q5 - Manual-posting origin and rights policy

**Answer: Yes.**

**Rationale:** User submission does not itself prove collection, derivative, retention, or model-processing rights. Documentary proof would be disproportionate for the pilot, so the usable boundary is an affirmative declaration plus fail-closed exceptions.

**Concrete default:** Require confirmation that the user may provide the posting, an origin of `direct_employer`, `approved_provider`, or `other_user_authorized`, and confirmation that it is not LinkedIn-derived. Store the declaration and policy decision. Permit one origin clarification. Reject known LinkedIn origin, unresolved origin after clarification, bulk submissions, and apparent acquisition workarounds. Analysis is private, observed at upload, not fetched, republished, shared, or used for training.

**Implications:** UX must say that the declaration is not a legal warranty and detection is incomplete. A LinkedIn exception cannot be created by changing copy or origin labels.

**Authority flag:** `PM-OWNED PILOT UX`; legal/source owner has `EXCLUSIVE AUTHORITY` over processing exceptions and approved-provider rights. LinkedIn remains blocked without written authorization.

## Q6 - Extraction states, repair, and clarification

**Answer: Modify. Use item states plus a posting-level terminal state.**

**Rationale:** Item-level evidence and normalization can diverge, while the posting still needs one replayable completion result. One repair and one user clarification bound cost and prevent pressure toward invented completeness.

**Concrete default:** Items move through `detected -> evidence_validated -> normalized|ambiguous|unmapped -> accepted|rejected`; `conflicting` may occur before acceptance. The posting ends `completed`, `completed_with_gaps`, `rejected`, or `abstained`. Invoke the model only for unresolved requirement-bearing spans. Allow one schema repair per model call and one user clarification total per posting, limited to provenance, document identity, or material facts the user can know. Accepted requirements require exact evidence, a valid locator, and validated modality.

**Implications:** Clarification cannot solicit employer intent, guessed proficiency, or occupational norms. Implicit, conflicting, unsupported, ambiguous, and unmapped candidates stay visible where useful but cannot become ranking inputs.

**Authority flag:** `PM-OWNED BEHAVIOR`; tech lead owns state-machine integrity, data/domain owners own normalization acceptance, and security owns hostile-content controls.

## Q7 - Reviewer-owned mappings and disclosed gaps

**Answer: Yes.**

**Rationale:** The existing six IDs and seven-course ledger are useful pilot seeds but do not support broad completeness or mastery claims.

**Concrete default:** The academic/domain owner approves course-to-skill links; the data/domain owner approves aliases and taxonomy mappings. Every accepted link stores source excerpt, depth, scope, reviewer, decision date, and version. Preserve `ambiguous` and `unmapped`. Publish role-level denominators for job mentions mapped, accepted mappings reviewed, relevant courses reviewed, and reviewed courses with at least one link. Do not publish a broad skills-gap summary unless the applicable role/course set has a declared coverage threshold approved before evaluation; until calibrated, this threshold remains an open, provisional gate.

**Implications:** A job skill without a reviewed course link is an evidence gap; a course without a reviewed link is unknown. Neither implies irrelevance, mastery, or a new recommendation.

**Authority flag:** `SHARED`; PM owns disclosure and feature scope, academic/domain owner has `EXCLUSIVE AUTHORITY` over course evidence, and data/domain owner has `EXCLUSIVE AUTHORITY` over canonical mappings.

## Q8 - One-hour successful deletion and 24-hour interrupted cleanup

**Answer: Yes.**

**Rationale:** Successful synchronous analysis does not justify retaining raw source content, and interrupted work needs a bounded cleanup backstop. Private derivatives remain source-derived and user-linked.

**Concrete default:** Assign a server-generated, server-scoped analysis ID. Delete raw text within one hour after successful analysis. On user deletion, remove raw and derived private records immediately as one operation. Delete all raw and derived private records for failed or interrupted work within 24 hours. Keep conversations unsaved. Retain content-free operational metadata for 30 days, limited to opaque IDs, versions, timestamps, states, counts, and deletion outcome; retain no prompt, source text, answer, student identifier, or secret.

**Implications:** Until authenticated server identity and tenant isolation exist, supplied-posting analysis is limited to controlled users with approved server-side scope. Save/export requires a new retention and rights decision.

**Authority flag:** `SHARED`; PM sets deletion-by-default, privacy/legal approve the schedule and metadata purpose, security/tech prove deletion and isolation. Selective deletion and tenant isolation are `NON-WAIVABLE`.

## Q9 - Adapter versus ingestion, scheduler, and publication ownership

**Answer: Yes.**

**Rationale:** Source contracts differ, but scheduling, retries, provenance, and kill behavior must remain uniform and auditable.

**Concrete default:** A source adapter owns authentication, source-field translation, contract-bound limits, lifecycle signals, attribution, and deletion hooks. The platform ingestion service owns registered jobs, idempotency keys, leases, queues, retries, provenance, and kill switches. The scheduler invokes only registered source-policy/query pairs. A named data/source owner approves publication after policy, freshness, quality, and coverage checks. Begin as boundaries inside the monolith; deploy an isolated worker before authorized network fetching or scheduling.

**Implications:** Adapters cannot self-schedule or self-publish. The ingestion service cannot invent source semantics, and a user URL can never create a source registration.

**Authority flag:** `SHARED`; tech lead owns architecture, data operations owns ingestion, data/source owner owns publication, and legal/source owner owns permitted access.

## Q10 - Objective graduation into shadow ranking

**Answer: Modify. Approve option C with explicit entry and exit gates.**

**Rationale:** Read-only value, lawful derivatives, reviewed mappings, and stable snapshots are prerequisites, not automatic permission to alter ranking.

**Concrete default:** Entry to ranking shadow mode requires all of the following: the Round 1 read-only crossover gate passes; source rights expressly cover ranking derivatives; both pilot roles meet predeclared publishable coverage; applicable mappings and course links are approved; no stale, implicit, conflicting, ambiguous, or unmapped evidence enters weights; and the candidate is deterministic and versioned. Shadow exit requires locked-task improvement over the static baseline, no eligibility or slot-contract change, no unacceptable all-six-career, diversity, stability, or fairness regression under predeclared tolerances, and side-by-side explanations. Exact effect-size and non-inferiority tolerances are provisional and must be fixed before shadow results are inspected.

**Implications:** No LLM scoring or separate unreviewed market bonus. Ranking has an independent kill switch and immediate static fallback. A failed gate returns the capability to read-only context.

**Authority flag:** `SHARED`; recommendation owner approves formula and tolerances, PM approves value tradeoff, legal/source owner approves derivative use, and release authority approves rollout. PM cannot waive any of these.

## Q11 - High-risk and random audit sampling

**Answer: Yes.**

**Rationale:** Locked sets test known cases; risk-based and random production sampling detect novel templates, rare high-impact paths, and silent drift.

**Concrete default:** During the pilot, review 100% of new source templates, new mapping categories, conflicts, implicit or uncertain candidates, citation failures, and ranking-change cases. Randomly sample 10% of accepted extraction and assistant outputs in each weekly cohort. Dual-review release-gate samples and adjudicate every disagreement. The 10% rate is provisional; reduction requires four consecutive weekly cohorts meeting gates with no critical defect, and any critical incident or statistically material drift returns sampling to the prior higher rate.

**Implications:** Use only redacted or authorized evidence. Record defect class, severity, affected versions, correction, replay scope, and kill decision.

**Authority flag:** `SHARED`; PM owns severity and continuation policy, evaluation owns sampling, domain owners adjudicate content, and security/privacy own their incident classes.

## Q12 - Comprehension and over-trust user tests

**Answer: Yes.**

**Rationale:** Satisfaction can coexist with harmful misunderstanding. The feature succeeds only when users identify evidence classes, limitations, and fallback correctly.

**Concrete default:** Retain the Round 1 moderated crossover with at least 20 target users and add scored tasks for citation selection, fact-versus-generated advice, unknown/stale evidence, exposure-versus-mastery, provider fallback, and readiness-versus-registration eligibility. Use a provisional pass gate of at least 80% correct on each critical distinction and no more than 5% unsupported takeaways overall; any critical misconception repeated by two or more participants blocks progression pending correction and retest. Include keyboard/screen-reader sessions and interview every participant who forms an unsupported takeaway.

**Implications:** High usefulness scores do not offset systematic over-trust. Report confidence intervals and qualitative causes; do not silently tune thresholds after results are visible.

**Authority flag:** `SHARED`; research owns protocol and interpretation, accessibility owner approves accessibility coverage, and PM owns continuation. Safety/privacy findings can independently block release.

## Q13 - Staged cohorts and rollback progression

**Answer: Modify. Approve evidence-bound cohorts with provisional minimum windows.**

**Rationale:** Introducing model synthesis, private uploads, live sources, and ranking together would make failures hard to attribute and rollback unsafe.

**Concrete default:** Cohort 0 is internal staff using synthetic or legally retained fixtures. Cohort 1 is supervised target students using deterministic Stage 1. Cohort 2 is the same controlled scope with model synthesis. Cohort 3 adds supplied-posting analysis. Live shared snapshots and ranking each receive later independent cohorts. Each cohort runs for at least five operating days and the required task sample, whichever is longer; the supervised value study still requires at least 20 target users. Entry requires prior gates; exit requires its acceptance, audit, comprehension, deletion, and operations evidence. Every capability has its own kill switch and deterministic rollback.

**Implications:** No supplied-posting analysis for unauthenticated general traffic. Never combine first model use, first private upload, first live source, and first ranking influence in one cohort.

**Authority flag:** `SHARED`; PM proposes cohort scope, privacy/security approve exposure, and release authority has `EXCLUSIVE AUTHORITY` to advance or roll back.

## Q14 - Content-free observability

**Answer: Yes.**

**Rationale:** Operational diagnosis requires versioned events and outcomes, not sensitive content. Body logging would conflict with the minimization and deletion posture.

**Concrete default:** Record only opaque non-content IDs and versions, routed intent, fallback reason, claim/citation counts, validation outcome, provider/model latency and cost, extraction state, mapping status, deletion timestamps/outcome, source freshness, queue depth, circuit state, and kill-switch changes. Exclude prompt bodies, source text, generated answers, student identifiers, credentials, database URLs, signed URLs, and raw payloads from general logs, metrics, traces, errors, dead letters, and support exports. Alert triggers must include authentication failure, budget cutoff, circuit open, deletion-SLA breach, critical validation breach, stale-source publication, and queue saturation; every alert names a responder and runbook.

**Implications:** Debug replay, if ever needed, is a separately approved store with separate access and retention, not an observability shortcut. Telemetry without an owner cannot satisfy a gate.

**Authority flag:** `SHARED`; backend owns routing/validation, data operations owns ingestion/freshness, DevOps owns provider/cost/queue, privacy owns deletion evidence, and product/evaluation owns usefulness and over-trust metrics.

## Q15 - Domain-specific authority matrix and non-waivable stops

**Answer: Yes.**

**Rationale:** Product can decide scope and value but cannot manufacture legal rights, academic validity, security evidence, privacy approval, budget, or release authorization.

**Concrete default:** Record each approval with capability scope, evidence, versions, owner, decision time, expiry or revisit trigger, and dependencies. Product approves scope, priority, UX contract, and value gates. Tech lead approves architecture and deterministic contracts. Academic/recommendation owner approves course evidence and ranking policy. Data/source owner approves canonical mappings and snapshot publication. Legal/source owner approves acquisition, storage, derivatives, model use, display, retention, and deletion rights. Privacy/security approve processor, payload, identity/tenancy, retention, deletion, secrets, and controls. Finance approves spend. Release authority approves cohort progression and production go/no-go.

**Implications:** Silence, another domain's approval, or a successful demo is not approval. Rejection or expiry disables the dependent capability when isolation is proven; otherwise the broader release stays blocked.

**Authority flag:** `PM-OWNED ONLY FOR PRODUCT DOMAIN`. Source authorization, authenticated tenant isolation for private multi-user data, selective deletion, secret safety, deterministic fallback, and zero critical security failures are `NON-WAIVABLE RELEASE STOPS`. No Product Manager override exists.

# SWE Product Manager: Grilling Round 3 Responses

**Flow ID:** `swe-product-manager`  
**Parent:** parent orchestrator  
**Decision basis:** Round 1 and Round 2 decisions, repository evidence, and only claims permitted or corrected by `research/citation-verification.md`. The scope and operating rules below are product defaults, not measured market facts or external approvals.

## Q1 - Narrow English-language Singapore Stage 2 pilot

**Answer: Yes.**

**Rationale:** The repository's reviewed course-skill evidence is limited to Software Engineer and Data Engineer pathways. Restricting language, geography, seniority, and aliases prevents title expansion from implying unsupported occupation coverage. O*NET and ESCO may supply labelled taxonomy context, but the verified sources describe occupational/classification data rather than a documented live-vacancy feed, and they do not establish Singapore employer requirements.

**Concrete default:** Limit Stage 2 to English-language evidence for entry-level or graduate Singapore roles in two canonical targets: `software_engineer` and `data_engineer`. For `software_engineer`, allow only `software engineer`, `software developer`, and explicit `junior` or `graduate` variants. For `data_engineer`, allow only `data engineer` and explicit `junior` or `graduate` variants. Exclude internships; frontend, backend, full-stack, analytics engineer, machine-learning engineer, and data scientist roles; and architect, lead, staff, principal, manager, or other senior variants. Unsupported or ambiguous titles return a scope message and are not coerced to a pilot role.

**Implications:** Fixtures, taxonomy mappings, evaluation strata, UI choices, and reporting must use the same allowlist. Taxonomy context must be labelled external context, not Singapore market demand or individual-employer evidence. Alias expansion requires reviewed mapping evidence and a new scoped product decision.

**Authority:** `PM-OWNED PILOT SCOPE`; the data/domain owner approves aliases and taxonomy mappings, the academic/domain owner approves course-skill links, and research/evaluation owns representative test coverage. Legal, privacy, security, and release approvals remain independently required for actual pilot operation.

## Q2 - Ephemeral supplied-posting analysis

**Answer: Yes.**

**Rationale:** Retaining an answer after its supporting private evidence is deleted would break the citation contract, while retaining derived claims would preserve source-derived, user-linked data. The current repository has no authenticated server identity or production tenant boundary, so durable history and export are outside the approved Stage 2 posture.

**Concrete default:** Give each supplied posting a server-scoped analysis ID and visible expiry. After successful analysis, keep raw input, extracted claims, citations, and the rendered result available for no more than one hour, then clear and delete them together. A user deletion request clears and deletes them immediately. Failed or interrupted work retains no user-visible result and remains subject to the existing 24-hour absolute cleanup backstop. Stage 2 provides no history, save, share, or export; revisiting requires a new authorized submission and analysis ID. Retain only the previously approved content-free operational metadata.

**Implications:** Citation resolution is guaranteed only during the active analysis window. Expiry and deletion must remove raw and derived private records as one operation and make them inaccessible. Any durable result, history, save, share, or export feature requires a separate rights, privacy, authenticated-tenancy, retention, deletion, and product decision.

**Authority:** `SHARED`; PM owns the ephemeral UX and feature exclusions, privacy/legal approve the purpose and schedule, and security/tech must prove tenant scope and deletion behavior. Selective deletion and tenant isolation are `NON-WAIVABLE RELEASE STOPS`; release authority decides cohort exposure.

## Q3 - Item-level evidence without aggregate gap claims

**Answer: Yes.**

**Rationale:** The current course-skill ledger is intentionally narrow and does not establish a representative denominator for broad role-level skills-gap, fit, coverage, or market-demand conclusions. Treating an absent reviewed link as a student or course deficiency would convert missing evidence into an unsupported claim.

**Concrete default:** Stage 2 shows only each explicit supplied-posting requirement or clearly labelled taxonomy concept, its exact evidence and modality where applicable, raw mention, mapping state, taxonomy and mapper version, reviewed course-exposure links, and `no reviewed course link`, `ambiguous`, `unmapped`, or `unknown` where evidence ends. Omit aggregate skills-gap summaries, fit or coverage scores, missing-skills rankings, frequency, trend, and market-demand claims.

**Implications:** The UI and evaluations must preserve item-level provenance and distinguish employer evidence from taxonomy context. No reviewed course link means only that the reviewed ledger contains no supported link; it does not mean no learning, course irrelevance, lack of mastery, or student deficiency. Aggregate claims require a later decision with predeclared role/course coverage denominators, source rights, thresholds, and validation fixed before results are inspected.

**Authority:** `PM-OWNED STAGE 2 CLAIM SCOPE`; the academic/domain owner has `EXCLUSIVE AUTHORITY` over course-skill evidence, the data/domain owner over canonical mappings, and legal/source owners over permitted source-derived claims. Product cannot waive missing evidence into an aggregate claim.

## Q4 - Independent Stage 2 mode evaluation

**Answer: Yes.**

**Rationale:** Role-target mode and supplied-posting mode rely on different evidence and create different misunderstanding and operational risks. Success in taxonomy-backed role exploration cannot validate private posting extraction, citation, and deletion; success on supplied postings cannot establish that taxonomy context is useful or correctly understood.

**Concrete default:** Evaluate `role_target` and `supplied_posting` as separate capabilities using their own locked tasks, task-success comparison, critical-distinction comprehension results, defect and unsupported-takeaway records, operational gates, and continuation decision. Apply the already approved usefulness and calibrated-trust thresholds to each mode separately. Do not average results or allow one mode to satisfy the other's gate.

**Implications:** Either mode may release, pause, be removed, or remain deterministic-only without forcing the same outcome for the other, provided capability isolation is proven. Each mode needs an independent kill switch, evidence record, and rollback path. Shared components may continue only where their own gates remain satisfied.

**Authority:** `SHARED`; research/evaluation owns the protocols and confidence-aware interpretation, PM owns each continuation decision, tech/security/privacy own mode-specific operational evidence, and release authority has `EXCLUSIVE AUTHORITY` over cohort progression. Safety, privacy, source-rights, or deletion failures can independently stop the affected mode.
