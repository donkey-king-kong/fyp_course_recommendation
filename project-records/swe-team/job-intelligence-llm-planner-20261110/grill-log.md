# Round 1

❓ **Q1 - One product, staged capabilities**: Product Manager, will you approve one course-recommendation product with staged assistant and job-context capabilities, rather than promising a single all-at-once “AI course and career adviser” or launching job intelligence as a separate product? The options are: (A) one bundled launch, which is simpler to market but couples assistant, source-rights, extraction, privacy, and market-data risk; (B) a separate job product, which isolates operations but fragments the student journey and duplicates the skill bridge; or (C) one product with independently gated stages: deterministic assistant contract, grounded course assistant, supplied-posting and taxonomy context, authorized shared snapshots, then separately evaluated deterministic market influence.

➡️ **Yes: approve option C.** Treat the stages as separately releasable capabilities with independent kill switches and success tests. Do not market later-stage market intelligence as present in the first release.

---

❓ **Q2 - Primary persona and first job to be done**: Product Manager, will you make the primary user an NTU computing student who already has a generated roadmap or recommendation and needs to understand and compare it, with role or posting context as a secondary job? The alternatives are: (A) lead with broad prospective-student catalog chat, which increases reach but lacks profile evidence; (B) lead with labor-market exploration, which depends on source coverage and a mature skill ontology; or (C) lead with “help me understand the recommendation I already received, its prerequisites, tradeoffs, and limitations,” then add “relate it to a target role or supplied posting.”

➡️ **Yes: approve option C.** Keep anonymous catalog help and generalized career exploration secondary until the primary explanation journey proves useful.

---

❓ **Q3 - Read-only value hypothesis**: Product Manager, will you explicitly test whether explanation and evidence are valuable without changing course ranking? The options are: (A) require job evidence to rerank recommendations immediately, which creates visible impact but confounds evidence quality with recommendation policy; (B) show read-only role/posting evidence beside unchanged recommendations, which is safer and independently testable but may feel less magical; or (C) omit job context until ranking is possible, which avoids a weak feature but delays learning.

➡️ **Yes: approve option B as the Stage 2 hypothesis.** The product must earn the right to influence ranking by first showing that students can understand skill evidence, identify unknowns, and make a better-informed comparison. If read-only context does not measurably improve those tasks, stop Stage 2 rather than forcing it into ranking.

---

❓ **Q4 - Assistant authority and answer boundary**: Product Manager, will you constrain the assistant to explain, compare, translate, and suggest a next step from supplied claims, while the deterministic backend remains the sole authority for readiness, prerequisites, scoring, ranking, and slot assignment? The alternatives are: (A) allow the model to infer or override those decisions for a more conversational experience; (B) allow hidden model-triggered recalculation; or (C) give the model no mutation or ranking tools, label generated advice separately, expose source conflicts, and require an explicit user action before any future preference change invokes the existing recommender.

➡️ **Yes: approve option C.** The assistant must not claim registration eligibility, mastery, employability, employer intent, current demand, or an optimal course. Expose score components only as clearly labelled explanations of existing backend behavior, not as objective quality measures.

---

❓ **Q5 - LinkedIn exclusion and source strategy**: Product Manager, will you exclude LinkedIn collection and LinkedIn-derived datasets from the product unless written authorization covers this exact use? The documented self-service permissions do not include job-search inventory retrieval; the documented Job Posting API is outbound, Apply Connect is an ATS workflow rather than a general search feed, and LinkedIn prohibits unauthorized automated collection. The options are: (A) scrape public or logged-in pages; (B) buy or accept indirectly scraped LinkedIn data; (C) wait for written LinkedIn authorization while using pinned occupational classifications, rights-checked user-supplied postings, and later a contract-approved source such as Adzuna, USAJOBS, or authorized employer-scoped Greenhouse/Lever data.

➡️ **Yes: approve option C.** Treat LinkedIn as a non-blocking partnership track, not an MVP dependency or an acquisition workaround. Do not claim live market coverage from O*NET or ESCO because they are occupational classifications, not documented vacancy feeds.

---

❓ **Q6 - User-supplied URL, text, and file behavior**: Product Manager, will you limit Stage 2 input to pasted text and approved text/PDF uploads, with a provenance declaration, private on-demand analysis, immediate deletion, and rejection of known LinkedIn origin? The alternatives are: (A) accept arbitrary URLs and fetch them, which is convenient but opens source-rights, SSRF, hostile-content, freshness, and retention problems; (B) accept any pasted content regardless of origin, which is easy to bypass and turns the user into an ingestion proxy; or (C) do not fetch URLs, reject declared or detected LinkedIn origin, parse supported text/files under size and content limits, and treat the result as observed-at-upload rather than current.

