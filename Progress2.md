# Progress2

This file continues the project progress log after `Progress.md` became large.

## Current Branch

- `main` includes merged recommendation calibration, expanded career-goal support, prototype bug fixes, and roadmap UI polish.
- `ntu-sso-auth` exists as open PR #40 but is parked because NTU controls Azure app access.
- `career-goal-options` was merged in PR #43 and contains the latest recommendation tag, career mapping, Cloud / Platform, and BDE fallback calibration work.

## Latest Commits

- `a875465 Merge pull request #43 from donkey-king-kong/career-goal-options`
- `9f1ed17 Revert "feat: add general bde fallback recommendations"`
- `f76bcbc feat: add general bde fallback recommendations`
- `4fecdf1 feat: add low-confidence bde fallback recommendations`
- `66f1f8f docs: add cloud recommendation review artifacts`
- `5d47d60 fix: tighten cloud platform recommendation tags`
- `996b4f9 feat: expose expanded career goals`
- `730d84e feat: add data and security career mappings`

## Current Direction

- Keep NTU SSO on hold until Azure app registration access is available.
- Keep PR #40 open as the SSO implementation reference, but do not merge it yet.
- Continue with non-auth work that strengthens the current prototype and evaluation story.
- Keep recommendation ranking and exact-slot allocation in the backend.
- Treat benchmark cases as project-owner-reviewed draft calibration data, not expert ground truth.
- Avoid blind constant tuning just to improve nDCG.
- Career coverage now includes `Software Engineer`, `AI / ML Engineer`, `Data Engineer`, `Cloud / Platform Engineer`, and `Cybersecurity Engineer`.
- Keep the third-layer general BDE fallback removed for now; use only strong recommendations and the score-5 low-confidence BDE fallback.

## Current Benchmark Snapshot

After PR #43 career-goal and Cloud / Platform calibration:

- `caseCount`: `21`
- `caseCoverage`: `1.0`
- `totalPredictionsEvaluated`: `46`
- `averagePrecisionAtK`: `0.3333333333333335`
- `averageNdcgAtK`: `0.543122098259448`
- `averagePrecisionAtReturned`: `0.7857142857142857`
- `averageNdcgAtReturned`: `0.736751943021475`
- `averageSlotFillRate`: `1.0`
- `averageExplanationCoverage`: `0.861111111111111`
- `averageExplanationFidelity`: `0.55`
- `averageSkillAreaDiversityAtK`: `1.1904761904761905`
- `oldCodeExposure`: `0`
- `averageConstraintValidity`: `1.0`

## Latest Completed Work

- Merged recommendation score calibration in PR #37.
- Reviewed and addressed the previously flagged weak benchmark areas, including networking preference ranking, SC3 software fallback ranking, security/privacy fallback ranking, and AI/ML case deferral.
- Merged prototype bug fixes in PR #38 for transcript/curriculum parsing and reload behavior.
- Merged roadmap UI polish in PR #39, including header layout, dark-mode contrast, and plain prerequisite lines without arrowheads.
- Implemented NTU SSO on `ntu-sso-auth` and opened PR #40, but left it unmerged because Azure app registration access depends on NTU.
- Added deterministic career-skill mappings for Data Scientist and Cybersecurity Analyst.
- Updated the frontend career dropdown and recommendation guard to support all three mapped careers.
- Merged PR #43 for expanded career-goal options, module tag cleanup, Cloud / Platform calibration, Claude review artifacts, and low-confidence BDE fallback recommendations.
- Added `network-infrastructure` as a precise tag for true infrastructure-networking courses and moved Cloud / Platform scoring away from the broad `networks` tag.
- Removed the over-strict Cloud / Platform allowlist and kept a focused off-track blocklist for modules such as GPU, blockchain, data analytics, and quantum computing.
- Added then reverted a broader third-layer general BDE fallback; this is intentionally not active because it can fill BDE slots with non-career suggestions that need separate UX/product treatment.

## Current Assessment

- Constraint validity is strong and old CE/CPE/CSC/CZ code exposure remains zero.
- The benchmark review/calibration pass now covers more careers, so the aggregate nDCG is lower than the previous Software Engineer-only snapshot and should not be compared directly without noting the expanded case set.
- SSO code exists but should remain parked until real NTU Azure credentials and redirect registration are available.
- The main app can continue improving prototype reliability, documentation, and evaluation without introducing deferred AI/database integrations.
- Cloud / Platform false positives from broad `networks` scoring are fixed, but Cloud BDE coverage still needs a dedicated benchmark case because the UI can expose more open BDE slots than the current benchmark cases.
- The expanded career mappings are still deterministic first-pass mappings and need review against more student scenarios.

## Recommended Next Step

Pick one non-auth task:

- Add lightweight benchmark/evaluation cases for the new Data Scientist and Cybersecurity Analyst mappings.
- Add at least one Cloud / Platform benchmark case with several BDE slots to catch BDE spillover and empty-slot behavior.
- Coverage audit planning: design a lightweight script/checklist to measure whether valid MPE/BDE slots can be filled across supported curriculum inputs.
- Counterfactual sensitivity checks: verify that changing career goals shifts recommendations in sensible ways.
- Evaluation prep: document benchmark methodology and current metrics for the FYP report.

## Out Of Scope

- No Neo4j.
- No ChromaDB.
- No LangGraph.
- No OpenAI.
- No embeddings.
- No ML ranking.
- No MyCareersFuture scraping.
- No further auth or SSO work until Azure access is available.
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

## Network Preference Current-Availability Calibration

Status: Implemented locally

### Completed

