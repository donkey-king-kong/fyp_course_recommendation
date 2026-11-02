# Evaluation Methodology and Results

This document describes how the recommendation system is evaluated offline, the current benchmark metrics, and the known limitations of the approach. It is the primary source for the FYP report's evaluation chapter.

---

## 1. Purpose and Scope

The evaluation covers the deterministic recommendation engine only — the backend-side module ranking, slot assignment, and explanation generation. It does not cover the transcript parser, curriculum guide parser, or any frontend behaviour.

**What the evaluation measures:**
- Whether the top-ranked modules match modules that a reviewer would consider appropriate for the student's career goal and preferences.
- Whether hard constraints are always obeyed (no completed modules, no deprecated codes, correct slot types).
- Whether the explanation references the correct career–skill path.
- Whether recommendations shift in the expected direction when inputs change (counterfactual sensitivity).

**What the evaluation does not measure:**
- Real student satisfaction or acceptance rates (no live user study yet).
- Expert-level ground truth — labels are project-owner-reviewed drafts, not adviser or TA verified.
- Whether the scoring weights are globally optimal.

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

Number of distinct `skillArea` values in the top-k predictions' career skill evidence. Higher is better because it means the student receives modules from different skill areas of their career rather than all from one.

### 3.8 oldCodeExposure

Count of predictions in top-k whose course code starts with `CE`, `CPE`, `CSC`, or `CZ`. Must always be 0. Any value above 0 is a hard failure.

### 3.9 constraintValidity

Fraction of top-k predictions that satisfy all hard constraints simultaneously: non-empty code, not an old code, not in `completedCourseCodes`, not in `curriculumCourses`, and slot type matches. Should always be 1.0.

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
| After career-first preference policy | 24 | 0.631 | 0.639 | 1.0 | 0 | Preference boost now scaled by career fit (`CAREER_FIT_FULL_PREFERENCE_SCORE = 15`); pass-2 interest picks added for unfilled slots; metrics dropped from the 24-case baseline (0.683→0.631 nDCG, 0.694→0.639 precision) because career-first scaling depresses preference boosts for modules with weak career signal, which pushes some previously passing modules down; 8 counterfactual checks (6 PASS, 1 INCONCLUSIVE, 1 new career-conflict PASS) |

**Note on comparing rows:** When case count increases, nDCG and precision aggregate over more cases. A drop in the average does not necessarily mean ranking quality degraded — it may reflect new cases where the system performs worse for previously untested scenarios. Use per-case breakdowns (`scripts/evaluate_recommendation_benchmark.py` output) to diagnose regressions.

---

## 5. Counterfactual Sensitivity Results

Script: `scripts/run_counterfactual_sensitivity.py`

Run with:
```bash
PYTHONPATH=. .venv/bin/python scripts/run_counterfactual_sensitivity.py --api-url http://127.0.0.1:8001/recommendations
```

Results from the `coverage-audit` branch (8 checks):

| Check | Result | Notes |
|---|---|---|
| Career swap: software-engineer-csc-007 → data-scientist | PASS | Recommendation set changed; `data-scientist` careerGoal appeared in score evidence |
| Career swap: software-engineer-csc-007 → cybersecurity-engineer | PASS | Recommendation set changed; `cybersecurity-engineer` careerGoal appeared in score evidence |
| Preference swap: software-engineer-csc-009 + `computer-security` | PASS | `cybersecurity` (alias for `computer-security`) appeared in matchedKeywords but not in baseline |
| Preference swap: ai-ml-engineer-csc-001 + `database` | INCONCLUSIVE | `database` was already in the baseline matchedKeywords (SC3020 via `skill:model implementation foundations:database`); adding the tag produced no new signal. See note below. |
| Career conflict: ai-ml-engineer-csc-001 career=ai-ml-engineer vs SWE prefs | PASS | All career picks retained `careerSkillEvidence.careerGoal == ai-ml-engineer` despite conflicting preferences |
| Completion change: software-engineer-csc-001 | PASS | Top module removed; slot still filled |
| Completion change: data-scientist-csc-001 | PASS | Top module removed; slot still filled |
| Completion change: cybersecurity-engineer-csc-001 | PASS | Top module removed; slot still filled |