➡️ **Yes: approve option C.** A URL may be retained only as user-supplied provenance text; it must not trigger retrieval. Unsupported, encrypted, binary, oversized, malicious, or origin-ambiguous inputs should fail closed with a bounded explanation.

---

❓ **Q7 - BYOK timing and token custody**: Product Manager, will you defer bring-your-own-key until a validated user need outweighs the secret-custody and support burden? The options are: (A) browser-stored or direct browser-to-provider keys, which reduce platform spend but expose credentials and fragment controls; (B) persist user keys server-side at launch, which creates immediate custody, tenancy, revocation, and breach obligations; or (C) use a platform-managed server credential for the initial release, then evaluate delegated authorization or customer-vault references, with session-only server memory as the first fallback before stored tenant secrets.

➡️ **Yes: approve option C.** No key may enter chat, URLs, cookies, localStorage, analytics, logs, or ordinary configuration. If persistent BYOK is later approved, it requires a separate credential screen, tenant-scoped secret storage, non-sensitive fingerprints, immediate revoke/replace, and explicit disclosure that the service can use the decrypted key.

---

❓ **Q8 - Deterministic versus LLM extraction**: Product Manager, will you make deterministic parsing and evidence validation the default, using an LLM only for unresolved requirement-bearing prose? The options are: (A) LLM-first extraction, which handles varied prose quickly but increases unsupported inference, drift, cost, and prompt-injection exposure; (B) deterministic-only extraction, which is reproducible but weak on ambiguous prose; or (C) a hybrid where deterministic code owns document structure, typed fields, offsets, quotes, hashes, schema checks, negation checks, and policy, while the LLM may only propose bounded semantic interpretations that pass application validation.

➡️ **Yes: approve option C.** Skip the model when deterministic output is complete. Give extraction models no browsing, credentials, writes, ranking authority, or arbitrary tools; unsupported semantics must abstain rather than be repaired into apparent certainty.

---

❓ **Q9 - Missing, vague, and conflicting requirements**: Product Manager, will you prefer explicit unknowns over a complete-looking answer? The options are: (A) infer conventional requirements from role norms, which feels useful but misstates employer evidence; (B) suppress ambiguous items, which produces cleaner output but hides uncertainty; or (C) preserve exact vague wording, mark missing fields unknown, retain conflicting assertions side by side, distinguish required/preferred/optional/unclear/negated alternatives, and show unmapped skills or absent course links without inventing a fit.

➡️ **Yes: approve option C.** Permit at most one targeted clarification when user input can actually resolve ambiguity; otherwise fall back through exact evidence, labelled taxonomy context, a concrete human/source check, and finally abstention.

---

❓ **Q10 - Taxonomy provenance and canonical skills**: Product Manager, will you treat the internal canonical skill registry as a reviewed bridge rather than a universal truth? The options are: (A) use model-generated skill labels ad hoc, which is fast but not replayable; (B) adopt one external taxonomy as authoritative for every market and course, which simplifies IDs but imports geographic and semantic mismatch; or (C) preserve raw mentions, pin taxonomy releases, use O*NET for U.S. occupation context, ESCO for European/multilingual concepts, ISCO for international roll-up, and maintain reviewed internal IDs and aliases for course links and vendor skills.

➡️ **Yes: approve option C.** Keep the existing six pilot skill IDs only as provisional seeds. Require named reviewers, versioned mapping decisions, exact/alias/broader/narrower/ambiguous/unmapped states, and precision-gated automation before expanding claims beyond reviewed course evidence.

---

❓ **Q11 - On-demand versus scheduled ingestion**: Product Manager, will you separate private on-demand analysis from later shared scheduled market ingestion? The options are: (A) schedule broad collection immediately, which promises freshness but is blocked by source rights and operations; (B) let users trigger arbitrary live fetches, which creates an ungoverned scraping path; or (C) keep supplied-posting analysis private and on demand, keep course recommendation recalculation on demand through the existing backend, and introduce scheduled shared snapshots only after one source is contract-approved, with any later refresh using the same governed pipeline.

➡️ **Yes: approve option C.** Ordinary users must not create cron schedules, fan out queries, or bypass source policy. Scheduled and approved on-demand source jobs must share quotas, provenance, deduplication, lifecycle rules, and kill switches.

---

