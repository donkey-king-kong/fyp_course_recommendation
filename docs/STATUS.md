# Current Project Status

Last updated: 2026-11-03. This is the session handoff; detailed history is in the [progress index](progress/README.md). Check Git for the current branch and working tree.

## What Works

- One FastAPI backend with router, schema, service, and data-access layers; PostgreSQL module catalog and faculty controls.
- React / TypeScript frontend with profile setup, uploaded curriculum roadmap, transcript extraction and matching, roadmap readiness, and exact-slot recommendations.
- Uploaded curriculum defines the student's roadmap; transcript completions are stored and matched separately. Without a curriculum guide, the roadmap shows an empty state.
- Deterministic backend scoring for six career goals: Software Engineer, AI/ML Engineer, Data Engineer, Cloud/Platform Engineer, Cybersecurity Engineer, and Data Scientist.
- Two-pass assignment: career recommendations first, then interest picks for remaining slots. Reviewed prerequisite rules and earlier planning nodes enforce the supported response contract.
- Existing offline benchmark, coverage audit, and counterfactual scripts record ranking, fill, and contract results. User state remains browser-side prototype persistence.

## Latest Evidence And Its Limits

The latest Cloud career-tag correction removed unsupported `backend-engineering` evidence from `SC4052` in the seed JSON and local database. The recorded 24-case follow-up reports nDCG@returned `0.7413`, precision@returned `0.7778`, full slot fill, and zero supplementary contract violations across 53 recommendations. The 180-cell grid records no empty slots or contract violations and 18 weak-fit cells. Positioned scenarios record 8 PASS / 1 INCONCLUSIVE; counterfactual checks record 6 PASS / 2 INCONCLUSIVE, with no failures.

An unchanged fresh baseline captured on 2026-11-03 against an owned backend and fingerprinted local database reproduced 24 cases / 53 recommendations, nDCG@returned `0.7413`, precision@returned `0.7778`, fill `1.0`, and zero supplementary violations. The 180-cell grid again found 18 weak-fit cells and no empty slots; positioned checks were 8 PASS / 1 INCONCLUSIVE and counterfactual checks 6 PASS / 2 INCONCLUSIVE. The [baseline and seven-case review packet](evaluation/Recommendation_Baseline_Review_2026-11-03.md) contains full traceability, discrepancies, and pending decisions. Historical prediction files remain separate snapshots. Draft explanation-path fidelity is `0.5`; full academic eligibility and expert validation remain unestablished.

The [Step 1 boundary review](evaluation/Recommendation_Boundary_Review_2026-11-03.md) reuses those unchanged captures and rechecked the same database fingerprint. Direct career positives, constrained interest-only *source routing*, indirect weak picks and inconclusive eligibility are distinguished; the proposed course-evidence rule is qualitative, **not** an implemented or numerically calibrated threshold. The constrained graphics interest fixture returns `ready` despite missing evidence for its catalog Year 2 standing requirement; this standing/fixture gap is separate from relevance and must not certify eligibility. A full-catalog interest-vs-weak-career control, a verified relevance-based open-slot example and one Cloud/Platform course-value judgment remain open.

See the [latest previous progress entry](progress/Progress2.md#cloud-career-tag-correction-and-deferred-interest-ranking-review), [evaluation](evaluation/Evaluation.md), and [technical audit](evaluation/Recommendation_Technical_Audit.md) for provenance and limitations.

## Next Priorities

1. Use the seven-case and boundary reviews for the **Software Engineer and Data Engineer pilot** while retaining all-six-career regression coverage. The owner confirmed strong eligible career matches first, then useful eligible explicit-interest alternatives for remaining slots, then explained open slots. Check eligible alternatives and the full-catalog transition/abstention controls before choosing a numeric strength boundary; this internal review is not independent expert validation or policy implementation. Preserve the full 24-case benchmark, especially cases 001-005. Resolve stale Cloud label paths and the `SC4001` neural-versus-computer-network semantic defect separately from threshold changes; `SC4022` does mention cyber-security applications, but strong secure-software credit remains contested.
2. Review course evidence and career/interest boundaries before choosing thresholds, then implement the bounded weak-fit policy in a separate work unit. Approved direction: strong career match -> normal recommendation; useful explicit interest match without strong career fit -> labelled interest alternative; neither -> leave the slot open with an explanation. This policy is not implemented yet, and 100% slot fill is not the goal.
3. Build a small, evidence-backed student skills picture using completed courses and static mappings first. Then add permitted job-market evidence for the two pilot roles, followed by grounded pathway chat and combined evaluation. Keep ranking and allocation deterministic and backend-owned; retain the other four careers and full-suite regression checks.
4. Work on NTU SSO and identity-scoped server persistence **after the recommendation-and-chat phase**, not as the next major feature. Retain backend-owned MSAL authentication, tenant-validated Azure `oid` and server-session boundaries.

The [development plan](plans/Development_Plan.md) replaces the old SSO-first sequence with dependency-based steps and no calendar deadlines. Source-access research can begin early, but this plan does not authorize starting all integrations.

## Unresolved And Deferred Work

- AI-focused Software Engineer cases still expose broad Cloud keyword credit and preference scaling concerns. Their policy review is now part of the baseline step; broader weight tuning remains deferred until evidence is reviewed. Do not hardcode winning courses.
- Cloud planning for a new prerequisite card is inconclusive where `SC1004` co-requisites or `MH2802` H2 Maths conditions remain unreviewed. Completed or existing earlier prerequisite paths have narrower supported behavior.
- Full prerequisite chains, co-requisites, cohort registration, offering availability, and workload/AU capacity remain outside current guarantees.
- Browser profile, transcript, curriculum, and completion state is inspectable and user-controlled; there is no production identity or cross-device user persistence.
- Job-source access, skill-depth representation and weak-fit thresholds remain undecided. MyCareersFuture is a candidate source, not a verified public API; permitted collection, storage and reuse must be established before integration.
- No job-market pipeline, student skills-gap model or LLM chat has been implemented. LangGraph/model work follows a working chat stub and understood workflow; RAGAS follows generated explanations. Keep the existing offline evaluator.
- Neo4j, ChromaDB, embeddings, ML/LLM ranking and A/B infrastructure are not required for the pilot and remain deferred.

## Documentation And Workflows

- [AGENTS.md](../AGENTS.md) contains lasting project rules and the startup reading order.
- [Progress3.md](progress/Progress3.md) is the active log; closed logs preserve previous work.
- The [PR skill](../.agents/skills/create-project-pr/SKILL.md) reads the single [PR template](workflows/PR_template.md). It does not authorize publication by itself.