**INCONCLUSIVE defined:** A check returns INCONCLUSIVE when the input change caused no observable difference in recommendations. It is not a failure — it documents a known property. Under the career-first policy, a preference tag only surfaces when a career-mapped, eligible module carries that tag and was not already recommended. If the module was already the top pick, the tag appears in both baseline and swap, so no new signal is produced.

**Preference-swap INCONCLUSIVE — documented property of career-first:** The `ai-ml-001 + database` swap is INCONCLUSIVE because SC3020 scores well enough on career signal alone to be the top pick regardless of the `database` preference. Four other tags were probed before settling on this check; all failed to trigger a genuine change because career-first suppresses off-career preferences before they can shift rankings: DS-001 + computer-network (career blocks it), DS-001 + computer-vision (no eligible CV module at SC3/4 level), DE-001 + cloud-computing (SC4052 prereq MH2802 is not CSC faculty), SE-011 + NLP (no eligible NLP module with SC4xxx slot fit). This is accurate behaviour, not a scoring bug — it confirms career-first is working. A genuine preference-swap PASS requires a case where the student's preferred tag introduces a module they would not otherwise see.

**Earlier correction (cloud-platform + computer-network):** The original `cloud-platform-engineer-csc-001 + computer-network` check was a no-op. That benchmark case already listed `computer-network` in its `preferredRecommendationTags`, so adding it again produced no change. The FAIL result was invalid. The guard in `run_preference_swap_check` now fails immediately if the added tag is already in the base case, preventing this class of mistake in future runs. A separate baseline comparison was added to detect the INCONCLUSIVE case.

**Residual benchmark weakness — cloud-001 SC3xxx slot:**
In `cloud-platform-engineer-csc-001`, `SC3030 Advanced Computer Networks` is labelled `highly-relevant` for the SC3xxx slot but the system assigns `SC3050 Advanced Computer Architecture` instead. The cause is that `SC3050` scores higher through same-faculty, MPE specialisation, and systems/cloud-computing tag boosts. The label may be over-optimistic, or the scoring weights need re-calibration. Recorded for review on the `career-first-preference-policy` branch.

---

## 6. Known Weaknesses and Future Work

### 6.1 Label quality

All labels are owner-reviewed drafts. Until a lecturer, TA, or senior student performs an independent review, precision and nDCG scores reflect alignment with the owner's own judgement.

**Planned:** Expert review or think-aloud session with a supervisor or senior student to validate a subset of labels. This is the single most credible evaluation improvement for the FYP report.

### 6.2 Coverage audit

Script: `scripts/run_coverage_audit.py`. Run with:
```bash
PYTHONPATH=. .venv/bin/python scripts/run_coverage_audit.py --api-url http://127.0.0.1:8001/recommendations --output data/coverage_audit_results.json
```

**Grid:** 6 careers × 5 slot configurations × 2 progress stages × 3 preference modes = 180 cells.
- Slot configs: `SC3xxx-only`, `SC4xxx-only`, `SC3-and-SC4`, `SC4-BDE-BDE`, `BDE-only`.
- Progress stages: Y2-end (15 modules completed) and Y4-end (35 modules completed).
- Preference modes: none, career-aligned, and career-conflicting.
- Faculty: CSC only (non-CSC is a known limitation, not covered by this audit).

**Results (re-run 2026-11-03 after request-shape fix):**
- Invariant violations: **0** across all 180 cells.
- Pass-2 interest picks: **0 fired** — all assigned slots were filled by career picks.
- Overall slot fill rate: **100%** across all 180 cells. No empty slot findings.

**Weak-fit picks (filled but low career signal):**

