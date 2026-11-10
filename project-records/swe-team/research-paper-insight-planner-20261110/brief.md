# Research Paper Insight Planner — Product Brief

**Status:** Draft for challenge and frame approval  
**Date:** 2026-11-10  
**Owner:** Product Manager (`swe-product-manager`)  
**Audience:** Orchestrator, grilling reviewer, Product Designer, Tech Lead, QA, DevOps/Security

## 1. Decision Summary

Build an MVP that accepts either a research topic or a paper URL, forms a transparent paper set, supports source inspection, and exports evidence-grounded Markdown. The output separates (1) paper-specific statements, (2) cross-paper synthesis, and (3) generated implementation advice. Every substantive factual claim must be traceable to an accessible source location or visibly marked unsupported/uncertain. The product must not bypass paywalls, imply that discovery is exhaustive, or present generated advice as a paper finding.

Recommended MVP defaults:

- Topic discovery returns a reviewable candidate list; users explicitly select the synthesis corpus.
- URL ingestion supports DOI, arXiv, PubMed/PMC, publisher landing pages, and direct PDFs where access is lawful.
- Open-access or user-authorized full text may be processed; metadata/abstract-only records stay visibly limited.
- The inspection experience anchors claims to page, section, figure, table, or quoted passage when available.
- Markdown export uses a fixed evidence schema with inline citation keys and a source register.
- Recommendations for recommender systems, fine-tuning, course recommendations, and other applications are labelled generated advice, with evidence links and assumptions.

## 2. Required Inputs and Assumptions

| Input | Current state | Product handling |
|---|---|---|
| Problem/opportunity | Supplied at concept level | Treat fragmented discovery, reading, synthesis, and provenance as the core problem. |
| Target users | Not explicitly supplied | Assume technical researchers, ML practitioners, graduate students, and evidence-oriented product/engineering teams. Validate first. |
| Desired outcomes | Partially supplied | Fast discovery/ingestion, inspectable evidence, trustworthy Markdown, and actionable synthesis. |
| Constraints | Plan-only; legitimate papers; evidence grounding; Markdown; legal/access boundaries | Treat these as hard scope constraints. Runtime, budget, geography, retention, and supported languages are unknown. |
| Available evidence | Product intent only; no user research, usage data, source-provider commitments, or benchmark corpus supplied | Do not treat demand, retrieval quality, or synthesis accuracy as validated. |
| Stakeholders | Parent orchestrator and downstream SWE roles are known | Assume users, product owner, legal/privacy, security, and source-provider owners are stakeholders; accountable names are missing. |
| Decision deadline | Missing | Recommended default: resolve blocking open decisions before `frame-approved`; set a dated milestone before Shape. |

## 3. Problem and Users

### Problem statement

People investigating a research topic or a known paper must move between search tools, publisher pages, PDFs, notes, and general-purpose generators. They struggle to know which papers are legitimate, which source text supports a summary, whether a conclusion belongs to one paper or several, and where generated implementation advice begins. This creates slow review, citation errors, overconfident synthesis, and unsafe implementation decisions.

### Target users and jobs

| User | Primary job | Current failure mode | Desired outcome |
|---|---|---|---|
| Applied ML practitioner | Translate research into an experiment or product approach | Advice is detached from methods, data, and limitations | An evidence-linked implementation starting point with explicit assumptions |
| Researcher or graduate student | Triage and compare papers on a topic | Search results are noisy; comparison notes lose provenance | A reviewable corpus and claim-level cross-paper synthesis |
| Educator or curriculum planner | Identify papers and concepts for course recommendations | Relevance, prerequisites, and pedagogical fit are conflated with paper findings | Clearly labelled course-use recommendations grounded in paper content |
| Technical product/engineering lead | Evaluate approaches such as recommenders or fine-tuning | Generated recommendations appear more certain than evidence warrants | Decision-ready options, trade-offs, and unresolved evidence gaps |

## 4. Goals, Non-goals, and Success

### Goals

- G1 — Let a user begin from either a topic or a paper URL without losing provenance.
- G2 — Make the selected paper set and access level explicit before synthesis.
- G3 — Support inspection from every material claim back to source evidence.
- G4 — Produce reusable Markdown covering overview, methods, findings, limitations, implementation guidance, and use-case synthesis.
- G5 — Prevent category confusion among paper-specific facts, cross-paper synthesis, and generated advice.
- G6 — Respect copyright, provider terms, access controls, privacy, and secure URL handling.

