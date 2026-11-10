# QA Report: Job Intelligence LLM Planner Audit

**Run audited:** `job-intelligence-llm-planner-20261110`  
**Audit date:** 2026-11-10  
**Auditor posture:** cross-artifact consistency and readiness audit; no legal, privacy, security, accessibility, source, finance, frame, shape, implementation, or release approval  
**Artifacts reviewed:** `final-plan.md`, `design.md`, `technical-plan.md`, `brief.md`, `planner-responses.md`, `grill-log.md`, and research notes under `research/`

## Executive Verdict

**Status: PASS for planning handoff, CONDITIONAL for Shape intake, BLOCKED for implementation/release.**

The final plan is materially consistent with the design proposal, technical plan, cited research, and three rounds of grill decisions. It preserves the core settled boundaries:

- one course-recommendation product with independently gated assistant and job-context capabilities;
- deterministic backend authority over prerequisites, readiness, filtering, scoring, ranking, exact-slot assignment, and open-slot reasons;
- Stage 1 and Stage 2 read-only behavior with no recommendation mutation;
- LinkedIn disabled unless written authorization covers the exact use;
- no arbitrary URL fetch and no LinkedIn-derived supplied-posting workaround;
- operator-managed server model credential, not tenant BYOK;
- deterministic fallback before model calls;
- immutable claim/citation identity and exact evidence for accepted factual claims;
- private supplied-posting results and private derivatives expiring together within one hour after successful analysis;
- Stage 2 item-level evidence only, with no aggregate gap, fit, coverage, demand, trend, or ranking claim;
- market-informed ranking deferred to a later deterministic proposal with separate entry and exit gates.

No material scope-widening contradiction was found. The remaining issues are readiness gaps, explicit authority dependencies, and evaluation details that must be closed before implementation or release.

## Source Coverage

| Artifact | Role in audit | Result |
|---|---|---|
| `final-plan.md` | Authoritative product plan and decision ledger | Internally coherent and reconciles the grill decisions |
| `design.md` | Proposed UX Shape input | Consistent with final product boundaries and trust language |
| `technical-plan.md` | Proposed buildable architecture | Consistent with authority boundaries and noninterference constraints |
| `brief.md` | Earlier product brief | Superseded by final plan where grill decisions narrowed scope |
| `planner-responses.md` | Product manager decision trail | Matches `grill-log.md` and final decision ledger |
| `grill-log.md` | Three rounds plus Final Frontier Certificate | All 34 decisions carried into final plan |
| `research/citation-verification.md` | Citation safety gate | Final plan uses corrected or planner-safe forms; no blocked claim reliance found |
| `research/linkedin-access.md` | LinkedIn/source-access research | Final plan preserves LinkedIn exclusion and rights-gated alternatives |
| `research/extraction-and-operations.md` | Extraction, taxonomy, freshness, provenance defaults | Final plan carries the core controls and labels internal defaults as proposed |
| `research/repo-analysis.md` | Current repository capability and gap analysis | Technical plan reflects current monolith, no assistant/job pipeline, no auth, sparse skills evidence |
| `research/security-constraints.md` | Security and release-blocking constraints | Final and technical plans preserve release blockers and non-waivable stops |

## Cross-Artifact Findings

### 1. Planning Authority Is Correctly Scoped

**Result: PASS**

The final plan repeatedly states that planning is complete but not frame-approved, shape-ready, implemented, or released. This matches:

- `design.md`, which is explicitly proposed Shape input only;
- `technical-plan.md`, which is proposed architecture only;
- `security-constraints.md`, which says production release is blocked;
- the Final Frontier Certificate, which says product frontier is empty but authority approvals remain outside product planning.

No artifact converts absence of legal, privacy, security, source, academic, finance, accessibility, or release approval into backlog consent.

### 2. Grill Decisions Are Reconciled

**Result: PASS**

The final decision ledger contains 34 settled decisions: 15 Round 1, 15 Round 2, and 4 Round 3. The concrete defaults, exclusions, owners, and revisit triggers match `planner-responses.md` and `grill-log.md`.

Key reconciliations verified:

- Stage 1 exact six intents are present.
- Stage 2 exact pilot scope is English-language evidence for Singapore-based NTU computing students exploring entry-level/graduate `software_engineer` and `data_engineer`.
- Unsupported titles are not coerced.
- `role_target` and `supplied_posting` are independent release units.
- Successful supplied-posting result lifetime is one hour, not the earlier broad 24-hour wording.
- BYOK remains disabled and the promised token is an operator/deployer-managed server secret.
- Ranking is not committed scope and remains a later deterministic proposal.

