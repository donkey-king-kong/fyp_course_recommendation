# Step 1 Remaining-Slot Control Review

Date: 2026-11-03. Scope: reviewed synthetic AI/ML `SC3xxx` examples **without** a strong remaining career match on the current CSC level-3 catalog, subject to the limitations below. This is a proposed future interest/open-slot decision, **not** an observed abstention, an expert benchmark label, proof of live registration, or an implemented policy. Compare the [frozen baseline](Recommendation_Baseline_Review_2026-11-03.md) and [previous full-catalog controls](Recommendation_Boundary_Controls_2026-11-03.md).

## Exact inputs and provenance

The [two separate cases](../../data/review/remaining_slot_controls_2026-11-03.json) copy the prior AI/ML Y4-end completed-course/curriculum/slot input and additionally mark `SC3021` Data Science Fundamentals as completed and present in the synthetic curriculum. The owner previously judged `SC3021` a strong AI/ML course **before** this hypothetical completion. The two new cases differ **only** by an explicit `human-computer-interaction` interest. Neither adds exclusions beyond the fixed curriculum; the open `SC3xxx` slot has no year/semester metadata, and no transcript AU or registration evidence is provided. They do **not** alter the frozen 24-case benchmark, its labels, or historical predictions.

The [full live-backend requests and responses](../../data/review/remaining_slot_2026-11-03/responses.json) were captured by the existing benchmark prediction runner from an owned, non-reloading `backend.main:app` process on `127.0.0.1:8013` (PID 60129 at capture). Its `/health` returned `{"status":"ok"}`. Source revision at launch: `104dc4952060954fb7c0b9d6d2e65e67ad46e577`; runner `servingRevision` is operator-declared, and `localCaptureWorktreeDirty=true` reflects the new uncommitted scenario input. The source-file SHA-256 set in the capture matches the original frozen baseline. The local PostgreSQL fingerprint from read-only repeatable-read snapshots **before and after capture** was `c443b5b0dbb72f014be71ba8780be963cbf09bb23a774b312859a4c1166faf8d` (4,318 modules; 4,178 prerequisite rows; 34 faculties), also matching the baseline. This is local provenance, not independent attestation of a remote backend or a timetable.

Input SHA-256: `de465b8804d58f44ad65b73151993ea574565ea69fe7c056bec0d224355724e1`. Response SHA-256: `4e65811bfbb7b9eff55d99e842528b7ce247c43ce2ad230fd8ca75093df82bb9`. Frozen benchmark input and historical prediction hashes are still `41dd39fd9c84b4ebdab56c749fb032e714c35e297e2e4affd77a1824b929eb3a` and `0716130f7e8df95f95d2bfb25df90fb0efd1fb905c34598c644fc4ed562dbf1b`. Request pairs differ only by interest, source hashes match baseline, and the response's nested and top-level recommendation copies match.