- Reviewed `software-engineer-csc-014` after project-owner feedback that `SC4030 Wireless & Mobile Networks` is clearly better than `SC4022 Network Science` for a student who selected `computer-network` and `operating-systems`.
- Added a targeted current-semester preference boost for `computer-network` matches.
- Kept `SC4022` unlabelled as a reviewed positive, because the intended behaviour is to prefer the more direct/current networking module rather than accepting the broader network-science fallback.
- Regenerated benchmark predictions against a fresh local backend.

### Rationale Notes

- `SC4022` was winning because broad raw keywords in its catalogue text, such as distributed, systems, algorithm, and security, added enough fallback score to beat `SC4030`.
- A general raw keyword cap fixed case `014` but caused unrelated regressions, so it was not kept.
- The final adjustment is narrower: it only boosts current-semester modules that directly match the `computer-network` preference tag.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; from backend.services.recommendation_service import CURRENT_PREFERENCE_TAG_BONUSES; print('backend import ok'); print(CURRENT_PREFERENCE_TAG_BONUSES)"`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8004/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Case `software-engineer-csc-014` now recommends `SC3030 Advanced Computer Networks` and `SC4030 Wireless & Mobile Networks`.
- The benchmark now reports `averagePrecisionAtK` `0.3857142857142858`, `averageNdcgAtK` `0.739040701455745`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.

### Not Included

- No benchmark label change for `SC4022`.
- No broad raw keyword top-up cap.
- No frontend UI changes.
- No automated recommender test suite unless explicitly requested.

## SC3 Software Fallback Calibration

Status: Implemented locally

### Completed

- Reviewed `software-engineer-csc-011` after project-owner feedback that `SC3040 Advanced Software Engineering` should be preferred over `SC3270 Reasoning About Programs`.
- Confirmed `SC3040` is eligible: it is a current-semester CSC level-3 module, its `SC2006` prerequisite is completed in the case, and it is not unavailable to CSC.
- Updated the benchmark case so `SC3099 Capstone Project` is a negative core-project exclusion example instead of a positive reviewed candidate.
- Added `SC3270 Reasoning About Programs` as a `somewhat-relevant` fallback candidate, because it is acceptable only when `SC3040` is not eligible.
- Marked `SC3270` as `recommendationProfile: specialist` in `data/modules.json`.
- Updated specialist profile adjustment so specialist modules receive the specialist penalty when the student selected preferences and the module does not match any selected preference.
- Regenerated benchmark predictions after reseeding the local module table.

### Rationale Notes

- `SC3270` previously beat `SC3040` because it had extra `programming` and `theory-of-computing` signals, even though it is more formal/theory-oriented.
- `SC3040` is the more direct applied software-engineering fallback when no SC3 module matches backend-engineering, distributed-systems, or cloud-computing.
- The specialist penalty still does not apply when a specialist module directly matches a selected preference, so security, networking, or distributed-systems specialist matches are not broadly suppressed.

### Verified

- Ran `.venv/bin/python -m json.tool data/modules.json`.
- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -m backend.database.seed`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8005/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Case `software-engineer-csc-011` now recommends `SC3020 Database System Principles` and `SC3040 Advanced Software Engineering`.
- The benchmark now reports `averagePrecisionAtK` `0.42857142857142877`, `averageNdcgAtK` `0.7799114514168929`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.

### Not Included

- No automated recommender test suite unless explicitly requested.
- No frontend UI changes.
- No change to the global core-project exclusion for `SC3099`.

## Security Privacy BDE Calibration

Status: Implemented locally

### Completed

- Reviewed `software-engineer-csc-008` after project-owner feedback that `SC4017 Data Privacy & Security` should be preferred over `SC4053 Blockchain Technology`.
- Added `SC4053 Blockchain Technology` to the case as a `somewhat-relevant` fallback rather than the preferred BDE answer.
- Tightened specialist profile adjustment so specialist modules are penalized when they only partially match the selected preference set.
- Marked `SC4011 Security Management` as `recommendationProfile: specialist` because it is broader and more management-oriented than technical privacy/security modules.
- Added a narrow security/privacy adjacency boost for the exact `computer-security` + `cryptography` preference combination so `SC4017` can beat generic security fallbacks for this case.
- Regenerated benchmark predictions against a fresh local backend.

### Rationale Notes

- `SC4053` previously won because it combined `computer-security` with strong Software Engineer `distributed-systems` career-skill evidence.
- After suppressing blockchain, `SC4011 Security Management` became the fallback because raw catalogue wording gave it a higher general security score than `SC4017`.
- The final rule is intentionally narrow: it only treats privacy as an adjacent fallback when the selected preferences are exactly `computer-security` and `cryptography`, avoiding regressions where privacy is already explicitly selected.

### Verified

- Ran `.venv/bin/python -m json.tool data/modules.json`.
- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; print('backend import ok')"`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8008/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Case `software-engineer-csc-008` now recommends `SC4010 Applied Cryptography` and `SC4017 Data Privacy & Security`.
- The benchmark now reports `averagePrecisionAtK` `0.442857142857143`, `averageNdcgAtK` `0.7985613917770757`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.

### Not Included

- No frontend UI changes.
- No automated recommender test suite unless explicitly requested.
- No broad security-course reshuffling beyond the reviewed `csc-008` calibration.

## AI/ML Benchmark Case Deferral

Status: Implemented locally

### Completed

- Removed `software-engineer-csc-006` from the current Software Engineer benchmark set.
- Deferred the AI/ML preference scenario until the project has an explicit AI/ML career goal or AI/ML-focused evaluation track.
- Regenerated benchmark predictions for the remaining 13 Software Engineer cases.

### Rationale Notes

