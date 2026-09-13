# AGENTS.md

## Project

This repository is a clean rebuild of my FYP course recommendation system.

New repo:

```text
/Users/bytedance/Desktop/fyp_course_recommendation
```

Reference repo:

```text
/Users/bytedance/Desktop/course-recommendation-system
```

Use the reference repo only as a blueprint. Do not blindly copy the entire old project.

## Goal

Build a course recommendation system for NTU students.

The system should eventually support:

- Student profile setup
- Course roadmap visualization
- Curriculum guide upload and roadmap extraction
- Transcript upload and completed course extraction
- Chat-based course recommendations
- Job-market-aware recommendations using MyCareersFuture data
- Future integration with Neo4j, ChromaDB, LangGraph, and OpenAI

## Tech Stack

Backend:

- Python
- FastAPI
- Pydantic
- LangGraph
- Neo4j
- ChromaDB
- MyCareersFuture scraper
- PDF curriculum guide parser
- PDF transcript parser

Frontend:

- React
- TypeScript
- Vite
- Material-UI
- ReactFlow
- Zustand
- TanStack Query
- Axios

## Rebuild Philosophy

This project is being rebuilt step by step so I understand every file.

For the high-level architecture and diagrams, refer to `Diagrams.md`.

Do not build everything at once.

Use small milestones.

After each milestone, explain:

- What files were created
- What each file does
- How to run or test it
- What is working
- What is intentionally not implemented yet
- What the next milestone should be

## Important Rules

- Do not add Neo4j until the static roadmap API works.
- Do not add ChromaDB until the basic recommendation flow exists.
- Do not add LangGraph until the chat stub works.
- Do not add OpenAI until the LangGraph structure is understood.
- Do not add frontend before the minimal backend is working.
- Do not over-engineer early milestones.
- Prefer simple working code over complex architecture.
- Ask before introducing major new dependencies.
- Keep explanations beginner-friendly.
- Explain why each file exists.
- Work inside the new repo unless explicitly told otherwise.
- Treat the old repo as read-only reference material.
- For the personalised roadmap flow, do not show the static roadmap as the default student roadmap once curriculum guide upload is being implemented.
- Treat `data/test_csc_roadmap.json` as sample/test data, not as the final source of truth for a student's roadmap.
- A student's uploaded curriculum guide should define the roadmap structure for that browser profile.
- A student's uploaded transcript should define completed modules separately from the curriculum guide.
- If only a transcript has been uploaded, store the transcript result but do not display a roadmap until a curriculum guide is uploaded.
- If only a curriculum guide has been uploaded, display the parsed curriculum guide in the current roadmap style without transcript-based completions.
- If both curriculum guide and transcript are uploaded, match completed transcript modules against the parsed curriculum roadmap.
- If neither curriculum guide nor transcript is uploaded, the roadmap page should show an empty-state message asking the student to upload a curriculum guide.
- New transcript uploads should override the previous transcript result for the active browser profile and rematch against the current curriculum guide if one exists.
- New curriculum guide uploads should override the previous curriculum result for the active browser profile and rematch against the current transcript if one exists.
- The Profile page should store the student's career goal so later MPE/choice-slot recommendations can use it.
- Browser storage is prototype persistence only; treat localStorage profile, curriculum, transcript, completion, and recommendation data as inspectable and user-editable.
- Backend recommendation requests currently receive user-controlled browser state, so do not treat submitted completed courses, profile fields, or uploaded-roadmap data as trusted production records.
- NTU SSO uses Microsoft Azure AD OAuth 2.0 Authorization Code flow via `msal`; do not build a fake NTU password form, scrape NTU login pages, or hardcode captured auth URLs.
- Use the Azure Object ID (`oid` from `id_token_claims`) as the stable user identity key; keep it separate from the student's matriculation number or email.

## Architecture Style

Use a layered architecture.

The project should be organized into clear responsibility layers:

- Frontend layer: React pages, components, hooks, state, and API calls
- API layer: FastAPI routers that receive requests and return responses
- Service layer: business logic such as roadmap handling, transcript processing, student context building, and recommendation logic
- Data access/tools layer: clients and utilities for Neo4j, ChromaDB, MyCareersFuture, transcript parsing, and OpenAI
- Data layer: static JSON files, databases, uploaded files, and external APIs

