# Weak-Fit Policy Comparison

Date: 2026-11-03. This is a controlled comparison against the [unchanged baseline](Recommendation_Baseline_Review_2026-11-03.md), not independent expert validation or proof of registration eligibility. The implementation was run from an owned non-reloading FastAPI process on `127.0.0.1:8016` at base revision `bc51115406ad6ae249d0b601ac56122e0bd90a91` with uncommitted policy changes; `servingRevision` in the captures is operator-declared, not a hash of the dirty worktree. The read-only repeatable-read local PostgreSQL row fingerprint before and after was `c443b5b0dbb72f014be71ba8780be963cbf09bb23a774b312859a4c1166faf8d`. Capture provenance includes local source-file hashes. No catalog, mapping, benchmark input, label, historical prediction, or evaluator was changed.

## Policy and outcomes

Pass 1 now requires at least one mapped career skill area with weight >= 6, relationship weight >= 0.75, and tag confidence >= 0.85. This is a **provisional evidence boundary**, not a calibrated universal strength threshold: structural/faculty/semester bonuses cannot satisfy it. Existing slot, exclusion, readiness, and score rules still apply. Pass 2 retains the existing explicit-interest matching and eligibility checks for unfilled slots. The backend returns `openChoiceSlots` with `no-supported-match` if neither pass assigns a slot, or `limit-reached` when the caller's result budget is exhausted. The roadmap labels backend interest picks and displays backend open-slot explanations.

| Comparison | Baseline | Policy run |
| --- | --- | --- |
| Frozen 24-case benchmark | 53 picks; nDCG@returned 0.7413; precision@returned 0.7778; 0 supplementary violations | Same totals and metrics; 0 violations; no open slots |
| Changed benchmark picks | `ai-ml-engineer-csc-001` assigns `SC3020` (indirect database relationship 0.3, career skill score 2) to `y3-s2-mpe1` | Same slot assigns `SC3021` (data-science relationship 0.75, confidence 0.9, skill-area weight 7, career skill score 5); the owner previously reviewed it as strong in this profile |
| Historical 180-cell grid | 180 filled; 18 diagnostic weak-fit cells; 0 contract violations | 180 filled; 0 diagnostic weak-fit cells; 0 interest picks, open slots, or violations |
| Positioned scenarios | 8 pass / 1 inconclusive | 8 pass / 1 inconclusive; 0 violations |
| Counterfactuals | 6 pass / 2 inconclusive | 6 pass / 1 inconclusive / **1 fail**; 0 supplementary violations |
| Separate reviewed pair after additionally completing `SC3021` | `SC3020` career pick both without interest and with HCI interest | No-interest: `SC3xxx` open with `no-supported-match`; HCI interest: `SC3061` as `interest`, readiness `ready` |

The failing counterfactual is `ai-ml-engineer-csc-001` plus a `database` preference. Its old expectation is a changed set or visible database keyword. The new career-first pass excludes the indirect `SC3020` and retains the two strong career picks `SC3021` and `SC4061`, so the preference cannot displace them. This is a **real failed existing sensitivity check**, not a passing invariant or a reason to relabel the check. The separate Software Engineer security preference check remains inconclusive. Review the test expectation against the approved career-first priority in a later evaluation work unit; do not tune the boundary to force a pass.

The only new open slot in these captures is the previously reviewed synthetic `remaining-ai-y4-no-interest` case. Its full CSC level-3 frontier, exclusions, and missing data/standing limitations are documented in the [remaining-slot review](Recommendation_Remaining_Slot_Review_2026-11-03.md). The paired HCI alternative matches the explicit interest and exact slot under the backend's supported prerequisite rules. Neither result verifies completed AU, cohort permission, offering, co-requisites, capacity, or actual registration. The older neural-network/computer-network and secure-software evidence concerns remain; zero diagnostic weak-fit grid cells does not prove every selected course is a strong content match.

## Reproduction

Full request/response captures, runner provenance, benchmark evaluation, grid, positioned checks, and counterfactual results are saved under `data/review/weak_fit_policy_2026-11-03/`. The frozen input SHA-256 is `41dd39fd9c84b4ebdab56c749fb032e714c35e297e2e4affd77a1824b929eb3a`. With the same database and an owned backend serving this policy, rerun the existing scripts into **new** paths using `--api-url`, `--serving-revision`, and `--database-fingerprint` as in the [baseline reproduction commands](Recommendation_Baseline_Review_2026-11-03.md#provenance-and-reproduction). Evaluate with `--k 5 --fail-on-contract-violations`; the counterfactual runner exits 1 for the documented failure.

Next review: obtain supervisor/TA feedback on disputed course mappings and provisional evidence strength, and separate the counterfactual's old preference expectation from the career-first product rule. Do not infer expert-reviewed quality or full academic eligibility from unchanged frozen metrics.