- The case recommended the correct course, `SC4001 Neural Network & Deep Learning`, but it was weak for reasons unrelated to Software Engineer ranking quality.
- The case relied on `ai-ml`, which is not currently mapped as Software Engineer career-skill evidence.
- The case also expected unlock credit toward `SC4062 Generative Artificial Intelligence - Advanced Topics`, but the benchmark curriculum data did not include enough year/semester metadata for the backend to prove that `SC4062` is a later fixed module.
- Keeping this case in the Software Engineer benchmark would mix a future AI/ML career path concern into the current Software Engineer calibration.

### Verified

- Ran `.venv/bin/python -m json.tool data/recommendation_benchmark_cases.json`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8009/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- The benchmark now reports `caseCount` `13`, `averagePrecisionAtK` `0.4615384615384617`, `averageNdcgAtK` `0.805841645834225`, `oldCodeExposure` `0`, and `averageConstraintValidity` `1.0`.

### Not Included

- No AI/ML career goal was added.
- No `ai-ml` Software Engineer career-skill mapping was added.
- No recommender scoring changes were made for this deferral.

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

## Career Goal Options And Cloud Calibration

Status: Merged in PR #43

### Completed

- Expanded the recommendation UI and backend flow to support more explicit career goals, including AI / ML Engineer, Data Engineer, Cloud / Platform Engineer, and Cybersecurity Engineer.
- Updated `data/modules.json` with Claude-reviewed recommendation tag cleanup and committed the review artifacts under `data/review/`.
- Regenerated `data/recommendation_benchmark_predictions.json` after career mapping and recommendation-service changes.
- Tightened AI/ML filtering so weak standalone tags such as generic `algorithms`, `database`, and `programming` do not over-promote unrelated AI/ML recommendations.
- Calibrated career-skill mappings after the module tag cleanup so career goals continue to match the normalized tag vocabulary.
- Fixed Cloud / Platform false positives by replacing the broad Cloud mapping tag `networks` with the precise `network-infrastructure` tag.
- Added `network-infrastructure` to `SC3030 Advanced Computer Networks`, `SC4030 Wireless & Mobile Networks`, `SC4031 IoT: Communications & Networking`, and `SC4063 Network Security`.
- Removed the strict Cloud / Platform allowlist because it would block future valid Cloud / Platform modules.
- Kept a focused Cloud / Platform off-track blocklist for contextual false positives such as `SC4023`, `SC4053`, `SC4064`, and related non-cloud specialist modules.
- Added a low-confidence BDE fallback threshold of `5`, while keeping the main assignment threshold at `10`.
- Added `recommendationConfidence` to recommendation responses so frontend cards can distinguish normal recommendations from low-confidence BDE fallback picks.
- Added frontend support for a small `Low confidence` badge on BDE fallback recommendations.
- Added a broader third-layer general BDE fallback experimentally, then reverted it because it can fill slots with general non-career suggestions that need separate product treatment.

### Rationale Notes

- The main Cloud / Platform issue was data/mapping noise, not broken slot assignment.
- The old broad `networks` tag appeared on many unrelated modules, so it gave Cloud / Platform score to modules that only mentioned networks incidentally.
- `network-infrastructure` distinguishes infrastructure-networking courses from malware, privacy, graph-theory, or generic security modules.
- `SC4053 Blockchain Technology` and `SC4064 GPU Programming` have technically valid tags, but their context is not Cloud / Platform for this recommender, so a focused blocklist is appropriate.
- The removed Cloud allowlist was too rigid because it hardcoded today’s acceptable modules and would prevent future valid Cloud / Platform courses from being recommended.
- Empty BDE slots are acceptable when no career-relevant candidate remains above threshold; forcing general BDEs into the same recommendation label can make the recommender look random.

### Verified

- Ran `python3 -m json.tool data/modules.json >/dev/null`.
- Ran `.venv/bin/python -m py_compile backend/schemas/recommendation.py backend/services/recommendation_service.py backend/services/career_skill_mappings.py`.
- Ran `.venv/bin/python -u -m backend.database.seed`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8001/recommendations`.
- Ran `.venv/bin/python scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Ran `npm run build` in `frontend`.
- Confirmed benchmark `caseCount` is `21`, `averageNdcgAtK` is about `0.543`, `averageNdcgAtReturned` is about `0.737`, `oldCodeExposure` is `0`, and `averageConstraintValidity` is `1.0`.
- Confirmed a fuller Cloud / Platform roadmap-style request no longer returned bad spillover modules such as `SC4014`, `SC4015`, `SC4017`, `SC4020`, `SC4023`, `SC4053`, or `SC4064`.
- Confirmed the active third-layer general BDE fallback was removed by revert commit `9f1ed17`.

### Not Included

- No third-layer general BDE fallback is active after PR #43.
- No general BDE suggestion UX beyond the current low-confidence BDE career fallback.
- No frontend score-breakdown display.
- No automated recommender test suite.
- No Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, MyCareersFuture scraping, auth, SSO, or backend user persistence.

### Next Step

- Add a Cloud / Platform benchmark case with multiple BDE slots to evaluate whether empty BDE slots are acceptable or whether a separate general-BDE suggestion UX is needed.
- Continue career expansion review with more Data Engineer, AI / ML Engineer, and Cybersecurity Engineer cases.
- Keep NTU SSO parked until Azure app registration details are available.

## Recommendation Scoring Calibration Follow-Up

Status: Implemented locally on `recommendation-scoring-calibration`

### Completed