### 3. Brief Open Questions Were Closed or Reclassified

**Result: PASS**

The earlier `brief.md` listed open decisions around geography, seniority, aliases, posting persistence, provider/cost, mapping reviewers, score exposure, anonymous catalog chat, first provider, and preference mutation. The final plan either settles these as product defaults or moves them to authority-deferred dependencies.

Examples:

- Geography/seniority/aliases are settled by Round 3 scope.
- Posting persistence is settled as one-hour active private result plus no history/save/share/export.
- Score components are qualitative-only; raw numeric components remain hidden.
- Anonymous catalog chat and preference mutation are explicitly deferred/excluded.
- First live provider is authority-deferred, not approved backlog.

### 4. Design Preserves Product Boundaries

**Result: PASS**

`design.md` aligns with `final-plan.md` on:

- first-class `Assistant` view rather than a floating general chat;
- three independently gated modes;
- hidden unreleased modes rather than aspirational disabled controls;
- claim-class labels and visible distinctions between deterministic facts, posting evidence, taxonomy context, normalized inference, and generated explanation;
- readiness not registration eligibility;
- exposure not mastery;
- no aggregate gap/fit/coverage/missing-skills score;
- no URL fetch and no LinkedIn-derived supplied-posting analysis;
- one active private analysis with visible expiry and delete;
- content-free analytics.

The design acceptance checklist is appropriately framed as future Shape/implementation acceptance, not evidence that the UI has passed.

### 5. Technical Plan Enforces Noninterference

**Result: PASS**

`technical-plan.md` gives concrete structural controls for the final plan's authority boundaries:

- no assistant/job-intelligence imports into `recommendation_service.py`;
- no recommendation-service import in assistant or posting modules;
- no Stage 2 tables in recommendation queries, views, or database roles;
- no market fields in `RecommendationRequest`;
- `MARKET_RANKING_ENABLED=false` absent from ordinary runtime configuration until an approved Stage 4 change;
- dependency and response-hash regression checks to fail CI if Stage 1/2 changes locked recommendation outputs.

This is stronger than a feature flag-only separation and matches the grill decision that Stage 2 cannot affect ranking before Stage 4 gates.

### 6. Citation Audit Is Respected

**Result: PASS**

`research/citation-verification.md` marks 117 claims verified, 10 usable only after correction, and 46 blocked. The final plan's external claims use the corrected safe forms for:

- LinkedIn Open Permissions and job-search inventory;
- Job Posting API outbound-posting scope;
- Apply Connect ATS workflow scope;
- O*NET/ESCO as taxonomy/classification context, not vacancy feeds;
- Schema.org fields not guaranteeing publisher completeness or typed values;
- structured outputs requiring application/evidence validation.

No blocked citation-audit claim was found being used as an external fact in the final plan.

### 7. Source and Security Constraints Are Carried Forward

**Result: PASS**

The final and technical plans preserve the key constraints from `linkedin-access.md`, `extraction-and-operations.md`, and `security-constraints.md`:

- no LinkedIn scraping, logged-in automation, indirect scraped datasets, or LinkedIn-origin supplied postings;
- no arbitrary URL fetch in Stages 0-2;
- future fetches only through registered source-policy/query pairs;
- isolated worker before authorized network collection/scheduling;
- SSRF, redirect/DNS, egress, hostile-content, and static-parsing controls before Stage 3;
- external model synthesis blocked until provider/privacy, secret, prompt/tool, cost, audit, and fallback gates pass;
- production private analysis blocked without authenticated server identity and tenant scope.

### 8. Evaluation Gates Are Consistent but Not Yet Operationalized

**Result: PASS WITH FOLLOW-UP**

The final plan is consistent with the planner decisions on locked sets, human review, dual annotation, task-success gates, comprehension gates, and audit sampling. It correctly labels thresholds as proposed release targets rather than measured results.

Follow-up remains required because the plan does not yet define:

- final fixture files and annotation guide;
- exact source/template/time split procedure;
- confidence-interval reporting method for the 20-user studies;
- final acceptance evidence package format per capability;
- who can reduce the 10% random weekly sampling rate after four clean cohorts.

