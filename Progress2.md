# Progress2

This file continues the project progress log after `Progress.md` became large.

## Current Branch

- `recommendation-score-calibration`

## Latest Commits

- `adfd2da fix: exclude core project recommendations`
- `57282fb test: add big data benchmark label`
- `95d4b46 feat: calibrate preference match boost`
- `f92c1a4 test: expand recommendation benchmark cases`
- `a3c7e58 feat: calibrate current semester bonus`

## Current Direction

- Continue improving the deterministic backend-owned recommendation system.
- Keep recommendation ranking and exact-slot allocation in the backend.
- Treat benchmark cases as project-owner-reviewed draft calibration data, not expert ground truth.
- Avoid blind constant tuning just to improve nDCG.

## Current Benchmark Snapshot

After excluding fixed/core project modules from recommendation candidates and regenerating the 14-case benchmark:

- `caseCount`: `14`
- `caseCoverage`: `1.0`
- `totalPredictionsEvaluated`: `32`
- `averagePrecisionAtK`: `0.3714285714285715`
- `averageNdcgAtK`: `0.7051533174757374`
- `averageExplanationCoverage`: `0.8214285714285714`
- `averageExplanationFidelity`: `1.0`
- `averageSkillAreaDiversityAtK`: `1.2142857142857142`
- `oldCodeExposure`: `0`
- `averageConstraintValidity`: `1.0`

## Latest Completed Work

- Reviewed `software-engineer-csc-001`, `software-engineer-csc-002`, and `software-engineer-csc-004`.
- Added missing draft candidate labels where the benchmark omitted valid recommendations.
- Updated the offline benchmark evaluator so rank-sensitive metrics sort exact-slot assignments by backend score instead of roadmap slot display order.
- Kept production recommender scoring unchanged during the review.

## Current Assessment

- Constraint validity is strong and old CE/CPE/CSC/CZ code exposure remains zero.
- The biggest recent issue was benchmark interpretation and incomplete draft labels, not a clear production scoring bug.
- `software-engineer-csc-002` still has lower explanation coverage because direct AI/ML preference modules currently do not have mapped Software Engineer career-skill evidence.

## Recommended Next Step

Review the weakest expanded benchmark cases before more scoring work:

- `software-engineer-csc-014`: decide whether `SC4022 Network Science` should be accepted as a reviewed positive or whether networking-course specificity/current availability needs another scoring signal.
- `software-engineer-csc-006`: inspect low precision with decent nDCG, likely caused by missing reviewed positives or intentionally narrow labels.
- `software-engineer-csc-008`: inspect low precision with decent nDCG, likely caused by missing reviewed positives or intentionally narrow labels.
- `software-engineer-csc-011`: inspect why the second SC3xxx backend-preference slot falls back to `SC3270 Mobile Application Development`.

For each case, decide whether:

- The recommendation is genuinely worse and scoring should be adjusted.
- The benchmark is missing a valid reviewed candidate.
- The benchmark relevance label should be adjusted.
- A future signal, such as availability, programme eligibility, or diversity weighting, should be documented instead of implemented now.

## Out Of Scope

- No Neo4j.
- No ChromaDB.
- No LangGraph.
- No OpenAI.
- No embeddings.
- No ML ranking.
- No MyCareersFuture scraping.
- No auth or SSO.
- No backend persistence for user state.
- No frontend score-breakdown UI unless explicitly requested.
- No automated recommender test suite unless explicitly requested.

## Expanded Benchmark And Preference Calibration

Status: Implemented locally

### Completed

- Imported Claude's normalized expanded benchmark file into `data/recommendation_benchmark_cases.json`.
- Increased benchmark coverage from 5 cases to 14 cases.
- Kept the expanded benchmark import as a separate commit: `f92c1a4 test: expand recommendation benchmark cases`.
- Confirmed all `curriculumCourses` entries are plain string course codes.
- Confirmed null `targetSlotId` values are only used for irrelevant negative reviewed candidates, following the original case-005 pattern.
- Regenerated `data/recommendation_benchmark_predictions.json` against a fresh local backend on port `8001`.
- Debugged `software-engineer-csc-014` and confirmed `SC3030 Advanced Computer Networks` was eligible but lost the SC3xxx slot to `SC3099 Capstone Project` by 2 points.
- Increased `PREFERENCE_FIRST_MATCH_BOOST` from `30` to `35` so explicit student topic preferences can win close comparisons against broad but non-preference software-engineering modules.
- Kept additional preference-match boosts and the preference cap unchanged.
- Regenerated predictions after the preference calibration.

