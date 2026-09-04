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