These are suitable Shape/evaluation tasks, not contradictions.

## Residual Risks

| Risk | Severity | Evidence | Required follow-up |
|---|---|---|---|
| Evaluation corpus size may be underpowered for heterogeneous posting extraction | Medium | `extraction-and-operations.md` proposes 300 logical families with 100 locked test families; final plan requires at least 100 locked posting families overall plus critical fallback strata | Research/evaluation owner should confirm whether the final minimum covers expected source/template diversity before release metrics are accepted |
| One-hour deletion promise depends on backup/PITR semantics | High | `technical-plan.md` notes PostgreSQL backup/PITR may conflict with the one-hour content promise | Privacy/security/DevOps must define backup deletion semantics or keep Stage 2B blocked |
| Current repo lacks authenticated server identity and tenant scope | High | `repo-analysis.md` and `security-constraints.md` identify browser-controlled localStorage and no backend student entity | Stage 2B and production model personalization must remain blocked until server-derived tenant scope and cross-tenant negative tests exist |
| Course-skill evidence remains sparse | High | `repo-analysis.md` identifies seven-course/nine-link preview and unknowns | Academic/domain owner must review and version course links; UI must keep item-level unknowns and avoid aggregate gap claims |
| Provider, endpoint, region, retention, and pricing are unresolved | Medium | Final plan and technical plan defer these to authority decisions | Provider adapter cannot be enabled until privacy/security/finance/release records exist |
| Accessibility and contrast evidence is not yet produced | Medium | `design.md` defines requirements but no test results | Accessibility owner must approve keyboard, screen-reader, contrast, reduced-motion, zoom, and mobile reflow evidence |
| Future source alternatives are candidates, not approvals | High | `linkedin-access.md` says public API docs do not settle commercial rights, retention, derivatives, LLM use, display, or deletion | Legal/source owner must record written source-specific rights before Stage 3 |

## QA Checks

| Check | Result | Notes |
|---|---|---|
| Final plan contains exact six Stage 1 intents | PASS | Matches Round 2 Q1 |
| Stage 2 mode separation is explicit | PASS | `role_target` and `supplied_posting` have independent gates |
| LinkedIn exclusion is preserved | PASS | No LinkedIn use without written authorization |
| Supplied-posting lifecycle matches Round 3 | PASS | One-hour successful active result; 24-hour failed/interrupted cleanup |
| No aggregate Stage 2 skills-gap claims | PASS | Item-level evidence only |
| No LLM ranking/scoring authority | PASS | Stage 4 separate deterministic proposal only |
| Model secret custody matches security guidance | PASS | Server-side operator credential; BYOK disabled |
| Numeric gates labelled proposed/not measured | PASS | Repeated in final plan and planner responses |
| Citation-audit blocked claims avoided | PASS | No blocked claim reliance found |
| Technical noninterference controls present | PASS | Import/query/request/CI checks proposed |
| Release blockers visible | PASS | Non-waivable stops preserved |
| Shape open questions do not widen scope | PASS | Open items are interaction/implementation choices |

## Required Actions Before Shape Approval

1. Create a Shape acceptance checklist that references the final plan's non-waivable boundaries, not the older brief's broader possibilities.
2. Freeze API and UI contracts for the six Stage 1 intents, including fallback, citations, limitations, unsupported intent, and stale-context behavior.
3. Define the evidence package template for each capability gate: fixtures, commands, sample outputs, reviewer decisions, known gaps, and rollback proof.
4. Assign named owners for academic/course-skill review, data/domain mapping review, privacy/security deletion approval, accessibility review, and release authority.
5. Decide whether the extraction evaluation corpus needs the full 300-family design default or whether the final 100-locked-family minimum is sufficient for the pilot's source/template mix.
6. Resolve backup/PITR, deletion tombstone, and operational metadata semantics before Stage 2B implementation starts.
7. Keep live source procurement, external model calls, private multi-user analysis, and any ranking work blocked until their authority records exist.

## Final QA Judgment

The planner artifacts are internally consistent and suitable for a parent handoff into constrained Shape work. The final plan correctly narrows the earlier brief, incorporates grill decisions, respects the citation audit, and preserves research/security constraints.

The handoff must not be treated as implementation approval. The safe next step is Shape work for contracts, UI states, schemas, fixtures, evaluation evidence packages, and operational controls under the exact boundaries already settled.
