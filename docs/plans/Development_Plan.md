# Development Plan

This is the agreed forward plan, replacing the previous SSO-first sequence. Work is ordered by dependencies and completion criteria, not calendar deadlines. Historical implementation details remain in the [progress logs](../progress/README.md); current capabilities and recorded evidence remain in [STATUS.md](../STATUS.md).

## Direction And Scope

The next pilot targets **Software Engineer** and **Data Engineer**. The existing six-career recommender remains available; the pilot does not remove other careers, and the full benchmark remains a regression check.

There are three connected parts:

| Part | Responsibility |
| --- | --- |
| Skills-gap recommendations | Use completed-course evidence to identify likely prior learning and useful next learning. |
| Job-market evidence | Refine the target role's skill requirements using a permitted, periodically refreshed source. |
| Pathway chat | Explain recommendations and help students explore confirmed preference changes. |

The backend remains responsible for eligibility, deterministic ranking and exact-slot allocation. Job data supplies evidence; an LLM does not override academic constraints or directly control core scores. Keep one FastAPI application and the existing layered architecture described in [Diagrams.md](../architecture/Diagrams.md).

```text
Curriculum guide -> available roadmap slots and planning constraints
Completed courses -> evidence of likely prior learning
Career goal -> static role skills, later refined by job-market evidence
These inputs -> remaining learning needs -> eligible recommended courses
Recommendation results and supporting evidence -> pathway chat
Confirmed preference changes -> backend recalculation
```

SSO and server-side user persistence come after this recommendation-and-chat phase. Recording the plan does not authorize starting all integrations.

## Agreed Weak-Fit Policy

**Approved product direction; bounded implementation captured, evidence threshold provisional.** See the [policy comparison](../evaluation/Recommendation_Weak_Fit_Policy_2026-11-03.md) for the observed outcomes and the failed counterfactual.

| Outcome | Intended behavior |
| --- | --- |
| Strong, evidence-supported career match | Recommend normally, subject to eligibility and slot fit. |
| Weak career fit but useful explicit interest match | Offer a clearly labelled interest-based alternative, not a strong career recommendation. |
| Neither a strong career match nor a useful interest match | Leave the slot open and explain that no strong match was found under the current constraints. |

- Do not fill slots just to maximize fill rate. Academic eligibility and recommendation relevance are different judgments.
- Eligibility filters apply to interest alternatives as well as career recommendations.
- A large total score, faculty bonus or structural fit alone is not evidence of strong career relevance.
- Confirmed priority: select strong eligible career matches first, even when the student has different explicit interests. Use still-open slots for useful eligible explicit-interest alternatives, clearly labelled; leave slots open with an explanation when neither qualifies. A merely plausible career match must not count as strong solely to fill a slot.
- Review examples before selecting numeric thresholds. The existing weak-fit audit heuristic and score-based confidence labels are diagnostics, not an approved implementation of this policy.
- Career-fit and interest-usefulness boundaries and the interaction with pass-2 interest filling still need review. Do not let an LLM choose these thresholds.
- An intentionally open slot is not automatically a failure. Evaluation must distinguish justified abstention from retrieval, eligibility or allocation defects.

## Work Sequence

| Step | Scope | Completion evidence | Status |
| --- | --- | --- | --- |
| 1. Baseline and policy | Capture current behavior, review pilot cases, define policy boundaries, then implement the bounded weak-fit change separately. | Reproducible baseline, reviewed examples, agreed acceptance criteria and a controlled policy comparison. | Policy merged; historical failed preference check preserved and its expectation separately reviewed as inconclusive for the AI/ML swap. Expert strength calibration remains pending. |
| 2. Student skills picture | Map relevant completed and candidate courses to shared skill identifiers and learning depth, using static role mappings first. | Traceable course-content evidence and reviewed examples of useful next learning. | Seven-course backend preview, two source-based review passes and limited coverage audit recorded; external validation and separately evaluated ranking integration remain pending. |
| 3. Job-market evidence | Integrate one permitted source for the two pilot roles; normalize and version extracted skills. | Reviewed extraction quality, dated snapshots and static-versus-market comparison. | Planned; source feasibility research can begin early. |
| 4. Pathway chat | Build a chat stub, understand a small workflow, then add grounded model responses and confirmed preference changes. | Supported explanations, validated recalculation and deterministic fallback behavior. | Planned; depends on stable recommendation evidence. |
| 5. Combined evaluation | Compare the baseline, skills-gap version, market-informed version and chat experience. | Human-reviewed comparisons, explanation evaluation and reproducible report evidence. | Planned; evaluation also runs throughout Steps 1-4. |
| 6. SSO and persistence | Add NTU authentication, then move user state to server storage. | Authenticated sessions and identity-scoped persistence. | Deferred until after the recommendation-and-chat phase. |