### Rationale Notes

- The expanded benchmark exposed ranking gaps that the original 5-case smoke benchmark did not cover.
- In `software-engineer-csc-014`, the student explicitly selected `computer-network` and `operating-systems`; `SC3030` matched the preferred `computer-network` tag but was narrowly beaten by the broad capstone module `SC3099`.
- Raising the first preference boost is a small calibration, not a hard filter: career relevance, eligibility, same-faculty fit, slot fit, and diversity still remain active.
- `SC4022 Network Science` still outranks `SC4030 Wireless & Mobile Networks` for the SC4xxx slot because both match `computer-network`, while `SC4022` has additional raw relevance signals. This needs reviewer judgement before further scoring changes.

### Verified

- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_predictions.json`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8001/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Before preference calibration on the 14-case benchmark: `averagePrecisionAtK` `0.37142857142857155`, `averageNdcgAtK` `0.6537369211651016`, `averageExplanationCoverage` `0.8214285714285714`, `averageExplanationFidelity` `0.9545454545454546`, `averageSkillAreaDiversityAtK` `1.2857142857142858`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.
- After preference calibration on the 14-case benchmark: `averagePrecisionAtK` `0.38571428571428584`, `averageNdcgAtK` `0.6751174799887892`, `averageExplanationCoverage` `0.8214285714285714`, `averageExplanationFidelity` `0.9583333333333334`, `averageSkillAreaDiversityAtK` `1.2142857142857142`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.
- `software-engineer-csc-014` improved from `precisionAtK` `0.0` and `ndcgAtK` `0.0` to `precisionAtK` `0.2` and `ndcgAtK` `0.2993278235316259`, with `SC3030` now selected for the SC3xxx slot.

### Not Included

- No benchmark label changes during the scoring calibration.
- No hard preference filter.
- No changes to additional preference boost steps or the preference cap.
- No frontend UI changes.
- No automated recommender test suite.
- No Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, MyCareersFuture scraping, auth, SSO, or backend user persistence.

## Current-Semester Benchmark Label Review

Status: Implemented locally

### Completed

- Reviewed `software-engineer-csc-009`, a no-preference Y4 CSC case with two SC4xxx MPE slots.
- Confirmed the backend predictions are `SC4023 Big Data Management` and `SC4013 Application Security`.
- Added `SC4023 Big Data Management` as a `relevant` reviewed candidate for this case.
- Kept production recommendation scoring unchanged.

### Rationale Notes

- `SC4023` has `backend-engineering`, `database`, and `data-science` recommendation tags.
- Its top career-skill evidence path is `Software Engineer -> software design and delivery -> backend-engineering -> Big Data Management`.
- For a no-preference Software Engineer profile, backend/data management is a defensible broad recommendation, even though it is not current-semester and should not be labelled highly relevant by default.
- This case still supports the current-semester interpretation: availability is a modest tie-breaker, not a hard relevance override.

### Verified

- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- `software-engineer-csc-009` improved from `precisionAtK` `0.2` and `ndcgAtK` `0.24630238874073` to `precisionAtK` `0.4` and `ndcgAtK` `0.5531464700081437`.
- Overall benchmark metrics are now `averagePrecisionAtK` `0.4000000000000002`, `averageNdcgAtK` `0.6970349143650328`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.

### Not Included

- No recommendation scoring changes.
- No regenerated prediction file because backend choices and scores did not change.
- No frontend UI changes.

## Core Project Recommendation Exclusion

Status: Implemented locally

### Completed

- Reviewed `software-engineer-csc-010`, where `SC3099 Capstone Project` appeared as a recommendation for a Y3 CSC student.
- Confirmed from curriculum context that `SC3099` is core for more recently matriculated CSC students, so it should be excluded as fixed curriculum context instead of treated as an MPE recommendation candidate.
- Added `SC3099` to `software-engineer-csc-010` `curriculumCourses`.
- Confirmed `SC2079 Multidisciplinary Design Project` should also not be recommended because it is a core project module and is phasing out for newer batches.
- Added a backend hard filter for non-recommendable core project modules: `SC2079` and `SC3099`.

### Rationale Notes

- This is an eligibility fix, not score tuning.
- Fixed/core project modules should be excluded before ranking because they are curriculum requirements, not elective choices.
- The backend guard protects the live app even if browser-provided curriculum exclusions are incomplete or user-editable.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; print('backend import ok')"`.
- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Regenerated predictions with `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8002/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Confirmed no benchmark predictions contain `SC2079` or `SC3099`.
- `software-engineer-csc-010` now recommends `SC3020 Database System Principles` for the SC3xxx slot and `SC4013 Application Security` for the SC4xxx slot.
- Overall benchmark metrics are now `averagePrecisionAtK` `0.3714285714285715`, `averageNdcgAtK` `0.7051533174757374`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.

### Not Included

- No frontend UI changes.
- No broader fixed/core module taxonomy yet.
- No automated recommender test suite.

## Networking Benchmark Candidate Review

Status: Reviewed, not changed

### Completed

- Reviewed `software-engineer-csc-014`, which covers a Y3 CSC student with `computer-network` and `operating-systems` preferences.
- Confirmed the current predictions are `SC3030 Advanced Computer Networks` for the SC3xxx slot and `SC4022 Network Science` for the SC4xxx slot.
- Confirmed `SC3030` is now selected correctly for the SC3xxx slot after the earlier preference-boost calibration and core-project exclusion.
- Inspected `SC4022 Network Science`, `SC4030 Wireless & Mobile Networks`, `SC4051 Distributed Systems`, `SC4050 Parallel Computing`, and `SC3030 Advanced Computer Networks` scoring signals.
- Kept production recommendation scoring unchanged for now.
- Kept benchmark labels unchanged until reviewer judgement decides whether `SC4022` should be accepted as a positive.

### Findings

- `SC4022` and `SC4030` both have the `computer-network` recommendation tag.
- `SC4030` is the more direct networking course for this preference because its title and catalogue description focus on wireless and mobile networks.
- `SC4030` is current-semester, while `SC4022` is not current-semester.
- `SC4022` wins because its broad catalogue text matches extra raw Software Engineer keywords such as `distributed`, `systems`, `algorithm`, and `security`.
- Current scoring for the inspected modules was:
- `SC3030`: career tag `0`, career skill `6`, current-semester `3`, preference `35`, same-faculty `8`.
- `SC4022`: career tag `11`, career skill `6`, current-semester `0`, preference `35`, same-faculty `8`.
- `SC4030`: career tag `0`, career skill `6`, current-semester `3`, preference `35`, same-faculty `8`.
- `SC4051`: career tag `0`, career skill `23`, current-semester `0`, preference `0`, same-faculty `8`.
- `SC4050`: career tag `21`, career skill `4`, current-semester `3`, preference `0`, same-faculty `8`, with specialist-profile penalty applied later.

### Decision Needed

- Option 1: Add `SC4022 Network Science` as a `relevant` reviewed candidate, but not `highly-relevant`, because it is defensible for network preference but broader and less direct than `SC4030`.
- Option 2: Calibrate raw keyword top-up so broad catalogue descriptions do not outrank direct/current preference-tag matches.
- Recommended next move: do a small calibration review of raw keyword top-up before editing labels, because this issue may affect other broad-description courses beyond case `014`.

### Not Included

- No benchmark-label edit for `SC4022` yet.
- No scoring change yet.
- No frontend UI changes.

## Security Benchmark Candidate Review

Status: Implemented locally

### Completed

- Reviewed `software-engineer-csc-003`, which covers computer-security, cryptography, two SC4xxx MPE slots, and one BDE slot.
- Confirmed the current predictions are `SC4010 Applied Cryptography`, `SC4017 Data Privacy & Security`, and `SC4053 Blockchain Technology`.
- Verified `SC4010` is the strongest match because it directly satisfies the cryptography/security preference.
- Verified `SC4017` remains a valid privacy/security recommendation and can fit either the SC4xxx path or the BDE slot under the current slot rules.
- Added `SC4053 Blockchain Technology` as a `relevant` reviewed candidate because the catalog description covers security, privacy, consensus protocols, distributed systems, and decentralized applications.
- Kept `SC4053` below `highly-relevant` because `SC4010` and `SC4013` are more directly aligned with cryptography and application-security practice.
- Kept production recommender scoring unchanged.

### Rationale Notes

- The current result is defensible as a security-adjacent BDE recommendation, not a clear scoring bug.
- `SC4053` receives strong career-skill evidence from distributed-systems plus computer-security, so the benchmark should not treat it as irrelevant for a security preference profile.
- A future programme-eligibility pass should decide whether MPE/BDE assignment should account for `not_available_to_programme` and `not_available_as_bde_ue_to_programme` metadata.

### Verified

- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- The benchmark now reports `averagePrecisionAtK` `0.56`, `averageNdcgAtK` `0.736612597935391`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.
- `software-engineer-csc-003` now reports `precisionAtK` `0.6` and `ndcgAtK` `0.7368524094319567`.

### Not Included

- No production recommendation scoring or allocation changes.
- No regenerated prediction file because the saved predictions are still current; only draft benchmark labels changed.
- No frontend UI changes.
- No automated recommender tests unless explicitly requested.

## Current-Semester Bonus Calibration

Status: Implemented locally

### Completed

- Replaced the hardcoded current-semester score bonus `1` with a named `CURRENT_SEMESTER_BONUS`.
- Set `CURRENT_SEMESTER_BONUS` to `3` so current-catalog availability is a small but visible tie-breaking signal.
- Kept current-semester availability as a soft boost, not a hard filter.
- Regenerated benchmark predictions because recommendation `score`, `currentSemesterBonus`, and `finalScore` values changed for currently offered modules.
- Confirmed selected recommendation choices and rank-sensitive benchmark metrics did not change.

### Rationale Notes

- Claude's note was accurate that a `+1` bonus was barely meaningful compared with career relevance, preference boosts, same-faculty boosts, and default-profile adjustments.
- A modest `+3` keeps availability subordinate to relevance while making it visible in score breakdowns.
- The project should not hard-filter non-current-semester modules yet because catalog current-semester data may not represent future offering plans.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; from backend.services.recommendation_service import CURRENT_SEMESTER_BONUS; print('backend import ok'); print(CURRENT_SEMESTER_BONUS)"`.
- Confirmed `CURRENT_SEMESTER_BONUS` is `3`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8001/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Benchmark metrics remained `averagePrecisionAtK` `0.56`, `averageNdcgAtK` `0.7747931100825681`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.

