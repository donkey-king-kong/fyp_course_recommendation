# Repository Analysis: Job Intelligence and LLM Assistant

Date: 2026-11-10  
Flow: `swe-tech-lead`  
Scope: repository reconnaissance only  
Repository: `/Users/bytedance/Desktop/fyp_course_recommendation`  
Branch observed: `job-intelligence-llm-planning`  
Graph status: no Graphify graph; findings use scoped source reads.

## Executive Summary

The repository is ready for a bounded, evidence-grounded assistant **after** two prerequisites: the pilot course-skill picture must be reviewed and a permitted job-data source must be selected. It is not ready for an LLM-controlled recommender.

The current product already exposes useful deterministic facts through FastAPI:

- uploaded curriculum structure and open choice slots;
- transcript-derived completed courses and completed AU;
- personalized roadmap nodes and prerequisite edges;
- per-course roadmap readiness;
- exact-slot recommendations, open-slot explanations, score components, and top career-skill evidence;
- a seven-course, nine-link skills preview for Software Engineer and Data Engineer.

These are suitable grounding inputs for read-only explanation and comparison. The assistant must present uploaded/browser data as user-supplied, transcript-derived skills as likely exposure rather than mastery, and recommendation readiness as planning support rather than registration eligibility.

There is currently no job-market pipeline, job-ad domain model, source client, chat schema/endpoint, conversation store, frontend chat surface, LangGraph/OpenAI dependency, or model evaluation harness. `CourseNode.jobSkills` exists only as a reserved empty field and the skills preview is backend-only.

The lowest-risk integration is:

1. Add versioned, source-permitted role/job-skill snapshots for Software Engineer and Data Engineer.
2. Normalize them to the existing stable pilot skill IDs.
3. Integrate market evidence into the deterministic backend role-skill signal, with static fallback and offline evaluation.
4. Add a read-only chat stub over bounded backend context.
5. Add a model only after the workflow is understood, preserving deterministic fallback and requiring explicit confirmation before preference changes trigger backend recalculation.

## Current Architecture

The application is one FastAPI service with routers, Pydantic schemas, services, SQLAlchemy data access, PostgreSQL, and checked-in JSON evidence. All routers are composed in `backend/main.py`; there is no separate AI service (`backend/main.py:L1-L40`).

The frontend is React/TypeScript/Vite with Zustand persistence. It has three views, `roadmap`, `modules`, and `profile`; there is no chat view (`frontend/src/App.tsx:L15-L28`). API URLs are hard-coded to `http://127.0.0.1:8000`, including the recommendation client (`frontend/src/api/recommendationsApi.ts:L6-L30`).

The intended layering is already compatible with the feature:

```text
Frontend page/component
  -> frontend API client
  -> FastAPI router + Pydantic schema
  -> service
  -> PostgreSQL / checked-in evidence / future permitted job client
```

Keep job ingestion and model-provider access in the data-access/tools layer. Keep policy, grounding assembly, confirmation state, and deterministic fallback in services. Do not let a frontend component or model call recommendation internals directly.

## Current Recommendation Flows

### Frontend request construction

`App.handleLoadRoadmapRecommendations`:

1. Requires an uploaded curriculum and projected roadmap.
2. Requires one of six supported career goals.
3. Combines transcript-applied course codes with manually completed roadmap courses.
4. sends only uncompleted choice slots, including stable slot ID, year, and semester;
5. sends all projected curriculum nodes for prerequisite planning;
6. excludes fixed curriculum courses by code and title;
7. sets the limit to the number of open slots;
8. stores the backend response in Zustand.

Evidence: `frontend/src/App.tsx:L218-L307`.

The persisted browser record includes profile, curriculum, transcript rows and counts, completed node IDs, recommendations, open slots, and stale reasons (`frontend/src/store/useProfileStore.ts:L16-L42`). Zustand writes this under `student-profile-storage` in localStorage (`frontend/src/store/useProfileStore.ts:L174-L176`, `L705-L708`). Profile/career/preference changes clear prior recommendations (`frontend/src/store/useProfileStore.ts:L263-L316`); curriculum, transcript, and completion changes mark results stale.