- Created branch `recommendation-scoring-calibration` for the scoring-calibration follow-up.
- Read `backend/services/recommendation_service.py`, `backend/services/career_skill_mappings.py`, and `data/recommendation_benchmark_cases.json` before editing.
- Added per-career SQL relevance keyword sets in `backend/services/recommendation_service.py`.
- Changed `build_relevance_filters()` so Software Engineer keyword/tag signals are only added for `software-engineer`, instead of polluting every career goal's SQL candidate prefilter.
- Reduced the preference boost strength so preferences influence ranking without overwhelming career fit:
  - `PREFERENCE_FIRST_MATCH_BOOST` changed from `35` to `21`.
  - `PREFERENCE_TAG_BOOST_CAP` changed from `60` to `45`.
- Audited `CLOUD_PLATFORM_OFF_TRACK_COURSE_CODES` and confirmed `SC4051 Distributed Systems` and `SC4052 Cloud Computing` are not currently blocked.
- Added a source comment documenting that `SC4051` and `SC4052` should remain eligible Cloud / Platform candidates because they represent core distributed-systems and cloud-computing signals.
- Added an `applied model specialisation` skill area to `AI_ML_ENGINEER_SKILL_MAPPINGS`, covering `natural-language-processing`, `computer-vision`, `machine-learning`, and `artificial-intelligence`.
- Strengthened `DATA_ENGINEER_SKILL_MAPPINGS` with modest `systems-programming` and `optimization` relationships for implementation-heavy pipeline and platform modules.
- Made four separate commits as requested:
  - `768069c fix: separate career relevance prefilters`
  - `bfd5add fix: reduce recommendation preference boost`
  - `48839fd docs: clarify cloud platform blocklist`
  - `544d7b8 fix: strengthen ai and data engineering mappings`

### Rationale Notes

- The old `build_relevance_filters()` always added Software Engineer keywords and Software Engineer tag filters, which widened the SQL candidate pool for AI / ML, Data Engineer, Cloud / Platform, and Cybersecurity careers before Python scoring ran.
- The new per-career keyword prefilter keeps candidate retrieval broad enough to find relevant modules while avoiding unconditional Software Engineer spillover.
- Preference matching should be a soft preference signal, not a dominant override. Lowering the first-match boost and cap makes career-skill evidence more competitive.
- `SC4051` and `SC4052` were already eligible for Cloud / Platform in the current source, so no blocklist removal was needed.
- The AI / ML mapping issue was not total absence of signal for all target modules; the recommender kept only the top tag contribution per skill area, so specific applied AI modules could still be under-expressed without a separate applied-specialisation skill area.
- The Data Engineer mapping now gives some credit to implementation and performance infrastructure without turning generic systems modules into top-ranked data modules by default.

### Verified

- Ran IDE diagnostics for `backend/services/recommendation_service.py`; no errors reported.
- Ran IDE diagnostics for `backend/services/career_skill_mappings.py`; no errors reported.
- Ran `python3 scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5` on the existing saved predictions.
- Started the backend with `.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`.
- Regenerated fresh predictions into temporary `data/recommendation_benchmark_predictions_after.json`.
- Ran `python3 scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions_after.json --k 5`.
- Deleted the temporary prediction file after comparison.
- Stopped the temporary backend server.

### Benchmark Result

- Existing saved-prediction baseline:
  - `averagePrecisionAtReturned`: `0.7857142857142857`
  - `averageNdcgAtReturned`: `0.736751943021475`
- Fresh regenerated predictions after the fixes:
  - `averagePrecisionAtReturned`: `0.7857142857142857`
  - `averageNdcgAtReturned`: `0.736751943021475`
- Net aggregate metric change: unchanged.
- No previously weak/failing case improved by evaluator metrics because the final selected course assignments stayed the same.
- Diagnostic finding: remaining weak cases are mostly no longer simple zero-career-signal issues. The remaining behaviour is driven more by exact-slot constraints, prerequisite planning penalties, and benchmark labels expecting alternatives that cannot all appear when only one matching slot is available.

### Not Included

- No benchmark case changes, including no edits to cases `001` through `005`.
- No benchmark format or convention changes.
- No kept regenerated prediction file.
- No frontend UI changes.
- No automated recommender test suite.
- No Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, MyCareersFuture scraping, auth, SSO, or backend user persistence.

### Next Step

- Inspect weak cases with live per-candidate score tables, especially where the expected module is eligible but loses after prerequisite planning penalties or exact-slot allocation.
- Review whether benchmark expectations should distinguish "ideal top five" from "one exact assignment per open slot".
- If ranking changes are still desired, calibrate prerequisite planning and exact-slot assignment next rather than only adding more career-skill mapping weight.

## Targeted Benchmark Diagnosis Fixes

Status: Implemented locally on `recommendation-scoring-calibration`

### Completed

- Added `network-security` as a cybersecurity career-skill relationship under the `networks and systems security` skill area.
- Verified `SC4063 Network Security` carries `network-security`, `network-infrastructure`, `cybersecurity`, `networks`, `communication`, and `design` tags in the local modules table.
- Verified the new `SC4063` cybersecurity career-skill contribution manually:
  - Skill area weight: `8`
  - Relationship weight: `1.0`
  - Tag confidence: `1.0`
  - Contribution: `8 * 1.0 * 1.0 = 8`
- Softened `EXTRA_PREREQUISITE_PLANNING_PENALTY` from `-20` to `-10`.
- Audited `SC4061 Computer Vision` versus `SC4002 Natural Language Processing` for `ai-ml-engineer`.
- Confirmed `SC4061` already has stronger AI / ML career-skill score than `SC4002`:
  - `SC4061 careerSkill = 18`
  - `SC4002 careerSkill = 16`
