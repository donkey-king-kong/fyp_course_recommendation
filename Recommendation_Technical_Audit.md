# Technical Audit: Course Recommendation System

Updated: 2026-11-03

## 1. Executive Summary

The current recommendation system is a deterministic, backend-owned ranking and exact-slot assignment pipeline.

It is implemented with:

- React and TypeScript for collecting browser-profile state and rendering results.
- FastAPI and Pydantic for the recommendation API.
- SQLAlchemy and PostgreSQL for module, availability, and prerequisite data.
- Curated module tags and static career-to-skill mappings for explainable relevance scoring.
- Rule-based filters, readiness checks, score components, and diversity-aware assignment.

It does not currently use:

- Neo4j or GraphRAG.
- ChromaDB, embeddings, or VectorRAG.
- LangGraph.
- OpenAI or another LLM.
- Machine-learned ranking.
- Live MyCareersFuture data.

The strongest current properties are explicit filters before ranking, inspectable score components, backend slot allocation, zero old-code exposure in the saved benchmark, and 100% validity under implemented benchmark checks. Those checks cover only a subset of academic and assignment constraints.

The main remaining concerns are owner-authored benchmark labels, weak-fit recommendations in some synthetic late-stage scenarios, permissive prerequisite planning, pass-2 prerequisite and allocation defects, saved predictions that disagree with current seed inputs, fixed calibration constants, and untrusted prototype browser state.

## 2. Scope And Sources Of Truth

Current source inspection was performed at commit `8c565e4bf1f9a8e5d9e7b2a9706def514291b65b` on `recommendation-technical-audit-update`. That commit only formats `data/ntu_mods.json`; application source remains the merged state after PR #51. The documentation correction is dated 2026-11-03.

The evidence has four distinct boundaries:

| Evidence | What it establishes | Limits |
| --- | --- | --- |
| Current source inspection and isolated helper probes | Code paths, formulas, and specific reproducible helper behavior at the reviewed commit | No live PostgreSQL query or browser verification |
| Historical saved benchmark predictions | Recomputed metrics for 24 cases and 53 saved recommendations against current draft labels | No new capture; runtime code, seed version, and database snapshot at capture are not recorded |
| Saved coverage output | Stored outcomes for the 180-cell synthetic CSC grid | Summary output, not a full response capture; narrower invariant checks and missing timing context |
| Previously recorded counterfactual results | Reported 7 PASS / 0 FAIL / 1 INCONCLUSIVE | Not independently rerun during this documentation correction |

The GPT 6.1 Sol Max review reported current seed-derived relevance-component differences for 15 of the 53 saved recommendations. That aggregate count is attributed to the review and was not independently recomputed here. One discrepancy was independently checked: saved Software Engineer `SC3050` evidence credits `networks` and `careerSkillScore = 5`, while current `data/modules.json` has only `computer-architecture` and `embedded-systems`, which produce a mapped Software Engineer skill score of `0`. This establishes disagreement with current seed inputs; it does not establish that the live database is wrong.

The primary source files are:

| Area | Source |
| --- | --- |
| Frontend request construction | `frontend/src/App.tsx` |
| Frontend API client | `frontend/src/api/recommendationsApi.ts` |
| API route | `backend/routers/recommendations.py` |
| Request and response schemas | `backend/schemas/recommendation.py` |
| Ranking and assignment logic | `backend/services/recommendation_service.py` |
| Career mappings | `backend/services/career_skill_mappings.py` |
| Module database seed | `backend/database/seed.py` |
| Benchmark cases | `data/recommendation_benchmark_cases.json` |
| Saved benchmark predictions | `data/recommendation_benchmark_predictions.json` |
| Offline evaluator | `scripts/evaluate_recommendation_benchmark.py` |
| Counterfactual checks | `scripts/run_counterfactual_sensitivity.py` |
| Coverage audit | `scripts/run_coverage_audit.py` and `data/coverage_audit_results.json` |
| Evaluation interpretation | `Evaluation.md` |

This document intentionally avoids copied implementation blocks and fixed source line numbers. Function names and constants are referenced instead so that future audits can be checked against the code without maintaining duplicate source listings.

## 3. Runtime Request Flow

The recommendation flow is:

