# Product Manager Responses to Grilling Recommendations

**Status:** Decision-ready response; `brief.md` remains unchanged  
**Decision basis:** Product intent and the draft brief only. Demand, provider coverage, pricing, legal approval, and accuracy baselines remain unvalidated.

## Decisions

### 1. Sole launch persona

**Answer: Yes.**

- **Default:** Launch for applied ML practitioners planning non-safety-critical experiments. The first job is: “decide the next bounded experiment from a user-confirmed research corpus.”
- **Boundary:** Researcher, student, educator, and product-lead personas remain discovery inputs, not launch personas or acceptance-test populations.
- **Rationale:** A single persona and decision context make utility, advice quality, terminology, and risk measurable. This narrows the broader audience currently stated in the brief.

### 2. Product promise

**Answer: Yes.**

- **Default:** Promise “traceable decision support over a corpus you confirm.” Do not promise search completeness, systematic review, truth ranking, peer-review judgment, or scientific authority.
- **Presentation:** Every run and export states that retrieval is bounded, corpus selection is user-controlled, and generated advice requires validation.
- **Rationale:** This aligns the product with its defensible trust advantage—inspectable provenance—rather than unsupported coverage or authority claims.

### 3. Corpus confirmation

**Answer: Yes.**

- **Default:** Synthesis cannot start until the user confirms at least one paper/version. Preserve the candidate set, included papers, excluded papers, exclusion reasons, and confirmation timestamp in run provenance and export.
- **Change handling:** Any membership or version change creates a new run revision; removed papers cannot remain cited.
- **Rationale:** This prevents hidden evidence selection and makes retrieval bias and user judgment auditable.

### 4. Bounded topic discovery

**Answer: Yes.**

- **Default:** Show at most 30 de-duplicated candidates per discovery run; default synthesis corpus is 8 papers with a hard cap of 20.
- **Disclosure:** Show exact query, providers, filters, ranking factors, retrieval timestamp, raw and de-duplicated counts, truncation, provider failures, access mix, and the statement “bounded candidate set—not exhaustive coverage.”
- **Rationale:** A bounded set supports review without implying literature completeness. The 30/8/20 limits are pilot defaults, not claims of optimality.

### 5. Full-text access

**Answer: Modify.**

- **Default:** Process full text only when open access or explicitly supplied by a user who attests authorization. Do not accept credentials, proxy access, paywall bypass, or unauthorized mirrors. If full text is unavailable, use permitted abstract/metadata and label every affected output `abstract-only`.
- **MVP scope:** A narrow single-paper PDF supply path may enter MVP only after upload security and legal checks; broader document libraries, reference-manager sync, and persistent uploads remain deferred.
- **Rationale:** This preserves the lawful-access rule while resolving the brief’s tension between authorized supply and its current deferral of all uploads.

### 6. Exact-version evidence

**Answer: Yes.**

- **Default:** Each supported paper-specific claim identifies the exact analyzed version and the most specific available location: quoted passage/span plus page and section, or figure/table/equation/abstract field as applicable.
- **Failure rule:** A locator that cannot resolve to that version is `evidence unavailable` or `parser degraded`; it cannot be presented as supported.
- **Rationale:** Paper-level citations alone do not establish entailment and can silently attach claims to the wrong version.

### 7. Analytical class labels

**Answer: Yes.**

- **Default:** Every analytical paragraph, list group, or table row has exactly one primary class: `PAPER-SPECIFIC`, `CROSS-PAPER SYNTHESIS`, or `GENERATED ADVICE`. Inputs may span classes, but the output block cannot.
- **Validation:** Zero missing, multiple, or invalid primary labels; any occurrence blocks export and release.
- **Rationale:** Exact classification prevents author findings, model inference, and recommendations from blending through formatting or inheritance.

### 8. High-stakes exclusions

**Answer: Yes.**

