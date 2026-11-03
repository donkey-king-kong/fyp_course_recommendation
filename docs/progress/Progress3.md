# Progress 3

Active development log. Earlier work is listed in the [progress index](README.md); current priorities live in [STATUS.md](../STATUS.md).

## Documentation Organization And Project PR Skill

Date: 2026-11-03

Status: Implemented; verification is recorded below.

### What Was Created And Changed

- Organized architecture, evaluation, reference, workflow, planning, and progress documentation under `docs/`.
- Preserved both earlier progress logs and the mistake history. Created a progress index identifying this log as active.
- Added `docs/STATUS.md` for current capabilities, next priorities, evidence boundaries, and deferred work, plus `docs/README.md` for navigation.
- Moved detailed milestone, SSO, and evaluation planning from `AGENTS.md` to `docs/plans/Development_Plan.md`. Historical planning details remain contextual, with current status taking precedence.
- Updated root `AGENTS.md` with startup links, preserved project rules, and the actual working-directory path. Updated the README and product document's live references and six-career summary.
- Added `.agents/skills/create-project-pr/SKILL.md`. It reads the single shared `docs/workflows/PR_template.md`, requires the project title/body conventions and assignee verification, and preserves conversation authorization.

### Verification

- The bundled skill-creator validator reports `Skill is valid!` for the PR skill.
- Verified all 58 local Markdown navigation links, including the skill's relative references and the latest historical-entry anchor.
- SHA-256 checks confirm 10 moved documents are byte-for-byte identical, including both closed progress logs, the mistake history, and the shared PR template. The product and evaluation documents have deliberate live-reference edits.
- Confirmed the detailed milestone, SSO, evaluation, and past-project reference guidance is retained in the planning document.
- Confirmed only `AGENTS.md` and `README.md` remain as root Markdown entry points and there is exactly one shared PR template.
- Checked new and edited documents for trailing whitespace. Existing historical formatting was preserved.
- `git diff --check` passes. Application tests and fresh recommendation captures were not run for this documentation-only change.

### What Is Not Included Yet

- No application, database, scoring, dependency, or evaluation-artifact changes.
- No SSO, server-side persistence, deferred ranking calibration, or AI integration.
- No PR creation or update; this work only prepares the reusable workflow. The project owner authorized commits and a push on the current branch.
- Existing ignored Impeccable installations under `.agent/` and `.gemini/` were retained; system skills were not changed.

### Next Step

Follow `docs/STATUS.md`: expert review before broader recommendation calibration, then NTU SSO and server-side persistence.

## Recommendation Development Plan And Weak-Fit Policy

Date: 2026-11-03

Status: Planning documents updated. Baseline capture, expert review and policy implementation remain pending.

### What Changed

- Replaced the old SSO-first development sequence with dependency-based steps: baseline/policy, student skills picture, job-market evidence, pathway chat, combined evaluation, then SSO and server persistence. No calendar deadlines are assigned.
- Scoped the improvement pilot to Software Engineer and Data Engineer while retaining existing support and regression coverage for all six careers.
- Recorded the owner's approved weak-fit direction: normal career recommendations for strong matches, labelled interest alternatives for useful explicit interest matches, and open slots with explanations when neither applies.
- Added a seven-case review shortlist, evidence checklist and acceptance criteria to `docs/plans/Development_Plan.md`. The shortlist comes from existing case descriptions, not new runtime results.
- Updated `docs/STATUS.md` and `AGENTS.md` so future work follows the new sequence and does not mistake approved policy for implemented behavior.
- Retained SSO's backend MSAL, validated-tenant identity and server-session boundaries as deferred guidance. The older 21-case review packet and closed progress logs remain historical records.

### Verification

- Checked local Markdown link targets in the four touched documents; all exist.
- Confirmed all seven shortlisted case IDs exist in the unchanged 24-case benchmark.
- Checked live planning guidance for stale SSO-first sequencing and month-based deadlines.
- `git diff --check` passes. Changes are limited to documentation.

### What Is Not Included Yet