### Step 1: Baseline And Policy Checklist

This checklist describes the work sequence. The baseline, reviews and bounded policy comparison have now been captured; expert validation and strength calibration remain outstanding.

1. **Capture the unchanged baseline.** Use existing benchmark, coverage and counterfactual runners against a verified backend and database. Record serving revision, database fingerprint, mapping/rule versions, exact requests, full responses and evaluator configuration. Keep historical predictions unchanged; use a separate labelled capture and retain a durable, privacy-reviewed evidence summary.
2. **Preserve evaluation inputs.** Keep the current 24 cases and labels stable, especially `software-engineer-csc-001` through `005`. Review findings are separate from label edits. Add necessary positioned or abstention scenarios separately; do not rewrite the frozen cases.
3. **Prepare a small pilot review.** Start with the seven cases below. Show student context, slot, returned course, meaningful alternatives, supporting course content, score components and eligibility limitations. Do not treat the highest score or existing label as the correct answer.
4. **Classify recommendations.** Review career fit, explicit interest fit, new learning beyond completed courses, evidence quality and readiness separately. Record a proposed outcome: career recommendation, interest alternative, open slot or unresolved pending evidence. Seek supervisor/TA review for contested course-content and label judgments.
5. **Resolve policy boundaries.** Use reviewed positive and negative examples to propose a minimum career-fit rule, an interest fallback rule and reasons for leaving slots open. Identify whether problems come from data, ranking, retrieval or labels before proposing changes. Thresholds remain unset until this review.
6. **Implement only the bounded policy change in a separate work unit.** After agreeing findings, adjust backend selection and necessary response/UI messaging. Rerun the frozen benchmark and existing audits on the same data; inspect changed courses and every newly open slot. Keep label corrections separate from scoring changes and do not add an automated recommender test suite.

Initial review shortlist, selected from existing case descriptions rather than fresh predictions:

| Case | Review purpose |
| --- | --- |
| `software-engineer-csc-001` | Backend/distributed preferences as a career-aligned comparison. |
| `software-engineer-csc-002` | AI-focused interests under a Software Engineer goal and mixed MPE levels. |
| `software-engineer-csc-003` | Security preferences, completed learning and a BDE slot. |
| `software-engineer-csc-005` | No-preference defaults and diversity. |
| `software-engineer-csc-013` | Advanced AI interests after prior AI/ML learning; contested career/preference balance. |
| `data-engineer-csc-001` | Database/distributed learning and the changed Cloud-versus-Big-Data selection. |
| `data-engineer-csc-002` | Cloud/parallel preferences after completed database study. |

This shortlist does not guarantee a weak-fit or empty-slot example in the current capture. Add separately identified scenarios for strong match, interest-only match, neither match and unresolved eligibility if needed. Reuse existing positioned scenarios where appropriate; code-only curriculum inputs do not establish full timing or unlock behavior.

The first review deliverable should be a compact table:

```text
Case and slot | current recommendation | alternatives | course evidence
Career fit | interest fit | likely new learning | eligibility uncertainty
Proposed outcome | reviewer rationale | unresolved question
```

Step 1 acceptance criteria:

- The baseline can be traced to its actual inputs, code and data, without calling old saved predictions a fresh run.
- Reviewed examples explain why each outcome is appropriate; unresolved judgments stay explicit.
- Agreed policy behavior preserves supported eligibility and response contracts, including for interest alternatives.
- Newly open slots have an evidence-based reason. Fill rate is reported, but is not the optimization target.
- Existing ranking metrics and all-six-career regression checks remain visible, even when results decline.
- Labels remain draft ground truth until independently reviewed; metric improvement alone is not approval.

See [Evaluation.md](../evaluation/Evaluation.md) for existing tools and evidence boundaries. The [older label review packet](../evaluation/Recommendation_Benchmark_Label_Review_Packet.md) describes an earlier 21-case comparison; it is historical context, not the new baseline review.

### Step 2: Student Skills Picture

- Use shared skill identifiers for courses, role requirements and later job evidence.
- Begin with a small relevant set of completed and candidate courses for the two pilot roles, not the entire catalog.
- Ground mappings in course descriptions or learning outcomes, with source, evidence and introductory/advanced depth. Keep unknown coverage explicit.
- Describe transcript-derived skills as likely prior learning, not demonstrated mastery. Introductory exposure must not suppress useful advanced study.
- Rank useful remaining learning using static role mappings first. Retain interests, slot fit, prerequisites, unlock value and diversity.
- Compare against the frozen baseline before attributing improvements to job data.