- **Default:** Exclude clinical diagnosis/treatment, legal decisions, public-safety or other high-stakes decisions, and autonomous production changes. Also exclude automatic code execution, training, deployment, purchasing, or policy action.
- **Allowed use:** Users may inspect papers in these domains, but the product must not generate decision recommendations for those contexts.
- **Rationale:** The launch evidence and controls cannot support harms or accountability requirements in high-stakes or autonomous settings.

### 9. Privacy, retention, and reuse

**Answer: Modify.**

- **Default:** Keep source bytes transient and delete them within 24 hours of run completion. Persist only identifiers, access state, locators/hashes, minimal quoted evidence, run provenance, and user-requested outputs for 30 days. Honor user deletion within 24 hours and redact raw content from operational logs.
- **Reuse:** No provider content, user-supplied documents, queries, annotations, or outputs are used for model training or evaluation without separate explicit opt-in and legal approval; consent is not bundled with product use.
- **Rationale:** Limited output/provenance persistence is needed for inspection and reproducibility, so “transient sources” should not mean “no durable run record.” Exact retention and vendor subprocessors require privacy/legal approval before release.

### 10. Release-blocking integrity failures

**Answer: Yes.**

- **Default:** Any fabricated source, citation that is presented as support but does not entail the claim, citation to the wrong version, fabricated quotation, unresolved evidence key, or missing/multiple class label blocks release.
- **Partial output:** Explicit partial output is allowed only when failed papers/sections are omitted or marked unavailable, all remaining claims pass validation, and omissions are listed prominently.
- **Threshold change:** Replace the brief’s proposed 95% sampled-entailment release gate with zero observed false-supported citations in the predeclared release audit. The 95% measure may remain a pilot diagnostic, not a release pass threshold.
- **Rationale:** A product centered on traceability cannot knowingly ship integrity defects while averaging them away.

### 11. Concierge validation before scale

**Answer: Yes.**

- **Default:** Recruit 10 launch-persona users within the permitted decision context. Run 20 predeclared tasks—10 topic and 10 URL tasks—with each user completing two tasks and every task represented once. Include open full text, abstract-only, malformed/unsafe URL, duplicate/version conflict, retracted/corrected paper, mixed access, provider failure, and inaccessible source states.
- **Independent audit:** Audit at least 100 substantive claims, stratified across papers, access states, and all three classes, by reviewers who did not create the outputs.
- **Build boundary:** Use concierge work or a throwaway prototype only. Do not commit to broad provider integrations or production architecture until corpus control, label comprehension, evidence navigation, integrity, and utility gates pass.
- **Rationale:** This is the smallest credible test of the core value and risk assumptions before expensive integration work.

### 12. Operating ceilings and stop rules

**Answer: Yes.**

- **Cost ceiling:** Direct variable provider/model cost is at most US$3 for a default run of up to 8 papers and US$8 for a capped 20-paper run.
- **Latency ceiling:** From confirmed corpus to reviewable export, p90 is at most 10 minutes for default runs and 20 minutes for capped runs, excluding user review time.
- **Reviewer burden:** Median user time to confirm the corpus and verify enough evidence to use the output is at most 10 minutes; p90 is at most 15 minutes.
- **Minimum utility:** At least 70% of completed pilot tasks yield a useful next-experiment decision without a material factual correction, and the user correctly distinguishes generated advice from paper findings.
- **Stop rules:** Stop scope expansion if any integrity blocker occurs; if more than 10% of valid runs exceed cost ceilings, more than 20% exceed latency/reviewer ceilings, or utility is below 70%, reduce corpus size/providers/output sections first. Remove generated advice before weakening evidence or label gates. Re-test against the same tasks before proceeding.
- **Rationale:** Predeclared ceilings prevent the pilot from rationalizing an accurate but unusable or uneconomic workflow. Finance/product authority must approve a different spend ceiling; pilot results may tighten, but not retroactively relax, the gates.

## Resolved Brief Tensions