### Non-goals for MVP

- No exhaustive systematic-review claim, citation-network completeness guarantee, or meta-analysis.
- No peer-review-quality determination beyond displaying available venue, retraction, version, and provenance signals.
- No paywall, authentication, DRM, CAPTCHA, or robots-control bypass.
- No autonomous code generation, model training, experiment execution, production architecture, or deployment plan.
- No collaborative annotation, reference-manager replacement, native mobile app, or full citation-style editor.
- No unsupported “best paper,” clinical/legal safety recommendation, or course-selection decision made on the user's behalf.
- No inference that a URL, DOI, repository host, citation count, or venue alone proves truth or legitimacy.

### Success measures

These are proposed MVP gates, not evidence-backed forecasts:

| Measure | Target | Measurement |
|---|---:|---|
| Input completion | ≥90% of a fixed test set of supported topic and URL tasks reaches a reviewable corpus or a specific recoverable error | Automated and manual benchmark across supported source/access states |
| Citation coverage | 100% of substantive paper-specific factual claims in export have a resolvable citation or an explicit `evidence unavailable` marker | Export validator plus sampled human audit |
| Label integrity | 100% of output blocks expose exactly one primary class: paper-specific, cross-paper synthesis, or generated advice | Schema validation |
| Citation correctness | ≥95% of sampled claims are entailed by the cited passage/location; zero fabricated sources | Independent blinded review on a predeclared corpus |
| Inspection usability | ≥80% of pilot users can open supporting evidence for a selected claim without assistance in ≤2 actions | Moderated usability test |
| Corpus control | 100% of topic runs disclose query, providers, retrieval time, filters, access level, and user-selected included papers | Event/export audit |
| Legal/access safety | Zero successful attempts in the security test suite to bypass access controls or fetch blocked private-network URLs | Security verification |
| Utility | ≥70% of target pilot users rate the exported brief as a useful starting point for their stated decision, while correctly identifying generated advice | Post-task survey and comprehension check |

## 5. Evidence, Assumptions, and Validation

### Evidence

- E1 — The supplied intent requires topic discovery and paper-URL ingestion.
- E2 — The supplied intent requires reading/inspection plus evidence-grounded Markdown.
- E3 — The supplied intent names overview, methods, findings, limitations, implementation guidance, and use-case synthesis.
- E4 — No user interviews, analytics, provider API agreements, retrieval benchmark, accuracy evaluation, or legal review is available.

### Material assumptions

- A1 — Users value inspectability enough to accept corpus confirmation and visible caveats.
- A2 — Open scholarly metadata and lawful full-text sources provide adequate MVP coverage.
- A3 — A fixed Markdown schema is reusable across disciplines despite heterogeneous paper structures.
- A4 — Claim-level grounding can achieve useful precision without making generation prohibitively slow or costly.
- A5 — Users understand the three evidence classes when labels remain present in reading and export contexts.
- A6 — English-language text-first papers are an acceptable MVP boundary.

### Smallest useful validation

Run a concierge prototype with 8–12 target users and a locked 20-task corpus: 10 topic tasks and 10 URL tasks spanning open PDF, abstract-only, malformed URL, duplicate/versioned paper, retracted paper, and inaccessible source. Manually produce the proposed export and inspection links. Validate corpus-selection comprehension, evidence navigation, label comprehension, useful output sections, and willingness to use the result in a real decision. Independently audit at least 100 generated claims. Do not build broad source integrations until this test supports A1, A3, A4, and A5.

## 6. Scope and User Flow

### Path A — Research topic

1. User enters a topic and may add optional intent, date range, domain, paper count, and use case.
2. System normalizes the query, records it, searches approved scholarly providers, and de-duplicates/version-groups results.
3. System presents candidate papers with title, authors, year, venue/repository, identifiers, version, access level, retraction/correction signal when available, and reason for match.
4. User includes/excludes papers and confirms the corpus; defaults and filters remain visible.
5. System retrieves lawful content, records per-paper access limits, extracts inspectable structure, and flags failures.
6. System generates paper cards, cross-paper synthesis, and generated guidance with class labels and citations.
7. User inspects evidence, changes the corpus or requests regeneration, then exports Markdown with provenance.

