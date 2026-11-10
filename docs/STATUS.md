# Current Project Status

Last updated: 2026-11-10. This is the session handoff; detailed history is in the [progress index](progress/README.md). Check Git for the current branch and working tree.

## What Works

- One FastAPI backend with router, schema, service, and data-access layers; PostgreSQL module catalog and faculty controls.
- React / TypeScript frontend with profile setup, uploaded curriculum roadmap, transcript extraction and matching, roadmap readiness, and exact-slot recommendations.
- Uploaded curriculum defines the student's roadmap; transcript completions are stored and matched separately. Without a curriculum guide, the roadmap shows an empty state.
- Deterministic backend scoring for six career goals: Software Engineer, AI/ML Engineer, Data Engineer, Cloud/Platform Engineer, Cybersecurity Engineer, and Data Scientist.
- Two-pass assignment: mapped-evidence career recommendations first, then explicit-interest picks for remaining slots. Unassigned slots receive backend explanations and interest picks are labelled in the roadmap. Reviewed prerequisite rules and earlier planning nodes enforce the supported response contract.
- Existing offline benchmark, coverage audit, and counterfactual scripts record ranking, fill, and contract results. User state remains browser-side prototype persistence.
- A small backend-only `POST /student-skills/preview` maps selected completed and candidate courses to six pilot skill IDs for Software Engineer (four applicable to Data Engineer). It labels course-content exposure, not mastery, and leaves role-unmapped courses unknown. It does not affect recommendation ranking.

## Latest Evidence And Its Limits

The latest Cloud career-tag correction removed unsupported `backend-engineering` evidence from `SC4052` in the seed JSON and local database. The recorded 24-case follow-up reports nDCG@returned `0.7413`, precision@returned `0.7778`, full slot fill, and zero supplementary contract violations across 53 recommendations. The 180-cell grid records no empty slots or contract violations and 18 weak-fit cells. Positioned scenarios record 8 PASS / 1 INCONCLUSIVE; counterfactual checks record 6 PASS / 2 INCONCLUSIVE, with no failures.

An unchanged fresh baseline captured on 2026-11-03 against an owned backend and fingerprinted local database reproduced 24 cases / 53 recommendations, nDCG@returned `0.7413`, precision@returned `0.7778`, fill `1.0`, and zero supplementary violations. The 180-cell grid again found 18 weak-fit cells and no empty slots; positioned checks were 8 PASS / 1 INCONCLUSIVE and counterfactual checks 6 PASS / 2 INCONCLUSIVE. The [baseline and seven-case review packet](evaluation/Recommendation_Baseline_Review_2026-11-03.md) contains full traceability, discrepancies, and pending decisions. Historical prediction files remain separate snapshots. Draft explanation-path fidelity is `0.5`; full academic eligibility and expert validation remain unestablished.

The [Step 1 boundary review](evaluation/Recommendation_Boundary_Review_2026-11-03.md) proposes a qualitative course-evidence rule, **not** an implemented or calibrated threshold. The separate [full-catalog controls](evaluation/Recommendation_Boundary_Controls_2026-11-03.md) reproduce weak first picks in Cloud/Platform and AI/ML interest pairs, but reveal better-supported career alternatives behind them: `SC3030` Advanced Computer Networks and `SC3021` Data Science Fundamentals. The owner confirmed `SC3050` is not a strong default Cloud/Platform match and **`SC3021` is a strong AI/ML match** for the reviewed student despite completed AI coursework. Neither profile qualifies as a no-strong-career interest fallback or an open slot. A valid full-catalog interest fallback and verified relevance-based open-slot result are still missing. The graphics fixture returns `ready` without evidence for its catalog Year 2 standing requirement; eligibility must be checked separately.

The [remaining-slot review](evaluation/Recommendation_Remaining_Slot_Review_2026-11-03.md) adds a *separate synthetic completion* of `SC3021` to the AI/ML Y4-end profile and audits all 26 CSC level-3 modules. No strong career course remains in that reviewed local frontier: the unchanged backend still selects indirect `SC3020` both without interest and with an HCI interest; the existing interest pass alone can select `SC3061` if the slot is open. Proposed outcomes are an explained open slot or a labelled HCI alternative, respectively, **not** observed endpoint results. The owner judged `SC3271` an optional mathematical foundation, not a strong default here; its description reaches retrieval but its empty tags yield zero score. Real transcript AU, cohort and registration eligibility remain unverified.

The [weak-fit policy comparison](evaluation/Recommendation_Weak_Fit_Policy_2026-11-03.md) records the new policy endpoint run on the same local database. The frozen 24-case results retain 53 picks, nDCG@returned `0.7413`, precision@returned `0.7778`, and zero contract violations; the one changed pick is owner-reviewed `SC3021` instead of indirect `SC3020` for AI/ML. The 180-cell grid has no open slots or diagnostic weak-fit picks. The separate remaining-slot pair now produces an explained open slot without interest or labelled `SC3061` with HCI interest. Counterfactual results are **6 pass / 1 inconclusive / 1 fail**: the database-preference check expects an observable change even though career-first now preserves the stronger picks. This failure is recorded, not tuned away. The numeric mapped-evidence rule is provisional and still needs expert review; these captures do not establish registration eligibility.