```text
Profile + curriculum guide + transcript-applied completions
  -> frontend builds open choice slots and exclusions
  -> POST /recommendations
  -> FastAPI router validates the Pydantic request
  -> recommendation service queries PostgreSQL candidates
  -> hard filters and readiness checks
  -> deterministic scoring per candidate and slot
  -> exact slot assignment with uniqueness and diversity rules
  -> optional pass-2 interest fill for remaining slots
  -> planned prerequisite nodes and edges
  -> frontend renders each result in matchedChoiceSlotId
```

### 3.1 Frontend trigger

`handleLoadRoadmapRecommendations()` in `frontend/src/App.tsx` runs only when:

- A curriculum guide exists.
- The guide has been converted into a roadmap.
- A supported career goal is selected.
- At least one uncompleted choice slot is present.

The frontend sends:

- `careerGoal`.
- `preferredRecommendationTags`.
- `studentFaculty` from the profile major.
- Completed module codes from the currently applied transcript and manually completed roadmap courses.
- Open choice-slot codes and exact slot objects.
- Curriculum courses with roadmap positions.
- Fixed curriculum codes and titles as exclusions.
- A bounded result limit based on the number of open slots.

The frontend does not rank or assign returned modules. It renders the backend assignment using `matchedChoiceSlotId`.

### 3.2 API boundary

`POST /recommendations` is defined in `backend/routers/recommendations.py`.

The router:

- Receives a `RecommendationRequest`.
- Opens a database session.
- Passes request fields to `recommend_courses()`.
- Returns a `RecommendationResponse`.
- Logs SQLAlchemy failures on the backend.
- Returns a safe `503` message when PostgreSQL is unavailable.

The route is intentionally thin. Recommendation policy belongs to the service layer.

### 3.3 Prototype trust boundary

Profile, curriculum, transcript, completion, and recommendation state currently originate from browser `localStorage`. The backend therefore receives user-controlled state.

The submitted fields are useful prototype inputs, but they must not be treated as authoritative production records. In particular:

- A student can edit completed modules or faculty context in browser storage.
- Uploaded curriculum and transcript results are not tied to a verified server-side identity.
- The self-declared Student ID is not a stable authentication key.

NTU SSO and server-side persistence keyed by Azure `oid` remain separate future work. No SSO implementation is active on merged `main`.

## 4. Supported Career Goals

The active static mapping supports six normalized career goals:

- `software-engineer`
- `ai-ml-engineer`
- `data-engineer`
- `data-scientist`
- `cloud-platform-engineer`
- `cybersecurity-engineer`

Each career contains weighted skill areas. Each skill area contains relationships to curated module recommendation tags, with relationship weights, tag confidence, and a rationale.

Conceptually:

```text
career goal
  -> weighted skill area
  -> weighted recommendation-tag relationship
  -> relationship-level tag confidence
  -> career-skill contribution
```

Unsupported career goals return an empty recommendation list. The service does not silently substitute a generic career.

## 5. Candidate Retrieval And Hard Filters

The service begins with a bounded SQL candidate query rather than loading the entire catalog.

The SQL prefilter uses:

- Active faculties.
- Slot-compatible module levels or BDE eligibility.
- Career-specific title/description keywords.
- Career-skill mapping tags.
- Relevant MPE specialisations.
- Software Engineer tag weights only for the Software Engineer career.

The previous audit incorrectly described the SQL relevance prefilter as applying Software Engineer signals to every career. `build_relevance_filters(career_goal)` is now career-aware.

This section describes pass-1 retrieval and filters. Pass 2 retrieves additional preference candidates; its data-loading and allocation limitations are described in section 9.

Candidates then pass through explicit service-level exclusions.

### 5.1 Completed, fixed, and duplicate learning

A module is excluded when:

- Its code is already completed.
- Its code is already a fixed curriculum course.
- Its normalized title duplicates an excluded curriculum title.
- Its title signature represents near-duplicate prior learning.

The allocator also guards against reusing codes and title equivalents across slots. This does not guarantee unique slot assignment for every API request: missing slot IDs can cause an already-filled slot to be considered unfilled before pass 2.

### 5.2 Deprecated codes

Codes beginning with the following prefixes are hard-filtered:

```text
CE, CPE, CSC, CZ
```

Current curricula use `SC` codes. This is not a scoring penalty. `legacyCodePenalty` remains in the response schema for compatibility and is always `0`.

### 5.3 Non-elective and restricted modules

The service excludes:

- Core project modules `SC2079` and `SC3099`.
- A curated set of Turing AI Scholar or TAISP-only modules for general profiles.
- Modules unavailable to the student's programme.
- BDE/UE modules whose programme restrictions block the student's programme.