### Step 3: Job-Market Evidence

- Verify permitted collection, storage and reuse before selecting a source. MyCareersFuture is a candidate, not a confirmed public API; do not build around unauthorized LinkedIn scraping.
- Start with Software Engineer and Data Engineer. Entry-level Singapore roles are the proposed initial search scope, to confirm during source review.
- Collect shared role-based snapshots periodically, not a new scrape per student. Deduplicate advertisements, distinguish required/preferred skills and normalize synonyms.
- Store permitted provenance, retrieval dates, sample counts and extraction versions. Do not present one job board's frequency counts as the whole labour market.
- Validate extraction against human-reviewed examples before ranking. Use deterministic parsing where sufficient; model-assisted extraction is a separate dependency decision.
- Refine the existing role-skill signal rather than adding overlapping relevance bonuses. Check that candidate retrieval can admit courses relevant to the new skills.
- Retain a clearly labelled static fallback when access fails or evidence is sparse. The refresh interval and source remain undecided.

### Step 4: Pathway Chat

- Support explanations, course comparisons, likely skill development and exploration of different preferences.
- Follow the existing prerequisite order: working chat stub, understood LangGraph structure, then OpenAI/model integration. Ask before new dependencies.
- Supply bounded recommendation results and supporting course/job evidence. Do not send raw transcripts or unnecessary student identifiers.
- Treat external text as untrusted data, validate structured model outputs and prevent instructions in source content from controlling tools.
- Require confirmation before applying preference changes; the backend recalculates the pathway. An LLM does not waive eligibility or silently replace courses.
- Keep deterministic explanations available if the model fails. LLM reranking is optional later research, not a requirement for this pilot.

### Step 5: Combined Evaluation

- Compare the current baseline with skills-gap recommendations, static with market-informed requirements, and existing explanations with chat-assisted understanding.
- Use a static/market by prior-learning-on/off comparison to separate contributions. Disabling inferred skills must not disable completion exclusions or prerequisite checks.
- Remove other scoring components individually after the main comparisons are stable. Record coupled effects such as career-fit-dependent preference scaling.
- Keep historical metrics unchanged for comparability; add separately versioned slot-aware relevance and justified-abstention observations where needed.
- Freeze common inputs for cross-version comparisons. Gen 1 has no ranking, so compare shared usability tasks rather than inventing ranking scores.
- A freshness claim needs older/newer snapshots of the same source, not merely a comparison with a different historical job dataset.
- Use human-reviewed relevance and skill evidence. Add RAGAS only when generated explanations exist, alongside human checks, with judge model/prompts/settings recorded.
- RAGAS faithfulness/relevance concerns explanations; it does not establish optimal ranking, academic eligibility or actual employment outcomes.
- Local consented usability sessions can use synthetic or anonymized profiles before SSO. Production usage logging and A/B infrastructure remain deferred.

### Step 6: NTU SSO And Persistence

**Deferred until after Steps 1-5.** Retain the design boundaries below, but verify current official Microsoft documentation and NTU tenant requirements before implementation.

- Use Microsoft MSAL OAuth 2.0 Authorization Code flow with a backend-owned callback and server session. Keep Azure tokens out of the frontend.
- Validate the intended tenant and token claims; an email substring is not an authorization check.
- Use Azure `oid` as the internal identity within the validated tenant, separate from matriculation number and display email.
- Prepare app registration, tenant authority, redirect configuration and server-side credentials. Ask before adding the MSAL dependency.
- Do not build a fake NTU password form, scrape login pages or hardcode captured authentication URLs.
- After SSO, migrate profile, curriculum, transcript, completion and recommendation state to identity-scoped server storage. Browser storage becomes a UI cache.
- Until then, browser data remains inspectable, editable prototype input, not a trusted academic record.

## Intentionally Excluded

- No blanket catalog-wide skill annotation or expansion beyond the two-role pilot yet.
- No Neo4j, ChromaDB or embeddings without a demonstrated need beyond the existing database.
- No multi-agent architecture, LLM-controlled core ranking or automated recommender test suite.
- No forced slot filling, unsupported skill-mastery claims or promises of full academic registration eligibility.
- No benchmark label changes solely to improve metrics, and no changes to frozen cases 001-005.

## Decisions Still Open

- The permitted job-data source, access/storage terms, refresh interval and acceptable sample coverage.
- Course-skill depth representation and handling of uncertain prior learning.
- Career/interest boundary thresholds, precise fallback behavior and evidence-based abstention reasons.
- Reviewer availability, later model/provider budget and privacy arrangements for evaluation.

Resolve these within their relevant steps, not by adding all integrations at once.