Reproduce with the same configured database, after verifying the fingerprint and serving revision. Run the backend in a separate terminal and capture to a **new** output path (timestamps will differ):

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8013
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/run_recommendation_benchmark_predictions.py --benchmark data/review/remaining_slot_controls_2026-11-03.json --api-url http://127.0.0.1:8013/recommendations --output /private/tmp/remaining-slot-recapture.json --serving-revision 104dc4952060954fb7c0b9d6d2e65e67ad46e577 --database-fingerprint c443b5b0dbb72f014be71ba8780be963cbf09bb23a774b312859a4c1166faf8d
shasum -a 256 data/review/remaining_slot_controls_2026-11-03.json data/review/remaining_slot_2026-11-03/responses.json
```

Both captured responses pass the existing `validate_response(request, response)` checks with **zero** violations. That contract does not check relevance, absence of omitted candidates, standing, course offering, co-requisites, AU capacity or real registration permission.

## Candidate frontier and course evidence

Using the backend's own `build_relevance_filters`, code/programme/fixed-course filters, `score_career_match`, specialisation/weak-signal rules, `get_matching_choice_slots` and `evaluate_recommendation_readiness` against the same DB/request: **26** CSC level-3 modules exist; **14** enter career retrieval. The disposition of those 14 under current rules is:

| Count | Courses | Why they do not establish a strong remaining AI/ML course |
| --- | --- | --- |
| 3 | `SC3000` Artificial Intelligence, `SC3010` Computer Security, `SC3021` Data Science Fundamentals | Already completed or fixed in this hypothetical profile. `SC3000` and owner-approved strong `SC3021` are not available to recommend again. |
| 4 | `CE3102`, `CSC301`, `CSC304`, `CZ3005` | Legacy/hard-excluded course-code prefixes. `CSC304` and `CZ3005` would have direct AI tags, but cannot be rescued by relevance scoring. |
| 1 | `SC3099` Capstone Project | Hard-excluded core project. |
| 1 | `SC3102` Signals, Systems & Transforms | Programme restriction includes CSC. |
| 2 | `SC3103` Embedded Programming, `SC3270` Reasoning About Programs | The existing weak-specialisation rule rejects their generic programming signal without a matching preference. Course descriptions concern embedded OS or programming-language proofs, not applied AI modelling for this student. |
| 1 | `SC3271` Logic, Proof, and the Foundations of Calculus | **Retrieved** by its description mentioning machine learning but then rejected for zero career signals because its recommendation tags are empty. Its content is genuinely useful mathematical preparation. The owner judges it an **optional foundation**, not a strong default for this applied AI/ML student with prior maths, AI, ML and NLP. Missing scored content is a separate tag/mapping coverage question, not permission to change data for this review. |
| 2 | `SC3020` Database System Principles, `SC3060` Computer Graphics & Visualisation | Both return `ready` under supported code rules, with career-skill scores **2** and **3**. `SC3020` teaches DBMS design and links only indirectly to training-data workflows; `SC3060` teaches geometry/rendering, not computer vision model learning, and its generic mathematics tag provides incidental AI credit. Neither is a strong default AI/ML course by content. `SC3060`'s catalog Year 2 standing is **not** verified by recommender readiness. |

The other **12** CSC level-3 modules are outside the current career-relevance retrieval (including `SC3061` Human Computer Interaction); their descriptions and slot eligibility were checked for hidden direct applied-AI content. `SC3061` instead provides the explicit-interest alternative. This frontier is **not** a proof about other curriculum slot types, future catalog changes, cohort permissions, actual course availability, or a real transcript. A missing course signal can conceal a valuable optional course; inspect such discrepancies separately before changing mapping data.

`SC3061` teaches usability, UI development and interaction design, directly matching `human-computer-interaction` rather than the AI/ML goal. It is not in the completed list, is CSC level 3, and has no stored code prerequisite or catalog standing requirement. The exact-slot/readiness functions report `ready`. Calling the existing `fill_interest_slots` function **in isolation with the HCI request and an unfilled slot** returns `SC3061` with `recommendationSource=interest`, preference 21, career skill 0, and the same slot ID. This checks an available supported pass-2 path, **not** an end-to-end result from the unchanged policy or proof of live registration.

## Current behavior and proposed outcome

| Case | Unchanged captured response | Reviewed outcome *if* eligibility and catalog are confirmed |
| --- | --- | --- |
| `remaining-ai-y4-no-interest` | `SC3020`, `career`, score 19: career skill 2, career tag 0, faculty 8, specialisation 6, current flag 3; `ready`. | **Open `SC3xxx` slot**, explaining that direct AI study is completed and no strong eligible career match was found in this audited frontier; do not invent an interest. |
| `remaining-ai-y4-hci-interest` | Same `SC3020`, `career`, score 19, no interest boost; `ready`. | **Interest alternative `SC3061`**, clearly labelled as HCI rather than AI/ML, after the same eligibility and prior-learning checks. If registration/slot rules disallow it, leave the slot open with the specific limitation instead. |

These are **reviewed expected outcomes**, not observed pass/fail policy results. Scores 2/3 are evidence diagnostics, **not** approved universal thresholds. The current system still fills both slots; do not alter the catalog, ranking, threshold, labels or evaluator to make the capture pass. In particular, do not treat a score of 19 or a faculty/specialisation bonus as sufficient career fit. The backend would have to recalculate selection in a *separate* implementation work unit; the frontend should render its result, not pick a course itself.

Remaining distinct gaps: transcript-derived completed AU, standing, exact programme/cohort/semester permission, co-requisites and capacity cannot be established from these browser-controlled requests. `SC3271`'s description-versus-tags disagreement and `SC3060`'s `ready`-despite-standing issue are data/eligibility findings, not weak-fit threshold fixes. Expert review of course-content judgments is still advisable. Stop before policy implementation; later compare every new open slot against the frozen 24 cases, 180-cell coverage grid, positioned scenarios and counterfactual checks. Do not edit the frozen cases 001-005.