- No scoring, frontend, database, dependency or benchmark-label changes.
- No fresh baseline capture, new review packet, expert validation or application test run.
- No job-data pipeline, course-skill model, LLM integration, SSO or server persistence.
- No commits, pushes or PR publication.

### Next Step

Capture the unchanged baseline with the existing runners and verified serving/data provenance. Prepare a compact review table for the seven pilot cases, adding separately identified boundary scenarios if the capture lacks interest-only or no-strong-match examples. Review evidence before choosing thresholds or implementing the weak-fit behavior.

## Unchanged Baseline Capture And Seven-Case Review Preparation

Date: 2026-11-03

Status: Capture and review preparation complete; human policy review pending.

### What Was Created

- Created `docs/evaluation/Recommendation_Baseline_Review_2026-11-03.md` with reproduction commands, source/database provenance, a seven-case/18-slot review table, discrepancy findings and proposed boundary questions.
- Saved full exact request/response captures and complete benchmark metrics under `data/review/baseline_2026-11-03/` for the existing 24-case benchmark, 180-cell grid, nine positioned scenarios and eight counterfactual checks.
- Updated `docs/STATUS.md` with the fresh capture and review stop point. The previously uncommitted planning changes in four documents were inspected and retained.

### Verification

- Owned backend on port 8013 from HEAD `c34650fe0ab8e4de53372b330cb691ef8311db0f`, with no backend/script/catalog diff. Local PostgreSQL had 4,318 modules, 4,178 prerequisites and 34 faculties; read-only row fingerprint `c443b5b0dbb72f014be71ba8780be963cbf09bb23a774b312859a4c1166faf8d` matched before and after. The capture files carry the operator-declared serving/database metadata and local source hashes; the report explains the provenance boundary.
- Benchmark: 24 unique cases, 53 recommendations, nDCG@returned `0.7413`, precision@returned `0.7778`, all slots filled, zero supplementary violations. Grid: 180/180 filled, 18 weak-fit cells, no violations or pass-2 interest picks. Positioned: 8 pass / 1 inconclusive; counterfactual: 6 pass / 2 inconclusive. The raw/evaluated case, count, response and violation totals agree.
- Preserved benchmark labels/input, frozen cases 001-005, historical predictions and historical coverage file. The review packet records their SHA-256 digests and the new capture hashes.

### Limitations And Next Step

- Course tags/label notes disagree in some places with current course content or reviewed Cloud prerequisites; these are reported as separate content/data-evidence questions. Code-only curricula do not prove full eligibility or actual offerings. Neither the shortlist nor the grid establishes a no-fit abstention example.
- Ask the supervisor/TA to review contested course evidence, eligibility and career/interest boundaries. Record extra boundary scenarios separately if needed. Stop before selecting thresholds or implementing the weak-fit policy; no scoring, data, evaluator, labels, commits or pushes were changed for this work unit.

## Internal Pilot Evidence Review

Date: 2026-11-03

Status: Evidence-based course review recorded; owner product decision pending.

- Compared the captured seven cases and 18 assigned slots with the full current database descriptions, curated tags, career mappings and reviewed prerequisite groups. Added per-case judgments to the baseline review packet: 15 plausible career-fit candidates, two explicit-interest candidates and one contested strong-fit candidate. These are internal content judgments, not new benchmark labels or proof of registration eligibility.
- Corrected an overbroad concern about `SC4022`: its Network Science description explicitly lists cyber-security applications, but does not demonstrate the depth of an applied software-security course. `SC4001`'s neural-network content being credited as computer networking remains a concrete semantic mapping defect. No course data or scores were changed.
- Escalated only the product trade-off between a supported but interest-mismatched SWE recommendation and a useful explicit-interest option. Missing abstention examples and complete academic eligibility evidence remain to be gathered before policy implementation. External expert validation is distinct from this internal review and would still be needed for an expert-reviewed FYP claim.
- Verified against the frozen capture and preserved the original uncommitted changes. No benchmark cases, labels, historical captures, policy code, commits or pushes were changed.

## Career-First Slot Priority Confirmed

Date: 2026-11-03

Status: Product priority clarified; weak-fit boundary review and implementation remain pending.