### Backend recommendation pipeline

`POST /recommendations` is a thin router that passes request fields into `recommend_courses`; database failures become HTTP 503 (`backend/routers/recommendations.py:L33-L77`).

`recommend_courses`:

1. Normalizes the career goal and rejects unsupported goals with an empty result.
2. Normalizes completed courses, preferences, exclusions, slots, and student faculty.
3. Queries active-faculty PostgreSQL modules using slot and role relevance filters.
4. Hard-filters completed/fixed, deprecated code families, projects, special-track courses, programme exclusions, and slot mismatch.
5. Requires strong mapped career evidence.
6. Evaluates prerequisite feasibility and possible earlier planned prerequisites.
7. Computes deterministic score components.
8. Assigns unique courses to exact slots.
9. Runs a second pass for explicit-interest alternatives only on remaining slots.
10. Returns exact assignments plus explained open slots.

Evidence: `backend/services/recommendation_service.py:L265-L561`.

Candidate retrieval uses title/description keywords, curated recommendation tags, career-skill tag relationships, and MPE specialisations (`backend/services/recommendation_service.py:L1119-L1142`). MPE slots require CSC and the matching level; BDE slots admit broader active-faculty candidates at a roadmap-year-derived level (`backend/services/recommendation_service.py:L1159-L1200`).

Career scoring is deterministic. Module tags contribute through weighted static career-skill relationships; raw SWE keyword/tag scoring only tops up the mapped score to avoid double counting (`backend/services/recommendation_service.py:L1575-L1642`). The API exposes the top evidence path, including role, skill area, tag, weights, confidence, contribution, and rationale (`backend/services/recommendation_service.py:L1725-L1744`; `backend/schemas/recommendation.py:L159-L247`).

Pass 2 queries preference-matched modules, reuses eligibility/readiness checks, sets career scores to zero, and labels the result `recommendationSource="interest"` with an explicit non-career reason (`backend/services/recommendation_service.py:L1287-L1461`). The frontend renders backend assignments by `matchedChoiceSlotId` and labels interest results as “Interest alternative” (`frontend/src/components/SemesterRoadmap.tsx:L173-L217`).

### Roadmap and readiness flow

`POST /roadmap/personalized` combines parsed curriculum, transcript placement, transcript-only modules, catalog prerequisite data, and edges (`backend/routers/roadmap.py:L33-L63`; `backend/services/personalized_roadmap_service.py:L15-L46`).

`POST /roadmap/readiness` evaluates each displayed course against completed node IDs, completed AU, prerequisite edges/text, and parsed standing requirements (`backend/routers/roadmap_readiness.py:L11-L29`). The service returns `completed`, `available`, or `locked`; it does not implement registration, timetable, cohort, or live offering checks (`backend/services/roadmap_readiness_service.py:L14-L60`, `L73-L124`). The frontend calls this endpoint whenever displayed courses or completion/standing inputs change (`frontend/src/components/SemesterRoadmap.tsx:L480-L523`).

This readiness endpoint and recommendation readiness are related but distinct:

- roadmap readiness evaluates displayed roadmap nodes;
- recommendation readiness selects a supported prerequisite branch and may create planned prerequisite cards;
- neither proves registration eligibility.

## Domain Models and Contracts

### Student and browser state

`StudentProfile` contains browser-entered `studentId`, fixed major `CSC`, `careerGoal`, and preferred recommendation tags (`frontend/src/store/useProfileStore.ts:L16-L23`). There is no backend student entity, authenticated identity, server-side profile, or conversation model.

### Curriculum and transcript

`CurriculumGuideResponse` holds major, cohort, total AU, semesters, standing requirements, nodes, and edges (`backend/schemas/curriculum.py:L32-L57`). Curriculum PDFs are parsed using PyMuPDF positioned words and text into roadmap-shaped data (`backend/services/curriculum_service.py:L23-L45`).

