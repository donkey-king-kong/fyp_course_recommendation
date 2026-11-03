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

The prerequisite and pass-2 defects from the earlier audit have now been addressed on `recommendation-planning-integrity`. Integrated captures have zero supplementary request/response contract violations. Remaining concerns are owner-authored labels, weak-fit recommendations, incomplete cohort/co-requisite/standing coverage, manually maintained rules, and untrusted browser state. Correctness improvements lowered draft-label alignment in the fresh same-database comparison; they did not improve every metric.

## 2. Scope And Sources Of Truth

Current source inspection covers `cdd488b` plus the uncommitted backend fixes on `recommendation-planning-integrity`. The parent agent launched an owned backend on port `8002` before the backend edits for the baseline, stopped that process, then launched the completed implementation against the same PostgreSQL state. This operational confirmation is separate from local Git metadata. Backend/rule hashes, raw capture hashes, metrics and per-case changes are preserved in `data/review/recommendation_planning_integrity_results.json`.

The evidence has distinct boundaries:

| Evidence | What it establishes | Limits |
| --- | --- | --- |
| Current source inspection and isolated helper probes | Reviewed AND/OR branches, allocation, scoring and shared artifacts | No browser verification or full registration eligibility proof |
| Fresh owned-server baseline and after captures | Same 24 cases, 53 recommendations, unchanged database, before/after backend behavior | Draft labels; serving revision is operator-declared, not inferred from local Git |
| Current positioned scenarios and counterfactual rerun | Nine positioned scenarios and eight live sensitivity checks | Bounded synthetic inputs; standing, offering and cohort eligibility remain unverified |
| Historical saved benchmark predictions | Recomputed metrics for 24 cases and 53 saved recommendations against current draft labels | No new capture; runtime code, seed version, and database snapshot at capture are not recorded |
| Saved coverage output | Stored outcomes for the 180-cell synthetic CSC grid | Summary output, not a full response capture; narrower invariant checks and missing timing context |
| Previously recorded counterfactual results | Historical 7 PASS / 0 FAIL / 1 INCONCLUSIVE | Distinct from the new 6 PASS / 0 FAIL / 2 INCONCLUSIVE rerun |

The earlier Sol Max review reported seed-derived relevance-component differences for 15 of the 53 historical saved recommendations. That aggregate remains attributed to the review; the `SC3050` example was independently confirmed. This old file is neither the fresh baseline nor the updated capture. Its nDCG `0.6313` must not be used as the baseline for the current implementation comparison.

The parent compared read-only fingerprints before and after using the same database configuration as the owned server: 4,318 modules, 4,178 prerequisite rows and 34 faculties were unchanged; no reseed occurred. The operator-declared combined fingerprint is `d77d095a173a8e5d83c55c203c68c2ba0a97eeaccd7a76b83e1471e66e544146`. Table hashes are in the evidence summary. Capture runners explicitly distinguish local revision/file hashes from declared serving revision and database evidence; local seed hashes alone do not prove database contents.

Full raw requests/responses remain in `/private/tmp/recommendation-planning-T66qUE/` and are ephemeral. The compact summary is the persistent repository evidence; raw captures are not committed. Historical prediction, coverage and label files remain unchanged.

The primary source files are:

| Area | Source |
| --- | --- |
| Frontend request construction | `frontend/src/App.tsx` |
| Frontend API client | `frontend/src/api/recommendationsApi.ts` |
| API route | `backend/routers/recommendations.py` |
| Request and response schemas | `backend/schemas/recommendation.py` |
| Ranking and assignment logic | `backend/services/recommendation_service.py` |
| Reviewed prerequisite groups | `backend/services/prerequisite_rules.py` |
| Career mappings | `backend/services/career_skill_mappings.py` |
| Module database seed | `backend/database/seed.py` |
| Benchmark cases | `data/recommendation_benchmark_cases.json` |
| Saved benchmark predictions | `data/recommendation_benchmark_predictions.json` |
| Offline evaluator | `scripts/evaluate_recommendation_benchmark.py` |
| Counterfactual checks | `scripts/run_counterfactual_sensitivity.py` |
| Coverage audit | `scripts/run_coverage_audit.py` and `data/coverage_audit_results.json` |
| Evaluation interpretation | `Evaluation.md` |
| Integrated evidence summary | `data/review/recommendation_planning_integrity_results.json` |

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
- Returns `422` for invalid positions or repeated explicit choice-slot IDs.

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

This section describes pass-1 retrieval and filters. Pass 2 retrieves additional preference candidates and loads their own prerequisite and unlock data before applying readiness (section 9).