Do not use a microservice architecture.

Do not split the app into multiple backend services.

Keep the backend as one FastAPI application with clear internal layers.

Use this backend flow:

```text
Router -> Service -> Client/Tool/Data -> Service -> Router
```

Use this frontend flow:

```text
Page -> Hook/Store -> API Client -> Backend -> Component UI
```

## Coding Principles

- Prefer simple, readable code over clever abstractions.
- Use clear separation of concerns.
- Routers should handle HTTP requests and responses only.
- Services should handle business logic.
- Models should define request, response, and domain data shapes.
- Clients should handle external APIs and databases.
- Utils should contain small pure helper functions.
- Use OOP selectively for stateful clients, external integrations, and cohesive services.
- Do not force classes for simple pure functions.
- Use Pydantic models for backend request and response schemas.
- When adding backend endpoints, include useful FastAPI/OpenAPI metadata such as summaries, parameter descriptions, response descriptions, examples, and expected error codes.
- Use TypeScript types or interfaces for frontend API data.
- Keep functions small and focused.
- Keep data flow explicit and easy to trace.
- Avoid hidden magic and unnecessary abstractions.
- Add comments only to explain non-obvious decisions.
- Prefer explanatory comments above a function instead of inside the function body, unless the comment explains a specific non-obvious line.
- Use one blank line between top-level function/comment blocks in project files; avoid adding two empty lines between every function.
- Build one feature at a time and avoid mixing multiple major concepts in one milestone.

## Git Workflow

- Do not work directly on `main`.
- Create a feature branch for each coherent work unit.
- A work unit can be a feature, setup task, refactor, documentation update, or part of a milestone.
- A phase or milestone does not have to map to exactly one branch.
- Before editing files, propose the branch name and explain why it matches the work being done.
- Branch names should describe the exact work being done.
- Branch names should be simple kebab-case names.
- Do not use slashes in branch names.
- Do not include milestone numbers in branch names.
- Good branch names: `fastapi-health-check`, `router-structure`, `static-roadmap-api`, `react-frontend`, `profile-page`, `transcript-upload`, `chat-stub`.
- Related small changes can be grouped into one themed branch once the foundation is stable.
- Use an umbrella branch when several mini-features support the same user-facing goal.
- Keep commits inside an umbrella branch small and logical.
- Do not mix unrelated areas in one branch.
- Good umbrella branch example: `roadmap-list-improvements` for grouping, search, and readability improvements to the roadmap course list.
- Bad umbrella branch example: one branch that mixes roadmap UI, transcript upload, database setup, and AI logic.
- Do not create commits unless I explicitly give the green light.
- When creating commits, use Conventional Commits.
- Prefer small, meaningful commits over large mixed commits.
- Do not combine multiple major developments into one commit.
- Each commit should represent one clear logical change.
- More commits are better when they make the development history easier to understand.
- Avoid redundant commits that only add noise.
- Good commit examples: `feat: add minimal FastAPI backend`, `fix: handle empty transcript uploads`, `docs: update architecture notes`, `refactor: move recommendation logic into service`, `chore: add backend dependencies`.

## Milestone Order

Follow this order unless I explicitly say otherwise.

For the high-level architecture and request flow, refer to `Diagrams.md`.

Struck-through items are complete. They are kept for history.

### Phase 1: Core App Foundation

1. ~~FastAPI health check~~
2. ~~Backend schemas and router structure~~

### Phase 2: Course Recommendation MVP

3. ~~Static roadmap API~~
4. ~~Minimal React frontend~~
5. ~~Connect frontend to roadmap API~~
6. ~~Profile page and state~~
7. ~~Transcript upload~~
8. ~~Curriculum guide upload and parsed roadmap display~~
9. ~~Basic MPE/choice-slot recommendation flow~~ (chat stub was deprioritised; recommendation engine was built instead)
10. ~~Backend-owned deterministic scoring, exact-slot assignment, career-skill mapping~~
11. ~~Offline benchmark evaluator (14 cases, nDCG ~0.705)~~
12. **NTU SSO authentication** ← next major milestone
13. Migrate user data from `localStorage` to server-side storage keyed by `oid`