### Path B — Paper URL

1. User enters one supported URL or DOI-like URL.
2. System validates the URL safely, resolves redirects, identifies the scholarly record/version, and retrieves permitted metadata and content.
3. System shows the canonical record, access level, available versions, and any ambiguity or retraction/correction signal.
4. User confirms the paper; if full text is unavailable, the system offers metadata/abstract-only analysis rather than implying full-paper coverage.
5. System provides the same inspection, labelled analysis, and Markdown export as Path A, with cross-paper sections marked not applicable until more papers are added.
6. User may expand from the paper to a topic/related-paper candidate list, but added papers require explicit confirmation.

### Required states

- Empty/start; query resolving; results available; no results; provider partially unavailable; duplicate/version conflict; corpus awaiting confirmation; ingesting; full-text ready; abstract-only; access denied; parse degraded; generation partial; generation complete; stale/regenerated; export ready; citation target unavailable; retracted/corrected signal; unsafe or unsupported URL.

## 7. Trust, Citation, and Access Policy

### Legitimacy and provenance

- A “paper” requires a scholarly record with at least title, author/organization attribution, publication/preprint context, and a stable identifier or canonical source URL.
- Discovery should prefer primary scholarly providers and canonical repositories. General web search may locate candidates but cannot by itself establish the canonical record.
- Display source provider, identifier, version/date, venue or repository, access level, retrieval timestamp, and known correction/retraction signal.
- Never label content “peer reviewed” unless provider metadata supports that status; preprints remain labelled preprints.
- Version grouping must not silently merge materially different versions; citations identify the analyzed version.

### Access and legal boundaries

- Process full text only when openly available, supplied through a user-authorized route, or otherwise licensed for the intended processing.
- Do not circumvent paywalls, login controls, CAPTCHAs, DRM, rate limits, robots directives, or provider terms.
- For inaccessible papers, retain allowed metadata/abstract and clearly limit conclusions; do not reconstruct full text from unauthorized mirrors.
- Store only the minimum content required by an approved retention policy. The default recommendation is transient processing with persisted metadata, citations, generated output, and user-approved notes—not source PDFs.
- Quote minimally and proportionately; prefer citations and paraphrase. Preserve author attribution and source links.
- URL fetching must reject unsupported schemes, local files, loopback/private/link-local destinations, redirect-to-private targets, and oversized or unexpected content.
- User-provided credentials are out of MVP. Institutional proxy and authenticated library access require separate legal/security approval.

### Claim classes

| Class | Meaning | Required presentation |
|---|---|---|
| `PAPER-SPECIFIC` | A statement attributable to one identified paper | Paper/version key plus source location and access scope |
| `CROSS-PAPER SYNTHESIS` | A comparison or inference derived across two or more selected papers | Supporting paper keys, agreement/conflict/gap note, and synthesis language—not quoted as an author claim |
| `GENERATED ADVICE` | A proposed application, implementation step, experiment, or course recommendation not directly claimed by the papers | Evidence links, assumptions, confidence/uncertainty, validation step, and warning that it is generated advice |

A block may cite multiple classes as inputs but must expose one primary class. Generated advice must never inherit the visual or textual treatment of a paper finding.

### Citation rules

- Every substantive factual paper-specific claim requires a citation key and the most specific available locator: page, section, paragraph/passage, figure, table, equation, or abstract field.
- Direct quotations require exact text and locator; generated text must not fabricate quotations.
- Cross-paper claims cite every paper needed to support the comparison and identify disagreement or incomparable methods.
- If only metadata/abstract is accessible, citations and analysis say `abstract-only`; absence from an abstract is not evidence of absence from the paper.
- Unsupported, low-confidence, or parser-dependent claims remain visibly marked and are excluded from confident conclusions.
- Citation links resolve to the inspected version where lawful; export includes a stable source register even if deep links later expire.

## 8. Prioritized Requirements and Backlog

Priority uses Must/Should/Could/Won't for MVP. Each requirement traces to a goal and user problem.