- The launch audience narrows from four personas to one; other personas move out of launch scope.
- User-authorized PDF supply becomes a narrowly gated option rather than part of the brief’s broad deferred upload capability.
- The 95% entailment proposal becomes a diagnostic; release requires zero observed false-supported citations.
- Persistence retains minimal run provenance for 30 days while raw source content remains transient.
- Generated advice stays in MVP only for non-safety-critical experiments and is the first scope removed if ceilings fail.

## Authority Required

- **Privacy/legal:** Approve source rights, limited quotation, 24-hour source deletion, 30-day run retention, vendor handling, and contractual no-training behavior.
- **Product/finance:** Approve any spend ceiling different from US$3 default/US$8 capped per run.
- All other recommendations are product defaults suitable for validation; they do not require further user authority before updating the brief.

## Concise Handoff

- **Designer:** Validate explicit corpus confirmation, persistent bounded-coverage disclosure, exact class labels, abstract-only/partial states, evidence opening, and whether verification fits the 10-minute median burden. Decide label placement and partial-output hierarchy without weakening visibility.
- **Tech Lead:** Treat exact-version identity, evidence locators, class validation, secure authorized upload, transient source handling, deletion, and fail-closed export checks as hard contracts. Decide feasible provider/locator mechanisms and instrument the cost/latency ceilings; do not select production architecture before validation passes.
- **QA:** Lock the 20 tasks and 100-claim independent audit before testing. Treat every integrity condition in Decision 10 as an individual zero-tolerance release gate.

## Grilling Round 2

**Status:** Product defaults accepted for validation; `brief.md` remains unchanged.

### 1. Provider-specific discovery controls

**Answer: Modify.**

- **Default:** Preserve the user query verbatim and show each provider's submitted query, expansions, filters, result limit, ranking mode, returned count, and failure state. Provider-native relevance remains the initial rank; the product may apply a separately visible merge rank using normalized relevance, recency, and method/domain diversity.
- **Control:** Users can inspect, disable, or revise expansions and rerun discovery. No hidden synonym, citation, recency, venue, or popularity boost may alter the candidate set.
- **Rationale:** Provider syntax and rank signals are not comparable. Reviewable provider-level revisions expose retrieval bias without requiring users to understand every API.

### 2. Conservative identity and deduplication

**Answer: Yes.**

- **Default:** Auto-merge only exact normalized DOI matches or an explicit repository-version relationship from a canonical provider. Repository IDs, bibliographic fingerprints, and title/author/year similarity may propose a group but cannot silently merge records.
- **Ambiguity:** Conflicting DOI, title, authorship, year, venue, or version metadata creates a visible `possible duplicate/version conflict`; records remain separate until the user confirms the relationship. Every citation remains bound to the analyzed record/version.
- **Rationale:** False merges can attach evidence to the wrong work and are more damaging than visible duplicates.

### 3. Inaccessible, corrected, and retracted papers

**Answer: Yes.**

- **Default:** Inaccessible papers remain in the register with `metadata-only`, `abstract-only`, `denied`, or `failed`; they cannot support full-text claims. Corrections are linked to the affected version and presented with both status and date.
- **Retractions:** Retracted papers are excluded from synthesis and advice by default, remain visible in discovery, and require explicit user inclusion for historical or methodological analysis. Their claims always carry a retraction warning and cannot be the sole basis for advice.
- **Rationale:** Visibility preserves research context; default exclusion prevents unavailable or withdrawn evidence from silently driving conclusions.

### 4. Contradictions and alternatives

**Answer: Yes.**

- **Default:** Represent each material issue as a structured record containing proposition, supporting papers/evidence, contradicting papers/evidence, comparability limits, plausible explanations, unresolved status, and alternative interpretations or approaches.
- **Output:** Do not collapse disagreement into a majority conclusion. If datasets, populations, methods, endpoints, or versions are not comparable, label the issue `incomparable`, not `contradiction`.
- **Rationale:** Structured disagreement preserves decision-relevant uncertainty and prevents fluent synthesis from manufacturing consensus.

### 5. Normative Markdown schema

**Answer: Yes.**