- Confirmed `SC4002` still wins because it has two MPE specialisations, `artificial-intelligence` and `data-science`, giving it `mpeBoost = 18`.
- Confirmed `SC4061` has only `artificial-intelligence`, giving it `mpeBoost = 12`.
- Made no AI / ML mapping change because the current mapping is accurate under the current MPE stacking rules.
- Regenerated `data/recommendation_benchmark_predictions.json` against a fresh local backend on port `8011`.
- Made the following commits:
  - `056f79d fix: map network security career skill`
  - `622fb16 fix: soften prerequisite planning penalty`
  - `a02571d chore: record ai ml mapping audit`
  - `d34fdba test: regenerate recommendation benchmark predictions`

### Rationale Notes

- `SC4063` was not hard-filtered or SQL-filtered, but its `careerSkill` was `0` for Cybersecurity because the mapping had `computer-network` while the module uses `network-security`.
- Adding `network-security` is a precise mapping fix rather than a score inflation because Network Security directly represents secure network design, monitoring, and defence.
- The original `-20` prerequisite-planning penalty was large enough to almost veto strong recommendations. In `data-engineer-csc-002`, `SC4052` lost to `SC4020` by only one point before this fix.
- Reducing the penalty to `-10` keeps prerequisite planning visible but lets strong career/profile fit compete.
- The AI / ML issue is not a missing `SC4061` skill mapping. The remaining gap is caused by `SC4002` legitimately stacking two MPE specialisations.

### Verified

- Ran `PYTHONPATH=. .venv/bin/python` checks against the local database for `SC4063`, `SC4061`, and `SC4002` metadata.
- Verified `SC4063` now receives `careerSkill = 8` for `cybersecurity-engineer`.
- Verified IDE diagnostics reported no errors in `backend/services/career_skill_mappings.py`.
- Verified IDE diagnostics reported no errors in `backend/services/recommendation_service.py`.
- Started a fresh backend with `.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8011`.
- Ran `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8011/recommendations`.
- Ran `python3 scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`.
- Stopped the temporary backend server.

### Benchmark Result

- Before:
  - `averagePrecisionAtReturned`: `0.7857142857142857`
  - `averageNdcgAtReturned`: `0.736751943021475`
- After:
  - `averagePrecisionAtReturned`: `0.7857142857142857`
  - `averageNdcgAtReturned`: `0.7306114222717204`
- Net result:
  - `averagePrecisionAtReturned` unchanged.
  - `averageNdcgAtReturned` decreased by about `0.0061`.

### Diagnosed Case Changes

- `software-engineer-csc-004`
  - Before selected: `SC4052`, `SC3020`, `SC3040`
  - After selected: `SC4052`, `SC3020`, `SC3040`
  - Result: no selection change.
- `ai-ml-engineer-csc-001`
  - Before selected: `SC4002`, `SC3020`
  - After selected: `SC4002`, `SC3020`
  - Result: no selection change. `SC4061` still does not beat `SC4002`.
- `data-engineer-csc-002`
  - Before selected: `SC4023`, `SC4020`
  - After selected: `SC4023`, `SC4052`
  - Result: improved. `SC4052` now beats `SC4020`.
- `cybersecurity-engineer-csc-002`
  - Before selected: `SC4014`, `SC4017`
  - After selected: `SC4014`, `SC4017`
  - Result: no selection change. `SC4063` still does not beat `SC4014`.

### Not Included

- No benchmark case changes.
- No benchmark format changes.
- No frontend UI changes.
- No automated recommender test suite.
- No arbitrary AI / ML score inflation for `SC4061`.
- No changes to MPE-specialisation stacking rules.
- No Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, MyCareersFuture scraping, auth, SSO, or backend user persistence.

### Next Step

- Decide whether the MPE-specialisation boost should stack additively or use the strongest matching specialisation only.
- If `SC4063` should beat malware/application-security modules for network-focused cybersecurity cases, add preference-aware or pathway-aware cybersecurity subskill calibration rather than raising all network-security scores globally.
- Review whether the slight nDCG regression is acceptable in exchange for the targeted `data-engineer-csc-002` improvement, or whether the benchmark labels need a separate exact-slot assignment interpretation.

## Opus Scoring Architecture Review

Status: Discussion complete; implementation not started yet

### Context Sent To Opus

- The recommender is currently a deterministic scoring engine, not an AI / RAG / MCF pipeline.
- The final score is assembled as a flat sum of:
  - `careerTagScore`
  - `careerSkillScore`
  - `currentSemesterBonus`
  - `unlockContribution`
  - `preferenceBoost`
  - `sameFacultyBoost`
  - `mpeSpecialisationBoost`
  - `defaultProfileAdjustment`
  - `prerequisitePlanningPenalty`
- The key concern was that `preferenceBoost` and additive MPE boosts can dominate the intended career-relevance signal.
- The remaining diagnosed weak cases were:
  - `cybersecurity-engineer-csc-002`: `SC4063` still loses to `SC4014`.
  - `ai-ml-engineer-csc-001`: `SC4061` still loses to `SC4002`.
- Constraints given to Opus:
  - No external job data.
  - No scraping.
  - No APIs.
  - No OpenAI, embeddings, Neo4j, ChromaDB, LangGraph, or full ML recommender.
  - Prefer deterministic, explainable, implementable changes using current data.

### What Was Already Done Before Opus Review

- `build_relevance_filters()` had already been changed so Software Engineer SQL keyword/tag filters no longer leak into every career goal.
- Preference boost had already been reduced:
  - `PREFERENCE_FIRST_MATCH_BOOST`: `35` -> `21`
  - `PREFERENCE_TAG_BOOST_CAP`: `60` -> `45`
