# Evaluation Methodology and Results

This document describes the deterministic recommender's evaluation, historical snapshots and the integrated `recommendation-planning-integrity` comparison on 2026-11-03. It is the primary source for the FYP report's evaluation chapter. Exact results, source/capture hashes and changed-case details are preserved in `data/review/recommendation_planning_integrity_results.json`; complete raw captures remain temporary.

---

## 1. Purpose and Scope

The evaluation covers the deterministic recommendation engine only — the backend-side module ranking, slot assignment, and explanation generation. It does not cover the transcript parser, curriculum guide parser, or any frontend behaviour.

**What the evaluation measures:**

- Whether the top-ranked modules match modules that a reviewer would consider appropriate for the student's career goal and preferences.
- Whether implemented code/slot checks and observable response contracts pass; this is not full academic eligibility.
- Whether the explanation references the correct career–skill path.
- Whether recommendations shift in the expected direction when inputs change (counterfactual sensitivity).

**What the evaluation does not measure:**

- Real student satisfaction or acceptance rates (no live user study yet).
- Expert-level ground truth — labels are project-owner-reviewed drafts, not adviser or TA verified.
- Whether the scoring weights are globally optimal.
- Complete co-requisite, cohort, standing, offering, workload or registration eligibility.

---

## 2. Benchmark Design

### 2.1 Label source

All cases are in `data/recommendation_benchmark_cases.json`. The file has a `reviewerStatus` field per case; all current cases are marked:

```
project-owner-reviewed-draft-not-expert-ground-truth
```

This means the labels are accepted for local benchmarking and regression detection but should not be cited as expert-validated ground truth in the final FYP report without a separate expert review pass.

### 2.2 Case schema

Each case provides:

| Field | Description |
|---|---|
| `caseId` | Unique identifier, e.g. `software-engineer-csc-001` |
| `careerGoal` | One of the six supported career goals |
| `preferredRecommendationTags` | Zero or more topic tags declared by the student |
| `completedCourseCodes` | Modules already done; the recommender must exclude these |
| `choiceSlots` | Open MPE and BDE slots to fill, each with a `slotId` and slot type (`SC3xxx`, `SC4xxx`, `BDE`) |
| `curriculumCourses` | All courses on the student's curriculum (completed + fixed); used to exclude non-elective modules |
| `reviewedCandidates` | Labelled positive and negative candidate modules with `expectedRelevance`, `expectedSkillPath`, and `reviewNotes` |

### 2.3 Relevance labels and gains

| Label | Gain | Meaning |
|---|---|---|
| `highly-relevant` | 3 | Should appear in the top recommendations; clearly maps to the career and preferences |
| `relevant` | 2 | A reasonable pick; career-skill mapping exists but preferences or diversity may vary |
| `somewhat-relevant` | 1 | Has some career signal but should not outrank stronger candidates |
| `irrelevant` | 0 | No career-skill mapping, or hard-filtered by a blocklist or preference mismatch |

A `targetSlotId` of `null` on an irrelevant candidate means the reviewer did not assign it to any slot; it exists as a negative example only.

### 2.4 Case selection criteria

Cases were chosen to:

- Cover each supported career goal with at least two cases.
- Test different year levels (Y3 with SC3xxx slots vs. Y4 with SC4xxx slots).
- Test BDE slots alongside MPE slots.
- Test preference-sensitive rankings (a student who declared `computer-security` preferences should get security modules ahead of broad infrastructure ones).
- Include at least one `irrelevant` negative candidate per case to confirm the hard filters work.

### 2.5 Careers covered

| Career goal | Case count |
|---|---|
| `software-engineer` | 13 |
| `ai-ml-engineer` | 2 |
| `data-engineer` | 2 |
| `cloud-platform-engineer` | 3 |
| `cybersecurity-engineer` | 2 |
| `data-scientist` | 2 |

---

## 3. Metric Definitions

All metrics are computed by `scripts/evaluate_recommendation_benchmark.py`. Rank-sensitive metrics sort predictions by backend score, not display order, because the backend assigns each module to an exact slot.