- **Default:** Publish a normative schema with semantic version, required headings/fields, controlled enums, citation grammar, stable-ID rules, null/not-applicable behavior, and validation rules. Each export declares `schema_version` and `generator_version`.
- **Compatibility:** Patch releases clarify without changing meaning; minor releases add backward-compatible optional fields; major releases may break consumers. A run revision never silently changes schema version.
- **Rationale:** A fixed but versioned contract makes exports testable and portable without freezing product learning.

### 6. Portable citation records

**Answer: Yes.**

- **Default:** Each citation record contains a stable evidence ID, stable paper ID, exact analyzed version, locator type/value, content anchor or checksum, access scope, retrieval timestamp, and lawful canonical URL. Human-readable anchors accompany provider deep links where possible.
- **Quotation:** Include only the minimum exact text needed to verify entailment; default maximum is two sentences or 50 words per evidence item, subject to stricter source terms. If lawful text cannot be retained, preserve locator and hash without the quote.
- **Rationale:** URLs and page numbers alone are brittle; portable identity plus version and anchor preserve auditability while minimizing copied text.

### 7. Advice bounded to the next experiment

**Answer: Yes.**

- **Default:** Generated advice proposes one next bounded experiment, not a roadmap or production decision. It must state hypothesis, smallest intervention, comparator, dataset/population, success and stop metrics, estimated effort, failure modes, and what result would change the decision.
- **Evidence status:** Show separate qualitative dimensions for source access, directness, consistency, applicability, and reproducibility: `strong`, `mixed`, `weak`, or `unknown`, each with a reason. Do not collapse these into one score.
- **Rationale:** A bounded experiment is useful to the launch persona while multidimensional status avoids false precision and hidden evidence gaps.

### 8. Fail-closed advice

**Answer: Yes.**

- **Default:** Suppress generated advice when any required supporting claim lacks resolved exact-version evidence, evidence is abstract/metadata-only for a method-dependent recommendation, a material contradiction is unresolved, applicability is `weak/unknown`, the only support is retracted, or no safe measurable experiment can be framed.
- **Fallback:** Export an `insufficient evidence for advice` decision with the blocking gaps and the smallest evidence-gathering action; never fill the advice section with generic recommendations.
- **Rationale:** Advice is the highest-risk class and must fail closed before evidence integrity is weakened.

### 9. Stratified 100-claim audit

**Answer: Modify.**

- **Default:** Audit at least 100 substantive claims, stratified across all three claim classes, full-text and limited-access states, providers, document formats, paper versions, and agreement/conflict outcomes. Each claim receives two independent reviewers; disagreements require adjudication by a third reviewer and are reported.
- **Mandatory edge cases:** Include wrong-version traps, duplicate ambiguity, inaccessible full text, corrected and retracted papers, parser-degraded locators, provider partial failure, direct quotations, contradictions/incomparability, and advice suppression under weak evidence.
- **Rationale:** Round 1 required independent review but did not require two judgments per claim or a fixed edge-case floor; both are needed to expose correlated reviewer error.

### 10. Class-specific audit rubrics

**Answer: Yes.**

- **Default:** `PAPER-SPECIFIC` passes only if identity/version, locator, access scope, attribution, quotation accuracy, and entailment pass. `CROSS-PAPER SYNTHESIS` additionally requires every necessary source, faithful agreement/conflict treatment, and comparability limits. `GENERATED ADVICE` additionally requires evidence linkage, applicability, bounded experiment, assumptions, uncertainty, and stop criteria.
- **Scoring:** Each dimension is pass/fail/not-applicable with reviewer rationale. Any critical failure fails the claim; aggregate averages cannot offset it.
- **Rationale:** One generic entailment score cannot test the distinct failure modes of attribution, synthesis, and recommendation.

### 11. Partial snapshots and reproducible revisions

**Answer: Yes.**