### Phase 3: Recommendation Depth and Evaluation

14. Expand career coverage beyond Software Engineer
15. Counterfactual sensitivity tests
16. Coverage audit (check slot-fill rate across degree/cohort combinations)
17. Expert review / think-aloud evaluation session
18. RAGAS evaluation layer for explanation quality

### Phase 4: AI and Data Integrations (deferred)

These are intentionally deferred. Do not start them until phases 1–3 are solid.

19. ~~MyCareersFuture scraper~~ (deprioritised; static career-skill mapping is sufficient for now)
20. Neo4j client and graph loader
21. ChromaDB client
22. LangGraph state, workflow, and nodes
23. OpenAI integration for explanation generation

## Recommendation Improvement Priority

This table tracks the improvement work on the deterministic recommendation engine specifically. It overlaps with the milestones above intentionally — the milestones track feature delivery order, this table tracks scoring/ranking improvement order within the recommendation system.

| Priority | Improvement | Status |
| --- | --- | --- |
| 1 | Backend-side eligibility and per-slot ranking | ~~Done~~ |
| 2 | Structured scoring features and score breakdown | ~~Done~~ |
| 3 | Prerequisite readiness and unlock-value logic | ~~Done~~ |
| 4 | Curated course taxonomy and student preference profile | ~~Done~~ |
| 5 | Diversity-aware assignment across slots | ~~Done~~ |
| 6 | Static career-to-skill mapping | ~~Done~~ (Software Engineer only) |
| 7 | Benchmark calibration and weak-case review | In progress (`recommendation-score-calibration`) |
| 8 | Expand career-skill mapping to more career goals | Next after benchmark stabilises |
| 9 | Counterfactual sensitivity tests | After career expansion |
| 10 | RAGAS / expert review evaluation | After system is stable |
| 11 | Neo4j or graph traversal | Later — only if prerequisite/skill queries outgrow SQL |
| 12 | Embeddings or vector search | Later — only for semantic matching of messy free text |
| 13 | LLM or LangGraph | Last — for explanation generation, not core ranking |

Do not jump to Neo4j, embeddings, LangGraph, or OpenAI before career expansion, counterfactual tests, and evaluation are done.

## Current State

See `Progress.md` and `Progress2.md` for the full history. Summary of completed work:

- FastAPI backend, router/schema/service structure, PostgreSQL module catalog, faculty controls.
- Static CSC roadmap data, `GET /roadmap`, `GET /modules`, `GET /modules/filters`, `GET /modules/{code}` endpoints.
- Vite React TypeScript frontend with roadmap UI (course cards, prerequisite arrows, search, lock indicators).
- Browser-side student login/profile state using Zustand and `localStorage`.
- Transcript upload and parser (two-column layout, `EX`/`TC` treated as completed).
- Curriculum guide upload: `POST /curriculum-guide` parses PDF into roadmap-shaped data; roadmap page uses it as source of truth.
- `POST /roadmap/personalized`, `POST /roadmap/readiness`, `POST /transcript/match-curriculum` endpoints.
- Profile page: Student ID, Major, Career Goal, topic preferences, curriculum guide and transcript upload.
- Recommendation system: backend-owned deterministic scoring, exact-slot assignment, career-skill mapping layer (`backend/services/career_skill_mappings.py`), near-duplicate detection, diversity tiebreaker, planned prerequisite nodes/edges.
- Offline benchmark evaluator with 14 cases; current nDCG ~0.705.

Current branch: `recommendation-score-calibration`

Active rules and constraints:
- Keep recommendation ranking and slot allocation in the backend; frontend is a rendering layer only.
- Hard-filter before ranking: completed/fixed modules, slot fit, prerequisite feasibility, near-duplicate prior learning.
- `CE`, `CPE`, `CSC`, `CZ` course-code prefixes are excluded from recommendation candidates (hard filter, not penalty).
- Career relevance is one factor among eligibility, student interests, curriculum fit, unlock value, and diversity.
- Do not show score breakdowns in the roadmap UI unless explicitly requested.
- Do not add automated recommender tests yet.
- Do not add Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture scraping, embeddings, or ML logic yet.
- Academic-standing requirements should use completed AU from transcript, not self-declared profile year.