| ID | Priority | Requirement | Trace | Rationale/trade-off |
|---|---|---|---|---|
| R1 | Must | Accept a topic and preserve the exact query, filters, providers, retrieval time, and result set. | G1, G2; noisy discovery | Enables reproducibility; costs provider integration effort. |
| R2 | Must | Accept and safely resolve supported paper URLs/DOIs with explicit canonical record and version. | G1, G6; provenance loss | Makes direct-paper use dependable without promising every host. |
| R3 | Must | Show de-duplicated/version-grouped candidates and require explicit corpus confirmation before synthesis. | G2; hidden corpus | Adds a step but prevents silent evidence selection. |
| R4 | Must | Record per-paper access scope: full text, partial, abstract-only, metadata-only, denied, or failed. | G2, G6; overclaiming | Limits apparent completeness. |
| R5 | Must | Provide a structured inspection model for paper text and extracted sections, including evidence locators and parser warnings. | G3; unverifiable summaries | Inspection is core trust value, not optional polish. |
| R6 | Must | Generate the fixed Markdown schema with paper-specific overview, methods, findings, limitations, and citation register. | G4; fragmented notes | Establishes a testable portable output. |
| R7 | Must | Generate cross-paper synthesis only for confirmed corpora of at least two papers and disclose agreement, conflict, and gaps. | G4, G5; false consensus | Prevents single-paper content masquerading as literature synthesis. |
| R8 | Must | Generate implementation/use-case guidance only under `GENERATED ADVICE`, including assumptions, evidence basis, validation steps, and uncertainty. | G4, G5; unsafe advice | Supports utility while preserving epistemic boundaries. |
| R9 | Must | Apply claim-level citations, citation validation, unsupported-claim markers, and no-fabricated-source checks. | G3, G5; citation errors | Principal release gate; may reduce fluent output. |
| R10 | Must | Enforce access/legal and secure-fetch boundaries, source rate limits, and no-paywall-bypass behavior. | G6; legal/security exposure | Hard constraint even when it reduces coverage. |
| R11 | Must | Expose partial failures and permit useful export from successfully processed papers without hiding omissions. | G2, G4; brittle workflows | Favors honest degradation over all-or-nothing failure. |
| R12 | Must | Export deterministic section order, provenance metadata, labels, and citation keys as Markdown. | G4, G5; non-reusable output | Supports downstream use and automated validation. |
| R13 | Should | Let users edit corpus membership and regenerate while preserving prior run provenance. | G2; changing research scope | High value after core trust path works. |
| R14 | Should | Surface available correction/retraction and publication-state signals without making a quality verdict. | G2, G3; legitimacy ambiguity | Useful warning; depends on provider coverage. |
| R15 | Should | Provide domain-neutral comparison dimensions plus optional use-case prompts for recommenders, fine-tuning, and course recommendations. | G4; generic synthesis | Improves actionability without hard-coding one domain. |
| R16 | Could | Expand from a URL to related-paper discovery, citation graph, or “similar methods.” | G1; narrow starting set | Valuable but can bias corpus and expand provider scope. |
| R17 | Could | Support user-uploaded PDFs, notes, collaborative annotations, and reference-manager sync. | G1, G4; workflow friction | Deferred due to storage, rights, privacy, and collaboration scope. |
| R18 | Won't | Claim exhaustive coverage, rank truth, bypass restricted access, or autonomously implement recommendations. | G6; overtrust | Explicit exclusion protects trust and scope. |

## 9. Markdown Output Contract

The export must preserve this order. Empty sections remain present with a reason rather than disappearing.

