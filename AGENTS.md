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
- Job-market-aware recommendations using a permitted source, with MyCareersFuture as a candidate
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

For the high-level architecture and diagrams, refer to [Diagrams.md](docs/architecture/Diagrams.md).

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
- When creating commits, use Conventional Commits format: `<type>: <description>`.
- Prefer small, meaningful commits over large mixed commits.
- Do not combine multiple major developments into one commit.
- Each commit should represent one clear logical change.
- More commits are better when they make the development history easier to understand.
- Avoid redundant commits that only add noise.
- Good commit examples: `feat: add minimal FastAPI backend`, `fix: handle empty transcript uploads`, `docs: update architecture notes`, `refactor: move recommendation logic into service`, `chore: add backend dependencies`.

## Current State And Planning

- Read [docs/STATUS.md](docs/STATUS.md) for current capabilities, evidence boundaries, priorities, and deferred work. Update that file after a coherent work unit; replace outdated status rather than appending history.
- Read [docs/plans/Development_Plan.md](docs/plans/Development_Plan.md) when milestone order, SSO design, or future evaluation planning is relevant. Do not start deferred integrations before the agreed prerequisite work is complete.
- Follow the dependency-based plan without calendar deadlines: baseline/policy, student skills picture, job-market evidence, pathway chat, combined evaluation, then SSO and server persistence. The initial improvement pilot targets Software Engineer and Data Engineer; retain the other supported careers.
- Read [docs/progress/README.md](docs/progress/README.md) to find the active progress log. Consult older logs only when their historical context is relevant.
- Preserve closed progress logs as historical records. Old branch names, paths, and metrics in those logs describe their original work, not the current session.
- Get the actual branch from Git; do not infer it from a documentation snapshot.

## Recommendation Constraints

- Keep recommendation ranking and slot allocation in the backend; the frontend renders results.
- Hard-filter before ranking: completed/fixed modules, slot fit, prerequisite feasibility, and near-duplicate prior learning.
- Exclude `CE`, `CPE`, `CSC`, and `CZ` course-code prefixes from recommendation candidates as a hard filter.
- Career relevance is one factor alongside eligibility, student interests, curriculum fit, unlock value, and diversity.
- Approved weak-fit direction: recommend strong career matches, offer useful explicit interest matches as labelled interest alternatives, and otherwise leave slots open with an explanation. This direction still requires baseline review and implementation; do not assume current score thresholds enforce it.
- Do not optimize for slot fill alone or infer strong career relevance from structural/faculty bonuses. Eligibility applies to all recommendation types; choose career/interest thresholds only after reviewing evidence.
- Treat transcript-derived skills as likely prior learning, not verified mastery. Ground course-skill and future job-skill mappings in source evidence.
- Do not show score breakdowns in the roadmap UI unless explicitly requested.
- Do not add automated recommender tests yet. Existing benchmark, coverage, and counterfactual scripts remain the evaluation tools.
- Use completed AU from the transcript for academic-standing requirements, not self-declared profile year.
- During baseline/policy work, do not add Neo4j, ChromaDB, LangGraph, OpenAI, job scraping, embeddings, or ML logic. Later integrations follow the development plan and separate work-unit approval.
- Verify job-data collection, storage and reuse permissions before integration; do not assume an accessible endpoint is an authorized public API or build around unauthorized LinkedIn scraping.
- Keep future pathway chat grounded in recommendation evidence. Confirm preference changes before applying them and have the backend recalculate; LLM-controlled scoring is not part of the pilot.
- Do not change benchmark labels without explicit course-content evidence or supervisor / TA review. Do not tune constants solely to improve draft-label metrics.
- Preserve frozen Software Engineer benchmark cases 001-005 unchanged; record review findings and new scenarios separately.
- Add RAGAS alongside the offline benchmark only after the recommendation system is stable and explanation evaluation warrants it. Expert review remains the next evaluation priority.

## Project Skills And Pull Requests

- For PR preparation, creation, or updates, read [.agents/skills/create-project-pr/SKILL.md](.agents/skills/create-project-pr/SKILL.md).
- Use the single shared [PR template](docs/workflows/PR_template.md); do not duplicate it inside the skill.
- PR titles and commits use `<type>: <short lowercase description>`. Do not mention milestones in commits, PR titles, or PR bodies.
- Read the template for every PR, use its exact headings, assign the PR to `@me` unless otherwise requested, and verify title, body, assignees, and URL before reporting completion.
- Creating a skill or preparing a PR does not authorize commits, pushes, or PR publication. Honor authorization already given in the conversation.

## Expected Working Directory

Work inside the active checkout:

```text
/Users/bytedance/Desktop/fyp_course_recommendation
```

Treat the reference repo as read-only. Older `/Users/zacklau/...` paths in planning and history are reference locations, not the working directory; verify availability before using them.

## Communication Style

Keep explanations structured, beginner-friendly, and manageable. After each milestone, explain:

```text
What was created
How it works
How to run it
What is not included yet
Next step
```

If the user seems confused, stop adding code and explain the current state.

## First Instruction For Any New AI Session

Start by reading this file, then:

1. Run `git status --short --branch`.
2. Read [docs/STATUS.md](docs/STATUS.md).
3. Read [docs/README.md](docs/README.md), [docs/Mistakes.md](docs/Mistakes.md), and [README.md](README.md).
4. Read [docs/architecture/Diagrams.md](docs/architecture/Diagrams.md).
5. Read [docs/progress/README.md](docs/progress/README.md), then the latest section of the active progress log.
6. Read other documents only when relevant to the requested work.

Before editing, propose the branch name, planned files, verification, and intentionally excluded work. Stay on an existing branch when the user explicitly requests it. Do not create commits unless explicitly authorized.