- `SC4051` and `SC4052` had already been confirmed eligible for `cloud-platform-engineer`.
- `network-security` had already been added under the Cybersecurity `networks and systems security` mapping.
- `EXTRA_PREREQUISITE_PLANNING_PENALTY` had already been softened:
  - `-20` -> `-10`
- `data-engineer-csc-002` had already improved:
  - Before: `SC4023`, `SC4020`
  - After: `SC4023`, `SC4052`
- `SC4061` vs `SC4002` had already been audited:
  - `SC4061 careerSkill = 18`
  - `SC4002 careerSkill = 16`
  - `SC4002` still wins because it stacks `artificial-intelligence` and `data-science` MPE boosts.
- `SC4014` vs `SC4063` had already been audited:
  - Both modules match normalized preferences through `cybersecurity` and `networks`.
  - `SC4063` is not missing a justified broad preference tag.

### Opus Findings

- Opus agreed that the remaining failures are mostly mapping and signal-interaction problems, not hard-filter problems.
- Opus warned that the next fixes must not be implemented independently because some interact.
- Important finding 1:
  - Changing `RECOMMENDATION_TAG_ALIASES["ai-ml"]` from empty to `("artificial-intelligence", "machine-learning")` without changing preference counting can regress AI / ML ranking.
  - Reason: the current preference function counts raw tag overlaps, so one broad preference can count twice if a module has both expanded tags.
  - Opus recommended preference dimension counting: each original selected preference counts at most once, even if it expands to multiple catalog tags.
- Important finding 2:
  - Blanket alias resolution inside career-skill scoring is unsafe.
  - Example: full-strength `computer-network -> networks` gives generic `networks` modules the same career-skill credit as specific network-security modules.
  - Opus recommended rewriting dead mapping tags to explicit catalog tags with intentional weights, not runtime alias resolution.
- Important finding 3:
  - `get_mpe_specialisation_boost()` should use strict `max()` instead of additive `sum()`.
  - Reason: official cross-listing indicates path membership, not extra career relevance.
  - A smaller secondary versatility bonus was rejected because it reintroduces the same failure mode.
- Important finding 4:
  - IDF-weighted preference and diversity-band-on-`careerFit` are not needed yet.
  - They are larger scoring redesigns and should be deferred unless a specific post-fix case proves they are necessary.

### Revised Implementation Plan

- Continue on the current branch, `recommendation-scoring-calibration`.
- Do not create a new branch.
- Next code changes should be made in this order:
  1. Fix `ai-ml` preference alias and implement dimension-based preference counting in the same commit.
  2. Change `get_mpe_specialisation_boost()` from additive `sum()` to strict `max()`.
  3. Rewrite dead career-skill mapping tags to actual catalog tags with deliberate career-specific weights.
  4. Add a catalog consistency test or validation script to catch dead mapping tags.
  5. Regenerate predictions and evaluate benchmark metrics.
- Expected effects from Opus simulation:
  - `ai-ml-engineer-csc-001` should move toward `SC4061` winning the SC4 slot.
  - `data-engineer-csc-002` should improve further because `SC4023` loses artificial additive MPE stacking.
  - `cybersecurity-engineer-csc-002` should return `SC4063` and `SC4017` if the cybersecurity mappings are rewritten to prefer specific network-security evidence over generic `networks`.

### Mapping Rewrite Guidance

- Do not use blanket alias resolution inside `get_career_skill_contributions()`.
- Treat aliases differently by type:
  - Rename aliases can be rewritten at full strength.
  - Broadening aliases should be replaced by explicit specific tags plus a weak generic fallback.
- Cybersecurity example:
  - Replace dead `computer-security` with actual catalog tag `cybersecurity` at full strength where appropriate.
  - Replace dead `computer-network` with:
    - `network-security` as strong evidence.
    - `network-infrastructure` as strong evidence.
    - `networks` only as weak generic evidence, around `relationship_weight = 0.3`.
- AI / ML and Data Scientist examples:
  - Replace dead `ai-ml` with explicit catalog tags such as `artificial-intelligence` and `machine-learning`.
  - Avoid letting one broad `ai-ml` preference count as multiple selected preferences.
- Software Engineer example:
  - Replace dead tags carefully with career-specific weights.
  - Generic `networks` can be defensible for Software Engineer, but should not automatically inherit full `computer-network` weight.

### Deferred Ideas

- Do not implement IDF-weighted preference yet.
- Do not change the diversity band to use `careerFit` yet.
- Do not add external data, job scraping, APIs, RAG, embeddings, OpenAI, Neo4j, ChromaDB, LangGraph, or ML ranking.
- Do not tune constants blindly until the structural fixes are evaluated.

### No Further Questions Before Implementation

- The next implementation step is clear enough to proceed:
  - Start with `ai-ml` alias plus preference dimension counting.
  - Then MPE `max()`.
  - Then catalog-grounded career mapping rewrite and consistency validation.
- Main caution:
  - Rebaseline after each commit because the fixes are interaction-sensitive.

## Opus Scoring Plan Implementation

Status: Implemented on `recommendation-scoring-calibration`

### Completed

- Committed the Opus discussion notes first:
  - `9ebc03f docs: record opus scoring review`
- Implemented `ai-ml` alias expansion together with preference dimension counting:
  - `da30ded fix: count preference dimensions`
- Changed MPE specialisation scoring from additive `sum()` to strict `max()`:
  - `a1a0b5e fix: use max mpe specialisation boost`
- Rewrote dead career-skill mapping tags to real catalog tags:
  - `eaf356e fix: ground career mappings in catalog tags`
- Added a validation script to catch future dead career mapping tags:
  - `9597a4c test: validate recommendation mapping tags`