❓ **Q12 - Freshness promise**: Product Manager, will you make freshness an evidence property instead of a blanket “current jobs” promise? The options are: (A) present the latest stored result as current until replaced; (B) hide timestamps to reduce interface complexity; or (C) label supplied postings as observed at upload, show pinned taxonomy versions, show observation windows and lifecycle state for authorized snapshots, warn or withdraw stale evidence under source-specific SLAs, and prohibit current-demand or trend wording without authorized longitudinal coverage.

➡️ **Yes: approve option C.** Do not choose a universal refresh interval in this round. Set cadence and stale thresholds per approved source contract, user value, rate limits, and measured update behavior; when evidence expires, fall back to labelled static role context or state that current evidence is unavailable.

---

❓ **Q13 - Cost and latency envelope**: Product Manager, will you require the model to justify its incremental delay and cost over deterministic answers? The options are: (A) optimize for answer richness with open-ended tokens and retries; (B) remove the model entirely; or (C) generate a deterministic fallback first, call one allowlisted model only for bounded synthesis, cap input/output/retries and per-user/global spend, target Stage 1 p95 at no more than 8 seconds with the model and 1 second for fallback under the agreed pilot load, and serve fallback on timeout, outage, validation failure, or budget exhaustion.

➡️ **Yes: approve option C as a provisional pilot envelope.** Measure task-success uplift against deterministic-only answers. If the model does not produce a material usefulness gain, or cannot meet the agreed latency and per-answer cost ceiling, remove model synthesis from that intent instead of relaxing controls.

---

❓ **Q14 - Privacy, retention, and conversation state**: Product Manager, will you launch with data minimization and no persistent conversation history? The options are: (A) send raw curriculum, transcript, posting, and history for maximum context; (B) persist chat and uploads in browser or server storage before authenticated tenancy and deletion exist; or (C) send only bounded structured course/result facts, exclude student IDs and raw academic documents, keep conversation persistence off, process supplied postings privately, offer immediate deletion, and delete raw posting text and derived private records within a disclosed short window no longer than 24 hours unless a stricter source or processor rule applies.

➡️ **Yes: approve option C.** Retain sanitized operational metadata by default, not prompt or response bodies. Any later persistence requires authenticated server identity, tenant scoping, export, selective deletion, explicit retention purposes, and processor terms covering region, retention, and deletion.

---

❓ **Q15 - Evaluation gates and kill criteria**: Product Manager, will you make release and continuation contingent on locked, human-reviewed evidence rather than demo quality? The alternatives are: (A) ship after qualitative internal review; (B) optimize a single aggregate score; or (C) require intent-stratified fixtures, adversarial cases, human task testing, and hard gates: every displayed factual claim has resolvable provenance; zero assistant-caused ranking/readiness/slot mutations; at least 99% factual-claim precision and required/preferred precision on accepted outputs; at least 99.5% citation resolution; automatic taxonomy mapping only after at least 98% precision by category; zero critical prompt-injection policy breaches, cross-user access, or secret leakage; and verified fallback, deletion, budget, and latency behavior.

➡️ **Yes: approve option C as the initial gate set, subject to calibration before release but not silent weakening.** Kill or pause a capability when source authorization is absent or withdrawn, read-only job context fails to improve the target task, model synthesis fails to beat deterministic answers enough to justify cost and latency, unsupported claims exceed the gate, deletion or tenant isolation fails, or the static deterministic fallback cannot be restored immediately.

# Round 2

❓ **Q1 - Exact assistant intents and deterministic routing**: Product Manager, will you freeze the Stage 1 intent allowlist to `explain_recommendation`, `explain_readiness_or_prerequisite`, `compare_current_recommendations`, `explain_open_slot`, `show_course_fact`, and `show_reviewed_skill_exposure`, with deterministic routing before any model call? The options are: (A) let the model infer and answer any course question, which feels flexible but creates unsupported routes; (B) use model intent classification for the allowlist, which handles varied wording but makes fallback provider-dependent; or (C) use explicit UI context plus deterministic rules to select one intent and required entity IDs, ask a clarification only when two supported routes remain plausible, and return `unsupported_intent` rather than letting synthesis widen scope. Under C, anonymous catalog chat stays P1, preference mutation is excluded from the pilot, and a comparison is limited to recommendations already in the current result.

➡️ **Yes: approve option C and this exact Stage 1 allowlist.** Each route must have its own context builder, deterministic template, required inputs, limitations, and abstention behavior. The model may phrase a routed answer but may not choose a different route, retrieve extra entities, or convert an unsupported request into advice.

---