```markdown
---
title: "<topic or paper title>"
generated_at: "<ISO-8601>"
run_id: "<stable run identifier>"
input_type: "topic | paper_url"
input_value: "<exact user input>"
corpus_status: "user-confirmed"
analysis_scope: "full-text | mixed-access | abstract-only"
providers: ["<provider>"]
---

# Research Insight Brief

## Scope and Provenance
- Query, filters, retrieval time, included/excluded papers, access limits

## Executive Overview
> Label: CROSS-PAPER SYNTHESIS | PAPER-SPECIFIC

## Paper Register
### [P1] Paper title
- Authors; year; venue/repository; DOI/identifier; version; publication state
- Access scope; source URL; retrieval timestamp; correction/retraction signal

## Paper-Specific Analysis
### [P1] Paper title
#### Overview
#### Research Question
#### Methods
#### Data and Evaluation
#### Findings
#### Limitations
#### Reproducibility and Artifacts
> Label: PAPER-SPECIFIC

## Cross-Paper Synthesis
### Agreements
### Disagreements
### Method and Dataset Comparability
### Evidence Gaps
> Label: CROSS-PAPER SYNTHESIS

## Implementation Guidance
### Candidate Approach
### Preconditions and Assumptions
### Minimal Experiment
### Metrics and Failure Modes
### Operational, Ethical, and Legal Considerations
> Label: GENERATED ADVICE

## Use-Case Synthesis
### Recommender Systems
### Fine-Tuning
### Course Recommendations
### Other User-Specified Use Case
> Label: GENERATED ADVICE

## Uncertainties and Unsupported Claims

## References and Evidence Map
- [P1:S1] claim/passage locator, version, page/section/figure/table, source URL

## Generation Notes
- Model/system version, schema version, partial failures, parser warnings
```

Schema rules:

- Each analytical paragraph or list item carries or inherits one primary class label.
- `[P#]` identifies an analyzed paper/version; `[P#:S#]` identifies evidence within that paper.
- Overview, methods, findings, and limitations are paper-specific before any cross-paper aggregation.
- Single-paper runs retain the cross-paper section with `Not applicable: one confirmed paper`.
- Use-case subsections are generated only when relevant; irrelevant named examples say why they do not apply.
- Generated advice includes a minimal validation step and never appears in the paper-specific section.

## 10. Acceptance Criteria

Each criterion is independently testable against a fixed benchmark and maps to requirements.

- AC1 — Given a topic, the system records the exact query, filters, providers, retrieval timestamp, raw candidate count, and de-duplicated candidate count before corpus confirmation. (R1)
- AC2 — Given a supported DOI, arXiv, PubMed/PMC, publisher, or direct-PDF URL, the system either identifies one canonical scholarly record/version or returns a specific ambiguity/unsupported/access error without generating analysis. (R2)
- AC3 — No topic-path synthesis starts until the user confirms at least one included paper; the export lists included and excluded candidates with exclusion reasons available. (R3)
- AC4 — Every paper displays exactly one current access state, and abstract-only/metadata-only papers cannot produce claims presented as full-text findings. (R4)
- AC5 — From a paper-specific claim, a user can open the cited inspected passage or the system shows a precise unavailable/degraded locator state; no claim links silently to an unrelated version. (R5)
- AC6 — A single-paper export contains every required Markdown heading in the specified order and explicitly marks cross-paper synthesis not applicable. (R6, R12)
- AC7 — A multi-paper export uses cross-paper claims only where at least two confirmed papers are cited and names conflicts or non-comparability when the source evidence differs. (R7)
- AC8 — Every implementation or use-case recommendation is labelled `GENERATED ADVICE` and includes assumptions, supporting evidence keys, uncertainty, and at least one validation step. (R8)
- AC9 — An export validator finds no substantive paper-specific factual claim lacking a citation key or explicit unsupported marker, and every key resolves to the source register. (R9)
- AC10 — On a locked human-audit sample of at least 100 claims, at least 95 are entailed by the cited evidence, none cite a fabricated paper, and all direct quotations match the source text. (R9)
- AC11 — Requests using `file:`, loopback, private/link-local addresses, credential-bearing URLs, redirect-to-private destinations, or disallowed/oversized content are rejected and produce no fetched-content analysis. (R10)
- AC12 — For a paywalled page without authorized full text, the system does not attempt bypass; it produces only allowed metadata/abstract analysis and clearly states the limitation. (R10)
- AC13 — If one provider or paper fails after corpus confirmation, successful papers remain inspectable/exportable and the failed source and affected sections are explicitly listed. (R11)
- AC14 — Repeating export for an unchanged completed run yields the same section order, paper keys, evidence keys, labels, and provenance fields, excluding explicitly documented volatile fields. (R12)
- AC15 — Editing corpus membership creates a new provenance record, and no removed paper remains cited in regenerated synthesis. (R13)
- AC16 — When provider metadata reports a retraction, correction, or preprint status, the paper register displays that status and does not convert it into an unsupported quality score. (R14)
- AC17 — In a label-comprehension test, at least 8 of 10 representative users correctly distinguish author findings, cross-paper inference, and generated advice across five sampled output blocks. (R6–R9)
- AC18 — Markdown renders without broken internal citation keys, and all external evidence URLs are syntactically valid or explicitly marked unavailable at export time. (R12)