### Not Included

- No hard current-semester availability filter.
- No recommendation choice changes.
- No benchmark label changes.
- No frontend UI changes.

## Unlock Contribution Calibration

Status: Implemented locally

### Completed

- Audited current benchmark predictions and confirmed selected recommendations currently have `unlockValue` `0`.
- Checked CSC modules with large catalog unlock counts and found they are mostly foundational fixed/core modules that are already completed or excluded from recommendation candidates.
- Kept the existing definition of `unlockValue`: it counts later fixed curriculum modules unlocked by a recommendation.
- Replaced the old `min(readiness.unlock_value, 3)` contribution with a named diminishing-returns helper.
- New unlock contribution steps are `4`, `3`, `2`, and `1`, so unlock values map to `0`, `4`, `7`, `9`, and a maximum of `10`.
- Regenerated benchmark predictions and confirmed current benchmark recommendation choices and metrics did not change because the current selected benchmark recommendations still have no later fixed-curriculum unlocks.

### Rationale Notes

- This addresses the weak cap without broadening unlock value into speculative future elective-candidate unlocks.
- A recommendation that unlocks multiple later fixed curriculum modules now matters more than before, but the cap remains modest so unlock value does not dominate career relevance or student preferences.
- Because the current benchmark cases mostly recommend late-year electives, unchanged metrics are expected and not a sign that the helper is unused in earlier-pathway scenarios.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; from backend.services.recommendation_service import get_unlock_contribution; print('backend import ok'); print([get_unlock_contribution(v) for v in range(6)])"`.
- Confirmed unlock contribution mapping `[0, 4, 7, 9, 10, 10]`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8001/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Benchmark metrics remained `averagePrecisionAtK` `0.56`, `averageNdcgAtK` `0.7747931100825681`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.
- The regenerated prediction file had only timestamp/API-url changes, so those generated metadata changes were not kept.