Transcript responses hold completed courses, all completed transcript courses, count, total earned AU, and unmatched codes (`backend/schemas/transcript.py:L7-L30`). Parsing recognizes completed grades including `EX` and `TC` and extracts term placement and AU (`backend/services/transcript_service.py:L11-L46`). Matching uses exact code then conservative title matching (`backend/routers/transcript.py:L31-L48`).

### Catalog and prerequisite data

`ModuleModel` stores code, title, AU, faculty, description, level, categories, recommendation tags, MPE specialisations, recommendation profile, latest offering fields, and programme restrictions (`backend/models/module.py:L10-L28`). Prerequisites are pairs in `module_prerequisites` (`backend/models/module_prerequisite.py:L8-L14`); faculty activation controls catalog/recommender inclusion (`backend/models/faculty.py:L8-L13`).

The database requires `DATABASE_URL` and uses short-lived SQLAlchemy sessions (`backend/database/connection.py:L9-L23`).

### Recommendations

`RecommendationRequest` includes career goal, topic preferences, faculty, completed codes, legacy/new slot forms, positioned curriculum courses, exclusions, and bounded limit (`backend/schemas/recommendation.py:L69-L133`).

Each recommendation includes:

- exact matched slot and position;
- matched career signals;
- selected/missing/existing/planned prerequisites;
- planned roadmap nodes and edges;
- readiness, unlock value, score, confidence, and full score breakdown;
- deterministic reason and source (`career` or `interest`).

Evidence: `backend/schemas/recommendation.py:L249-L314`. Open slots have exact slot ID, reason, and student-facing message (`L316-L337`).

### Student skills

`StudentSkillsRequest` is restricted to `software-engineer` and `data-engineer`; completed and candidate codes are explicitly user supplied (`backend/schemas/student_skills.py:L5-L23`). Responses distinguish prior learning, candidate learning, introductory/advanced course-content depth, and unmapped completed/candidate codes (`backend/schemas/student_skills.py:L25-L51`).

The service reads a checked-in JSON ledger, normalizes codes, excludes completed courses from candidate learning, joins evidence to role-relevant skill IDs, and leaves unknowns explicit (`backend/services/student_skills_service.py:L11-L74`).

## Endpoint Inventory

| Endpoint | Current responsibility | Assistant relevance |
| --- | --- | --- |
| `GET /health` | Process health | Operational only |
| `POST /curriculum-guide` | Parse curriculum PDF | Ground roadmap structure; never send raw PDF to a model by default |
| `POST /transcript` | Parse completed transcript rows and AU | Ground likely completion; sensitive and user controlled |
| `POST /transcript/match-curriculum` | Match transcript to roadmap | Ground matched/unmatched completion context |
| `POST /roadmap/personalized` | Build ready-to-render roadmap | Primary bounded roadmap context |
| `POST /roadmap/readiness` | Evaluate completion/prerequisite/standing state | Explain available/locked status with limitations |
| `GET /modules`, `/modules/{code}`, `/modules/filters` | Search/catalog detail | Course facts and comparisons |
| `GET/PATCH /faculties...` | Catalog inclusion controls | Admin concern; must not become an assistant tool |
| `POST /recommendations` | Deterministic retrieval, filtering, ranking, assignment | Authoritative recommendation result |
| `POST /student-skills/preview` | Pilot course-skill evidence | Likely prior/next learning for two pilot roles |

Route evidence: `backend/main.py:L32-L40`; curriculum `backend/routers/curriculum.py:L10-L40`; transcript `backend/routers/transcript.py:L15-L48`; module routes `backend/routers/modules.py:L44-L122`; recommendation and skills routes cited above.

There is no `/chat`, `/assistant`, `/jobs`, `/job-skills`, or market snapshot endpoint.

## Data Sources

### Implemented sources