Candidates then pass through explicit service-level exclusions.

### 5.1 Completed, fixed, and duplicate learning

A module is excluded when:

- Its code is already completed.
- Its code is already a fixed curriculum course.
- Its normalized title duplicates an excluded curriculum title.
- Its title signature represents near-duplicate prior learning.

The allocator also guards against reusing codes and title equivalents across slots. Omitted slot IDs are normalized to deterministic, collision-safe IDs before both passes; explicit duplicate IDs are rejected. Pass 2 receives the remaining result budget and the same slot identities.

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

Both passes call the same readiness helper with candidate-specific prerequisite data. `prerequisite_rules.py` stores reviewed alternatives as outer OR groups, whose inner members are all required (AND). The source is the local MPE 2025 listing dated 14/7/2026 for AY2025-and-later cohorts, plus shared core rules from the 2023/24 and 2026/27 guides. The older `SC2002` OR rule is kept distinct from `SC2003`; titles do not make those courses equivalent.

Examples: `SC4052` requires `SC1004 OR MH2802`; `SC4012` requires `SC2002 AND SC2005`; `SC4051` requires `SC2005 AND SC2008`. The graph omitted Cloud Computing's `SC1004` alternative, so the reviewed source corrects a data omission rather than treating `SC1004` and `MH2802` as equivalent modules.

For unreviewed courses, missing maps and ambiguous multi-code graph lists are rejected. An explicitly loaded empty/singleton graph is a bounded compatibility fallback for stored direct course requirements, not proof that raw standing or co-requisite requirements are absent. `SC3103` is explicitly unresolved because the MPE source says “TBC (Pending Approval)”; its graph singleton cannot override that pending requirement.

Every member of a selected branch must be supported by:

- A completed catalog-known course or one of the two reviewed legacy pairs (`CZ2007`/`SC2207`, `CZ2101`/`SC2001`).
- A catalog-known fixed curriculum node with an ID and strictly earlier position, subject to programme checks.
- A permitted new supplementary prerequisite card with usable title/AU data, a real earlier remaining roadmap semester, and reviewed own course requirements already completed.

The helper prefers branches with fewer new cards, then fewer existing planned prerequisites; fully completed branches win over planning branches. A wholly completed branch is `ready`; an earlier fixed curriculum path is still `needs-prerequisite-planning`, with no new card or extra penalty. The response reports only the selected branch.

New cards do not consume elective slots. Timing can come from an earlier uncompleted fixed curriculum semester or an open choice slot. A new card cannot silently duplicate a later fixed curriculum prerequisite, require an unverified chain/co-requisite, or rely solely on catalog presence. Any new cards apply the unchanged `-10` penalty once per recommendation.

`MH2802` has an unverified H2 Maths/equivalent condition, and `SC1004` has unresolved cohort-dependent co-requisites. Neither is currently eligible as a new Cloud prerequisite card merely because an earlier semester exists. Completed `SC1004` works, and earlier fixed `MH2802` can support the curriculum plan; that reuse does not independently certify its H2 Maths condition. Readiness remains course-path assistance, not full academic registration approval.

### 6.1 Planned node and edge integrity

Nodes are constructed from the accepted readiness plan. `add_planned_roadmap_artifacts()` shares a prerequisite card across recommendations, keeps its earliest accepted position, and avoids ID collisions with curriculum/slot nodes. Edges use actual existing node IDs or generated nodes present across the complete response. Consumers must read all returned recommendations to resolve shared nodes.

The historical saved benchmark contains five dangling `SC4052`/`MH2802` edges; the fresh owned-server baseline also has five. The updated benchmark has zero supplementary violations. The fresh 180-cell grid moves from 36 dangling-edge contract failures to zero. A positioned `SC4012` scenario generates `SC2002` in Year 3 Semester 1 and connects it to the Year 4 target while the only elective slot is the target. Its own OR requirement is supported by completed `SC1003`; completed `SC2005` satisfies the other target requirement.

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
- The request still has result budget available.

Both passes use the normalized slot identities. Pass 2 receives `limit - len(pass1Results)` and stops at that budget.

It searches slot-compatible modules matching those preferences without requiring a career signal. Results explicitly use:

```text
recommendationSource = "interest"
```

Their reason states that they match the student's interests but are not directly tied to the career goal.

The historical and fresh 24-case benchmarks and 180-cell grids contain zero interest picks. The new positioned graphics scenario does exercise pass 2: `SC3060` returns with source `interest`, score `21`, and null career evidence. This demonstrates the fallback path, not academic standing eligibility.

### 9.3 Historical findings and current resolutions

The earlier review found four issues, now addressed:

| Historical issue | Current implementation |
| --- | --- |
| Additional candidates reused first-pass prerequisite/unlock maps | Pass 2 queries prerequisites, details and unlocks for its own candidate codes; missing map data is not replaced with an empty list |
| Penalty shown but omitted from interest score | `score = max(1, basePreferenceBoost + unlockContribution + prerequisitePlanningPenalty)`; `finalScore` agrees and assignment thresholds apply |
| Pass 2 appended beyond `limit` | Remaining budget is passed explicitly and enforced during selection |
| ID-less slots could be refilled | IDs are generated once before either pass, collision-safe and deterministic by request index; duplicate explicit IDs return `422` |

Temporary in-memory probes verify fresh data retrieval, missing-map rejection, budgets, omitted-ID collisions, score-floor consistency, and shared artifact integrity. Full-response supplementary checks pass in the integrated captures. A single live interest case is useful coverage, but not a comprehensive fallback evaluation or evidence that the old edge cases affected normal frontend users.

## 10. Response And Explanation Contract

Each recommendation includes:

- Module identity, AU, faculty, and level.
- Matched slot code and normalized exact slot ID (frontend-provided or backend-generated).
- Optional roadmap year and semester.
- MPE specialisations.
- Matched signals.
- Selected-branch prerequisite codes and missing prerequisites.
- Existing and planned prerequisite codes.
- Planned prerequisite modules, nodes, and edges.
- Readiness status and unlock value.
- Final score and confidence.
- Deterministic score breakdown with consistent final score in both passes.
- A template-based explanation reason.
- `recommendationSource`, either `career` or `interest`.

The explanations are deterministic templates built from scoring signals and the evidence-selection policy. They are not LLM-generated prose. Prerequisite fields describe the selected reviewed course branch; remaining co-requisite, standing, cohort and registration limits are not certified.

The roadmap UI intentionally does not display the full score breakdown. The breakdown remains available through the API and saved evaluation artifacts for debugging and evaluation.

## 11. Data Sources

The active recommendation path uses PostgreSQL tables populated by `backend/database/seed.py`.

Important seed inputs include:

- `data/modules.json` for curated module metadata, recommendation tags, profiles, and specialisations.
- `data/course_catalog.json` for normalized catalog details and programme restrictions.
- Enriched prerequisite data used to populate prerequisite relationships.

`data/ntu_mods.json` is a tracked historical/raw data artifact and is not read by the current runtime recommendation path.

## 12. Historical And Current Benchmark Snapshots

The controlled planning-fix comparison in this section predates the Cloud career-tag correction in commit `1e30917`. Fresh API verification with both changes gives nDCG@returned `0.7413165112`, precision@returned `0.7777777778`, full slot fill and zero supplementary contract violations. Draft explanation-path fidelity is `0.5`; expected paths require review after Cloud's backend tag is removed. See `Evaluation.md` section 4.3 and the latest `Progress2.md` entry for the follow-up evidence and the deferred Software Engineer interest-ranking review. Historical captures and their declared revisions remain unchanged.

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

Thus `1.0` means **100% validity under the legacy benchmark checks**, not full correctness. The five historical dangling edges are examples it misses. New supplementary validation reads the complete request/response and separately checks budgets, known slot IDs/positions, duplicate slots/modules, edge endpoint existence, strictly earlier prerequisite placement where observable, and `score`/`finalScore`/floored component-sum consistency. Missing positions/data are reported as not observable; this checker does not reconstruct academic or programme policy.

### 12.3 Synthetic requests and current seed inputs

Read-only inspection verified that all 567 curriculum entries across the 24 saved requests have neither year/semester positions nor titles, and every request has empty `excludedCourseTitles`. Benchmark choice slots do carry positions, but these curriculum inputs cannot exercise earlier-curriculum readiness, later-curriculum unlock value, or title-based exclusion/equivalence as the frontend does.

The 15-of-53 seed disagreement count remains historical and attributed to Sol Max. New captures save complete responses, source/rule/seed hashes and explicitly declared serving/database evidence. The benchmark runner supports positioned curriculum objects, fixed-title exclusions and choice placeholders, but the unchanged 24-case dataset remains code-only; the positioned scenarios provide separate input-shape coverage.

### 12.4 Fresh same-database implementation comparison

The owned-server baseline at `cdd488b` and the completed fixes used the same 24 draft-labelled cases, the same 53 assignments and unchanged PostgreSQL tables. Labels, seeds, career-skill mappings and scoring constants were unchanged. A new reviewed prerequisite rule mapping was added; that is the policy change being evaluated.