❓ **Q2 - Snapshot identity and citation semantics**: Product Manager, will you define citations as immutable references to the exact evidence version used to generate an answer, rather than links to whatever record is current at display time? The options are: (A) cite mutable URLs or course records, which is simple but makes old answers silently change; (B) copy excerpts into each answer, which preserves display but duplicates source-controlled content; or (C) assign immutable snapshot and claim IDs, bind every citation to a locator and content hash, resolve it against the retained permitted version, and show `superseded`, `stale`, `withdrawn`, or `unavailable` without substituting newer evidence. Source text is displayed only when policy permits; otherwise the UI shows structured attribution and the reason evidence cannot be reproduced.

➡️ **Yes: approve option C.** A later source refresh creates new claims and can trigger a new answer version; it never rewrites an old answer's premises. Treat a broken locator, purged snapshot, or policy-withdrawn excerpt as a visible loss of evidence and make the answer non-reusable for factual decisions.

---

❓ **Q3 - Operator credential and provider-failure behavior**: Product Manager, will you treat the promised API token as an environment-scoped operator secret whose absence or failure disables only model synthesis? The options are: (A) block the assistant until a token works; (B) ask users to supply a replacement key; or (C) validate provider configuration at startup and through a secret-free health signal, keep the application ready in deterministic-only mode when the key is absent, revoked, quota-exhausted, rate-limited, or the provider is unavailable, open a circuit breaker after bounded failures, and require an operator to restore service. Authentication failures revoke/rotate rather than retry; rate limits honor provider guidance; no failure exposes token fragments or raw payloads.

➡️ **Yes: approve option C.** Users receive the already-generated fallback plus a concise `model_enhancement_unavailable` state, not a credential prompt or repeated provider calls. Alert operators on authentication failure, spend cutoff, failure-rate breach, or circuit state, while preserving all deterministic assistant routes.

---

❓ **Q4 - Model and provider portability**: Product Manager, will you make the application contract provider-neutral while accepting that prompts and evaluations remain model-specific? The options are: (A) bind domain services directly to one SDK, which is fastest initially but spreads provider semantics; (B) promise interchangeable providers, which understates schema, refusal, token, retention, and quality differences; or (C) place one narrow adapter behind versioned synthesis and extraction contracts, normalize request IDs, usage, refusal, timeout, and error classes, store provider/model version in provenance, and require locked shadow evaluation before switching provider, endpoint, region, or model snapshot.

➡️ **Yes: approve option C.** Support one provider in the pilot, keep deterministic behavior independent of it, and add a second adapter only for a real continuity or procurement need. Portability means bounded replacement cost and comparable evidence, not zero-effort equivalence.

---

❓ **Q5 - Manual-posting origin and rights policy**: Product Manager, will you require an affirmative provenance declaration on every supplied posting and reject unresolved origin rather than treating upload as permission? The options are: (A) accept any text because the user supplied it; (B) demand documentary proof, which is strong but unusable for students; or (C) ask the user to confirm they may provide it, choose an origin category, and confirm it is not LinkedIn-derived; store the declaration and policy decision; ask one origin clarification if ambiguous; reject known LinkedIn origin, unknown-after-clarification origin, bulk submissions, and apparent acquisition workarounds. Do not claim the declaration is a legal warranty or that detection is complete.

➡️ **Yes: approve option C for the pilot.** Allow `direct_employer`, `approved_provider`, and `other_user_authorized` origins only, all for private analysis without fetching, republication, sharing, or training. Any LinkedIn exception remains a separate legal/source-owner decision and cannot be created through UX wording.

---

❓ **Q6 - Extraction state machine and clarification budget**: Product Manager, will you make extraction a replayable state machine with one user clarification total per supplied posting? The options are: (A) repeatedly ask until the record looks complete; (B) silently choose the most likely interpretation; or (C) move each item through `detected -> evidence_validated -> normalized|ambiguous|unmapped -> accepted|rejected`, with `conflicting` available before acceptance; invoke the model only for unresolved requirement-bearing spans; allow one schema repair; and ask one user clarification only when it can resolve provenance, document identity, or a material ambiguity the user can actually know. All other uncertainty remains explicit or abstains.

➡️ **Yes: approve option C.** The clarification cannot solicit missing employer intent, guessed proficiency, or occupational norms. Accepted requirements need exact evidence and validated modality; implicit, conflicting, or unsupported candidates cannot become ranking inputs.

---

❓ **Q7 - Canonical mapping governance and course-evidence gaps**: Product Manager, will you keep the six current skill IDs as a narrow pilot namespace and block broad skills-gap claims until the course ledger is independently reviewed and coverage is disclosed? The options are: (A) auto-expand IDs and course links from model output, which improves apparent coverage but creates unreviewed facts; (B) hide unmapped jobs/courses, which makes the feature look complete; or (C) appoint an academic/domain owner for course-to-skill links and a data/domain owner for aliases, require source excerpt, depth, scope, reviewer, decision date, and version for every accepted link, preserve `ambiguous` and `unmapped`, and publish coverage denominators by role and course set. The existing seven-course ledger remains author-reviewed evidence, not independent validation.