- NTU scraper output is normalized to `data/course_catalog.json` and `data/course_offerings.json`, then seeded into PostgreSQL (`README.md:L36-L52`).
- `data/modules.json` supplies curated recommendation tags and profile metadata.
- `data/ntu_prerequisite_unlock_graph.json` supplies prerequisite/unlock relationships.
- `data/mpe_specialisation_paths.json` supplies MPE path membership.
- uploaded curriculum PDFs define each browser profile’s roadmap.
- uploaded transcript PDFs define completed-course rows and completed AU.
- `data/student_skill_evidence.json` supplies the pilot source-linked course-skill ledger.
- `backend/services/career_skill_mappings.py` supplies static role-to-skill-area-to-tag mappings for six roles (`backend/services/career_skill_mappings.py:L838-L844`).
- benchmark and review JSON files supply offline evaluation inputs and saved evidence, not live product facts.

The seed combines modules, catalog descriptions, offerings, specialisations, and programme restrictions (`backend/database/seed.py:L15-L59`, `L291-L348`).

### Existing job-skill-shaped inputs

The usable shared skill IDs today are:

| Skill ID | SWE | DE | Course evidence |
| --- | --- | --- | --- |
| `programming-foundations` | yes | yes | `SC1003` introductory |
| `software-engineering-practice` | yes | no | `SC2006` introductory |
| `software-delivery-management` | yes | no | `SC2006` introductory, `SC3040` advanced |
| `data-storage` | yes | yes | `SC3020` introductory, `SC4023` advanced |
| `distributed-systems` | yes | yes | `SC4023`, `SC4051` introductory |
| `cloud-service-platforms` | yes | yes | `SC4052` introductory |

Evidence: `data/student_skill_evidence.json:L2-L49`, `L51-L106`.

The broader static career mappings already contain weighted role skill areas and normalized recommendation-tag relationships. These are recommendation evidence, not job-ad observations. They are the natural join target for normalized market skills, but the pilot ledger’s stable IDs and the broader mapping’s skill-area names are not yet represented by one explicit canonical ontology.

`CourseNode.jobSkills` is only a future-display placeholder (`backend/schemas/roadmap.py:L38`); production roadmap nodes currently set it to an empty list (`backend/services/personalized_roadmap_service.py:L60-L78`, `L119-L136`). Values in `data/test_csc_roadmap.json` are sample/test data and must not be treated as product evidence.

## What the Assistant Can Safely Answer Today

“Safely” means answer from current bounded data while stating provenance and limitations.

### Supported with grounding

- What career goal and topic preferences are currently selected, while labeling them as browser-entered.
- Which courses the uploaded transcript parser marked completed, their parsed term/AU/grade fields, and which matched the uploaded curriculum.
- Which roadmap courses are completed, available, or locked under parsed prerequisite/standing rules.
- What requirements the readiness service reports missing.
- What exact courses the deterministic backend assigned to each open slot.
- Whether a result is a career recommendation or labelled interest alternative.
- Why the backend recommended a course, using its returned reason, matched signals, score components, and top career-skill evidence path.
- Which prerequisite courses are completed, present earlier, missing, or proposed as planning nodes.
- Why a slot was left open (`no-supported-match` or `limit-reached`).
- Catalog facts: code, title, description, AU, faculty, categories, level, latest seeded offering metadata, prerequisites, unlocks, and MPE specialisations.
- For Software Engineer/Data Engineer only, which of the six pilot skill IDs have source-linked introductory/advanced course exposure among submitted completed/candidate courses.
- Which submitted pilot courses are unmapped and therefore unknown.
- Side-by-side comparison of already returned recommendations using deterministic response fields and catalog facts.

### Must be qualified

- Transcript-derived skills are **likely prior exposure**, not mastery.
- Uploaded and manually checked completion data are user-controlled prototype state.
- “Available” or recommendation `ready` means the implemented checks passed, not that NTU permits registration.
- Latest offering fields come from the seeded snapshot and are not a live timetable guarantee.
- Recommendation scores explain current backend behavior; they do not prove optimality or labour-market outcome.
- Course-skill evidence is narrow, author-reviewed, and not independently validated.