### Not Included

- No change to which modules count as unlocked.
- No speculative unlock value for future elective candidates.
- No benchmark label changes.
- No frontend UI changes.
- No automated recommender test suite unless explicitly requested.

## Legacy Code Penalty Cleanup

Status: Implemented locally

### Completed

- Removed the dead `get_course_code_generation_adjustment()` helper from `backend/services/recommendation_service.py`.
- Removed the unused internal `course_code_adjustment` variable from recommendation scoring and explanations.
- Kept `legacyCodePenalty` in the API score breakdown as `0` for frontend and saved-prediction compatibility.
- Kept old CE/CPE/CSC/CZ handling as a hard eligibility filter before ranking instead of a soft score penalty.

### Rationale Notes

- Claude's note was accurate that `get_course_code_generation_adjustment()` always returned `0`.
- Since deprecated code families are now filtered before scoring, a soft legacy-code penalty is no longer part of the active ranking design.
- Keeping the public `legacyCodePenalty` field avoids a frontend/type/storage compatibility change while making the backend implementation less misleading.

### Not Included

- No recommendation behavior change.
- No API response field removal.
- No frontend type changes.
- No new soft code-generation gradient between current `SC` modules.

## BDE-Specific Availability Filter

Status: Implemented locally

### Completed

- Added `not_available_as_bde_ue_to_programme` to the `modules` table model as a JSON list.
- Updated the seed script to read `not_available_as_bde_ue_to_programme` from `data/course_catalog.json` and populate the modules table by course code.
- Added a seed-time schema helper so local databases gain the new column without introducing Alembic yet.
- Added a BDE-only hard eligibility filter in `backend/services/recommendation_service.py`.
- Kept MPE slot behavior separate; the new BDE/UE restriction only affects BDE slot matching and prerequisite planning into BDE slots.
- Used conservative programme-token matching so `CSC`, `CSC(2024-onwards)`, and `CSC 4` can match a CSC profile while `CSEC` and `REP(CSC)` do not.
- Regenerated benchmark predictions against a fresh local backend and confirmed recommendation choices did not change, so timestamp/API-url-only prediction changes were not kept.

