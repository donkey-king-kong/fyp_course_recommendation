# Catalog Mutual-Exclusion Review

Date: 2026-11-03

## Finding And Change

The checked-in [course catalog](../../data/course_catalog.json) lists `SC1015` (Introduction to Data Science & Artificial Intelligence) and `SC3021` (Data Science Fundamentals) as **mutually exclusive in both directions**. Their descriptions cover introductory data-science thinking and Python work. Despite `SC1015` appearing in submitted completions, the existing owned backend recommended `SC3021` in the frozen AI/ML Engineer `001` and Data Scientist `001` cases. This is a concrete eligibility defect, not evidence for a prior-learning score penalty.

The catalog also lists `SC1004` and `SC1104` (both Linear Algebra for Computing, with the same description) as reciprocally exclusive. One saved 180-cell coverage response selected `SC1104` despite submitted `SC1004`.

The backend now loads *reciprocal, exact-code* catalog declarations and excludes a candidate if its reciprocal partner is in submitted `completedCourseCodes`. Both the career and interest candidate passes apply the same hard filter before scoring. A one-sided or malformed catalog entry is not enough to exclude a course. This reads the checked-in catalog at startup; the database's `modules` table does not store mutual-exclusion pairs. The filter does not infer mastery, penalize shared topics, alter ranking constants, or resolve programme/cohort-specific registration rules.

## Controlled Comparison

Inputs: frozen 24-case benchmark SHA-256 `41dd39fd9c84b4ebdab56c749fb032e714c35e297e2e4affd77a1824b929eb3a`; catalog SHA-256 `e94466a7834bd551bf86dfbca33c5c30c2ec6e4f9dbb59df3aa7389752a61d63`. The owned localhost FastAPI process ran the edited working tree based on `e438605`; its `modules`, `module_prerequisites` and `faculties` read-only fingerprint was `c443b5b0dbb72f014be71ba8780be963cbf09bb23a774b312859a4c1166faf8d` both before and after. The historical capture declares the same fingerprint but did not independently attest it. Existing saved inputs, labels and historical predictions were not edited.

| Frozen case | Historical selection | Filtered selection | Review |
| --- | --- | --- | --- |
| AI/ML Engineer `001` | `SC3021` and `SC4061` | `SC4061`; `SC3xxx` left open with `no-supported-match` | `SC3021` conflicts with completed `SC1015`; no verified strong alternative for that exact slot in this request. |
| Data Scientist `001` | `SC3021` and `SC4000` | `SC3000` and `SC4000` | `SC3000` is a distinct AI course and not catalog-excluded by `SC1015`; it remains a provisional career/content judgment, not independently validated registration advice. |

The other 22 case selections were unchanged, including frozen Software Engineer `001`-`005`. All 24 responses passed existing supplementary contract checks with **zero violations**. Evaluator summary: 53 -> 52 returned recommendations; average slot fill 1.000 -> 0.9792; precision@5 0.3333 -> 0.3250; nDCG@5 0.5339 -> 0.5213. These are effects of an eligibility correction against draft labels, **not** a reason to weaken it or relabel the benchmark.

The existing 180-cell grid has **19 changed cells**: 18 replace/remove `SC3021` after `SC1015` and one replaces `SC1104` after `SC1004`. Six AI/ML Y4-end `SC3xxx` cells now leave that slot open; there were zero invariant/contract violations. The nine positioned scenarios remained eight pass and one inconclusive, with zero contract violations. The opt-in nine-check counterfactual run was nine pass, zero inconclusive/fail, with zero contract violations. The formerly inconclusive AI/ML database swap now passes because the newly open slot accepts an `interest`-sourced `SC3020`; this conditional result is **not** comparable as evidence of a newly improved preference model. Its previously saved inconclusive response remains historical evidence.

## Boundaries And Reproduction

The catalog is a checked-in snapshot, not a live registrar feed; an absent or unilateral declaration is not a clearance. Submitted completions are user-controlled prototype state, and the filter does not check future fixed-course clashes, all curricular mutual exclusions, current offering, credit recognition or student-specific waivers. Catalog and database versions must be reviewed together before production use. The separate seven-course skills preview and its progression judgments are unchanged.

To repeat the comparison, start the current branch's FastAPI app with the configured 4,318-row local module database; run `scripts/run_recommendation_benchmark_predictions.py` against the frozen benchmark, then `scripts/evaluate_recommendation_benchmark.py`, `scripts/run_coverage_audit.py` in `historical-grid` and `positioned-scenarios` modes, and `scripts/run_counterfactual_sensitivity.py` with the existing opt-in interest control. Record the actual process revision, catalog hash and read-only database fingerprint with each new capture. This review used temporary captures outside the repository; the checked-in historical artifacts remain frozen.