### Not supported today

- Current Singapore job-demand counts, trends, salary, employer demand, or “most in-demand” skills.
- Any MyCareersFuture-derived statement.
- A student’s verified mastery, employability, job readiness, or probability of getting a role.
- Full degree audit, workload suitability, timetable clashes, live vacancies, cohort restrictions, co-requisites, or registration permission.
- Market-informed skills gaps or market-informed course ranking.
- Reliable skills claims for courses outside the seven-course pilot ledger.
- Autonomous profile edits, course replacement, slot assignment, or prerequisite waiver.
- Multi-turn memory beyond browser state; no chat history exists.

## Likely Integration Points

### Job intelligence

Add a data/tool boundary such as `backend/clients/job_market_client.py` only after source permission is confirmed. Its output should feed a service-owned normalized snapshot model, not the recommender directly.

Recommended domain concepts:

- `JobSourceSnapshot`: source, retrieval timestamp, jurisdiction, query scope, sample count, terms/version, extraction version.
- `JobPostingEvidence`: source posting ID/hash, role classification, required/preferred marker, evidence excerpt, observed date.
- `MarketSkillEvidence`: canonical skill ID, normalized label, aliases, frequency/coverage, confidence, provenance.
- `RoleSkillSnapshot`: pilot role, entry-level scope, evidence window, market skills, quality flags.

Persist snapshots as versioned shared role evidence, not per-student scrapes. Keep raw permitted data separate from normalized evidence and record deduplication/extraction versions, as required by `docs/plans/Development_Plan.md:L112-L120`.

The first service integration should refine the existing role-skill evidence used by `build_relevance_filters` and `score_career_match`, while retaining the static mapping as fallback. Avoid adding a second independent “market bonus” that double-counts the same concept.

### Course-skill bridge

Expand the existing ledger/service rather than deriving skills ad hoc in prompts. Establish one canonical skill registry that maps:

```text
job source term/alias
  -> canonical skill ID
  -> role requirement evidence
  -> course-content evidence with depth
```

Keep unknowns and uncertain mappings explicit. Any prior-learning ranking change should be a separately evaluated backend policy change before market evidence or chat consumes it.

### Assistant backend

Add schemas and a router only after a non-model stub contract is agreed. A minimal contract should accept:

- user message;
- bounded profile fields needed for the question;
- current roadmap/recommendation identifiers or structured snapshots;
- optional short conversation history;
- explicit pending action/confirmation token, if applicable.

The assistant service should call narrow context builders rather than receiving raw localStorage wholesale. Reuse service-level operations for module lookup, roadmap/readiness facts, recommendation responses, and skills preview.

Return structured grounding metadata with the answer:

- claim/source references;
- data freshness;
- limitations;
- proposed preference change, if any;
- `confirmationRequired`;
- deterministic fallback answer.

Do not expose faculty mutation endpoints as tools. Do not let model output call `recommend_courses` with silently modified inputs. A confirmed preference change should update browser state through an explicit frontend action and then invoke the existing `POST /recommendations` flow.

### Assistant frontend

Add a dedicated API client and typed assistant contract. A chat panel can read current Zustand state, but it should send only the bounded fields required by the backend contract. The UI must:

- distinguish deterministic facts from model-generated synthesis;
- show source/freshness labels;
- show unsupported/unknown states;
- display a confirmation control before applying preference changes;
- preserve current stale-recommendation behavior;
- avoid persisting raw transcripts or sensitive chat content to third-party services by default.

## Verification Conventions

The repository has no backend unit-test framework in `backend/requirements.txt` and no frontend test script. Backend dependencies are FastAPI, PyMuPDF, multipart, dotenv, psycopg2, SQLAlchemy, and Uvicorn (`backend/requirements.txt:L1-L7`). Frontend verification is `npm run build` (`tsc -b && vite build`) and `npm run lint` (`oxlint`) (`frontend/package.json:L6-L25`).