### Rationale Notes

- This preserves the hard-filter-before-ranking architecture by removing modules that are known to be unavailable as BDE/UE before scoring and exact-slot assignment.
- The BDE/UE metadata is different from general `not_available_to_programme`, so it should not affect MPE slots.
- The matching rule is intentionally narrower than substring matching to avoid excluding unrelated programmes that merely contain the same letters.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; print('backend import ok')"`.
- Ran `.venv/bin/python -m json.tool data/course_catalog.json`.
- Ran `.venv/bin/python -m backend.database.seed`.
- Confirmed 24 local module rows now have non-empty `not_available_as_bde_ue_to_programme` metadata.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8001/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Benchmark metrics remained `averagePrecisionAtK` `0.56`, `averageNdcgAtK` `0.7747931100825681`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.
- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_predictions.json`.
- Ran `git diff --check`.
- IDE diagnostics reported no errors in the edited files.

### Not Included

- No recommendation scoring or ranking constant changes.
- No benchmark label changes.
- No kept prediction-file changes because choices did not change.
- No frontend UI changes.
- No automated recommender test suite unless explicitly requested.
- No Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, MyCareersFuture scraping, auth, SSO, or backend user persistence.

## Benchmark Evaluator Reporting Cleanup

Status: Implemented locally

### Completed

- Updated `scripts/evaluate_recommendation_benchmark.py` to make metric ordering explicit in the JSON output.
- Added top-level `metricOrder` and `metricOrderNote` fields.
- Added each case's `rankedCourseOrder`, showing course code, backend score, and matched choice slot ID.
- Kept the evaluator aligned with the backend contract: API responses are exact slot assignments for frontend rendering, while rank-sensitive benchmark metrics use backend score order.

### Rationale Notes

- This makes future case-by-case review easier because reviewers can immediately see the score-ranked order without manually inspecting the full prediction payload.
- The cleanup documents why nDCG may differ from response order and prevents future confusion between roadmap display order and ranking order.

### Verified

- Ran `.venv/bin/python -m compileall scripts/evaluate_recommendation_benchmark.py`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.

### Not Included

- No production recommendation scoring or allocation changes.
- No benchmark label changes in this cleanup.
- No regenerated prediction file.
- No frontend UI changes.

## Programme Availability Filter

Status: Implemented locally

### Completed

- Added a pre-ranking hard filter in `backend/services/recommendation_service.py` for modules that explicitly list the student's programme in `not_available_to_programme`.
- Kept the check conservative by matching exact comma-separated programme tokens only, so `CSC` does not accidentally match similar programme codes such as `CSEC` or `REP(CSC)`.
- Regenerated benchmark predictions against a fresh local backend and confirmed the current CSC benchmark recommendations did not change.

### Rationale Notes

- This preserves the hard-filter-before-ranking architecture: candidates known to be unavailable to the student's programme are removed before scoring.
- The first implementation uses the existing database column only, avoiding schema changes.
- BDE-specific availability such as `not_available_as_bde_ue_to_programme` is still not enforced because that metadata is not currently stored in the modules table.

### Verified

- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8001/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- The regenerated recommendation choices stayed the same, so the prediction file was not kept with timestamp-only changes.

### Not Included

- No database schema changes.
- No BDE-specific `not_available_as_bde_ue_to_programme` filtering yet.
- No current-semester hard availability filter.
- No production scoring or allocation changes.
- No frontend UI changes.

## Blockchain Relevance Label Correction

Status: Implemented locally

### Completed

- Revisited `SC4053 Blockchain Technology` in `software-engineer-csc-001`.
- Changed its expected relevance from `relevant` to `somewhat-relevant`.
- Updated the review note to make clear that blockchain is related to distributed backend engineering through consensus and decentralised systems, but remains a specialist domain.

### Rationale Notes

- `SC4053` should not be treated as equally useful as broader backend/distributed recommendations such as `SC4051 Distributed Systems` or `SC4052 Cloud Computing`.
- Keeping it as `somewhat-relevant` still gives partial credit for the distributed-systems/security connection without overvaluing a niche blockchain module.

### Not Included

- No production recommendation scoring or allocation changes.
- No regenerated prediction file.
- No frontend UI changes.

## No-Preference Benchmark Candidate Review

Status: Implemented locally

### Completed

- Reviewed `software-engineer-csc-005`, which covers default Software Engineer recommendations when no topic preferences are selected.
- Confirmed the current predictions are `SC4023 Big Data Management`, `SC4013 Application Security`, and `SC4051 Distributed Systems`.
- Compared the current predictions against the reviewed candidates and score breakdowns.
- Changed `SC4040 Advanced Topics In Algorithms` from `highly-relevant` to `relevant`.
- Kept production recommender scoring unchanged.

### Rationale Notes

- `SC4040` is useful for algorithmic reasoning, performance trade-offs, and implementation depth, so it remains relevant.
- It is not an obvious top no-preference default because it is an advanced/specialist algorithmic module rather than a broadly applied backend, distributed, or secure software engineering module.
- The current selected modules are defensible defaults under the existing broad-default metadata and deterministic scoring.

### Verified

- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- The benchmark now reports `averagePrecisionAtK` `0.56`, `averageNdcgAtK` `0.7747931100825681`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.
- `software-engineer-csc-005` now reports `precisionAtK` `0.6` and `ndcgAtK` `0.773468039695752`.

### Not Included

- No production recommendation scoring or allocation changes.
- No regenerated prediction file because the saved predictions are still current; only draft benchmark labels changed.
- No frontend UI changes.
- No automated recommender tests unless explicitly requested.