The owner accepted the career-first behavior with that failure retained historically; [PR #56](https://github.com/donkey-king-kong/fyp_course_recommendation/pull/56) merged the policy into `main`. The separate [preference-check review](evaluation/Recommendation_Preference_Check_Review_2026-11-03.md) preserves those historical responses and results. A fresh run with revised interpretation gives **7 pass / 1 inconclusive / 0 fail** on exactly the same 15 request/response pairs: the SWE swap actually changes picks, while the AI/ML database swap remains inconclusive rather than passing. An opt-in HCI open-slot control gives **8 pass / 1 inconclusive / 0 fail** with two more saved-response-matched captures; it demonstrates one conditional interest path, not general preference usefulness, registration eligibility, resolution of `SC4022`'s disputed security credit, or validation of the provisional career-strength boundary.

The [pilot course-skill ledger](../data/student_skill_evidence.json) covers seven courses and nine evidence links with exact catalog excerpts and [second-pass depth judgments](evaluation/Student_Skills_Pilot_Review_2026-11-03.md). A [saved-response coverage audit](evaluation/Student_Skills_Coverage_2026-11-03.md) finds 23/35 selected-course occurrences mapped across 15 pilot cases after adding a narrow `SC4052` cloud-platform link; 12 remain unknown and three SWE cases have no mapped selection. Coverage is not selection quality. This narrow skills preview has no job evidence, skill-mastery inference, or ranking effect; real student completions remain user-controlled prototype input.

See the [latest previous progress entry](progress/Progress2.md#cloud-career-tag-correction-and-deferred-interest-ranking-review), [evaluation](evaluation/Evaluation.md), and [technical audit](evaluation/Recommendation_Technical_Audit.md) for provenance and limitations.

## Next Priorities

1. Define and separately evaluate any bounded prior-learning ranking change for the **Software Engineer and Data Engineer pilot**. The source-based second pass was the author's review, not independent supervisor/TA validation. Keep unknown coverage explicit, use transcript-derived completions as likely exposure rather than mastery, and compare against the frozen all-six-career benchmark. The preview is a foundation, not a complete skills-gap recommender.
2. Obtain expert input on the provisional career-strength boundary and disputed course content. Preserve both the historical failed database-preference check and its separately reviewed inconclusive interpretation; the opt-in open-slot pair is one positive conditional interest control, not a general preference claim. Preserve frozen cases 001-005. Resolve stale Cloud label paths and `SC4001`'s neural-versus-computer-network semantic defect separately; `SC4022`'s secure-software credit and `SC3040`'s broad architecture/testing tags remain contested.
3. Only after the static skills picture is reviewed, add permitted job-market evidence for the two pilot roles, then grounded pathway chat and combined evaluation. Keep ranking and allocation backend-owned and deterministic; retain the other four careers.
4. Work on NTU SSO and identity-scoped server persistence **after the recommendation-and-chat phase**, not as the next major feature. Retain backend-owned MSAL authentication, tenant-validated Azure `oid` and server-session boundaries.

The [development plan](plans/Development_Plan.md) replaces the old SSO-first sequence with dependency-based steps and no calendar deadlines. Source-access research can begin early, but this plan does not authorize starting all integrations.

## Unresolved And Deferred Work

- AI-focused Software Engineer cases still expose broad Cloud keyword credit and preference scaling concerns. Their policy review is now part of the baseline step; broader weight tuning remains deferred until evidence is reviewed. Do not hardcode winning courses.
- Cloud planning for a new prerequisite card is inconclusive where `SC1004` co-requisites or `MH2802` H2 Maths conditions remain unreviewed. Completed or existing earlier prerequisite paths have narrower supported behavior.
- Full prerequisite chains, co-requisites, cohort registration, offering availability, and workload/AU capacity remain outside current guarantees.
- Browser profile, transcript, curriculum, and completion state is inspectable and user-controlled; there is no production identity or cross-device user persistence.
- Job-source access remains undecided; the pilot introductory/advanced course-depth judgments and weak-fit evidence threshold are provisional, not expert-calibrated. MyCareersFuture is a candidate source, not a verified public API; permitted collection, storage and reuse must be established before integration.
- No job-market pipeline, skills-gap ranking model or LLM chat has been implemented. LangGraph/model work follows a working chat stub and understood workflow; RAGAS follows generated explanations. Keep the existing offline evaluator.
- Neo4j, ChromaDB, embeddings, ML/LLM ranking and A/B infrastructure are not required for the pilot and remain deferred.

## Documentation And Workflows

- [AGENTS.md](../AGENTS.md) contains lasting project rules and the startup reading order.
- [Progress3.md](progress/Progress3.md) is the active log; closed logs preserve previous work.
- The [PR skill](../.agents/skills/create-project-pr/SKILL.md) reads the single [PR template](workflows/PR_template.md). It does not authorize publication by itself.
- The repository now contains reusable SWE Team and Agent Flow tooling plus a
  [research-paper insight product plan](../project-records/swe-team/research-paper-insight-planner-20261110/final-plan.md).
  The plan and its architecture are proposed inputs only; they are not approved
  course-recommender scope and no application integration has started.