Recommendation verification is intentionally offline/script based:

- capture live endpoint outputs with revision, file hashes, and operator-declared database fingerprint (`scripts/run_recommendation_benchmark_predictions.py:L19-L59`);
- evaluate saved predictions against draft labels and validate response contracts (`scripts/evaluate_recommendation_benchmark.py:L1-L37`, `L70-L120`);
- run the six-career coverage grid (`scripts/run_coverage_audit.py:L1-L14`, `L37-L74`);
- run controlled counterfactual checks while preserving inconclusive/failure findings (`scripts/run_counterfactual_sensitivity.py:L1-L11`, `L78-L120`);
- validate mapping tags and preference aliases against the catalog (`scripts/validate_recommendation_mappings.py:L9-L73`).

Project rules explicitly say not to add an automated recommender test suite yet; existing benchmark, coverage, and counterfactual scripts remain the evaluators (`AGENTS.md:L205-L214`).

For this feature, verification should extend those conventions:

- versioned fixture snapshots for permitted job data;
- deterministic normalization/deduplication checks;
- human-reviewed extraction samples;
- static-fallback behavior under source failure/sparse evidence;
- baseline versus prior-learning versus market-informed captures;
- chat contract checks for grounding, unsupported claims, prompt injection, confirmation, model timeout/failure, and deterministic fallback;
- human explanation review before optional RAGAS, consistent with `docs/plans/Development_Plan.md:L131-L141`.

## Constraints and Risks

### Critical

1. **Source authorization is unresolved.** MyCareersFuture is a candidate, not a confirmed public API. Collection, storage, reuse, retention, and display rights must be established before implementation (`docs/STATUS.md:L47-L50`; `AGENTS.md:L209-L211`).
2. **Browser state is untrusted.** Student ID, profile, curriculum, transcript results, completions, and recommendations are editable localStorage data. Assistant answers must not describe them as verified records (`frontend/src/store/useProfileStore.ts:L131-L176`; `docs/plans/Development_Plan.md:L145-L153`).
3. **Academic eligibility is incomplete.** Co-requisites, complete prerequisite chains, cohort rules, workload, live offerings, timetable, vacancies, and registration permission are outside current guarantees (`docs/STATUS.md:L42-L49`).
4. **An LLM must not control ranking or eligibility.** Backend deterministic filtering, ranking, and exact-slot allocation are explicit product boundaries (`docs/plans/Development_Plan.md:L17-L28`, `L122-L129`).

### High

5. **Skill evidence is sparse.** Seven courses and nine links cannot support broad skills-gap claims; 12 of 35 selected-course occurrences in the pilot audit remained unknown (`docs/STATUS.md:L29-L29`).
6. **Evidence quality is provisional.** Course depth judgments and the strong-career threshold are not independently expert calibrated; disputed semantic mappings remain.
7. **Ontology mismatch.** Pilot stable skill IDs, broad career-skill-area names, curated recommendation tags, and future job-source terms do not yet share one explicit canonical model.
8. **Prompt injection/data poisoning.** Job descriptions and uploaded document text are untrusted. Source text must be data-only, structured outputs validated, and tool permissions fixed outside prompts (`docs/plans/Development_Plan.md:L122-L129`).
9. **Privacy boundary.** Raw transcripts and unnecessary identifiers must not be sent to model providers. Provider, retention, region, budget, and evaluation privacy arrangements are undecided.

### Medium

10. **No server conversation persistence or auth.** Multi-turn history would initially be browser-controlled and non-portable.
11. **No current model dependencies or test harness.** LangGraph/OpenAI must follow a working chat stub and explicit dependency approval (`AGENTS.md:L81-L84`).
12. **Hard-coded frontend API origin.** A new assistant client would repeat the current localhost coupling unless configuration is introduced deliberately.
13. **Staleness.** Recommendations have stale-input tracking, but future job snapshots and assistant answers need their own source version/freshness semantics.
14. **Score leakage/confusion.** Score breakdowns are diagnostic and intentionally hidden from the roadmap UI; exposing them conversationally may encourage false precision (`AGENTS.md:L205-L207`).
15. **Admin tool exposure.** Faculty activation changes candidate availability and must remain outside assistant capabilities.