### 3.1 precision@k

Fraction of the top-k predictions whose `expectedRelevance` is `highly-relevant` or `relevant`.

```
precision@k = |{relevant predictions in top k}| / k
```

`k = 5` is the default. Because most cases return fewer than 5 predictions (2–3 slots), precision@k is almost always lower than precision@returned — do not use it alone.

### 3.2 nDCG@k

Normalised Discounted Cumulative Gain at cutoff k, using the gains table above.

```
DCG(list) = sum over rank i: gain[i] / log2(i + 2)
nDCG@k   = DCG(predicted top k) / DCG(ideal top k)
```

Ideal DCG is computed from the full set of reviewed candidates, sorted by gain descending, at the same cutoff k.

### 3.3 precision@returned and nDCG@returned

Same as the @k variants but using the actual number of returned predictions instead of a fixed k. These are the most informative metrics for this system because the number of returned predictions equals the number of open slots, which varies per case.

### 3.4 averageSlotFillRate

```
slotFillRate = min(assignedSlots, expectedSlots) / expectedSlots
```

An average of 1.0 means every open slot received a recommendation. Drops below 1.0 if the system runs out of eligible candidates for some slot.

### 3.5 explanationCoverage

Fraction of top-k predictions whose `scoreBreakdown.careerSkillEvidence` is non-null. A value of 1.0 means every recommendation has a career–skill path attached.

### 3.6 explanationFidelity

Fraction of top-k predictions where the derived `careerSkillPath` (from `careerGoal -> skillArea -> tag -> title`) matches the reviewer's `expectedSkillPath` exactly. Only predictions with a non-`N/A` `expectedSkillPath` contribute. `null` means no eligible predictions to compare.

### 3.7 skillAreaDiversityAtK

Number of distinct `skillArea` values in the top-k predictions' career skill evidence. Higher indicates more represented career skill areas; it is a breadth observation, not an independent guarantee of better recommendations.

### 3.8 oldCodeExposure

Count of predictions in top-k whose course code starts with `CE`, `CPE`, `CSC`, or `CZ`. Must always be 0. Any value above 0 is a hard failure.

### 3.9 constraintValidity

The retained legacy metric measures nonempty/current codes, completed/fixed-code exclusion and limited slot compatibility over the score-ranked top K. BDE is accepted without a year-level check. A value of `1.0` means those implemented checks passed; it does not establish full prerequisite, programme or artifact correctness.

### 3.10 Supplementary response validation

`validate_response()` examines the complete response, separately from the legacy metric. It checks result budget, known exact slot IDs and positions, duplicate module/slot assignments, planning-edge endpoints across shared nodes, preceding prerequisite placement where positions are available, and agreement between `score`, `finalScore` and the component sum with its floor of `1`. `rawPreferenceBoost` is explanatory metadata and is not added twice. Null career evidence on interest picks is valid.

Each check reports checked/skipped counts, violations and a status. Missing evidence is not silently counted as a pass. These are observable contracts; the evaluator does not reconstruct academic or programme policy. `--fail-on-contract-violations` gives the offline evaluator a nonzero exit while retaining all historical metrics. Live coverage and counterfactual runners also record supplementary failures separately and fail on them.

---

## 4. Benchmark History

Each row represents a snapshot taken after a meaningful change. Metrics are not directly comparable across rows because the case set grew.

