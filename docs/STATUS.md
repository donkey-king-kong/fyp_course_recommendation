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

These are recorded results from the combined planning-integrity and tag-correction work, not fresh validation of this documentation cleanup. Draft explanation-path fidelity is `0.5`; some expected paths still reflect the removed Cloud tag. Historical prediction files remain separate snapshots. Full academic eligibility and expert validation are not established by these checks.

See the [latest previous progress entry](progress/Progress2.md#cloud-career-tag-correction-and-deferred-interest-ranking-review), [evaluation](evaluation/Evaluation.md), and [technical audit](evaluation/Recommendation_Technical_Audit.md) for provenance and limitations.

## Next Priorities

1. Conduct expert review / think-aloud on changed and weak-fit recommendations, contested course content, and expected explanation paths before changing labels or scoring constants.
2. Implement NTU SSO as the next major feature after benchmark review. Use backend-owned Microsoft MSAL OAuth callback and a server session; keep Azure tokens out of the frontend. Use tenant-validated Azure `oid` as the internal identity, separate from matriculation number and display email. App registration, tenant configuration, and the MSAL dependency require preparation; ask before major new dependencies.
3. Migrate profile, curriculum, transcript, completion, and recommendation state to server-side storage keyed by authenticated identity after SSO. Browser storage becomes a UI cache.

Read the [development plan](plans/Development_Plan.md) when starting these features; verify integration details against current official documentation before implementation.

## Unresolved And Deferred Work

- Broader interest-ranking calibration is deferred at the project owner's request. AI-focused Software Engineer cases still expose broad Cloud keyword credit and preference scaling concerns. Review content and policy before tuning; do not hardcode winning courses.
- Cloud planning for a new prerequisite card is inconclusive where `SC1004` co-requisites or `MH2802` H2 Maths conditions remain unreviewed. Completed or existing earlier prerequisite paths have narrower supported behavior.
- Full prerequisite chains, co-requisites, cohort registration, offering availability, and workload/AU capacity remain outside current guarantees.
- Browser profile, transcript, curriculum, and completion state is inspectable and user-controlled; there is no production identity or cross-device user persistence.
- Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML ranking, MyCareersFuture scraping, RAGAS, and A/B infrastructure remain deferred. Keep the existing offline evaluator.

## Documentation And Workflows

- [AGENTS.md](../AGENTS.md) contains lasting project rules and the startup reading order.
- [Progress3.md](progress/Progress3.md) is the active log; closed logs preserve previous work.
- The [PR skill](../.agents/skills/create-project-pr/SKILL.md) reads the single [PR template](workflows/PR_template.md). It does not authorize publication by itself.