These rules prevent ranking modules that should never be offered as ordinary choices.

### 5.4 Slot fit

Slot compatibility is a hard requirement.

- `SC3xxx` accepts current `SC` level-3 modules.
- `SC4xxx` accepts current `SC` level-4 modules.
- BDE slots can use broader active-faculty candidates, subject to availability and programme restrictions.
- A BDE slot with a year requires the module level to match that year, clamped to levels 1–4. An omitted year bypasses this level check.
- MPE-listed modules are reserved from BDE assignment while unfilled MPE slots remain, where possible.

### 5.5 Career eligibility

Pass-1 candidates must have at least one career signal:

- A direct or fallback career-tag score.
- A mapped career-skill score.
- An MPE specialisation boost for the selected career.

The service also applies focused AI/ML and Cloud/Platform guards for known low-value or off-track candidates. Cloud/Platform currently includes a curated course-code blocklist for known false positives.

## 6. Prerequisite Readiness And Planning

Pass 1 evaluates prerequisites for each candidate-slot pair. Pass 2 calls the same readiness helper, but can supply an empty prerequisite list because additional candidates lack retrieved data (section 9).

The service considers:

- Completed module codes.
- Fixed curriculum modules scheduled before the target slot.
- Other open choice slots and roadmap timing.
- Whether a missing prerequisite exists in the catalog and can be planned.
- Some slot and programme checks when searching for plannable prerequisite modules; these checks are not applied consistently by the permissive catalog fallback.
- Later curriculum modules that the candidate can unlock.

`evaluate_recommendation_readiness()` implements the following simplified policy:

- No listed prerequisites produces `ready`.
- Any one completed prerequisite produces `ready`, even if other listed prerequisites remain incomplete.
- Any matching earlier fixed curriculum prerequisite, including a title equivalent, produces `needs-prerequisite-planning` with no extra planning penalty and no new prerequisite codes.
- Otherwise, the helper searches for known prerequisites that fit earlier open slots.
- If that search fails, catalog-known prerequisites can still produce `needs-prerequisite-planning`, even when no earlier slot exists or fits. This fallback checks catalog presence, but does not reapply every programme restriction or prove a feasible placement.
- With neither a completed/earlier path nor a catalog-known missing prerequisite, the helper returns no candidate for that slot.

Extra prerequisite planning receives `EXTRA_PREREQUISITE_PLANNING_PENALTY = -10` in pass 1. The status represents permissive planning assistance, not proof of full prerequisite satisfaction. The flat prerequisite list cannot distinguish true AND requirements from OR alternatives, and does not fully model exemptions or special approvals.

### 6.1 Planned node and edge integrity

`build_planned_roadmap_nodes()` requires an earlier semester among the remaining open slots and usable prerequisite detail data. `build_planned_roadmap_edges()` can emit an edge for a planned prerequisite code without checking that its source node was generated. Acceptance by readiness therefore does not guarantee a complete, feasible roadmap artifact.

The saved benchmark contains five `SC4052` recommendations with a planned `MH2802` prerequisite edge and no generated source node. This count was independently verified in cases `software-engineer-csc-001`, `software-engineer-csc-005`, `software-engineer-csc-007`, `software-engineer-csc-009`, and `software-engineer-csc-013`. Each has zero planned nodes and one edge from `recommended-prerequisite-y4-s1-mpe1-mh2802`. These dangling edges are outside the implemented benchmark validity checks.

## 7. Deterministic Scoring

For a pass-1 career recommendation, the final score is:

```text
max(1,
  careerTagScore
  + careerSkillScore
  + currentSemesterBonus
  + unlockContribution
  + scaledPreferenceBoost
  + sameFacultyBoost
  + mpeSpecialisationBoost
  + defaultProfileAdjustment
  + prerequisitePlanningPenalty
)
```

### 7.1 Career skill score

`careerSkillScore` is the primary career relevance signal.

For each skill area, `get_career_skill_contributions()` takes the maximum matching contribution:

```text
skill-area weight × relationship weight × relationship tag confidence
```

The service sums those per-area maxima and rounds the nonnegative total half up using `round_positive_score()` (`int(total + 0.5)`). Several tags in one skill area do not stack, but different skill areas can each contribute.

`tagConfidence` is configured on the tag-to-skill relationship in `career_skill_mappings.py`. It is a shared manually chosen mapping value, not a separately inferred probability for each module.