- The owner confirmed career-first selection: strong eligible career matches take priority even when preferences differ; use remaining slots for useful eligible explicit-interest alternatives, otherwise leave slots open with an explanation. A plausible or structurally high-scoring course is not automatically a strong career match.
- Updated the development plan, current status and seven-case review packet to distinguish this decision from unchosen strength thresholds, unverified academic eligibility and the separate implementation work. The existing baseline captures, draft labels, scripts and application code were not changed.

## Step 1 Recommendation Boundary Review

Date: 2026-11-03

Status: Internal qualitative review recorded; full-catalog transition, true abstention and one course-value judgment remain open. No policy implementation.

- Created `docs/evaluation/Recommendation_Boundary_Review_2026-11-03.md` from the unchanged benchmark, coverage, positioned and counterfactual captures. Compared direct Data Engineer and AI/ML positives with indirect AI/ML database and Cloud/Platform architecture picks, the constrained graphics interest source path, and inconclusive Cloud prerequisite planning.
- Proposed a content-evidenced minimum career-fit rule, a verified explicit-interest fallback and explained abstention reasons. No universal numeric threshold is approved; a weak full-catalog winner is not proof that no better eligible alternative exists.
- Rechecked the database fingerprint and the frozen input, historical prediction and new-capture hashes against the baseline packet. No application, course data, evaluators, case labels or captures were changed.
- Found a separate standing/fixture gap: `SC3060`'s catalog requires Year 2 standing, but its no-completions positioned request returns `ready`; the recommender does not establish standing from completed AU. Its interest-source routing passes, but student eligibility is unproven. No policy or eligibility code was changed.
- Next: verify an unrestricted interest-versus-weak-career pair with valid academic standing and a genuinely relevance-based open-slot case; investigate mapping defects and unresolved registration separately.

## Cloud/Platform Boundary Decision

Date: 2026-11-03

Status: Owner course-value judgment recorded; full-catalog controls and implementation remain pending.

- `SC3050` Advanced Computer Architecture is useful complementary systems study, but is not a strong default Cloud/Platform recommendation merely because no direct course is available. A verified explicit architecture interest remains a separate possible reason to consider it.
- An open slot is conditional on checking the full set of eligible career and interest candidates. Updated the boundary packet and status; no scoring, catalog, benchmark or evaluator changes were made.

## Step 1 Full-Catalog Boundary Controls

Date: 2026-11-03

Status: Captured six separate synthetic diagnostics; interest masking confirmed, true relevance-based abstention not observed. No policy implementation.

- Added two versioned scenario sets and unchanged-backend full request/response captures, documented in `docs/evaluation/Recommendation_Boundary_Controls_2026-11-03.md`. The frozen 24-case inputs, labels, historical predictions and original captures were preserved.
- Cloud/Platform Y2-end returns weak `SC3050` with and without a graphics interest, but excluding it solely for diagnosis exposes `SC3030` Advanced Computer Networks with supported prerequisite `SC2008`; do not call that slot a no-career-fit example.
- AI/ML Y4-end returns indirect `SC3020` with and without an HCI interest. `SC3061` has matching content and supported slot/course prerequisites, yet receives no slot under current career-first fill. A one-course diagnostic exclusion exposes `SC3021`, an unreviewed data-science foundation after completed AI/ML courses.
- Existing response-contract validation reported zero violations for all six cases. The owned backend, source-file hashes and local DB fingerprint were consistent with the baseline; the DB fingerprint was unchanged after capture. The absent transcript-AU/standing and real registration checks are still separate gaps.
- Stop before policy implementation: inspect the eligible candidate frontier and course depth for a defensible no-fit/true-open example; do not tune constants to force one. The project-owner `SC3050` judgment remains recorded, but is not an unconditional open-slot instruction.

## AI/ML Course-Value Decision

Date: 2026-11-03

Status: Owner judgment recorded after the six-case capture; no benchmark relabelling or policy change.