The audit flags picks where `careerSkillScore < 5` and `careerTagScore == 0` — slots that are filled but only on faculty or structural signal rather than direct career relevance. Three distinct module codes appear across 26 cells:

| Module | Career | Slot config | Progress | Why weak |
|---|---|---|---|---|
| `SC3040 Advanced Software Engineering` | cybersecurity-engineer | SC3xxx-only | Y4-end | SC3010 (the only cyber-tagged SC3xxx module) is already completed; SC3040 fills via faculty boost, no direct cyber tag |
| `SC3050 Advanced Computer Architecture` | cloud-platform-engineer | SC3xxx-only | Y2/Y4-end | Fills on faculty + systems tag; cloud-computing tag is not present at SC3 level |
| `SC3020 Database Management Systems` | ai-ml-engineer | SC3xxx-only | Y4-end | Strong data tag but no direct AI/ML career-tag match at SC3 level after SC3 AI modules are completed |

These are quality observations, not invariant failures. The system fills the slot rather than leaving it empty, which is the correct behaviour. Whether these picks should be labelled `low-confidence` or suppressed in favour of an explicit "no strong match" message is a product decision for a later milestone.

**Correction note:** The first run of this audit (merged in PR #50, 2026-11-03) reported a false cybersecurity SC3xxx gap at Y4-end. The root cause was a bug in `build_request()`: it sent `majorCode` and `year` (not recognised API fields) and omitted `studentFaculty`. Without `studentFaculty: "CSC"`, the CSC faculty bonus (+8 points) was absent, dropping SC3040's score below the MPE minimum threshold of 10. With the correct request shape, SC3040 scores 15 and fills the slot. The bug affected all 180 cells — the first run's "100% fill rate in 174 cells" was also measured on unrealistic requests without faculty context.

### 6.3 RAGAS evaluation layer

The explanation quality metrics (coverage, fidelity) are currently rule-based — they check whether the `expectedSkillPath` string matches exactly. Once the system generates richer natural-language explanations, RAGAS can add:
- **Faithfulness**: does the explanation only cite facts present in the student's profile and curriculum?
- **Answer relevancy**: does the explanation actually address the student's career goal?

**Deferred until:** The recommendation system has LLM-generated explanations (currently deterministic templates).

### 6.4 A/B or interleaving test

Not feasible until real NTU students use the system in production. Requires the NTU SSO authentication milestone to be complete and students consenting to logging.

### 6.5 Counterfactual sensitivity gaps

No confirmed gaps after the `counterfactual-sensitivity-checks` branch correction. The original recorded finding (cloud-platform + `computer-network`) was an invalid check — the base case already had that tag, so no real swap occurred. The guard in `run_preference_swap_check` now catches this class of mistake automatically.

A residual benchmark weakness exists: `SC3030 Advanced Computer Networks` loses the SC3xxx slot in `cloud-platform-engineer-csc-001` to `SC3050 Advanced Computer Architecture`, even though the case carries `computer-network` as a preference. This is a scoring calibration issue, not a sensitivity failure. It is being investigated on the `career-first-preference-policy` branch.

The counterfactual script should be expanded with conflict checks (career goal vs. mismatched preferences) as new cases are added.

---

## 7. Files

| File | Purpose |
|---|---|
| `data/recommendation_benchmark_cases.json` | Benchmark cases with labelled candidates |
| `data/recommendation_benchmark_predictions.json` | Saved live predictions from the most recent benchmark run |
| `scripts/evaluate_recommendation_benchmark.py` | Offline evaluator — reads both files, outputs JSON metrics |
| `scripts/run_recommendation_benchmark_predictions.py` | Calls live backend and saves predictions |
| `scripts/run_counterfactual_sensitivity.py` | Counterfactual checks against live backend |
| `scripts/validate_recommendation_mappings.py` | Validates career-skill tag names against modules.json |
| `backend/services/career_skill_mappings.py` | Career-to-skill-to-tag mappings used by the recommender |
| `backend/services/recommendation_service.py` | Scoring, filtering, slot assignment, and explanation logic |
