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

Status: Complete

### Completed

- Added the ReactFlow package through `@xyflow/react`.
- Added a `RoadmapGraph` component.
- Converted roadmap courses into graph nodes.
- Converted roadmap prerequisite links into graph edges.
- Added a simple manual layout based on year and semester.
- Rendered the graph alongside the existing summary and searchable course list.
- Opened and merged PR #9.

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

## Roadmap Graph Readability

Status: Implemented locally

### Completed

- Marked the roadmap visualization foundation as complete after PR #9.
- Added `Frontend_design.md` with project-specific frontend reference guidance.
- Recorded the old frontend as a visual and behavior reference only.
- Shifted the roadmap UI toward the old dark `NTU Course Recommender` style.
- Increased graph node spacing.
- Added clearer node labels with course code, academic units, and title.
- Set graph nodes to connect from left to right.
- Styled graph edges with smooth lines and arrow markers.
- Improved the graph container height, border, radius, and background.
- Added hover emphasis for connected roadmap courses and prerequisite arrows.
- Added a semester-based roadmap component that groups courses by year and semester.
- Added course cards with course code, title, type, AU, and checkbox-style completion indicators.
- Added curved SVG prerequisite arrows behind the course cards.
- Added an `All arrows` toggle for prerequisite arrow visibility.
- Switched the main app view from `RoadmapGraph` to `SemesterRoadmap`.
- Added frontend-only checkbox toggling for completed courses.
- Added a light/dark theme toggle with a moon icon.
- Refined hover behavior so unrelated arrows disappear while connected arrows stay sharp and visible.
- Adjusted hover layering so active arrows render above faded cards while connected cards stay on top.
- Set emphasized prerequisite arrows to clear white with no glow for the current dark-mode pass.

### Verified

- Frontend build passes.
- Frontend lint passes.
- Browser shows the `NTU Course Recommender` header.
- Browser shows the semester-based roadmap layout.
- Browser shows course cards grouped by year and semester.
- Browser supports light and dark roadmap themes.
- Browser hover behavior keeps only connected arrows visible.

### Not Included

- `RoadmapGraph` and ReactFlow are still kept for now as a possible future reference.
- Completed-course checkbox state is frontend-only and resets on refresh.
- No personalized roadmap generation yet.
- No profile-specific completed course state yet.
- No backend, database, recommendation, or AI changes.

## Profile Page and State

Status: Complete

### Completed

- Installed Zustand for global state management.
- Created `useProfileStore` with the `persist` middleware to track student profile (normalized Student ID, Major, Year, Semester) and completed course IDs across page reloads.
- Updated `SemesterRoadmap.tsx` to read and toggle completed courses via the global store instead of local component state.
- Created a `ProfilePage` component with a form to view and edit student details, including Student ID and Major, as well as a stats card showing the number of completed courses.
- Updated `App.tsx` with a top navigation bar to switch between the "Roadmap" and "Profile" views.
- Styled the Profile page to match both dark and light modes.

### Verified

- Frontend build and lint passes.
- Zustand store persists data to `localStorage`.
- Completing a course in the Roadmap instantly updates the count on the Profile page.
- Modifying profile details on the Profile page persists through reloads.
- Navigation correctly switches between views.

### Not Included

- No backend changes or persistence for user profiles (everything is frontend `localStorage` for now).
- No actual course recommendation logic yet.
- No transcript upload or automated course extraction yet.

## Browser Login Page

Status: Implemented locally

### Completed

- Added a frontend-only login/onboarding screen.
- Used the existing persisted Student ID as the temporary browser-side user identity.
- Gated the main Roadmap/Profile application behind Student ID entry.
- Kept this as browser persistence only, without backend authentication or database persistence.

### Not Included

- No password-based login.
- No backend user table.
- No authentication session, JWT, or cookie handling.

## Current Handoff

Status: Ready for next work

### Current App State

- Backend has `GET /health` and `GET /roadmap`.
- Frontend asks first-time browser users for Student ID before showing the main app.
- Frontend loads roadmap data and manages user profile state using Zustand with `localStorage` persistence.
- Frontend includes navigation tabs for Roadmap and Profile pages.
- Roadmap courses can be toggled as completed, syncing with the global profile store.

### Next Recommended Work

- Implement transcript upload and completed course extraction (Milestone 7), or
- Begin working on the Chat stub (Milestone 8).

### Onboarding For Next Session

- Read `AGENTS.md`, `Diagrams.md`, `Mistakes.md`, `Progress.md`, and `README.md`.
- Run `git status --short --branch`.
- Propose a branch name and plan before editing files.
- Avoid adding Neo4j, ChromaDB, LangGraph, OpenAI, transcript upload, or recommendation logic until the simpler frontend roadmap flow is understood.