- The owner considers `SC3021` Data Science Fundamentals a **strong AI/ML career fit** for the reviewed student despite completed `SC3000`, `SC4000` and `SC4002`. The diagnostic output had found it behind weak `SC3020`; its supported prerequisite path returned `ready`, without verifying live registration.
- This corrects the initial interpretation of the AI/ML HCI pair: HCI is a plausible explicit interest, but should not displace the owner-approved strong `SC3021` career course. Like Cloud's `SC3030` behind `SC3050`, it demonstrates why a weak first pick does not prove there is no strong career option.
- A separate full-catalog profile with no strong eligible career course is still required to review interest fallback and an explained open slot. Updated the current boundary review and status; no scripts, scorer, evaluator, catalog, labels or raw captures were altered.

## Step 1 Remaining-Slot Review

Date: 2026-11-03

Status: Separately captured and reviewed a conditional no-strong-career example; no policy implementation or observed abstention.

- Added `data/review/remaining_slot_controls_2026-11-03.json`, its live unchanged-backend response capture, and `docs/evaluation/Recommendation_Remaining_Slot_Review_2026-11-03.md`. The hypothetical AI/ML Y4-end profile additionally completes the previously owner-approved strong `SC3021`; the no-interest and HCI-interest requests otherwise match.
- Audited all 26 CSC level-3 modules using the service's candidate filters and readiness rules. The two remaining `ready` career picks, `SC3020` (database, career skill 2) and `SC3060` (graphics/mathematics, career skill 3), do not provide strong default applied-AI content. The owner reviewed `SC3271` as an optional mathematical foundation, not a strong default; its description triggers retrieval, but its empty scored tags drop it. This data/mapping gap is separate from the weak-fit policy.
- The current endpoint still selects `SC3020` for both cases. Calling pass 2 alone with a free HCI slot returns `SC3061` labelled `interest`. Proposed outcomes are an explained open slot with no interest or an HCI interest alternative, subject to eligibility; neither is an observed endpoint response under the unchanged policy.
- The existing response checker reports zero violations for both requests. Serving source hashes and the read-only pre/post database fingerprint match the frozen baseline. Frozen cases, labels, historical predictions, ranking, thresholds, catalog and evaluator remain unchanged.
- Stop for review before a separate implementation work unit. Transcript-completed AU, exact programme/cohort/semester conditions, course offering and registration permission are not established by these synthetic browser-controlled requests; evaluate each newly open slot after any later policy change.

## Bounded Weak-Fit Policy And Controlled Comparison

Date: 2026-11-03

Status: Policy implementation and local comparison complete; provisional evidence rule and one failed counterfactual need review before advancing to the student skills picture.

- On `recommendation-weak-fit-policy`, added a mapped-skill strength gate before backend career assignment, retained the eligibility-checked explicit-interest pass, and returned exact unassigned slot IDs with `no-supported-match` or `limit-reached` explanations. The roadmap labels interest alternatives, renders open slots, and persists both kinds of response for the active browser profile. No catalog, mapping, labels, frozen inputs, or evaluator changed.
- An owned non-reloading backend on port 8016 and the same read-only local database fingerprint produced separate full captures under `data/review/weak_fit_policy_2026-11-03/`. The [comparison](../evaluation/Recommendation_Weak_Fit_Policy_2026-11-03.md) records unchanged 24-case metrics (53 picks, nDCG@returned 0.7413, precision@returned 0.7778, zero violations) with one changed AI/ML pick: reviewed strong `SC3021` replaces indirect `SC3020`. The 180-cell grid has zero diagnostic weak-fit picks, no open slots, and no violations; positioned checks remain 8 pass / 1 inconclusive.
- The separate no-strong-career pair now yields an explained open `SC3xxx` slot without interest, and a backend-labelled `SC3061` HCI interest alternative with explicit interest. Every newly open slot in these captures is this previously reviewed synthetic example.
- Counterfactual checks are 6 pass / 1 inconclusive / **1 fail**. Adding a database preference to the AI/ML case no longer changes the career-first selection, contrary to that existing check's expectation. Preserve the failed result for policy/evaluation review; do not manipulate the mapped-evidence constants or labels to turn it green.
- Frontend build, backend response-schema smoke checks and `git diff --check` passed. Actual transcript AU, offering, cohort and registration permission, and independent expert review remain outside these checks. Next: review this provisional boundary and the counterfactual expectation before starting the separate student-skills work unit.