## 11. Dependencies, Constraints, and Risks

### Dependencies

- Approved scholarly metadata/search providers and stable identifier resolution.
- Lawful full-text sources and provider-specific terms/rate limits.
- Reliable PDF/HTML parsing with page and structural locators.
- Grounded generation and claim/citation validation capability.
- Legal/privacy review of ingestion, quotation, storage, and provider use.
- Security review of remote fetching, content handling, and generated-output risks.
- Evaluation corpus, trained reviewers, and a reproducible claim-audit method.

### Key risks and mitigations

| Risk | Impact | Mitigation / release posture |
|---|---|---|
| Fabricated or mismatched citations | Critical trust failure | Fail closed on unresolved evidence keys; independent claim audit; zero fabricated-source gate |
| Abstract-only overgeneralization | Incorrect findings/limitations | Access-state enforcement and explicit abstract-only language |
| Retrieval bias or apparent exhaustiveness | Misleading literature view | Show query/providers/filters/date and require corpus confirmation |
| Version, duplicate, correction, or retraction confusion | Claims attach to wrong record | Version-aware grouping and exact analyzed-version citations |
| Copyright/provider-term breach | Legal and availability risk | Approved-source allowlist, minimal retention/quotation, legal gate |
| SSRF, malicious PDFs/HTML, prompt injection | Security or integrity compromise | Isolated parsing, URL/network controls, content limits, untrusted-text treatment |
| Generated advice mistaken for evidence | Unsafe decisions | Mandatory class labels, separate sections, assumptions and validation steps |
| Domain heterogeneity | Misleading fixed schema | Preserve unknown/not-reported states and validate across multiple domains |
| Metric gaming through citation density | Many citations but weak entailment | Human entailment audit and disagreement checks, not count alone |
| Provider outages/rate limits | Broken workflows | Partial-result behavior, retry guidance, provider health disclosure |
| Sensitive topic/query retention | Privacy concern | Data minimization, configurable deletion, no training reuse by default pending decision |
| Cost/latency escalation | Poor adoption | Corpus caps, staged generation, transparent limits; decide after pilot measurements |

## 12. Open Decisions and Recommended Defaults

| Decision | Recommended default | Owner | Why reviewer must challenge it |
|---|---|---|---|
| Primary launch persona | Applied ML practitioners first; support research/education second | Product owner | Use-case guidance may distort a research-first product. |
| Source coverage | Start with Crossref/OpenAlex-style metadata plus canonical open repositories; approve exact providers in Shape | Product + Legal + Tech Lead | Coverage, terms, and identifiers vary materially. |
| Full-text policy | Open or explicitly user-authorized content only; no credentials in MVP | Legal/Security | May make URL success appear low for commercial publishers. |
| Corpus size | Default 8, user cap 20 papers per run | Product + Tech Lead | Quality, latency, cost, and synthesis depth trade off. |
| Ranking | Relevance with recency/diversity signals shown; no opaque “quality” score | Product | Ranking bias shapes evidence before user selection. |
| Input language | English text-first MVP | Product owner | Excludes users and research; multilingual support affects evaluation. |
| Persistence | Persist metadata, outputs, and evidence map; source content transient by default | Privacy/Legal + Tech Lead | Inspection, reproducibility, deletion, and cost pull in opposite directions. |
| Advice generation | Opt-in use-case guidance after evidence summary | Product owner | User intent may justify default-on, but overtrust risk is high. |
| Confidence display | Use evidence-status language, not numeric confidence | Product + Design | Numeric scores invite false precision; qualitative labels may be vague. |
| Retraction handling | Warn prominently and include only after explicit user confirmation | Product + Legal | Exclusion may hide historically relevant evidence; inclusion may spread harm. |
| Export editability | Export Markdown without claiming post-export citation integrity after user edits | Product + Design | Users need flexibility but provenance can become stale. |
| Quality release gate | ≥95% sampled entailment and zero fabricated sources; block if missed | Product + QA | Threshold is proposed without baseline and may be too lenient or infeasible. |
| User data reuse | No provider/user content used for model training by default | Privacy/Legal | Business and model-quality goals may pressure a different choice. |
| Decision deadline | Set before Shape begins; no architecture selection until legal/source defaults close | Orchestrator | Current deadline and accountable names are missing. |