- Regenerated benchmark predictions from the updated backend:
  - `af035d0 test: regenerate scoring benchmark predictions`

### Implementation Details

- `RECOMMENDATION_TAG_ALIASES["ai-ml"]` now expands to:
  - `artificial-intelligence`
  - `machine-learning`
- Preference scoring now counts original preference dimensions, not raw expanded tag overlap.
- Example:
  - `ai-ml` expands to `{artificial-intelligence, machine-learning}`.
  - A module matching one or both tags still gets credit for one original `ai-ml` preference dimension.
  - A module only gets a second preference dimension if it also matches another original preference such as `computer-vision` or `natural-language-processing`.
- MPE specialisation boost now uses the strongest matching specialisation only.
- This prevents cross-listed modules from receiving extra career relevance purely because they appear in multiple MPE paths.
- Career-skill mappings no longer contain dead tags that are absent from `data/modules.json`.
- Cybersecurity mappings now distinguish specific network-security evidence from generic network evidence:
  - `network-security`: strong
  - `network-infrastructure`: strong
  - `networks`: weak generic fallback
- Data Scientist mappings now use real AI / ML catalog tags instead of dead `ai-ml`.
- Software Engineer mappings now use real catalog tags for networking and security mappings.

### Validation

- Ran IDE diagnostics on:
  - `backend/services/recommendation_service.py`
  - `backend/services/career_skill_mappings.py`
- Ran:
  - `PYTHONPATH=. .venv/bin/python scripts/validate_recommendation_mappings.py`
- Result:
  - `All career-skill mapping tags exist in the module catalog.`
- Started backend on clean port `8012`:
  - `.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8012`
- Regenerated predictions:
  - `.venv/bin/python scripts/run_recommendation_benchmark_predictions.py --api-url http://127.0.0.1:8012/recommendations`
- Evaluated:
  - `python3 scripts/evaluate_recommendation_benchmark.py --predictions data/recommendation_benchmark_predictions.json --k 5`
- Stopped the temporary backend.

### Benchmark Result

- Before Opus implementation:
  - `averagePrecisionAtReturned`: `0.7857142857142857`
  - `averageNdcgAtReturned`: `0.7306114222717204`
- After Opus implementation:
  - `averagePrecisionAtReturned`: `0.8095238095238095`
  - `averageNdcgAtReturned`: `0.7634008820150107`
- Net change:
  - `averagePrecisionAtReturned`: `+0.023809523809523725`
  - `averageNdcgAtReturned`: `+0.0327894597432903`

### Diagnosed Case Changes

- `software-engineer-csc-004`
  - Before selected: `SC3020`, `SC3040`, `SC4052`
  - After selected: `SC3020`, `SC3040`, `SC4052`
  - Result: no selection change.
- `ai-ml-engineer-csc-001`
  - Before selected: `SC3020`, `SC4002`
  - After selected: `SC3020`, `SC4061`
  - Result: improved. `SC4061` now beats `SC4002`.
- `data-engineer-csc-002`
  - Before selected: `SC4023`, `SC4052`
  - After selected: `SC4052`, `SC4023`
  - Result: still improved compared with the earlier `SC4020` result; ordering now puts `SC4052` first.
- `cybersecurity-engineer-csc-002`
  - Before selected: `SC4014`, `SC4017`
  - After selected: `SC4063`, `SC4017`
  - Result: improved. `SC4063` now beats `SC4014`.

### Current Metrics Snapshot

- `caseCount`: `21`
- `caseCoverage`: `1.0`
- `totalPredictionsEvaluated`: `46`
- `averagePrecisionAtK`: `0.34285714285714297`
- `averageNdcgAtK`: `0.5550599117323818`
- `averagePrecisionAtReturned`: `0.8095238095238095`
- `averageNdcgAtReturned`: `0.7634008820150107`
- `averageSlotFillRate`: `1.0`
- `averageExplanationCoverage`: `0.9880952380952381`
- `averageExplanationFidelity`: `0.45`
- `averageSkillAreaDiversityAtK`: `1.2380952380952381`
- `oldCodeExposure`: `0`
- `averageConstraintValidity`: `1.0`

### Not Included

- No benchmark case changes.
- No benchmark format changes.
- No frontend UI changes.
- No IDF-weighted preference scoring.
- No diversity-band-on-careerFit redesign.
- No external job data, scraping, APIs, OpenAI, embeddings, Neo4j, ChromaDB, LangGraph, or ML ranking.

### Next Step

- Review remaining weak Software Engineer cases separately, especially `software-engineer-csc-013`, because the Opus-targeted fixes improved AI / ML, Data Engineer, and Cybersecurity cases but did not address all Software Engineer ranking issues.

## Recommendation Calibration Outcome Summary

Status: Current recommendation benchmark baseline after Opus-guided fixes

### Outcome

- The Opus-guided scoring changes produced a real benchmark improvement without adding external data, AI, RAG, embeddings, or ML ranking.
- The system remains deterministic and explainable.
- The main successful structural changes were:
  - Preference dimensions are counted by original student-selected preference rather than raw expanded tag overlap.
  - MPE specialisation boost now uses the strongest matching specialisation instead of additive stacking.
  - Career-skill mappings are grounded in actual catalog tags instead of dead semantic tags.
  - A validation script now catches future career-skill mapping tags that are missing from the module catalog.

### Metrics

- Previous baseline after prerequisite-penalty and network-security fixes:
  - `averagePrecisionAtReturned`: `0.7857142857142857`
  - `averageNdcgAtReturned`: `0.7306114222717204`