## Weak-Fit Policy Handoff

Date: 2026-11-03

Status: The owner accepted the career-first behavior despite the one failed database-preference counterfactual and chose to review that check's expectation separately. This does not turn the failed check into a pass or validate the provisional strength threshold. The policy and its complete comparison were published in [PR #56](https://github.com/donkey-king-kong/fyp_course_recommendation/pull/56), assigned to the owner and merged into `main`. No frozen benchmark input, label, historical prediction or evaluator was changed to accommodate the failure.

## Pilot Student Skills Preview

Date: 2026-11-03

Status: First small evidence-backed slice on `student-skills-picture`; no recommendation ranking change.

- Added `data/student_skill_evidence.json`, a six-course/seven-link pilot ledger for four skill IDs (three applicable to DE) and the existing Software Engineer and Data Engineer role areas. Each link carries an exact excerpt from `data/course_catalog.json` and an introductory or advanced **course-content** depth. `SC4051` is introductory *for distributed-systems exposure* because its description says it introduces those concepts; course level alone does not establish advanced learning.
- Added request/response schemas, a pure service, and `POST /student-skills/preview`. It separates submitted completed-course evidence (likely prior learning) from submitted candidate-course evidence (possible next learning), reports unmapped codes rather than assigning zero skill, and rejects unsupported career goals. A completed course is not repeated as candidate learning. The result does not certify transcripts, student mastery, prerequisites, offering, eligibility or recommendation quality.
- Checked that all seven excerpts occur in the named catalog entries and all shared IDs point to real static pilot role areas. The catalog snapshot SHA-256 is `e94466a7834bd551bf86dfbca33c5c30c2ec6e4f9dbb59df3aa7389752a61d63`. HTTP smoke checks cover introductory, advanced, unknown, overlap and unsupported-goal behavior; the in-process test helper required optional `httpx`, so live HTTP was used without adding a dependency. A fresh 24-case recommendation capture matches the saved policy recommendations and open slots exactly: 53 picks, nDCG@returned 0.7413, precision@returned 0.7778 and zero supplementary contract violations. Frozen inputs and historical predictions retain their recorded hashes.
- The [seven-link content review](../evaluation/Student_Skills_Pilot_Review_2026-11-03.md) narrowed `SC1003` to programming foundations, separated `SC2006`/`SC3040` into SWE-only software-engineering practice, and distinguished `SC4023`'s advanced data-storage topic from its introductory distributed-systems slice. DE submissions of `SC2006`/`SC3040` are now explicitly unmapped for this role rather than silently credited as pipeline skill or zero skill. Rechecked all excerpts, role areas and both role responses; no ranking change. Next: independent review of contested depth/role relevance before using likely prior exposure for ranking. Keep the separate counterfactual expectation review visible.

## Pilot Skills Coverage Follow-Up

Date: 2026-11-03

Status: Read-only pilot-case audit and one source-backed cloud-platform evidence addition on `student-skills-picture`; no ranking, labels or evaluator changed. The earlier six-course/seven-link counts above describe the initial preview commit.

- Across 15 saved Software Engineer / Data Engineer cases, the initial ledger covered 14/35 selected-course occurrences. Nine unmapped selections were `SC4052`. Its catalog introduces cloud computing, service models and distributed services, and both pilot roles have an existing cloud-related infrastructure area; added an introductory `cloud-service-platforms` link without claiming backend implementation or AI/ML skills.
- The [coverage audit](../evaluation/Student_Skills_Coverage_2026-11-03.md) now counts 23/35 mapped occurrences and 12 unknown across the same saved policy responses. Three SWE cases have no mapped selection. These counts measure ledger coverage, not recommendation validity, skill mastery, or live eligibility; disputed security, neural-network and network-science paths remain unmapped.
- The ledger now holds seven courses, eight links and five IDs (four applicable to DE). All excerpts and role references were rechecked. Independent depth/role review and a separate evaluated design for likely-prior-learning ranking are still pending; the accepted failed preference counterfactual remains separate.