Current next steps (from `Progress2.md`):
- Review weak benchmark cases: `software-engineer-csc-014`, `-006`, `-008`, `-011`.
- Then: NTU SSO authentication (see section below).

## NTU SSO Authentication

**Status: Not yet implemented. This is the next major feature after benchmark review.**

NTU SSO is done via **Microsoft Azure AD** (NTU uses Microsoft 365), using the OAuth 2.0 Authorization Code flow with the `msal` Python library. Reference implementation: `NTUCourseGenie` at `/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/NTUCourseGenie/course_v2/login_utils/login_ui.py`.

### How it works

1. **App Registration**: Register an app in NTU's Azure AD tenant. Requires `APP_REG_CLIENT_ID`, `APP_REG_CLIENT_SECRET`, and `AUTHORITY` (`https://login.microsoftonline.com/<ntu-tenant-id>`).

2. **Login initiation**: Backend (or frontend redirect) calls `app.get_authorization_request_url(scopes=["User.Read"])` to get the Azure AD auth URL, then redirects the user there.

3. **Callback**: After NTU login, Azure AD redirects back to the app with `?code=<auth_code>` in the URL.

4. **Token exchange**: Backend calls `app.acquire_token_by_authorization_code(auth_code, scopes=["User.Read"])`. Returns `access_token` and `id_token_claims`.

5. **NTU email validation**: Check `"ntu.edu.sg" in id_token_claims["preferred_username"]` to reject non-NTU accounts.

6. **User identity**: Use `id_token_claims["oid"]` (Azure Object ID) as the stable unique user identifier — it never changes even if the student's email or name changes.

7. **Profile picture**: Optionally fetch from `https://graph.microsoft.com/v1.0/users/{oid}/photo/$value` with the access token.

### Key design decisions

- Use `oid` (Azure Object ID) as the primary key for the user record in the database, not the student ID or email.
- Store `email` and `name` from `id_token_claims["preferred_username"]` and `id_token_claims["name"]` as display fields only.
- Do not build a fake NTU password form, scrape NTU login pages, or hardcode captured SAML/auth URLs.
- Do not use SAML unless NTU specifically provides a SAML metadata URL; prefer OIDC/OAuth via Azure AD.
- The `oid` is stable across devices and sessions: the same student logging in from any device gets the same `oid`, enabling cross-device persistence.

### How user data persists across sessions and devices

The `oid` from Azure AD is the anchor. It is stable forever — the same value is returned every time the same student logs in, from any device or browser.

**Why `oid` and not email or student ID:**

| Identifier | Problem |
|---|---|
| Email | Can change (graduation, name change) |
| Student/matric number | Not reliably exposed as an OIDC claim |
| `oid` | Stable forever, unique per user per tenant, same on every device |

**Session token flow:**

After the OAuth code exchange succeeds, the FastAPI backend should:
1. Verify the `oid` from `msal` token claims.
2. Look up or create the user record in the database by `oid`.
3. Issue its own JWT (or signed httpOnly cookie) with the `oid` embedded.
4. Return that JWT to the frontend.

The frontend sends the JWT on every API request. The Azure access token is used once to verify identity and never sent to the frontend.

```
First login (any device):
  Azure returns oid → backend checks DB → not found → create user record → issue JWT

Any later login (same or different device):
  Azure returns same oid → backend finds existing record → issue JWT with their data
```

**Current state vs. after SSO:**

- Right now the app uses `localStorage` with a self-declared Student ID.
- After SSO: the Student ID field goes away; `oid` is the identity.
- All profile, curriculum, transcript, and recommendation data moves to server-side storage keyed by `oid`.
- `localStorage` becomes a UI cache only (e.g., last active tab), not a data store.
- A student logging in on a phone gets the exact same state as on their laptop.

**Watch out for multiple Azure AD tenants:** NTU may have separate tenants for students and staff. Pin the `AUTHORITY` URL to the student tenant so non-NTU Microsoft accounts are rejected at the tenant level, before the email check.

### Required env vars

```
APP_REG_CLIENT_ID=<azure app registration client id>
APP_REG_CLIENT_SECRET=<azure client secret>
AUTHORITY=https://login.microsoftonline.com/<ntu-tenant-id>
```