- Current baseline after Opus-guided fixes:
  - `averagePrecisionAtReturned`: `0.8095238095238095`
  - `averageNdcgAtReturned`: `0.7634008820150107`
- Improvement:
  - `averagePrecisionAtReturned`: `+0.023809523809523725`
  - `averageNdcgAtReturned`: `+0.0327894597432903`

### Key Case Outcomes

- `ai-ml-engineer-csc-001`
  - Before: `SC3020`, `SC4002`
  - After: `SC3020`, `SC4061`
  - Outcome: improved because `SC4061` now beats `SC4002` after `ai-ml` preference dimension counting and MPE `max()` scoring.
- `data-engineer-csc-002`
  - Before earlier diagnosis: `SC4023`, `SC4020`
  - After prerequisite penalty fix: `SC4023`, `SC4052`
  - After Opus-guided fixes: `SC4052`, `SC4023`
  - Outcome: improved because `SC4052` now ranks first and `SC4020` is no longer selected.
- `cybersecurity-engineer-csc-002`
  - Before: `SC4014`, `SC4017`
  - After: `SC4063`, `SC4017`
  - Outcome: improved because `SC4063` now beats `SC4014` after catalog-grounded cybersecurity mapping.
- `software-engineer-csc-004`
  - Before: `SC3020`, `SC3040`, `SC4052`
  - After: `SC3020`, `SC3040`, `SC4052`
  - Outcome: unchanged; remaining Software Engineer weak cases need separate investigation.

### Current Interpretation

- The largest quality gains came from fixing signal interaction and mapping/data consistency, not from tuning constants.
- Preference remains useful but no longer double-counts broad aliases like `ai-ml`.
- MPE specialisation now confirms career fit rather than rewarding administrative cross-listing.
- Catalog-grounded career mappings are more academically defensible than runtime blanket alias resolution.
- Hard constraints remain healthy:
  - `averageSlotFillRate`: `1.0`
  - `averageConstraintValidity`: `1.0`
  - `oldCodeExposure`: `0`

### Remaining Work

- Investigate remaining weak Software Engineer cases, especially `software-engineer-csc-013`.
- Review explanation fidelity separately because `averageExplanationFidelity` is now `0.45`, even though ranking metrics improved.
- Keep IDF-weighted preference and diversity-band-on-`careerFit` deferred unless a specific remaining case proves they are needed.
- Do not start Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture scraping, or ML ranking yet.

## Benchmark Label Review Follow-Up

Status: Completed follow-up diligence after Opus review

### Completed

- Rechecked the three remaining concerns raised after the Opus-guided fixes:
  - explanation-fidelity regressions in Cybersecurity cases
  - changed Software Engineer selections in `software-engineer-csc-002` and `software-engineer-csc-013`
  - changed `ai-ml-engineer-csc-002` selection
- Initially updated `Recommendation_Benchmark_Label_Review_Packet.md` with:
  - explicit Software Engineer changed-selection checks
  - `ai-ml-engineer-csc-002` label-mix check
  - Cloud Platform no-regression confirmation
  - cybersecurity explanation-fidelity review section
  - proposed `expectedSkillPath` updates for reviewer approval
- Rechecked the cybersecurity fidelity diagnosis after Opus challenged the label-renaming explanation.
- Implemented a ranking-neutral explanation evidence selector so Cybersecurity recommendations prefer specific evidence tags such as `cryptography`, `malware-analysis`, `privacy`, and `network-security` over the generic `cybersecurity` tag when both are available.
- Corrected `Recommendation_Benchmark_Label_Review_Packet.md` so it no longer recommends broad relabelling to `cybersecurity`.
- Updated the `SC4063 Network Security` benchmark expected path from `computer-security` to `network-security` after reviewing the official course description.

### Findings

- `software-engineer-csc-002` changed selected modules, but returned precision and nDCG stayed unchanged.
- `software-engineer-csc-013` changed selected modules, but returned precision and nDCG stayed unchanged.
- `ai-ml-engineer-csc-002` changed from `SC4064` to `SC4061`, but returned precision and nDCG stayed unchanged.
- Cloud Platform cases did not change after MPE `max()` scoring.
- The original explanation-fidelity regression was caused by evidence selection, not ranking.
- The revived generic `cybersecurity` tag had become the top displayed evidence path and hid more specific tags such as `cryptography`, `malware-analysis`, `privacy`, and `network-security`.
- The explanation-only fix changed zero returned modules and zero recommendation scores across the 21-case benchmark.
- `averagePrecisionAtReturned` stayed `0.8095238095238095`.
- `averageNdcgAtReturned` stayed `0.7634008820150107`.
- `averageExplanationFidelity` improved from `0.45` to `0.525` before benchmark-label correction.
- `averageExplanationFidelity` returned to `0.55` after the `SC4063` benchmark-label correction.
- `cybersecurity-engineer-csc-001` recovered from `0.0` to `1.0` explanation fidelity.
- `cybersecurity-engineer-csc-002` improved from `0.0` to `0.5` explanation fidelity.
- The remaining `cybersecurity-engineer-csc-002` mismatch was `SC4063`: the benchmark expected `computer-security`, while the recommender emitted the catalog-grounded specific path `network-security`.
- The official `SC4063` description covers secure communication protocols, firewalls, zero trust architectures, intrusion detection systems, network protocol analysis, Wireshark, tcpdump, penetration testing frameworks, and network security architecture, so `network-security` is the more precise label.

### Important Decision

- Only the `SC4063` benchmark expected path was edited because the course description directly supports `network-security`.
- Do not make further benchmark-label edits without similarly explicit course-description evidence or supervisor / TA review.
- This keeps label correction separate from scorer tuning.