| Metric | Fresh baseline | After fixes |
| --- | ---: | ---: |
| Precision@5 | 0.3333 | 0.3250 |
| nDCG@5 | 0.5482 | 0.5175 |
| Precision@returned | 0.7778 | 0.7569 |
| nDCG@returned | 0.7571 | 0.7158 |
| Case coverage / slot fill | 1.0 / 1.0 | 1.0 / 1.0 |
| Explanation coverage | 1.0 | 1.0 |
| Explanation fidelity | 0.5652 | 0.5652 |
| Skill-area diversity@5 | 1.3333 | 1.3333 |
| Legacy validity / old-code exposure | 1.0 / 0 | 1.0 / 0 |
| Supplementary contract violations | 5 | 0 |

The relevant nDCG change is **0.7571 → 0.7158**, not the historical file's `0.6313` → current result. Draft-label alignment decreased while observed contract validity improved. This is a tradeoff to review with an expert, not a reason to retune constants immediately.

Concrete selection changes include:

| Case | Changed selection |
| --- | --- |
| Software Engineer `002` | `SC4064` → `SC4052` |
| Software Engineer `003` | `SC4012` → `SC4052` |
| Software Engineer `013` | `SC4064` → `SC4052`; `SC4001` moves to the later slot |
| Data Engineer `001` | `SC4023` → `SC4052` |
| Cloud/Platform `003` | Same modules; Cloud score `47` → `57`, `needs-prerequisite-planning` → `ready`; score order becomes `SC4050`, `SC4052`, `SC4051` |

Restoring the completed `SC1004` Cloud alternative removes the unchanged `-10` planning penalty and changes scores and diversity-band selection. The AND gate also prevents a single completed prerequisite from satisfying `SC4012`, verified separately. In Software Engineer `003`, both `SC2002` and `SC2005` are completed: its replacement is not evidence that `SC4012` was blocked by the AND gate. The summary records 12 cases with code, score, readiness or slot-position changes; four change their selected module set.

Full captures remain temporary. The persistent summary contains precise metrics, hashes and changed-case details. Historical `data/recommendation_benchmark_predictions.json` remains intact and retains its older results.

## 13. Counterfactual Sensitivity

The historical counterfactual record contains eight checks:

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

The current live rerun is **6 PASS / 0 FAIL / 2 INCONCLUSIVE**, with zero supplementary contract violations. Both `software-engineer-csc-009 + computer-security` and `ai-ml-engineer-csc-001 + database` already contain the tag or alias in baseline output evidence. The script correctly declines to count that as a newly introduced signal. The two career swaps, career-conflict check and three completion changes pass. No fresh baseline counterfactual run was taken; the old 7/1 record is retained as history, not a same-process before/after result.

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

The historical coverage result used the legacy `check_invariants()` component: old-code exclusion, completed-code exclusion and limited slot compatibility when a returned ID resolves to a known slot. It does not itself reject unknown slot IDs or check the other contracts. The current runner retains those results for comparison and additionally calls `validate_response()` on the complete request/response. Its supplementary failures are saved separately and cause a nonzero exit. Empty-slot reporting remains a separate measurement.

The file contains per-cell summaries rather than complete recommendation responses and no capture timestamp, code commit, or database snapshot. The 100% fill result applies to this synthetic grid and its stored output, not every degree/cohort, positioned roadmap, or current database state.

### 14.2 Fresh grid and separate positioned scenarios

The fresh same-database historical grid still has 180 cells and 100% fill before and after. Legacy invariant violations stay zero. New full-response contract failures drop from 36 dangling edges to zero; weak-fit cells drop from 20 to 18. Neither fresh grid has interest picks. The older saved file's 26 weak-fit cells describe a different capture and are preserved.

The separately selected positioned mode has nine scenarios: **8 PASS / 0 FAIL / 1 INCONCLUSIVE**, with zero supplementary violations. It covers completed Cloud alternatives, existing prerequisite edges, the successful supplementary `SC4012`/`SC2002` plan, no-earlier-placement exclusion, BDE year fit, a title-exclusion control/pair and a real `SC3060` interest pick. The new Cloud-plan scenario is inconclusive because its own supporting conditions remain unreviewed. `SC3060` has a raw Year 2 standing condition; the observed interest path and course-only readiness do not certify that standing.

These scenarios are deliberately catalog-constrained contract checks, not a second relevance benchmark. Their outcomes and the unpositioned grid metrics remain separate. Negative exclusions are inconclusive if their positive control cannot return the candidate.

## 15. Strengths

### 15.1 Clear separation of responsibilities

The active flow follows the intended layered architecture:

```text
Frontend -> Router -> Service -> Database/tools -> Service -> Router -> Frontend
```