### Rules for implementation

- Use Microsoft MSAL (`msal` Python package) for the backend token exchange.
- The FastAPI backend should own the OAuth callback endpoint (e.g., `GET /auth/callback`).
- Issue a server-side session token (e.g., JWT or opaque token stored in an httpOnly cookie) after the token exchange succeeds; do not pass the Azure access token to the frontend.
- Keep the app's internal user ID (`oid`) separate from the student's matriculation number.
- The student's matriculation number may be derivable from their NTU email but should not be treated as a stable identity key.

## Recommendation Evaluation

### Current approach

The current offline benchmark uses a hand-reviewed set of 14 cases evaluated with precision@k, nDCG@k, explanation coverage, explanation fidelity, skill-area diversity, old-code exposure, and constraint validity. This is deterministic and fast but relies entirely on manually reviewed labels.

### RAGAS eval framework

Explore using **RAGAS** (`ragas` Python package) for a more structured evaluation layer. RAGAS was designed for RAG pipelines but its metrics transfer well to recommendation systems with LLM-generated explanations:

- **Faithfulness**: does the recommendation explanation only make claims supported by the student's actual profile and curriculum data?
- **Answer relevancy**: does the recommended module actually address the student's career goal and topic preferences?
- **Context precision / recall**: are the right signals (career-skill mappings, prerequisite chain, student preferences) being used and weighted correctly?

RAGAS needs a dataset of `(question, context, answer, ground_truth)` tuples. For this system that maps to `(student profile, curriculum + career-skill context, recommended modules + explanation, reviewed positive labels)`.

Reference implementation in a past FYP: `/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/NTUCourseGenie/course_v2/ragas_eval/`

### Other evaluation approaches to explore

| Approach | What it measures | When to use it |
|---|---|---|
| **Offline benchmark (current)** | Precision@k, nDCG@k against hand-reviewed labels | Fast iteration; catches ranking regressions |
| **RAGAS** | Faithfulness and relevancy of LLM-generated explanations | Once explanations become a key output |
| **A/B or interleaving test** | Which ranking produces more clicks/accepts from real users | If real NTU students use the system |
| **Expert review / think-aloud** | Whether a knowledgeable person (supervisor, senior student) agrees with the top recommendations | Good for FYP evaluation chapter; low sample count is fine |
| **Counterfactual sensitivity** | Does changing career goal, completed modules, or preferences actually shift the ranked list in a sensible direction? | Catches cases where scoring is correct on average but insensitive to meaningful input changes |
| **Coverage audit** | What fraction of valid MPE/BDE slots can the system fill with at least one eligible recommendation? | Ensures the system does not silently leave slots empty for certain degree/cohort combinations |
| **Constraint validity (current)** | Are all hard rules (no old codes, no completed modules, slot type match) always satisfied? | Keep as a required pass on every benchmark run |

### Rules

- Do not replace the current offline benchmark with RAGAS; add it alongside as a complementary layer.
- Expert review is the most credible evaluation for an undergraduate FYP and should be included in the final report.
- Counterfactual sensitivity tests can be written as simple assertion scripts without a full test suite.
- Do not build the RAGAS or A/B evaluation layer until the recommendation system itself is stable.

## Expected Working Directory

Always work inside:

```text
/Users/zacklau/Desktop/y4s1/fyp/fyp_course_recommendation
```

## Reference Files From Past FYP Repos

Use these only when needed:

```text
/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/NTUCourseGenie/
/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/CourseNavigator/
/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/shing-hao/
```

## Communication Style

When helping me, be structured but not overwhelming.

Use this format after each milestone:

```text
What was created
How it works
How to run it
What is not included yet
Next step
```

If I seem confused, stop adding code and explain the current state.

## First Instruction For Any New AI Session

If this is the first time an AI assistant is working in this repo, start by reading this file.

Then read these files before proposing work:

```text
Diagrams.md
Mistakes.md
Progress.md
README.md
```

Then do only this:

- Run `git status --short --branch`.
- Continue from the latest section in `Progress.md`.
- Before editing files, propose the branch name, planned files, test plan, and what is intentionally out of scope.
- Do not create commits unless explicitly told to.