The response includes one selected evidence path through:

- Career goal.
- Skill area.
- Skill-area weight.
- Matched tag.
- Relationship weight.
- Tag confidence.
- Contribution score.
- Mapping rationale.

Normally, the displayed path is the strongest matching contribution. For Cybersecurity, `get_top_evidence_skill_contribution()` intentionally prefers the strongest available specific tag if the overall strongest tag is generic `cybersecurity`. For example, saved `SC4010` evidence displays `cryptography = 6` rather than `cybersecurity = 10`. The total ranking score still uses the per-skill-area maxima; this specificity policy changes the explanation evidence only. See the `Benchmark Label Review Follow-Up` entry in `Progress2.md` for the rationale.

### 7.2 Career tag score

`careerTagScore` is a fallback top-up from direct keyword or curated tag matching. It protects modules whose relevance is not fully represented by the mapping, without always double-counting the same mapped evidence.

### 7.3 Preference boost and career-first policy

Preference matches use diminishing returns:

```text
first matching preference dimension: 21
additional dimensions:             12, 8, 6, 4
maximum base preference boost:     45
```

Alias dimensions prevent equivalent choices such as `computer-security` and `cybersecurity` from being counted as separate interests.

The `8`-point privacy adjacency adjustment for a specific security/cryptography combination is included inside `get_preference_boost()`, before the base cap. The `9`-point current-semester `networks` adjustment is added afterward:

```text
basePreferenceBoost = min(diminishingReturns + privacyAdjacency, 45)
rawPreferenceBoost = basePreferenceBoost + currentNetworkAdjustment
maximum rawPreferenceBoost = 45 + 9 = 54
```

The total of `54` was reproduced with an isolated helper probe. Pass 2 uses the capped base preference boost only and omits this separate current-network adjustment.

The resulting raw preference boost is scaled by career fit:

```text
if careerSkillScore >= 15:
    applied preference boost = raw preference boost
else:
    applied preference boost = round(raw boost * careerSkillScore / 15)
```

This career-first policy proportionally attenuates preferences for weak mapped career fit; it does not guarantee ordering by career score. With all other components equal, career score `10` plus scaled raw preference `45` gives `10 + round(45 × 10 / 15) = 40`, which beats career score `25` without preferences. The example was independently reproduced. Preference scaling uses Python's `round()`, unlike the half-up helper used for career-skill totals.

The API exposes both `rawPreferenceBoost` and the applied `preferenceBoost` for diagnosis.

### 7.4 Other score components

| Component | Current behavior |
| --- | --- |
| Current semester | `+3` when the module is currently offered |
| Same faculty | `+8` when module faculty matches `studentFaculty` |
| MPE specialisation | Up to `+12` for a career-aligned official MPE path |
| Broad default profile | `+14` in the relevant default-profile context |
| Specialist profile | `-16` when a specialist module lacks supporting preferences |
| Prerequisite planning | `-10` when extra prerequisite planning is needed |
| Unlock contribution | Stepped `4, 3, 2, 1` contribution based on later modules unlocked |

### 7.5 Assignment thresholds and confidence

- Ordinary and MPE recommendations require a score of at least `10`.
- BDE recommendations can use a fallback threshold of `5`.
- A BDE result scoring from `5` through `9` is marked `recommendationConfidence = "low"`.
- The broader general BDE fallback that could fill slots with unrelated modules remains reverted.

## 8. Exact-Slot Assignment And Diversity

Candidates are scored per eligible slot and sorted by raw score, then course code for deterministic ties.

Assignment order is:

1. MPE slots.
2. BDE slots.
3. Other slot types.

Within the same category, earlier roadmap semesters are assigned first.

The allocator prevents reuse of:

- Course codes.
- Normalized titles.
- Near-duplicate title signatures.

Diversity is subordinate to relevance:

- Only candidates within `10` raw score points of the best eligible candidate participate in the diversity comparison.
- Repeated non-preferred tags incur an `8`-point diversity adjustment per prior use.
- Repeated preferred tags incur only a `2`-point adjustment.

This makes diversity a local tiebreaker among similarly relevant modules. It cannot replace a clearly stronger candidate merely to produce different tags.

## 9. Two-Pass Recommendation Policy

### 9.1 Pass 1: career recommendations

Pass 1 applies career relevance filters and the full scoring formula. Results use:

```text
recommendationSource = "career"
```