### 15.2 Hard filters precede ranking

Both passes check completed/fixed learning, old code families, restricted projects, programme availability, slot fit and the bounded prerequisite policy before selection. Reviewed grouped requirements and conservative new-card checks improve this boundary; they still do not certify every academic constraint.

### 15.3 Backend owns ranking and allocation

The frontend renders backend assignments by roadmap node ID instead of re-ranking a global candidate list. Normalized identities and shared result budgets now apply consistently across both passes.

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
- Separate full-response contract checks and positioned artifact scenarios.

## 16. Limitations And Risks

### 16.1 Benchmark labels are not independent ground truth

The same project owner who calibrates the recommender also reviews the labels. This can create confirmation bias. Expert review is the highest-priority evaluation improvement.

### 16.2 Slot fill does not guarantee recommendation quality

The older saved grid has 26 weak-fit cells; the fresh grid has 18 after fixes. Full fill does not establish recommendation quality. A future product decision is needed between:

- Showing a weak recommendation with a clear low-confidence label.
- Leaving the slot unfilled and stating that no strong match exists.
- Asking the student to broaden goals or preferences.

### 16.3 Curated data and constants require maintenance

Career mappings, module tags, profile labels, blocklists, and scoring constants are manually maintained. They are explainable, but can become stale when the catalog changes.

### 16.4 Reviewed prerequisite policy remains bounded

Reviewed OR/AND groups replace the permissive any-one shortcut for covered courses. The current MPE listing is a bounded policy, not a cohort-independent registration certificate. Unreviewed graph-empty/singleton fallbacks still cover only stored direct course requirements. Co-requisites, standing, exemptions, transfer credits and special approvals remain outside this model. New prerequisite cards require reviewed own requirements already completed; unknown chains are excluded rather than silently planned.

### 16.5 Current-semester availability is a soft signal

A relevant module can be recommended even if it is not currently offered. This is useful for multi-year planning but requires clear UI communication.

### 16.6 Pass 2 has limited evaluation coverage

The four reported implementation defects are fixed and temporary probes cover their contracts. The positioned `SC3060` scenario confirms one live interest pick, while the ordinary benchmark and coverage grid still contain none. Broader real preference scenarios and explanation review remain useful; one success does not establish general fallback quality.

### 16.7 Prototype identity and persistence are untrusted

Until SSO and server-side storage are implemented, browser state is inspectable and editable. It cannot support production authorization or cross-device persistence.

### 16.8 Saved metrics have incomplete provenance and input coverage

The historical artifacts retain their provenance limitations. New captures record source/rule/seed hashes, declared serving/database evidence, complete responses and raw-file hashes. The unchanged 24 cases and 180-cell grid still omit curriculum timing/titles; positioned scenarios address selected paths separately. Temporary raw files may disappear, so the persistent summary records the comparison without pretending the full captures are committed.

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

### Remaining implementation and verification boundaries

The prerequisite, pass-2 allocation/scoring, artifact and capture follow-ups from the previous audit were implemented in this work unit. Remaining work should be scoped separately:

1. Obtain expert feedback on the changed Cloud selections and draft-label disagreements before score calibration.
2. Review additional prerequisite/co-requisite sources only when needed; preserve cohort distinctions and conservative unresolved behavior.
3. Improve real positioned input and interest-flow coverage without claiming full academic validity from contract checks.
4. Decide weak-fit product behavior and future raw-capture retention policy.
5. Keep authenticated identity/persistence and deferred integrations separate from core ranking.

## 19. Overall Assessment

The system is currently a credible deterministic recommendation prototype, not an AI recommender.

Its foundation now includes reviewed prerequisite branches, conservative new-card planning, consistent pass-2 data/scoring/allocation, complete-response validation and capture provenance. Integrated evidence supports zero observed contract violations and full synthetic slot fill. Draft-label nDCG declined in the same-database comparison; academic/cohort boundaries and subjective ranking questions remain.

The latest reflection is therefore:

- Do not add graph, vector, workflow, or LLM infrastructure merely to make the architecture appear more advanced.
- Do not interpret 100% slot fill as 100% recommendation quality.
- Keep source behavior, historical snapshot metrics, synthetic coverage, and recorded counterfactual outcomes distinct.
- Treat the fixed defects and zero observed contract violations as bounded engineering evidence, not comprehensive academic correctness.
- Do not tune constants solely to improve owner-authored nDCG.
- Use expert review to improve the credibility of labels and identify whether weak-fit recommendations are acceptable.
- Keep core ranking deterministic and backend-owned while authentication and persistence mature separately.
