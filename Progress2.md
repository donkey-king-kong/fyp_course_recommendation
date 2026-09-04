# Progress2

This file continues the project progress log after `Progress.md` became large.

## Current Branch

- `recommendation-score-calibration`

## Latest Commits

- `05fbee5 docs: add benchmark candidate review`
- `b0f3fb6 test: align recommendation benchmark evaluation`

## Current Direction

- Continue improving the deterministic backend-owned recommendation system.
- Keep recommendation ranking and exact-slot allocation in the backend.
- Treat benchmark cases as project-owner-reviewed draft calibration data, not expert ground truth.
- Avoid blind constant tuning just to improve nDCG.

## Current Benchmark Snapshot

After aligning the offline evaluator with backend score order for exact-slot assignments:

- `averagePrecisionAtK`: `0.52`
- `averageNdcgAtK`: `0.7240371676639045`
- `averageExplanationCoverage`: `0.9`
- `averageExplanationFidelity`: `1.0`
- `averageSkillAreaDiversityAtK`: `1.4`
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

Review the remaining benchmark cases:

- `software-engineer-csc-003`: confirm security/cryptography recommendations, BDE handling, and diversity behavior.
- `software-engineer-csc-005`: confirm no-preference default recommendations, broad-default behavior, and whether currently selected modules match the intended default Software Engineer profile.

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
