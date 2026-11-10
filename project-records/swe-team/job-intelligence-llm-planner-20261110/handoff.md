# Job Intelligence LLM Planner — Orchestrator Handoff

**Run:** `job-intelligence-llm-planner-20261110`  
**Repository:** `/Users/bytedance/Desktop/fyp_course_recommendation`  
**Status:** Planning package complete; not frame-approved, not shape-ready, not implemented, not released

## Authoritative Artifacts

- [Final product plan](final-plan.md) is the authoritative product framing.
- [Product design handoff](design.md) is a proposed Shape input for UX states.
- [Technical plan](technical-plan.md) is a proposed Shape input for architecture.
- [QA report](qa-report.md) audits cross-artifact consistency and residual risks.

## Supporting Evidence

- [Initial brief](brief.md) captures the first Product Manager draft.
- [Grill log](grill-log.md) records three grilling rounds and the final frontier certificate.
- [Planner responses](planner-responses.md) records Product Manager decisions for all grill rounds.
- [Repository analysis](research/repo-analysis.md) maps existing recommendation-system integration points.
- [LinkedIn access research](research/linkedin-access.md) records source-access constraints.
- [Extraction and operations research](research/extraction-and-operations.md) records parser, taxonomy, scheduling, and LLM-operation findings.
- [Security constraints](research/security-constraints.md) records pre-frame security and operational requirements.
- [Citation claims](research/citation-claims.md) and [citation verification](research/citation-verification.md) record the two-pass claim audit.

## Process Summary

- Three discovery tracks ran before planning: repository analysis, LinkedIn/source-access research, and extraction/operations research.
- A two-pass citation audit froze 173 claims, verified 117, corrected 10 into planner-safe form, and blocked 46 from use.
- DevOps/Security produced pre-frame constraints for source rights, secrets, content isolation, privacy, retention, prompt injection, cost, and kill switches.
- The Product Manager created the initial brief.
- An independent griller challenged the plan across three rounds.
- The Product Manager answered 34 material decisions.
- The final grilling check declared the product frontier empty.
- Product Design and Tech Lead produced proposed Shape inputs.
- QA independently audited the planning package and reported planning handoff pass, Shape intake conditional, and implementation/release blocked pending authority gates.

## Settled Product Frame

- Stage 1 is a grounded assistant for explaining existing course recommendations, roadmap, prerequisites, evidence, and tradeoffs.
- Stage 2 is a separately governed job-evidence companion, not a ranking feature.
- LinkedIn is authorization-only; no scraping, logged-in automation, indirect scraped datasets, or LinkedIn-origin supplied postings are in scope.
- The LLM may explain and transform validated evidence, but cannot mutate recommendations, readiness, prerequisites, ranking, scoring, or slots.
- The initial model credential is deployer-managed server-side configuration, not user BYOK.
- Supplied-posting analysis is private, no-fetch, non-LinkedIn, declaration-gated, item-level only, and expires within one hour after success.
- Interrupted or failed private posting work must be cleaned within 24 hours.
- Market-informed ranking requires a later deterministic proposal, shadow evaluation, source rights, coverage, regression evidence, and explicit authority approval.

## Current Gate

Do not start implementation until the owner records at least:

1. Product approval of the final plan and acceptance criteria.
2. Legal/source-owner approval for allowed job sources and LinkedIn exclusion wording.
3. Privacy/security approval for retention, deletion, isolation, telemetry, provider terms, and model-secret handling.
4. Recommendation-owner approval for course-skill mappings and noninterference tests.
5. Design acceptance of UX copy, accessibility states, deletion affordances, and over-trust prevention.
6. Tech Lead acceptance of the proposed architecture, integration order, file ownership, and verification commands.
7. QA acceptance of fixtures, metrics, audit sampling, and release gates.

Until those approvals exist, the correct workflow state is **planning complete but not frame-approved**.