## 13. Handoffs

### Product Designer

Design for two entry jobs, corpus confirmation, inspection, and honest partial states—not a final visual direction yet.

- User needs: quick start, visible corpus control, claim-to-evidence navigation, comprehension of three claim classes, and recoverable partial failures.
- Workflows: topic discovery/selection; URL resolution/confirmation; evidence inspection; corpus revision/regeneration; Markdown preview/export.
- Required states: all states listed in Section 6, especially abstract-only, access denied, parser degraded, stale citation, retraction/correction, and mixed-access corpus.
- Content constraints: never collapse class labels; always show analyzed version/access scope; avoid “verified,” “comprehensive,” or “recommended” without qualification.
- Decisions required: label treatment and inheritance, evidence-opening interaction, corpus-confirmation friction, partial-result messaging, stale/regenerated output treatment, and accessibility for dense scholarly content.
- Open UX questions: Can users distinguish synthesis from advice without reading a legend? Where should provider/query limitations persist? How should unavailable locators and conflicting versions be explained?

### Tech Lead

Shape the system only after product/legal source defaults are approved; do not reinterpret evidence classes as implementation details.

- Priorities: R1–R12 are MVP gates; R13–R15 follow only if Must requirements fit the delivery boundary; R16–R17 remain deferred.
- Contracts needed: canonical paper/version identity, access state, corpus/run provenance, evidence locator, claim class, citation key, partial-failure record, and deterministic export schema.
- Constraints: no access-control bypass, secure remote fetch, untrusted document isolation, exact-version citations, explicit mixed-access behavior, and no hidden corpus mutation.
- Verification: map tests to AC1–AC18; establish the locked corpus and independent entailment review before release claims.
- Decisions required: provider feasibility and terms, locator fidelity by format, parsing isolation boundary, transient/persisted data boundary, deterministic identity/key strategy, model/provider observability, and cost/latency envelope.
- Technical questions: How are redirects and version aliases canonicalized? What citation locator survives PDF/HTML differences? How does generation fail closed on missing evidence? How are prompt injection and malicious files contained? Which fields can be deterministically regenerated?

### Grilling Reviewer

Challenge these decisions before `frame-approved`:

- Whether the primary user and first decision context are narrow enough to evaluate.
- Whether corpus confirmation, limits, and ranking defaults adequately expose retrieval bias.
- Whether “legitimate paper” and publication-state signals are precise without implying truth or quality.
- Whether full-text/access defaults are lawful, useful, and commercially viable.
- Whether the three claim classes remain unambiguous in every output section and edge state.
- Whether the proposed 95% entailment gate and zero-fabrication gate are sufficient and measurable.
- Whether generated implementation/course advice belongs in MVP or should follow validated evidence workflows.
- Whether persistence, deletion, source retention, and model-training reuse defaults protect users and providers.
- Whether English-only, 8-paper default, 20-paper cap, and named use cases bias the product too early.
- Whether the smallest validation can disprove the core assumptions before source integrations or architecture commitments.

## 14. Decisions and Next Actions

- Product owner: confirm primary persona, advice-in-MVP, corpus limits, launch language, and success thresholds.
- Legal/privacy: approve source/provider, access, quotation, retention, deletion, and training-reuse boundaries.
- Grilling reviewer: pressure-test assumptions, exclusions, metrics, and defaults listed above.
- Product Designer: test class-label comprehension and evidence-navigation workflow after frame approval.
- Tech Lead: assess provider/locator/security feasibility only after blocking product and legal decisions close.
- QA: define the locked benchmark, claim sampling protocol, and pass/fail evidence for AC1–AC18.
- Orchestrator: assign accountable stakeholder names and a dated decision deadline; record `frame-approved` only after material trade-offs are accepted.