### 9.2 Pass 2: interest-only fill

The intended pass-2 trigger is:

- Pass 1 leaves at least one exact slot empty.
- The student selected topic preferences.

Actual empty-slot detection compares returned `matchedChoiceSlotId` values against `get_choice_slot_identity(slot)`. These agree for the normal frontend payload, but can disagree when an API caller omits a slot ID.

It searches slot-compatible modules matching those preferences without requiring a career signal. Results explicitly use:

```text
recommendationSource = "interest"
```

Their reason states that they match the student's interests but are not directly tied to the career goal.

Both the saved 24-case benchmark and the corrected 180-cell coverage output contain zero interest picks. Neither saved evaluation establishes correctness of this fallback.

### 9.3 Confirmed implementation defects and API edge cases

Source inspection confirms four issues:

1. **Missing prerequisite and unlock retrieval.** `recommend_courses()` loads prerequisite, prerequisite-detail, and unlock maps for the first-pass candidate set. `fill_interest_slots()` retrieves additional candidates but reuses those maps. For a new candidate, `.get(module.code, [])` can turn unknown prerequisite data into an empty list and therefore `ready`; unlock value can also be understated. Actual prerequisites must be retrieved for the second-pass candidate set before readiness is dependable.
2. **Score-breakdown mismatch.** Interest score is `max(1, basePreferenceBoost + unlockContribution)`. A prerequisite penalty can appear in `scoreBreakdown` without being subtracted from `score` or `finalScore`.
3. **Result-budget overflow.** Pass 1 respects `limit`, but pass 2 receives no remaining budget. Its results are appended without a final limit cut. The Sol Max review reproduced two recommendations for two slots with `limit = 1` in an isolated in-memory probe.
4. **Refilling an ID-less slot.** `slotId` is optional. A returned `None` ID does not match the synthesized slot identity, so an already-assigned slot can enter pass 2 again. The Sol Max review reproduced both a career pick and an interest pick for one ID-less slot.

The allocation probes are attributed to the Sol Max review and were not rerun during this correction; the enabling source paths were checked. Live incidence of all four issues remains unverified. The current frontend supplies roadmap node IDs and uses `max(1, openChoiceSlots.length)` as its limit, so the API edge-case probes do not establish a current normal-UI failure. These defects are outstanding; this documentation change implements no fixes.

## 10. Response And Explanation Contract

Each recommendation includes:

- Module identity, AU, faculty, and level.
- Matched slot code and optional slot ID (provided by the frontend).
- Optional roadmap year and semester.
- MPE specialisations.
- Matched signals.
- Prerequisites and missing prerequisites.
- Existing and planned prerequisite codes.
- Planned prerequisite modules, nodes, and edges.
- Readiness status and unlock value.
- Final score and confidence.
- Deterministic score breakdown, subject to the pass-2 penalty discrepancy in section 9.
- A template-based explanation reason.
- `recommendationSource`, either `career` or `interest`.

The explanations are deterministic templates built from scoring signals and the evidence-selection policy. They are not LLM-generated prose. Prerequisite fields and artifacts inherit the readiness and data-loading limitations above.

The roadmap UI intentionally does not display the full score breakdown. The breakdown remains available through the API and saved evaluation artifacts for debugging and evaluation.

## 11. Data Sources

The active recommendation path uses PostgreSQL tables populated by `backend/database/seed.py`.

Important seed inputs include:

- `data/modules.json` for curated module metadata, recommendation tags, profiles, and specialisations.
- `data/course_catalog.json` for normalized catalog details and programme restrictions.
- Enriched prerequisite data used to populate prerequisite relationships.

`data/ntu_mods.json` is a tracked historical/raw data artifact and is not read by the current runtime recommendation path.

## 12. Offline Benchmark Snapshot

The saved benchmark contains 24 project-owner-reviewed draft cases:

| Career | Cases |
| --- | ---: |
| Software Engineer | 13 |
| AI / ML Engineer | 2 |
| Data Engineer | 2 |
| Data Scientist | 2 |
| Cloud / Platform Engineer | 3 |
| Cybersecurity Engineer | 2 |

The historical saved prediction file records `generatedAt = 2026-11-02T17:30:47.260945+00:00` and `apiUrl = http://127.0.0.1:8001/recommendations`. It does not record the serving source commit, seed-input hashes, or database snapshot. Its `source = "live-backend"` means it was captured from an endpoint at that time, not that this audit queried the live backend.

Running:

```bash
.venv/bin/python scripts/evaluate_recommendation_benchmark.py \
  --predictions data/recommendation_benchmark_predictions.json \
  --k 5
```

reproduces the following saved-snapshot metrics, without recapturing recommendations or writing output files:

| Metric | Saved-snapshot value |
| --- | ---: |
| Case count | 24 |
| Case coverage | 1.0 |
| Predictions evaluated | 53 |
| Average precision@5 | 0.2750 |
| Average nDCG@5 | 0.4558 |
| Average precision@returned | 0.6389 |
| Average nDCG@returned | 0.6313 |
| Average slot-fill rate | 1.0 |
| Explanation coverage | 1.0 |
| Explanation fidelity | 0.6667 |
| Skill-area diversity@5 | 1.4167 |
| Old-code exposure | 0 |
| Constraint validity under implemented checks | 1.0 |

Rank-sensitive metrics sort predictions by backend score rather than roadmap display order. The API response is an exact slot-assignment list, so response order is not itself a global ranking.

`precision@5` is structurally harsh because most cases return only one to three modules. `precision@returned` and `nDCG@returned` are more representative of the current exact-slot design, but neither should be treated as expert-ground-truth performance yet.

### 12.1 Interpretation

The saved prediction snapshot supports these conclusions:

- Every evaluated recommendation passes the implemented code-exclusion and limited slot-fit checks.
- Deprecated code exposure is zero.
- Every expected slot ID is represented in the saved benchmark; this does not prove unique assignments or feasible prerequisite plans.
- Every recommendation has career-skill evidence in the current saved predictions.
- Ranking relevance and explanation-path agreement remain mixed.
- The saved career-first snapshot has lower aggregate draft-label alignment than the earlier recorded 24-case baseline. Missing code/data/database provenance and current seed disagreements prevent attributing that difference solely to the policy.

The labels are still project-owner-reviewed drafts. Calibration against those labels measures consistency with the project owner's current judgement, not independent academic or industry correctness.

### 12.2 What constraint validity checks

`prediction_is_constraint_valid()` checks nonempty module code, old-code exclusion, completed-code exclusion, fixed curriculum code exclusion, and limited slot fit. Slot fit requires a known slot ID; SC slots check the code-level digit, while every BDE assignment is accepted without checking its year-level rule. At `k = 5`, all 53 saved recommendations fall within the evaluated per-case cutoff.

Thus `1.0` means **100% validity under implemented benchmark checks**. It does not validate complete prerequisite feasibility, programme restrictions, BDE year-level compatibility, duplicate assignments or slot identity uniqueness, title equivalence, result limits, or planning node/edge integrity. The five dangling `SC4052` prerequisite edges are examples of defects that this metric cannot detect.

### 12.3 Synthetic requests and current seed inputs

Read-only inspection verified that all 567 curriculum entries across the 24 saved requests have neither year/semester positions nor titles, and every request has empty `excludedCourseTitles`. Benchmark choice slots do carry positions, but these curriculum inputs cannot exercise earlier-curriculum readiness, later-curriculum unlock value, or title-based exclusion/equivalence as the frontend does.

The 15-of-53 seed disagreement count remains attributed to the Sol Max review (section 2). Re-evaluating saved predictions checks metrics against labels; it does not rerun current scoring against the live catalog. A future capture should record the serving commit, mapping and seed hashes, active faculties, and a reproducible database version/snapshot alongside requests and responses.

## 13. Counterfactual Sensitivity

The previously recorded counterfactual run contains eight checks. These were not independently rerun during this documentation correction:

- Two career swaps: pass.
- One observable preference swap: pass.
- One AI/ML career-conflict check: pass.
- Three completion changes: pass.
- One preference swap: inconclusive.

Overall:

```text
7 PASS
0 FAIL
1 INCONCLUSIVE
```

The inconclusive `ai-ml-engineer-csc-001 + database` check did not introduce a new observable signal because `database` was already represented in the baseline recommendation evidence. It is not evidence of a ranking failure.

The script now guards against adding a preference already present in the base case and compares swapped output with baseline evidence. This corrects the earlier invalid Cloud/Platform check where `computer-network` had already been selected.

The recorded checks indicate that career, preference, and completion inputs can affect results in those scenarios; they do not independently establish current-runtime behavior or complete sensitivity.

## 14. Corrected Coverage Audit

The saved coverage audit reports outcomes for:

```text
6 careers
× 5 slot configurations
× 2 progress stages
× 3 preference modes
= 180 cells
```

It covers CSC synthetic profiles only.

Verified directly from `data/coverage_audit_results.json`:

| Finding | Result |
| --- | ---: |
| Cells | 180 |
| Recorded invariant violations | 0 |
| Empty slots | 0 |
| Cells with empty slots | 0 |
| Pass-2 interest picks | 0 |
| Low-confidence picks | 0 |
| Cells with weak-fit picks | 26 |
| Total weak-fit picks | 26 |

The three weak-fit module codes are:

- `SC3020`
- `SC3040`
- `SC3050`

These slots are filled, but the picks have `careerSkillScore < 5` and `careerTagScore == 0`. They rely more heavily on faculty, systems, data, or structural fit than direct career evidence.

The first audit incorrectly reported six empty Cybersecurity SC3xxx cells. Its request builder omitted `studentFaculty` and sent fields the API ignored. Without `studentFaculty: "CSC"`, the `+8` faculty boost disappeared and `SC3040` fell below the MPE score threshold. The corrected script delegates to the benchmark request builder and reports no empty slots.

The request-shape correction restored faculty context and recognized API fields. It did not make these synthetic requests equivalent to production roadmap requests.

### 14.1 Timing and validation boundaries

`build_slots()` supplies slot IDs and codes without year or semester. Coverage curriculum entries contain codes only. Omitting slot year bypasses the BDE year-level restriction; omitting curriculum timing prevents assessment of earlier-curriculum prerequisite readiness and later-curriculum unlock value. Semester placement and prerequisite artifact integrity cannot be meaningfully assessed from this grid. The frontend supplies slot positions, curriculum positions and titles, and title exclusions.

Coverage uses `check_invariants()` from the counterfactual script. It checks old-code exclusion, completed-code exclusion, and limited slot compatibility only when the returned slot ID resolves to a known slot. Unknown slot IDs are not themselves rejected. It does not check fixed-code exclusion, nonempty codes, or the broader omitted validations listed in section 12.2. Empty-slot reporting is separate and also does not prove assignment uniqueness.

The file contains per-cell summaries rather than complete recommendation responses and no capture timestamp, code commit, or database snapshot. The 100% fill result applies to this synthetic grid and its stored output, not every degree/cohort, positioned roadmap, or current database state.

## 15. Strengths

### 15.1 Clear separation of responsibilities

The active flow follows the intended layered architecture:

```text
Frontend -> Router -> Service -> Database/tools -> Service -> Router -> Frontend
```

### 15.2 Hard filters precede ranking

Pass 1 checks completed modules, fixed curriculum content, old code families, restricted projects, programme availability, slot fit, and its simplified readiness policy before scoring. That explicit structure is useful, while permissive planning and pass-2 missing data limit the academic guarantees.

### 15.3 Backend owns ranking and allocation

The frontend renders backend assignments by roadmap node ID instead of re-ranking a global candidate list. Exact assignment works with normal frontend IDs, but optional IDs and pass-2 budget handling leave API edge cases documented in section 9.

### 15.4 Deterministic and inspectable output

The same inputs and database state produce the same output. Score components, evidence paths, readiness, confidence, and source are available for diagnosis.

### 15.5 Evaluation goes beyond one aggregate metric

The project now combines:

- Offline relevance metrics.
- Constraint validity.
- Old-code exposure.
- Explanation coverage and fidelity.
- Counterfactual sensitivity checks.
- A systematic coverage audit.

## 16. Limitations And Risks

### 16.1 Benchmark labels are not independent ground truth

The same project owner who calibrates the recommender also reviews the labels. This can create confirmation bias. Expert review is the highest-priority evaluation improvement.

### 16.2 Slot fill does not guarantee recommendation quality

The saved synthetic coverage grid fills every slot, but 26 cells contain weak-fit picks. A future product decision is needed between:

- Showing a weak recommendation with a clear low-confidence label.
- Leaving the slot unfilled and stating that no strong match exists.
- Asking the student to broaden goals or preferences.

### 16.3 Curated data and constants require maintenance

Career mappings, module tags, profile labels, blocklists, and scoring constants are manually maintained. They are explainable, but can become stale when the catalog changes.

### 16.4 Prerequisite semantics are simplified

The flat representation does not fully model complex alternatives, co-requisites, exemptions, transfer credit, or special approvals. Any-one-prerequisite readiness and catalog-only fallback can overstate academic feasibility; generated prerequisite edges can lack source nodes.

