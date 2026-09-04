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