- **Default:** A provider failure creates an immutable partial discovery snapshot recording provider/query revision, request time, returned IDs/order, pagination/truncation, error class, and completeness warning. Successful results remain reviewable but the snapshot cannot be labelled complete.
- **Revision:** Retry or provider recovery creates a new run revision linked to its parent; it never mutates the prior candidate set or confirmed corpus. Synthesis regeneration requires renewed corpus confirmation when membership/version changes.
- **Rationale:** Partial utility is valuable only when outages and subsequent changes remain reproducible and visible.

### 12. Enforceable retention and no-training controls

**Answer: Modify.**

- **Default:** Source bytes and derived full-text caches expire and are deleted within 24 hours of run completion across first-party systems, queues, backups where technically feasible, subprocessors, and failed-job stores. Deletion events are auditable; user deletion triggers the same deadline. Operational logs contain no raw paper or user-document text.
- **Vendors:** Contracts and technical configuration must prohibit training, model improvement, human review except approved support incidents, and retention beyond the service window. A vendor that cannot contractually and operationally meet these controls is ineligible.
- **Authority:** Privacy/legal must approve the deletion definition, backup treatment, audit evidence, and subprocessor terms before launch; product cannot waive these controls.
- **Rationale:** A UI promise is insufficient when subprocessors retain content or use it for training.

### 13. Hard per-run variable-cost enforcement

**Answer: Yes.**

- **Default:** Treat US$3 as the target for the default run of up to 8 papers and US$8 as the hard ceiling for every run up to the 20-paper cap. Estimate cost before generation, reserve the remaining budget by stage, meter actual provider/model spend, and stop optional stages before the ceiling can be exceeded.
- **Failure behavior:** At the ceiling, return a labelled partial export and cost ledger; do not silently downgrade evidence checks, exceed the cap, or auto-charge more. Retries and provider fallbacks count toward the same run revision's ceiling.
- **Rationale:** The already accepted ceiling must be an execution control, not a post-run dashboard metric.

### 14. Scale economics and contribution-margin gate

**Answer: Modify.**

- **Default:** Keep pilot variable-cost compliance separate from scale viability. Before production scale, model per-run revenue allocation against model/provider, storage/egress, moderation/support, audit, and failed-run costs at expected corpus/access mixes.
- **Gate:** Default scale gate is non-negative contribution margin at p90 cost and at least 60% contribution margin at the expected default-run mix, with integrity, latency, and utility gates still passing. Pilot labor is reported separately and cannot be hidden from the operating model.
- **Authority:** Product/finance must approve pricing and any different contribution-margin threshold before a scale commitment; pilot validation may inform but cannot silently relax this gate.
- **Rationale:** Meeting an US$8 cost cap does not establish a sustainable business when price, failures, support, and review costs are unknown.

## Round 2 Authority Decisions

- **Privacy/legal:** Approve enforceable 24-hour deletion semantics, backup and subprocessor treatment, audit evidence, and contractual no-training terms.
- **Product/finance:** Approve pricing and any contribution-margin threshold different from the 60% default before production scale.
- **Not reopened:** The accepted US$3 target and US$8 hard per-run ceiling remain binding; changing them requires explicit product/finance authority, but implementation and validation do not.
- All other Round 2 items are reversible product defaults for the concierge validation and require no additional user-authority decision.

## Round 2 Handoff

- **Designer:** Make provider/query revisions, ambiguity, access/publication state, contradictions, evidence dimensions, advice suppression, and partial-run revisions understandable without hiding them behind tooltips. Decide interaction and content hierarchy, not whether these states exist.
- **Tech Lead:** Define contracts for conservative identity, immutable run revisions, normative schema validation, portable evidence IDs/anchors, fail-closed advice, provider snapshots, TTL propagation, auditable deletion, and hard budget stops. Decide mechanisms; preserve the product invariants.
- **QA:** Lock the two-reviewer stratified 100-claim sample, mandatory edge cases, and class-specific rubrics before outputs are produced. Test cost-stop, deletion/subprocessor evidence, partial snapshots, revision reproducibility, and every fail-closed trigger independently.
- **Orchestrator:** Route only the privacy/legal and scale-economics authority decisions above; do not reopen settled product defaults during Shape.