## Recommended Delivery Boundaries

1. **Decision and source feasibility:** settle source rights, pilot role/query scope, snapshot cadence, retention, and human review criteria.
2. **Canonical skill evidence:** review the current course-skill ledger; define canonical IDs/aliases and uncertain-mapping representation.
3. **Job snapshot pipeline:** ingest one permitted source into versioned, reproducible shared snapshots; no per-user scrape.
4. **Deterministic market integration:** compare static and market-informed role evidence with static fallback; keep all-six-career regression visible.
5. **Read-only chat stub:** answer from structured current facts without a model; establish citations, unknowns, and fallback contract.
6. **Grounded model synthesis:** add one provider only after workflow review; no ranking authority or raw transcript transfer.
7. **Confirmed recalculation:** model may propose a preference change, but the user confirms and the existing backend recalculates.
8. **Combined evaluation:** human review, adversarial grounding checks, reproducible captures, and only then optional RAGAS.

This sequence matches the repository’s dependency plan: student skills, job evidence, pathway chat, combined evaluation, then SSO/persistence (`docs/plans/Development_Plan.md:L48-L57`).

## Questions for the Product Manager

1. Is the pilot still limited to entry-level Singapore Software Engineer and Data Engineer roles? What exact titles/seniority aliases are in and out?
2. Which job source has confirmed collection, storage, reuse, retention, and end-user display permission? Who signs off on that interpretation?
3. What does “job intelligence” need to show in the first release: skill presence, frequency, trend, required/preferred status, representative excerpts, or all of these?
4. What snapshot cadence and maximum acceptable staleness should be displayed to students?
5. What minimum sample size/coverage makes a market claim publishable, and what fallback wording is required below it?
6. Should market evidence change ranking in the first release, or first appear as read-only evidence alongside unchanged recommendations?
7. Who reviews canonical job-skill aliases and course-skill mappings: supervisor, TA, domain expert, or product owner?
8. What is the accepted behavior when a job skill has no mapped course, or a course has no reviewed skill evidence?
9. Which assistant intents are in MVP: explain a recommendation, compare courses, explain readiness, show likely skills, explore preferences, or broader course Q&A?
10. Should the assistant answer only about the current profile/roadmap, or also support anonymous catalog questions?
11. What actions may the assistant propose? Is preference change the only mutating action in the pilot?
12. What exact confirmation interaction is required before applying a proposed preference change and recalculating?
13. Should conversation history persist only for the browser session, in localStorage, or not at all until authenticated server persistence exists?
14. Which model/provider, data region, retention policy, cost ceiling, and latency target are acceptable?
15. May any parsed transcript fields be sent to the provider, or must the backend reduce them to course codes/aggregate AU first?
16. What citations must students see: course catalog excerpts, job-source excerpts, snapshot metadata, recommendation evidence paths, or all?
17. What student-facing disclaimer is required for non-verified academic eligibility and likely exposure versus mastery?
18. Is deterministic fallback mandatory for every supported intent, or may the assistant decline when the model is unavailable?
19. What human evaluation tasks and acceptance thresholds define success for usefulness, grounding, and preference confirmation?
20. Are score components permitted in assistant explanations, despite being intentionally hidden from the roadmap UI?

## Conclusion

The repository already provides a strong deterministic grounding layer, especially exact-slot recommendation evidence and roadmap readiness. The near-term engineering gap is not “add an LLM”; it is to establish permitted, versioned job evidence and a reviewed canonical skill bridge. Once those exist, a thin assistant service can explain bounded backend facts and propose confirmed preference changes without taking ownership of eligibility, ranking, or allocation.