➡️ **Yes: approve option C.** In the pilot, a job skill without a reviewed course link is shown as an evidence gap, and a course without a reviewed skill link remains unknown. Do not infer irrelevance, mastery, or a new recommendation; pause role-level gap summaries when reviewed course coverage is too sparse to support them.

---

❓ **Q8 - Private analysis lifecycle**: Product Manager, will you use deletion-by-default for supplied postings and every private derivative? The options are: (A) retain extracted results after raw text deletion, which improves convenience but preserves source-derived and user-linked data; (B) keep everything only in browser memory, which avoids server persistence but cannot support bounded asynchronous processing or deletion evidence; or (C) create a server-generated analysis ID with tenant/session scope, delete raw text within one hour after successful analysis, delete raw and derived private records immediately on request and together by default, enforce a 24-hour absolute cleanup for interrupted work, retain only content-free operational metadata for 30 days, and keep conversations unsaved. Browser `studentId` is not an authorization key.

➡️ **Yes: approve option C.** Until authenticated server identity exists, limit the pilot to controlled users with an approved server-side scope; do not expose persistent private analysis to general multi-user traffic. Any save/export feature requires a later privacy decision, source-compatible rights, authenticated tenancy, and a separate retention schedule.

---

❓ **Q9 - Source adapter, scheduler, and publication ownership**: Product Manager, will you keep source-specific access in adapters while one platform ingestion service owns scheduling and one data owner controls publication? The options are: (A) let each adapter schedule, normalize, and publish itself, which is fast per source but duplicates governance; (B) put source logic in a generic crawler, which centralizes operations but erases contract-specific behavior; or (C) make adapters own authentication, source fields, terms-bound limits, lifecycle signals, attribution, and deletion hooks; make the ingestion service own idempotent jobs, leases, queues, retries, provenance, and kill switches; and make a named data/source owner approve a snapshot for student-visible use after quality and policy checks.

➡️ **Yes: approve option C.** Begin inside the FastAPI monolith as separate service and adapter boundaries; deploy an isolated worker only when authorized network fetching or scheduling begins. The scheduler may invoke only registered source-policy/query pairs and can never turn a user URL into a new source.

---

❓ **Q10 - Graduation of job evidence into ranking**: Product Manager, will you require a separate ranking change proposal after read-only Stage 2 succeeds, rather than treating accumulated job evidence as automatic permission to influence recommendations? The options are: (A) add a market bonus as soon as snapshots exist, which creates visible impact but risks double counting and unstable policy; (B) never use market evidence in ranking; or (C) permit graduation only when the Q3 read-only user gate passes, source rights cover ranking derivatives, canonical mappings and course evidence are approved, snapshot coverage is publishable for both pilot roles, and a versioned deterministic candidate policy beats the static baseline on locked task outcomes without unacceptable all-six-career, eligibility, diversity, stability, or fairness regressions.

➡️ **Yes: approve option C.** The recommendation owner must approve the exact formula and thresholds, product must approve the user tradeoff, and release authority must approve rollout evidence. Ship it behind an independent kill switch with side-by-side explanations, shadow results first, no LLM scoring, no implicit requirements, no stale evidence, and immediate reversion to the static mapping.

---

❓ **Q11 - Audit sampling and adjudication**: Product Manager, will you add risk-based human sampling on top of the locked evaluation sets? The options are: (A) review only failures reported by users; (B) review a uniform tiny sample, which is easy but can miss rare high-impact paths; or (C) review 100% of new source templates, new mapping categories, conflicts, implicit/uncertain candidates, citation failures, and ranking-change cases during pilot, plus a random 10% of accepted extraction and assistant outputs per weekly cohort, with dual review for release-gate samples and adjudication of disagreements. Sampling rates may decrease only after a recorded stable window and may increase automatically on drift or incidents.

➡️ **Yes: approve option C as a provisional operating policy.** Audits must use redacted or properly authorized evidence, record defect class and affected versions, and feed correction, replay, and kill decisions. Product owns severity definitions; evaluation owns sampling; domain owners adjudicate content; security/privacy review their incident classes.

---

