# Progress

This file tracks what has been completed during the rebuild.

## FastAPI Health Check

Status: Complete

### Completed

- Read `AGENTS.md` for rebuild rules, architecture style, coding principles, branch workflow, and milestone order.
- Read `Diagrams.md` for the high-level architecture and request flow.
- Proposed and used the branch name `fastapi-health-check`.
- Created the minimal backend folder structure.
- Added `backend/main.py` with a FastAPI app and `/health` endpoint.
- Added `backend/requirements.txt` with FastAPI and Uvicorn dependencies.
- Updated `README.md` with setup, run, and health check instructions.
- Updated `.gitignore` to ignore `.venv/`, `.env`, and Python cache files.
- Created a local `.venv` virtual environment.
- Installed backend dependencies into `.venv`.
- Started the FastAPI development server.
- Tested `GET /health` successfully.
- Committed the backend health check work.
- Opened and merged PR #1.

### Verified

```json
{"status":"ok"}
```

### Notes

- `.env.example` was removed because it is not needed yet.
- Router files, services, models, frontend, database code, and AI integrations were intentionally not included in this first backend change.

## Router And Schema Structure

Status: Complete

### Completed

- Create a dedicated health router.
- Create a Pydantic response schema for the health check.
- Keep the `/health` response unchanged.
- Keep business logic, database code, frontend code, and AI integrations out of this change.
- Committed the router and schema structure.
- Opened and merged PR #2.

### Verified

```json
{"status":"ok"}
```

## Static Roadmap API

Status: Complete

### Completed

- Added static CSC roadmap data in `data/csc_roadmap.json`.
- Added roadmap response schemas.
- Added a roadmap service that reads the static JSON file.
- Added `GET /roadmap`.
- Included the roadmap router in the FastAPI app.
- Verified `GET /roadmap` returns 29 nodes and 22 edges.
- Verified `GET /health` still returns `{"status":"ok"}`.
- Committed the static CSC roadmap data.
- Committed the static CSC roadmap endpoint.
- Opened and merged PR #3.

### Not Included

- No frontend roadmap visualization yet.
- No student-specific filtering yet.
- No recommendation logic yet.
- No database or graph integration yet.

## Minimal React Frontend

Status: Complete

### Completed

- Created a Vite React TypeScript frontend in `frontend/`.
- Simplified the generated starter app to a plain placeholder page.
- Added frontend ignore rules for dependency and build output folders.
- Installed frontend dependencies.
- Verified the production build.
- Verified lint passes with zero warnings and errors.
- Verified the dev server renders the placeholder page.
- Updated the root `README.md` with frontend setup and run instructions.
- Removed the generated frontend README.
- Kept frontend ignore rules centralized in the root `.gitignore`.
- Committed the frontend setup, README update, and ignore-rule cleanup.
- Opened and merged PR #4.

### Verified

```text
FYP Course Recommendation
Frontend is running.
```

### Not Included

- No frontend design system yet.
- No backend API calls yet.
- No roadmap visualization yet.
- No Material-UI, ReactFlow, Zustand, TanStack Query, or Axios yet.

## Connect Frontend To Roadmap API

Status: Complete

### Completed

- Add a small frontend API function to call `GET /roadmap`.
- Add TypeScript types matching the roadmap response.
- Display a simple text summary of the roadmap data.
- Keep the UI plain and avoid adding design libraries.
- Add CORS config so the Vite frontend can call the FastAPI backend in development.
- Update the README with a note to run both backend and frontend.
- Verified the frontend displays roadmap data from the backend.
- Committed the frontend-roadmap connection.
- Opened and merged PR #5.

### Verified Display

```text
Roadmap loaded
Courses: 29
Prerequisite links: 22
First course: SC1003
```

## Roadmap Course List

Status: Complete

### Completed

- Added a frontend `CourseList` component.
- Displayed each roadmap course with code, title, year, semester, academic units, and type.
- Kept the UI plain without adding visualization or design libraries.
- Verified the frontend renders the roadmap course list in the browser.
- Committed the course list work.
- Opened and merged PR #6.

### Verified Display

```text
Course List
SC1003 - Introduction to Computational Thinking and Programming
Year 1, Semester 1 - 3 AU - Core
```

### Not Included

- No ReactFlow graph yet.
- No profile-specific completed course state yet.

## Roadmap List Improvements

Status: Complete

### Completed

- Clarified the themed umbrella branch workflow in `AGENTS.md`.
- Grouped roadmap courses by year and semester.
- Added simple course search by course code or title.
- Improved plain course list readability with spacing, separators, muted metadata, and an empty state.
- Added explanatory comments to backend roadmap loading and frontend roadmap list code.
- Kept changes frontend-only except for documentation.
- Opened and merged PR #8.

### Verified

- Frontend build passes.
- Frontend lint passes.
- Browser shows semester groups.
- Searching `SC1003` filters to the matching course.
- Searching a non-matching term shows `No courses found.`

### Not Included

- No Material-UI yet.
- No backend changes.
- No profile-specific completed course state yet.

## Roadmap Visualization Foundation

Status: Implemented locally

### Completed

- Added the ReactFlow package through `@xyflow/react`.
- Added a `RoadmapGraph` component.
- Converted roadmap courses into graph nodes.
- Converted roadmap prerequisite links into graph edges.
- Added a simple manual layout based on year and semester.
- Rendered the graph alongside the existing summary and searchable course list.

### Verified

- Frontend build passes.
- Frontend lint passes.
- Browser shows the `Roadmap Graph` section.
- Browser shows ReactFlow controls, confirming the graph is mounted.

### Not Included

- No advanced graph layout yet.
- No custom node design yet.
- No profile-specific completed course state yet.
- No backend, database, recommendation, or AI changes.

## Current Handoff

Status: Ready for next work

### Current App State

- Backend has `GET /health` and `GET /roadmap`.
- Frontend loads roadmap data from the backend.
- Frontend displays a roadmap summary, basic graph, and grouped searchable course list.
- Markdown onboarding files are now intended to be tracked in Git.

### Next Recommended Work

- Review and merge roadmap visualization foundation, or
- Improve graph layout and node readability.

### Onboarding For Next Session

- Read `AGENTS.md`, `Diagrams.md`, `Mistakes.md`, `Progress.md`, and `README.md`.
- Run `git status --short --branch`.
- Propose a branch name and plan before editing files.
- Avoid adding Neo4j, ChromaDB, LangGraph, OpenAI, transcript upload, or recommendation logic until the simpler frontend roadmap flow is understood.