| Snapshot | Cases | nDCG@returned | precision@returned | constraintValidity | oldCodeExposure | Notes |
|---|---|---|---|---|---|---|
| Initial 5-case smoke test | 5 | ~0.7 | ~0.8 | 1.0 | 0 | Software engineer only; used for early calibration |
| Expanded to 14 cases | 14 | 0.705 | 0.795 | 1.0 | 0 | Added Y3/Y4 variation and preference-sensitive cases |
| After preference calibration | 14 | 0.675 | 0.786 | 1.0 | 0 | `PREFERENCE_FIRST_MATCH_BOOST` raised 30→35; SC3030 now wins SC3xxx slot for `computer-network` profile |
| Expanded to 21 cases (PR #43) | 21 | 0.737 | 0.786 | 1.0 | 0 | Added AI/ML, Data Engineer, Cloud/Platform, Cybersecurity cases; BDE fallback calibrated |
| Expanded to 24 cases | 24 | 0.683 | 0.694 | 1.0 | 0 | Added 2 Data Scientist cases and 1 Cloud/Platform multi-BDE case; all 6 careers now covered |
| Historical career-first saved file | 24 | 0.631 | 0.639 | 1.0 | 0 | Older saved capture with incomplete serving/data provenance; do not use as the baseline for the current fixes |
| Fresh owned-server baseline, `cdd488b` | 24 | 0.7571 | 0.7778 | 1.0 | 0 | Same cases and database as the following row; five supplementary dangling-edge violations |
| Integrated planning-integrity fixes | 24 | 0.7158 | 0.7569 | 1.0 | 0 | Reviewed prerequisite groups and pass-2/artifact fixes; zero supplementary violations; draft-label alignment decreased |

**Note on comparing rows:** When case count increases, nDCG and precision aggregate over more cases. A drop in the average does not necessarily mean ranking quality degraded — it may reflect new cases where the system performs worse for previously untested scenarios. Use per-case breakdowns (`scripts/evaluate_recommendation_benchmark.py` output) to diagnose regressions.

### 4.1 Current controlled implementation comparison

The parent launched a baseline backend before the edits and restarted an owned backend on port `8002` after the fixes. Before/after read-only database fingerprints matched: 4,318 modules, 4,178 prerequisite relationships and 34 faculties. No reseed, career-skill mapping changes, scoring-constant tuning or label edits occurred. The new prerequisite rule mapping is the evaluated policy change.

| Metric | Fresh baseline | After fixes |
| --- | ---: | ---: |
| Cases / recommendations | 24 / 53 | 24 / 53 |
| Precision@5 | 0.3333 | 0.3250 |
| nDCG@5 | 0.5482 | 0.5175 |
| Precision@returned | 0.7778 | 0.7569 |
| nDCG@returned | 0.7571 | 0.7158 |
| Slot fill / case coverage | 1.0 / 1.0 | 1.0 / 1.0 |
| Explanation coverage | 1.0 | 1.0 |
| Explanation fidelity | 0.5652 | 0.5652 |
| Skill-area diversity@5 | 1.3333 | 1.3333 |
| Legacy validity / old-code exposure | 1.0 / 0 | 1.0 / 0 |
| Supplementary contract violations | 5 | 0 |

The relevant nDCG decrease is `0.7571050903913039` → `0.7157687115138366`. Comparing against the older `0.6313` file would misrepresent the effect of these fixes.

Restoring Cloud Computing's verified `SC1004 OR MH2802` requirement makes completed `SC1004` usable and removes an erroneous `-10` planning penalty. Software Engineer cases `002` and `013` replace `SC4064` with `SC4052`; case `003` replaces `SC4012`; Data Engineer `001` replaces `SC4023`. Cloud/Platform `003` keeps the same modules but Cloud score rises from `47` to `57` and moves ahead of `SC4051` in score and slot order, after `SC4050`. Twelve cases have code, score, readiness or slot-position changes; four change their selected module set.

The AND gate separately prevents one prerequisite satisfying `SC4012`'s `SC2002 AND SC2005` requirement. Case `003` has both completed, so its replacement is a changed score/selection outcome rather than rejection by that gate. Lower draft-label agreement requires expert review of these choices; it does not justify changing constants merely to recover the old nDCG.

### 4.2 Provenance and retained artifacts

The persistent summary stores baseline Git-source hashes, reviewed after-source hashes, per-case changes, metrics, compact scenario outcomes, database table fingerprints and raw capture hashes/paths. The after serving declaration is `cdd488b+uncommitted-planning-fixes`. Serving revision and database fingerprint are explicitly operator-declared; local Git/file hashes alone cannot identify a running process or its database. The parent verified matching read-only table fingerprints using the same configuration as the owned backend.

Full raw captures are in `/private/tmp/recommendation-planning-T66qUE/` and may disappear. Only the compact evidence summary is intended as persistent repository evidence. Existing benchmark labels, `data/recommendation_benchmark_predictions.json` and `data/coverage_audit_results.json` retain their historical contents.

### 4.3 Subsequent Cloud career-tag correction

Commit `1e30917` removes `backend-engineering` from Cloud Computing's curated tags. The same one-tag correction was applied to its local PostgreSQL row, and fresh API responses matched the preceding read-only diagnostic. With the planning fixes above included, precision@returned is `0.7777777778`, nDCG@returned is `0.7413165112`, slot fill remains `1.0`, and supplementary contract violations remain zero. This is a separate follow-up to the table above, not a replacement for its controlled planning-fix comparison.

Data Engineer case `001` now selects Big Data Management; the cloud-preferring case `002` still ranks Cloud ahead. Draft explanation-path fidelity falls to `0.5`, requiring review of expected paths after Cloud's evidence changes from backend implementation to distributed infrastructure. No benchmark labels were changed. The coverage audit retains 180 filled cells with zero violations and 18 weak-fit cells; positioned scenarios remain 8 PASS / 1 INCONCLUSIVE / 0 FAIL, and counterfactual checks remain 6 PASS / 2 INCONCLUSIVE / 0 FAIL.

The full follow-up captures remain temporary under `/private/tmp/recommendation-career-relevance/`, and no fresh full-database fingerprint was taken after the targeted row update. `Progress2.md` records the course-content rationale and the deferred review of Software Engineer keyword credit and interest scaling. That ranking-quality review does not block other project work.

---

## 5. Counterfactual Sensitivity Results

Script: `scripts/run_counterfactual_sensitivity.py`

Run with:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/run_counterfactual_sensitivity.py \
  --api-url http://127.0.0.1:8000/recommendations \
  --output /private/tmp/counterfactual-review.json
```

Run against a separately started backend. Historical records contain 7 PASS / 0 FAIL / 1 INCONCLUSIVE. The current live rerun contains **6 PASS / 0 FAIL / 2 INCONCLUSIVE**, with zero supplementary violations. The old counterfactual baseline was not rerun, so these are distinct recorded outcomes, not a controlled before/after counterfactual comparison.

| Check | Historical record | Current rerun | Current observation |
| --- | --- | --- | --- |
| SWE `007` → Data Scientist | PASS | PASS | Recommendation set and career evidence change |
| SWE `007` → Cybersecurity | PASS | PASS | Recommendation set and career evidence change |
| SWE `009` + `computer-security` | PASS | INCONCLUSIVE | `cybersecurity` alias is already in baseline output evidence |
| AI/ML `001` + `database` | INCONCLUSIVE | INCONCLUSIVE | `database` is already in baseline output evidence |
| AI/ML `001` with conflicting SWE preferences | PASS | PASS | Career evidence retains the selected career |
| SWE `001` completion change | PASS | PASS | Completed recommendation is removed; slots remain filled |
| Data Scientist `001` completion change | PASS | PASS | Completed recommendation is removed; slots remain filled |
| Cybersecurity `001` completion change | PASS | PASS | Completed recommendation is removed; slots remain filled |

**INCONCLUSIVE defined:** In these two preference checks, the tag/alias already appears in baseline evidence, so the assertion does not establish a newly introduced preference signal. It should not be counted as a pass or a failure, or interpreted as proof that every ranking component is insensitive. Interest-only results may legitimately have null career evidence; the script now handles that safely.

Earlier exploratory preference probes are historical observations, not current eligibility explanations. In particular, Cloud prerequisites are now governed by verified `SC1004 OR MH2802` branches; neither a blanket faculty argument nor the old flat graph correctly describes current behavior. Expert review and genuinely new preference signals remain necessary to assess sensitivity depth.

**Earlier correction (cloud-platform + computer-network):** The original `cloud-platform-engineer-csc-001 + computer-network` check was a no-op. That benchmark case already listed `computer-network` in its `preferredRecommendationTags`, so adding it again produced no change. The FAIL result was invalid. The guard in `run_preference_swap_check` now fails immediately if the added tag is already in the base case, preventing this class of mistake in future runs. A separate baseline comparison was added to detect the INCONCLUSIVE case.

**Residual label-review work:** Earlier Cloud/Platform SC3xxx choices raised disagreements between `SC3030` and `SC3050`. Those historical scoring explanations should not substitute for current case evidence. Review weak-fit choices and the current changed Cloud selections with a supervisor or senior student before changing labels or weights.

---

## 6. Known Weaknesses and Future Work

### 6.1 Label quality

All labels are owner-reviewed drafts. Until a lecturer, TA, or senior student performs an independent review, precision and nDCG scores reflect alignment with the owner's own judgement.

**Planned:** Expert review or think-aloud session with a supervisor or senior student to validate a subset of labels. This is the single most credible evaluation improvement for the FYP report.

### 6.2 Coverage audit

Script: `scripts/run_coverage_audit.py`. Run against a separately started backend, saving a new temporary file:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/run_coverage_audit.py \
  --api-url http://127.0.0.1:8000/recommendations \
  --mode historical-grid --output /private/tmp/coverage-review.json
```

**Grid:** 6 careers × 5 slot configurations × 2 progress stages × 3 preference modes = 180 cells.

- Slot configs: `SC3xxx-only`, `SC4xxx-only`, `SC3-and-SC4`, `SC4-BDE-BDE`, `BDE-only`.
- Progress stages: Y2-end (15 modules completed) and Y4-end (35 modules completed).
- Preference modes: none, career-aligned, and career-conflicting.
- Faculty: CSC only (non-CSC is a known limitation, not covered by this audit).

**Historical saved result after the request-shape correction:**

- Invariant violations: **0** across all 180 cells.
- Pass-2 interest picks: **0 fired** — all assigned slots were filled by career picks.
- Overall slot fill rate: **100%** across all 180 cells. No empty slot findings.

**Weak-fit picks (filled but low career signal):**

The audit flags picks where `careerSkillScore < 5` and `careerTagScore == 0` — slots that are filled but only on faculty or structural signal rather than direct career relevance. Three distinct module codes appear across 26 cells:

| Module | Career | Slot config | Progress | Why weak |
|---|---|---|---|---|
| `SC3040 Advanced Software Engineering` | cybersecurity-engineer | SC3xxx-only | Y4-end | SC3010 (the only cyber-tagged SC3xxx module) is already completed; SC3040 fills via faculty boost, no direct cyber tag |
| `SC3050 Advanced Computer Architecture` | cloud-platform-engineer | SC3xxx-only | Y2/Y4-end | Low mapped/direct career signal in that saved snapshot; faculty/structural fit still fills the slot |
| `SC3020 Database System Principles` | ai-ml-engineer | SC3xxx-only | Y4-end | Below the weak-fit mapped-score cutoff, with no fallback career-tag score in that saved snapshot |

These are quality observations, not legacy invariant failures. Whether weak picks should be labeled low confidence or replaced with an explicit “no strong match” message remains a product decision requiring reviewer feedback. Full fill alone does not settle it.

**Correction note:** The first run of this audit (merged in PR #50, 2026-11-03) reported a false cybersecurity SC3xxx gap at Y4-end. The root cause was a bug in `build_request()`: it sent `majorCode` and `year` (not recognised API fields) and omitted `studentFaculty`. Without `studentFaculty: "CSC"`, the CSC faculty bonus (+8 points) was absent, dropping SC3040's score below the MPE minimum threshold of 10. With the correct request shape, SC3040 scores 15 and fills the slot. The bug affected all 180 cells — the first run's "100% fill rate in 174 cells" was also measured on unrealistic requests without faculty context.

**Fresh same-database grid comparison:**

| Observation | Fresh baseline | After fixes |
| --- | ---: | ---: |
| Cells / fully filled cells | 180 / 180 | 180 / 180 |
| Legacy invariant violations | 0 | 0 |
| Supplementary contract violations | 36 dangling edges | 0 |
| Weak-fit cells | 20 | 18 |
| Interest picks | 0 | 0 |

The historical file's 26 weak-fit cells remain distinct from the fresh 20 → 18 comparison. The unpositioned grid omits slot year/semester and curriculum positions/titles, so it cannot validate BDE year matching, earlier fixed prerequisite paths or semester placement. Its legacy invariant checker is narrow; current runners also save full responses and independent supplementary checks, whose failures cause a nonzero exit.

**Positioned scenarios, reported separately:**

Use `--mode positioned-scenarios` to run catalog-constrained positioned/titled contracts. The integrated run has nine scenarios: **8 PASS / 0 FAIL / 1 INCONCLUSIVE**, with zero supplementary violations.

- `SC4052` is ready with completed `SC1004`, and reuses earlier fixed `MH2802` with a valid edge.
- New Cloud prerequisite planning remains inconclusive: `MH2802` has an unverified H2 Maths condition and `SC1004` unresolved co-requisites, so neither new card is assumed feasible.
- `SC4012` with completed `SC1003` and `SC2005` generates an earlier `SC2002` card and edge. The earlier semester is supplied by an uncompleted fixed `CC0001` node; prerequisite cards do not consume elective slots.
- BDE year fit and title exclusion pass, with positive controls to avoid counting missing catalog fixtures as successful exclusions.
- `SC3060` returns as a real pass-2 interest pick with score `21` and null career evidence. Its raw Year 2 standing condition is not independently validated by the request/response checks.

Reviewed requirements use OR groups with AND members, narrow reviewed legacy pairs and conservative unresolved behavior (`SC3103` is pending approval). Current source supports these bounded course paths; it does not certify full chains, academic standing, co-requisites, cohort rules, offerings or AU capacity.

### 6.3 RAGAS evaluation layer

The explanation quality metrics (coverage, fidelity) are currently rule-based — they check whether the `expectedSkillPath` string matches exactly. Once the system generates richer natural-language explanations, RAGAS can add:

- **Faithfulness**: does the explanation only cite facts present in the student's profile and curriculum?
- **Answer relevancy**: does the explanation actually address the student's career goal?

**Deferred until:** The recommendation system has LLM-generated explanations (currently deterministic templates).

### 6.4 A/B or interleaving test

Not feasible until real NTU students use the system in production. Requires the NTU SSO authentication milestone to be complete and students consenting to logging.

### 6.5 Counterfactual sensitivity gaps

The original Cloud/Platform preference FAIL was an invalid no-op check. The guard now detects tags already selected in the input. Two current checks are inconclusive because their tags are already present in baseline output evidence; those checks do not establish sensitivity to a new signal.

Expert review should prioritize weak-fit picks and the changed selections in section 4.1. Do not classify every disagreement with owner-authored labels as a scoring bug or tune constants to recover an aggregate score.

The counterfactual script should be expanded with conflict checks (career goal vs. mismatched preferences) as new cases are added.

---

## 7. Files

| File | Purpose |
|---|---|
| `data/recommendation_benchmark_cases.json` | Benchmark cases with labelled candidates |
| `data/recommendation_benchmark_predictions.json` | Preserved historical prediction snapshot, not the current integrated capture |
| `data/review/recommendation_planning_integrity_results.json` | Persistent compact before/after evidence, metrics and capture/source hashes |
| `scripts/evaluate_recommendation_benchmark.py` | Offline evaluator — reads both files, outputs JSON metrics |
| `scripts/run_recommendation_benchmark_predictions.py` | Calls live backend and saves predictions |
| `scripts/run_counterfactual_sensitivity.py` | Counterfactual checks against live backend |
| `scripts/validate_recommendation_mappings.py` | Validates career-skill tag names against modules.json |
| `backend/services/career_skill_mappings.py` | Career-to-skill-to-tag mappings used by the recommender |
| `backend/services/recommendation_service.py` | Scoring, filtering, slot assignment, and explanation logic |
| `backend/services/prerequisite_rules.py` | Reviewed course-prerequisite groups, legacy pairs and unresolved policy |