❓ **Q12 - User testing beyond the read-only value gate**: Product Manager, will you test comprehension and calibrated trust, not satisfaction alone? The options are: (A) rely on usefulness ratings; (B) measure task completion without checking misconceptions; or (C) retain the Round 1 moderated crossover gate and add scored tasks for choosing the supporting citation, distinguishing recommendation fact from generated advice, identifying unknown or stale evidence, interpreting exposure versus mastery, recovering from provider fallback, and understanding that readiness is not registration eligibility. Include accessibility sessions and interview users who form unsupported takeaways.

➡️ **Yes: approve option C.** A capability fails even with high satisfaction if users systematically over-trust taxonomy context, stale postings, course-skill exposure, or generated advice. Research owns the protocol and confidence-aware interpretation; product owns the continuation decision and must record any threshold change.

---

❓ **Q13 - Rollout cohorts and rollback progression**: Product Manager, will you roll out by evidence boundary rather than percentage traffic alone? The options are: (A) release all Stage 1 and Stage 2 features to every user after offline gates; (B) use an ordinary percentage rollout that mixes users and evidence modes; or (C) progress through internal staff on synthetic/retained fixtures, supervised target students on deterministic Stage 1, the same controlled cohort with model synthesis, and only then a supplied-posting cohort; keep live shared snapshots and ranking in later independent cohorts. Each cohort has an observation window, entry/exit evidence, capability-specific kill switch, and deterministic rollback.

➡️ **Yes: approve option C.** Do not expose supplied-posting analysis to unauthenticated general traffic, and do not combine first use of a model, private posting upload, a new source, and ranking influence in one cohort. Release authority advances only the capability whose gate evidence is complete.

---

❓ **Q14 - Observability and alert ownership**: Product Manager, will you adopt content-free operational telemetry with explicit owners and service-level triggers? The options are: (A) log prompts and outputs for easy debugging; (B) collect only aggregate uptime, which protects content but cannot diagnose evidence failures; or (C) record non-content IDs and versions, routed intent, fallback reason, claim/citation counts, validation outcome, model/provider latency and cost, extraction state, mapping status, deletion completion, source freshness, queue depth, circuit state, and kill-switch changes, while excluding prompt bodies, source text, answers, student identifiers, and secrets from general logs.

➡️ **Yes: approve option C.** Backend owns routing/validation metrics, data operations owns ingestion/freshness, DevOps owns provider/cost/queue alerts, privacy owns deletion evidence, and product/evaluation owns usefulness and unsupported-takeaway dashboards. Alerts must map to a named responder and runbook; telemetry without an owner cannot satisfy a release gate.

---

❓ **Q15 - Authority gates and non-waivable stops**: Product Manager, will you use a recorded approval matrix in which each authority can approve only its domain and cannot be inferred from another gate? The options are: (A) let the Product Manager accept residual risk for the pilot; (B) require unanimous approval for every change, which is safe but blocks ordinary iteration; or (C) let product approve scope/value, tech lead approve architecture, academic/recommendation owner approve course evidence and ranking policy, data/source owner approve mappings and snapshot publication, legal/source owner approve acquisition and reuse rights, privacy/security approve processor, tenancy, retention, and controls, finance approve spend, and release authority approve cohort progression. Source authorization, tenant isolation, selective deletion, secret safety, deterministic fallback, and zero critical security failures are non-waivable release stops.

➡️ **Yes: approve option C.** Every approval records scope, evidence, version, expiry or revisit trigger, and owner; silence is not approval. A rejection or expired approval disables only the dependent capability where isolation is proven, otherwise the broader release remains blocked.

# Round 3

❓ **Q1 - Exact Stage 2 pilot segment**: Product Manager, will you freeze the Stage 2 pilot to English-language evidence for Singapore-based NTU computing students exploring entry-level or graduate `software_engineer` and `data_engineer` roles? Under this boundary, `software engineer`, `software developer`, and explicit graduate/junior variants map to the first role; `data engineer` and explicit graduate/junior variants map to the second. Internships and specialized or senior titles such as frontend, backend, full-stack, analytics engineer, machine-learning engineer, data scientist, architect, lead, staff, principal, and manager remain outside the role-target pilot unless separately reviewed. Because O*NET and ESCO are U.S.- and EU-oriented reference classifications, their concepts must be labelled external taxonomy context rather than Singapore employer evidence.

➡️ **Yes: approve this narrow segment.** It gives the value study a coherent population and prevents title aliases from silently broadening the skill model. Unsupported titles should return a bounded scope message, not be forced into the nearest pilot role.

---

