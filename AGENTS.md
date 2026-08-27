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

### Phase 1: Core App Foundation

1. FastAPI health check
2. Backend schemas and router structure

### Phase 2: Course Recommendation MVP

3. Static roadmap API
4. Minimal React frontend
5. Connect frontend to roadmap API
6. Profile page and state
7. Transcript upload
8. Curriculum guide upload and parsed roadmap display
9. Chat stub

### Phase 3: AI and Data Integrations

10. Basic MPE/choice-slot recommendation flow
11. MyCareersFuture scraper
12. Skill extractor
13. Neo4j client
14. Graph loader
15. ChromaDB client
16. LangGraph state, workflow, and nodes
17. Replace chat stub with LangGraph
18. OpenAI integration

## Current State

Completed foundations:

- FastAPI backend with `GET /health`.
- Backend router, schema, and service structure.
- Static CSC roadmap data in `data/test_csc_roadmap.json`.
- Backend `GET /roadmap` endpoint.
- Minimal Vite React TypeScript frontend.
- Frontend API call to `GET /roadmap`.
- Semester roadmap UI with course cards, prerequisite arrows, search, and completed-course state.
- Roadmap visually marks prerequisite-blocked courses with locked styling and missing prerequisite codes.
- Browser-side student login/profile state using Zustand and `localStorage`.
- Transcript upload endpoint and frontend upload UI for marking completed roadmap courses.
- Transcript parser handles two-column transcript layouts and treats `EX` and `TC` as completed.
- Profile page shows separate counts for completed roadmap courses, completed transcript modules, and unmatched transcript modules.
- Profile page shows latest transcript upload details for matched roadmap courses and unmatched transcript module codes.
- PostgreSQL module catalog data seeded from static module JSON files.
- Backend module catalog API with `GET /modules`, `GET /modules/filters`, and `GET /modules/{code}`.
- Module descriptions seeded from `data/course_catalog.json` where available.
- Faculty activation controls through a `faculties` table and `/faculties` API endpoints.
- Frontend NTU Modules page with search, filters, pagination, module detail overlay, and persisted tab/filter state.
- Backend `POST /curriculum-guide` endpoint parses the CSC AY2023-24 curriculum guide PDF into roadmap-shaped data.
- Frontend Profile page can upload a curriculum guide PDF and stores the parsed guide in browser state per active Student ID.
- Frontend Roadmap page now uses the uploaded curriculum guide as the student roadmap source of truth.
- Roadmap page shows an empty state instead of the static roadmap when the active profile has no uploaded curriculum guide.
- Roadmap page includes a `Clear roadmap` action that removes the uploaded curriculum guide while keeping transcript results saved.
- Profile page stores career goal through a dropdown for future MPE/choice-slot recommendation work.
- Roadmap lock indicators now handle uploaded curriculum prerequisite text, including text-only requirements such as `Year 4 standing`.

Current next step:

- Continue from `Progress.md`.
- Improve roadmap eligibility for text-only academic-standing requirements.
- Use `profile.yearOfStudy` to unlock requirements like `Year 4 standing` when the active profile is in Year 4 or above.
- Keep polishing the roadmap/profile flow before starting unrelated milestones.
- Do not add Neo4j, ChromaDB, LangGraph, OpenAI, or advanced recommendation logic yet.

## Expected Working Directory

Always work inside:

```text
/Users/bytedance/Desktop/fyp_course_recommendation
```

## Reference Files From Old Repo

Use these only when needed:

```text
/Users/bytedance/Desktop/course-recommendation-system/backend/main.py
/Users/bytedance/Desktop/course-recommendation-system/backend/routers/
/Users/bytedance/Desktop/course-recommendation-system/backend/models/schemas.py
/Users/bytedance/Desktop/course-recommendation-system/backend/db/
/Users/bytedance/Desktop/course-recommendation-system/backend/agents/
/Users/bytedance/Desktop/course-recommendation-system/backend/pipeline/
/Users/bytedance/Desktop/course-recommendation-system/backend/utils/
/Users/bytedance/Desktop/course-recommendation-system/frontend/src/
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