### 16.5 Current-semester availability is a soft signal

A relevant module can be recommended even if it is not currently offered. This is useful for multi-year planning but requires clear UI communication.

### 16.6 Pass 2 lacks saved evaluation coverage and has confirmed defects

Interest-only recommendations did not appear in the saved benchmark or any of the 180 coverage cells. Missing prerequisite/unlock retrieval, penalty mismatch, result-budget overflow, and inconsistent handling of absent slot IDs need implementation work and targeted validation before relying on this fallback.

### 16.7 Prototype identity and persistence are untrusted

Until SSO and server-side storage are implemented, browser state is inspectable and editable. It cannot support production authorization or cross-device persistence.

### 16.8 Saved metrics have incomplete provenance and input coverage

Saved predictions disagree with some current seed-derived signals, and the artifacts lack serving-code/database versions. Code-only curriculum inputs, missing coverage timing, and narrow validators leave important behaviors unmeasured. Reproduced metrics establish saved-snapshot label agreement and limited validity only.

## 17. Deferred Integrations

The following remain intentionally deferred:

- Neo4j, unless prerequisite and skill queries outgrow the relational model.
- ChromaDB or embeddings, unless messy free-text semantic matching becomes necessary.
- LangGraph, until there is a clear multi-step chat workflow.
- OpenAI, primarily for explanation generation rather than core ranking.
- RAGAS, until natural-language explanations become a major output.
- A/B or interleaving tests, until authenticated real-student usage exists.

The deterministic recommender should remain the core decision engine even if an LLM later improves explanation phrasing.

## 18. Recommended Next Steps

### Immediate evaluation step

Run an expert review or think-aloud session with a supervisor or knowledgeable senior student.

The reviewer should examine a manageable subset covering:

- At least one case from each career.
- A mixture of MPE and BDE slots.
- Strong, weak-fit, and prerequisite-planning recommendations.
- Cases where draft labels and current ranking disagree.

Record agreement, disagreement, suggested relevance labels, and reasoning. Do not tune scoring during the session.

### After expert review

1. Update benchmark labels only where reviewer evidence supports a change.
2. Separate label corrections from scoring changes in Git history.
3. Decide the product policy for weak-fit recommendations.
4. Add targeted pass-2 interest cases if that fallback remains part of the design.
5. Resume NTU SSO only when Azure app-registration access is available and implement the approved Microsoft MSAL authorization-code design.

### Outstanding implementation and verification follow-ups

These findings are documented, not fixed. Keep each implementation change scoped and reviewable:

1. Retrieve prerequisite, prerequisite-detail, and unlock data for all pass-2 candidates; distinguish unknown data from confirmed absence.
2. Enforce the remaining result budget across both passes and use consistent slot identities, including a deliberate policy for omitted IDs.
3. Align pass-2 `score`, `finalScore`, and penalty components in the breakdown.
4. Review prerequisite satisfaction semantics, programme checks in the catalog fallback, feasible placement, and node/edge integrity.
5. Expand evaluation checks to cover the omitted constraints and targeted pass-2/positioned-roadmap cases. No new automated recommender tests are added in this documentation work.
6. Recapture predictions after the relevant fixes with serving code, seed/mapping, and database provenance. Preserve snapshot results so comparisons remain interpretable.

## 19. Overall Assessment

The system is currently a credible deterministic recommendation prototype, not an AI recommender.

Its engineering foundation provides explicit filters, backend allocation, and inspectable scoring. Saved evidence supports old-code and completed-code exclusion under the implemented checks. Academic readiness, artifact integrity, and pass-2 allocation have concrete gaps alongside the subjective ranking questions created by curated mappings, manual labels, and product policy.

The latest reflection is therefore:

- Do not add graph, vector, workflow, or LLM infrastructure merely to make the architecture appear more advanced.
- Do not interpret 100% slot fill as 100% recommendation quality.
- Keep source behavior, historical snapshot metrics, synthetic coverage, and recorded counterfactual outcomes distinct.
- Resolve the documented prerequisite and pass-2 defects before treating limited validity metrics as comprehensive correctness evidence.
- Do not tune constants solely to improve owner-authored nDCG.
- Use expert review to improve the credibility of labels and identify whether weak-fit recommendations are acceptable.
- Keep core ranking deterministic and backend-owned while authentication and persistence mature separately.