❓ **Q2 - Ephemeral supplied-posting result UX**: Product Manager, will you make supplied-posting analysis explicitly ephemeral so the citation and deletion contracts agree? The alternatives are: (A) retain the answer and extracted claims after deleting raw text, which preserves convenience but retains private source-derived records; (B) retain an answer whose citations can no longer resolve, which conflicts with the evidence contract; or (C) show an expiry time, keep the result only for the active analysis window, clear the rendered result when the user deletes it or the successful-analysis window expires, and provide no history, save, share, or export in the pilot. A later revisit requires a new authorized submission and a new analysis ID.

➡️ **Yes: approve option C.** Treat the one-hour successful-analysis deletion point as the maximum result lifetime, with immediate clearing on user deletion and the existing 24-hour cleanup only for failed or interrupted work. Any durable result becomes a separate persistence, rights, tenancy, and deletion decision.

---

❓ **Q3 - No aggregate skills-gap claim in Stage 2**: Product Manager, will you omit broad role-level “skills gap,” coverage score, fit score, and missing-skills summary claims from Stage 2? The reviewed course ledger is intentionally narrow, and no approved coverage denominator currently establishes that an aggregate gap is representative. Stage 2 can instead show each explicit posting skill or labelled taxonomy concept, its mapping state, any reviewed course-exposure link, and `no reviewed course link` or `unknown` where evidence ends.

➡️ **Yes: approve item-level evidence only for Stage 2.** Reconsider an aggregate summary only after the relevant role and course set have a predeclared coverage denominator and threshold approved before results are inspected. Absence of a reviewed link must never be displayed as absence of learning, course irrelevance, or student deficiency.

---

❓ **Q4 - Independent value gates for the two Stage 2 modes**: Product Manager, will you require role-target context and supplied-posting analysis to earn release independently rather than letting one mode's results carry the other? The role-target mode tests whether labelled taxonomy context helps comparison without being mistaken for employer demand. The supplied-posting mode tests whether exact posting evidence and reviewed course links improve understanding without creating unsupported takeaways. Both may use the same controlled participants, but each needs its own locked tasks, task-success comparison, critical-distinction comprehension results, defect record, and continuation decision.

➡️ **Yes: approve independent gates.** Apply the already settled usefulness and calibrated-trust thresholds to each mode separately, and release, pause, or remove each capability on its own evidence. Do not average the modes into one Stage 2 pass.

# Final Frontier Certificate

**Flow ID:** `product-griller`  
**Parent:** parent orchestrator  
**Review posture:** independent final review after Round 3  
**Result:** `PRODUCT FRONTIER EMPTY`

## Design-tree recomputation

The settled trunk is one course-recommendation product with separately gated
assistant and job-context capabilities. Its product branches are fully resolved:

- Stage 1 is a read-only, deterministic-first assistant with six allowlisted
  intents, immutable claim citations, bounded optional synthesis, no persistent
  conversation, no preference mutation, and no authority over recommendation,
  readiness, prerequisites, scoring, ranking, or slot assignment.
- Stage 2 contains two independently evaluated modes: taxonomy-backed role
  context and ephemeral supplied-posting analysis. It is limited to English
  evidence for Singapore-based NTU computing students considering entry-level
  or graduate `software_engineer` and `data_engineer` roles under the exact
  alias exclusions settled in Round 3.
- Stage 2 presents item-level evidence only. It has no aggregate skills-gap,
  fit, coverage, missing-skills, frequency, trend, current-demand, or ranking
  claim.
- Supplied-posting analysis is private, non-LinkedIn, declaration-gated,
  no-fetch, and ephemeral. Successful results and all supporting private
  evidence expire together within one hour; there is no history, save, share,
  or export.
- Live sources, durable private records, BYOK, anonymous catalog chat,
  preference mutation, and market-informed deterministic ranking are later
  capabilities requiring new gates or explicit new product decisions.

No unanswered product decision is currently reachable without first obtaining
evidence or approval assigned to another authority. Reopening any settled
question requires a recorded trigger from its decision, not implementation
preference.

## Settled decision count

**34 product decisions are settled:** 15 in Round 1, 15 in Round 2, and 4 in
Round 3. A `Modify` response still counts as settled because each such response
replaced the recommendation with a concrete default, boundary, and authority.

## Deferred authority items

These are not product-frontier questions and must not be answered by the parent
planner:

1. **Legal/source authority:** approve any LinkedIn exception and the first live
   source's acquisition, storage, derivative, model-use, display, attribution,
   retention, and deletion rights.
2. **Privacy/security authority:** approve provider/endpoint/region, minimum
   payload, retention exceptions, authenticated tenancy, deletion evidence,
   secret custody, hostile-content controls, and production external-model use.
3. **Finance/product sponsor:** approve the selected provider and final spend
   ceiling within or by replacing the provisional pilot envelope.
4. **Academic/recommendation owner:** approve course-skill evidence and, only
   after the later ranking proposal, the deterministic formula, tolerances, and
   academic-policy impact.
5. **Data/domain/source owner:** approve canonical aliases, taxonomy mappings,
   role/course coverage denominators, and any shared snapshot publication.
6. **Research/evaluation and accessibility owners:** approve study protocol,
   confidence-aware interpretation, locked-set adequacy, and accessibility
   coverage; they do not decide product continuation.
7. **Tech lead/DevOps/security:** approve architecture, deterministic contracts,
   isolation, breaker tuning, operational controls, and verification evidence;
   they do not widen product scope.
8. **Release authority:** make cohort progression, production go/no-go, and
   rollback decisions after all applicable domain approvals are recorded.

Source authorization, authenticated tenant isolation for private multi-user
data, selective deletion, secret safety, deterministic fallback, and zero
critical security failures remain non-waivable release stops.

## Exact final-plan reconciliation instructions

The parent orchestrator must reconcile the final plan as follows:

1. Replace the brief's open-decision list with two explicit lists:
   `settled product decisions` and `deferred authority approvals`. Do not leave
   geography, seniority, aliases, posting persistence, score exposure,
   anonymous catalog chat, mapping reviewers, or preference mutation marked
   open.
2. Carry all 34 decisions into the final decision ledger, preserving each
   concrete default, exclusion, owner, revisit trigger, and provisional numeric
   target. Mark targets as proposed gates, not measured results or external
   facts.
3. Amend Stage 1 scope to the exact six-intent allowlist from Round 2 Q1.
   Specify deterministic routing, per-intent fallback, qualitative-only score
   explanations, immutable citation identity, deterministic-only readiness
   under provider failure, and no anonymous catalog chat or mutation.
4. Amend Stage 2 scope to the exact Round 3 role, geography, language,
   seniority, and alias boundary. Split `role_target` and `supplied_posting`
   into independent release units with separate tests, kill switches,
   continuation decisions, and rollback evidence.
5. Replace any general 24-hour supplied-posting retention wording with the
   settled lifecycle: immediate deletion on request; successful raw input,
   claims, citations, derivatives, and rendered result deleted together within
   one hour; failed/interrupted work cleaned within 24 hours; content-free
   operational metadata retained for 30 days under the approved purpose.
6. State that Stage 2 has item-level evidence only. Remove or defer every
   aggregate gap, fit, coverage, missing-skills, frequency, trend, demand, or
   ranking output until a later predeclared coverage and authority decision.
7. Reconcile the token language so the promised pilot token is an
   environment-scoped operator secret. BYOK remains disabled; model failure
   degrades to deterministic fallback and never prompts a user for credentials.
8. Preserve LinkedIn rejection, no arbitrary URL fetching, affirmative posting
   provenance, exact-evidence requirements, explicit unknown/ambiguous states,
   and taxonomy-versus-employer-evidence labels in requirements, UX, tests, and
   rollout gates.
9. Place every authority-bound item in a dependency/approval matrix with owner,
   evidence, scope, version, decision time, expiry or revisit trigger, and
   dependent capability. Do not convert absent approval into backlog consent.
10. Sequence execution as Stage 0 contract/fixtures, deterministic Stage 1,
    evaluated model synthesis, independently gated Stage 2 modes, then
    separately authorized live snapshots. Market-informed ranking remains a
    later proposal and must not appear as committed delivery scope.

## Proposed Shape/design questions

The following questions may be resolved during shaping and technical design.
They intentionally do **not** change product scope or require another product
grilling round:

- What API and schema decomposition best enforces the six intent contracts,
  immutable claim identity, posting state machine, and deletion transaction?
- How should the UI visually distinguish deterministic facts, employer
  evidence, taxonomy context, normalized inference, generated advice,
  unknowns, expiry, and fallback without overwhelming the student?
- Which existing FastAPI service boundaries should host context assembly,
  policy validation, provider adapters, and the future isolated ingestion
  worker?
- How should fixtures, annotation tools, replay records, and content-free
  telemetry be structured to prove the settled gates reproducibly?
- What exact interaction copy and component behavior best communicate posting
  provenance, one-hour expiry, unsupported role scope, non-registration
  readiness, and exposure-not-mastery?
- Which operational dashboards, runbooks, alert thresholds, and kill-switch
  mechanisms best implement the named ownership model?

These are implementation and interaction-design choices only. Any proposed
answer that broadens inputs, claims, persistence, authority, role coverage,
source access, model powers, or ranking effect creates a new product decision
and invalidates this certificate for that branch.
