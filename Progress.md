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

Status: Complete

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

Status: Complete

### Completed

- Added a frontend-only login/onboarding screen.
- Used the existing persisted Student ID as the browser-side user identity.
- Store profile records by Student ID so one browser can remember more than one profile.
- Gated the main Roadmap/Profile application behind Student ID entry.
- Added logout support to clear only the active user and return to the login screen.
- Kept this as browser persistence only, without backend authentication or database persistence.

### Verified

- Frontend lint passes.
- Frontend build passes.
- Student ID login validates the entered ID before activating a profile.
- Logout returns to the login screen without deleting browser-saved profile records.

### Not Included

- No password-based login.
- No backend user table.
- No authentication session, JWT, or cookie handling.

## Transcript Upload

Status: Implemented locally

### Completed

- Added a backend `POST /transcript` endpoint that accepts official PDF transcripts.
- Added PyMuPDF for PDF text extraction.
- Added transcript row parsing based on `Code`, `Course`, `AU`, `Grade`, and `Grade Point`.
- Treats `EX` and `TC` as completed, like letter-graded passed modules.
- Improved transcript parsing for two-column transcript layouts where course titles can wrap across lines.
- Filters parsed transcript courses against the static CSC roadmap.
- Returns both roadmap-matched completed courses and the total number of completed modules parsed from the transcript.
- Added frontend transcript upload UI on the Profile page.
- Updates completed roadmap courses in the active browser profile after upload.
- Shows separate Profile stats for completed roadmap courses, completed transcript modules, and unmatched transcript modules.
- Shows the latest transcript upload details, including matched roadmap courses and unmatched transcript module codes.

### Verified

- Backend compiles successfully.
- Transcript extraction service parses generated PDF text rows.
- `POST /transcript` returns completed roadmap courses from a sample PDF.
- `EX` grades are returned as completed courses with no grade point.
- `TC` grades are returned as completed transcript modules.
- Wrapped rows such as `SC1015` in a two-column transcript are parsed correctly.
- Frontend lint passes.
- Frontend build passes.
- Profile page shows the latest matched and unmatched transcript upload details after refresh.

### Not Included

- No OCR for scanned/image-only PDFs yet.
- No backend database persistence yet.
- No recommendation logic yet.

## Roadmap Data Path Update

Status: Implemented locally

### Completed

- Updated the static roadmap service to read `data/test_csc_roadmap.json`.
- Kept the existing `GET /roadmap` endpoint contract unchanged.
- Preserved the current static-roadmap approach while recommendation logic is not implemented yet.

### Verified

- Backend compile check passes.
- Roadmap service loads 29 nodes and 22 edges from `data/test_csc_roadmap.json`.

### Not Included

- No personalized roadmap generation yet.
- No recommendation logic yet.
- No Neo4j, ChromaDB, LangGraph, or OpenAI integration.

## Roadmap Locked Prerequisite Indicators

Status: Implemented locally

### Completed

- Added frontend-only roadmap eligibility logic using completed roadmap course IDs and each course's prerequisite list.
- Visually marks only prerequisite-blocked roadmap courses instead of adding extra labels to completed or available courses.
- Shows a `Locked` chip and a `Missing: ...` line for courses with incomplete prerequisites.
- Uses a muted grey locked-course style in light mode and a clearer muted red locked-course style in dark mode.
- Keeps locked courses manually checkable for now so transfer credits, exemptions, exchange modules, and special approvals are still possible.

### Verified

- Frontend diagnostics return no issues.
- Frontend build passes.

### Not Included

- No backend changes.
- No recommendation logic.
- No hard blocking of locked course checkboxes.
- No Neo4j, ChromaDB, LangGraph, or OpenAI integration.

## Current Handoff

Status: Ready for next work

### Current App State

- Backend has `GET /health` and `GET /roadmap`.
- Frontend asks first-time browser users for Student ID before showing the main app.
- Frontend loads roadmap data and manages profile records by Student ID using Zustand with `localStorage` persistence.
- Frontend includes navigation tabs for Roadmap and Profile pages.
- Roadmap courses can be toggled as completed, syncing with the global profile store.
- Roadmap includes a "Clear completed" action to uncheck all completed courses for the active profile.
- Roadmap visually marks prerequisite-blocked courses with locked styling and missing prerequisite codes.
- Profile page can upload an official PDF transcript and auto-mark completed roadmap courses.
- Profile page shows separate counts for matched roadmap courses, completed transcript modules, and unmatched transcript modules.
- Profile page lists the latest matched roadmap courses and unmatched transcript module codes from transcript upload.

### Next Recommended Work

- Review and merge the roadmap locked-prerequisite indicator branch, or
- Continue polishing the roadmap/profile flow before starting chat or recommendation work.

### Onboarding For Next Session

- Read `AGENTS.md`, `Diagrams.md`, `Mistakes.md`, `Progress.md`, and `README.md`.
- Run `git status --short --branch`.
- Propose a branch name and plan before editing files.
- Avoid adding Neo4j, ChromaDB, LangGraph, OpenAI, transcript upload, or recommendation logic until the simpler frontend roadmap flow is understood.

## PostgreSQL Module Catalog API

Status: Implemented locally

### Completed

- Created the `modules-catalog-page` branch for module catalog backend and frontend work.
- Added backend module response schemas for module summaries, paginated module lists, and filter option lists.
- Added a module catalog service that reads from PostgreSQL instead of exposing the full JSON dataset to the browser.
- Added `GET /modules` for paginated module listing with optional `search`, `faculty`, `level`, `category`, `current_only`, `limit`, and `offset` query parameters.
- Added `GET /modules/filters` so the frontend can populate filter dropdowns from real database values.
- Added `GET /modules/{code}` for exact module detail lookup with prerequisites and unlocks.
- Added database error handling so module endpoints return `503` when PostgreSQL cannot serve module data.
- Added comments above functions in the new module API files to explain their purpose.
- Added detailed Swagger/OpenAPI metadata for the module endpoints, including summaries, parameter descriptions, response descriptions, example response payloads, and expected error codes.
- Updated the FastAPI app title, description, and version so `/docs` is clearer for backend API review.
- Added Pydantic `model_config` examples to module response schemas so Swagger shows realistic expected outputs.
- Added module description enrichment to the seed script using `data/course_catalog.json` where descriptions are available.
- Added a `module_prerequisites` table to store prerequisite relationships while deriving unlocks through reverse lookup.

### Verified

- Backend compile check passes.
- FastAPI OpenAPI schema generation passes.
- Service-level checks can list modules, fetch exact module details, and load filter options.
- Seed script populates 4317 modules, 4178 prerequisite relationships, and available course descriptions.
- HTTP checks pass for `GET /modules`, `GET /modules/filters`, and exact module lookup.

### Not Included

- No timetable day/time filters because timetable data is not stored yet.
- No recommendation logic, Neo4j, ChromaDB, LangGraph, or OpenAI integration.

## Frontend Module Catalog Page

Status: Implemented locally

### Completed

- Added frontend TypeScript types for module summaries, paginated module lists, filter options, and query parameters.
- Added a frontend modules API client that calls the backend instead of loading static JSON directly in the browser.
- Added an `NTU Modules` page with search, faculty filter, level filter, category filter, availability filter, and pagination.
- Added module cards that show code, title, AU, faculty, latest semester, categories, prerequisite count, and unlock count.
- Added a module detail overlay that opens from a module card and closes through the close button, Escape key, or outside click.
- Refined the modules layout based on `Frontend_design.md` and removed the oversized count card.
- Improved readability for `requires` and `unlocks` chips in light and dark themes.
- Added navigation to switch between Roadmap, Modules, and Profile.
- Persisted the selected app tab in `localStorage` so refresh keeps the current tab.
- Persisted module search/filter/page state in `localStorage` so refresh keeps the current catalogue view.

### Verified

- Frontend build passes with `npm run build`.
- Browser loads module data through backend API calls.
- Module detail opens as a popup overlay instead of an inline panel.
- Refresh keeps the selected tab and active module filters.

### Not Included

- No Material-UI migration yet.
- No timetable filtering yet.
- No recommendation/chat logic on the module cards yet.

## Faculty Activation Controls

Status: Implemented locally

### Completed

- Added a `faculties` table with `name` and `is_active` columns.
- Seeded the `faculties` table from distinct module faculty values.
- Defaulted `CSC` and `CE` to active for the current MVP scope while preserving existing faculty status values on reruns.
- Added backend schemas, service logic, and routes for faculty activation management.
- Added `GET /faculties`, `GET /faculties/active`, and `GET /faculties/inactive`.
- Added `PATCH /faculties/status` to set all faculties active or inactive.
- Added `PATCH /faculties/{name}/activate` and `PATCH /faculties/{name}/deactivate`.
- Added `409 Conflict` handling when activating an already active faculty or deactivating an already inactive faculty.
- Updated the module catalogue service to filter modules by active faculties from PostgreSQL instead of a hardcoded list.
- Updated Swagger/OpenAPI documentation for the new faculty endpoints and active-faculty module filtering.

### Verified

- Backend compile check passes.
- Seed script creates 34 faculty rows.
- Active faculties default to `CE` and `CSC`.
- `/modules` and `/modules/filters` only use active faculties.
- Duplicate activate/deactivate service calls raise the expected conflict errors.

### Not Included

- No frontend admin UI for changing faculty active status yet.
- No authentication or authorization around the faculty management endpoints yet.
- No database migration tool yet; local table creation still uses `Base.metadata.create_all`.

## Curriculum Guide Upload Backend

Status: Implemented locally

### Completed

- Renamed the current branch to `curriculum-guide-upload` because the work now includes implementation, not only documentation.
- Updated `AGENTS.md` so future work treats uploaded curriculum guides as the source of truth for personalised roadmap display.
- Added the sample CSC AY2023-24 curriculum guide PDF at `data/ccds_ay23-24_csc.pdf`.
- Added backend curriculum guide response schemas for parsed courses, semesters, prerequisite edges, and the full parsed guide response.
- Added a backend curriculum parser service that extracts positioned PDF words with PyMuPDF.
- Added first-pass parsing for the current CSC curriculum guide format by detecting semester headers, course rows, course titles, academic units, prerequisites, and choice slots.
- Marks `SC3xxx`, `SC4xxx`, `BDE`, and rows with choice wording as choice slots for future MPE/elective recommendation work.
- Added `POST /curriculum-guide` to accept a curriculum guide PDF and return roadmap-shaped data.
- Registered the curriculum guide router in the FastAPI app.

### Verified

- Backend compile check passes.
- Direct parser check returns `Computer Science`, `AY2023-24`, `135` total AU, 8 semesters, 44 roadmap rows, and 19 prerequisite edges from `data/ccds_ay23-24_csc.pdf`.
- HTTP check for `POST /curriculum-guide` returns `200 OK` with parsed curriculum JSON.
- Frontend and backend diagnostics return no issues.

### Not Included

- No frontend curriculum guide upload UI yet.
- No Roadmap page changes yet.
- No browser profile persistence for parsed curriculum guides yet.
- No transcript-to-uploaded-curriculum rematching yet.
- No MPE/choice-slot recommendation scoring yet.
- No universal parser for every NTU curriculum guide layout.
- No Neo4j, ChromaDB, LangGraph, or OpenAI integration.

## Curriculum Guide Frontend Flow

Status: Implemented locally

### Completed

- Added frontend curriculum guide types matching the backend `POST /curriculum-guide` response.
- Added a frontend API client for uploading curriculum guide PDFs.
- Extended the browser profile store to persist career goal, uploaded curriculum guide data, uploaded curriculum filename, and raw completed transcript course codes per active Student ID.
- Updated transcript storage so transcript-only uploads are saved without requiring a curriculum guide.
- Added local matching that maps completed transcript course codes to uploaded curriculum guide rows when a curriculum guide exists.
- Added curriculum guide upload controls to the Profile page.
- Added a career goal field to the Profile page for future MPE/choice-slot recommendations.
- Updated the Roadmap page so it no longer loads or displays the static roadmap by default.
- Added a Roadmap empty state that asks the student to upload a curriculum guide before showing roadmap content.
- Mapped uploaded curriculum guide nodes and edges into the existing semester roadmap UI.

### Verified

- Frontend lint passes.
- Frontend production build passes.
- Diagnostics return no issues.
- Spacing check found no triple-newline gaps in edited frontend files.

### Not Included

- No recommendation scoring yet.
- No backend persistence for uploaded curriculum guides or transcripts.
- No automatic frontend end-to-end browser test yet.
- No universal curriculum guide parser beyond the current backend support for the CSC AY2023-24 guide format.
- No Neo4j, ChromaDB, LangGraph, or OpenAI integration.

## Uploaded Roadmap Controls

Status: Implemented locally

### Completed

- Added a `Clear roadmap` action to the roadmap page.
- Clearing the roadmap removes the uploaded curriculum guide from the active browser profile.
- Transcript results are kept when clearing the roadmap so they can be rematched after another curriculum guide upload.
- Improved the `Clear roadmap` button contrast in light mode while preserving the dark-mode styling.
- Passed uploaded curriculum guide `prerequisiteText` and `isChoiceSlot` values into the roadmap UI.
- Updated roadmap eligibility so text-only prerequisite requirements are shown as locked when they cannot be automatically verified.
- Cleaned `useProfileStore.ts` interface comments so the state fields are easier to scan.

### Verified

- Frontend lint passes.
- Frontend production build passes.
- Diagnostics return no issues.

### Not Included

- `Year 4 standing` and similar academic-standing requirements are based on completed AU, not profile year.
- Locked checkboxes are still manually checkable for exemptions, transfer credits, exchange modules, and special approvals.
- No recommendation scoring yet.
- No backend persistence for uploaded curriculum guides or transcripts.
- No Neo4j, ChromaDB, LangGraph, or OpenAI integration.

## Latest Handoff

Status: Ready for next work

### Current App State

- Backend has `GET /health`, `GET /roadmap`, `POST /transcript`, module catalogue endpoints, faculty endpoints, and `POST /curriculum-guide`.
- Uploaded curriculum guides are now the source of truth for the active student's roadmap display.
- The Roadmap page shows an empty state when no curriculum guide is uploaded.
- The Roadmap page can clear the uploaded curriculum guide without deleting saved transcript results.
- Transcript uploads are stored separately and rematched against the uploaded curriculum guide when both exist.
- Profile page supports curriculum guide upload, transcript upload, and career goal selection.
- Roadmap cards can show completed, available, and locked states based on completed roadmap courses and parsed prerequisite information.

### Next Recommended Work

- Keep academic-standing eligibility based on completed AU from transcript results and parsed curriculum guide standing rules.
- Continue improving how completed AU is explained to students in the roadmap/profile flow.
- Keep polishing the roadmap/profile flow before starting MPE/choice-slot recommendation logic.

### Onboarding For Next Session

- Read `AGENTS.md`, `Diagrams.md`, `Mistakes.md`, `Progress.md`, and `README.md`.
- Run `git status --short --branch`.
- Continue on a focused branch and avoid unrelated AI/data integrations.
- Do not add Neo4j, ChromaDB, LangGraph, OpenAI, or advanced recommendation logic yet.

## Basic Recommendation Flow

Status: Implemented locally

### Completed

- Created the `basic-recommendation-flow` branch for the first recommendation-system work.
- Limited the Profile career goal dropdown to `Software Engineer` for the first supported recommendation path.
- Added backend recommendation schemas for request data, recommended courses, prerequisite recommendations, and response data.
- Added `POST /recommendations` as the first backend recommendation endpoint.
- Added a simple recommendation service for the current MVP.
- Added frontend recommendation API types and a `fetchRecommendations` API client.
- Added a reusable `ClassicLoader` spinner component for recommendation-loading states.
- Moved recommendation loading to the Profile page under Career Goal with a `Load Roadmap` button.
- Added a small `Go to roadmap...` link below the Profile roadmap-loading action.
- Lifted recommendation state into `App.tsx` so the Profile page can trigger loading and the Roadmap page can render the results.
- Displayed recommendations directly inside suitable roadmap choice-slot cards instead of showing them as a Profile result list.
- Added loading feedback on the Roadmap page while recommendations are being fetched.
- Assigned one recommendation per available choice slot so repeated BDE recommendations do not appear across every BDE card.
- Added basic BDE year-level preference so lower-level BDE modules are preferred earlier and higher-level modules are preferred around Year 3 or Year 4.
- Added curriculum exclusion fields so fixed curriculum modules are not recommended again by matching either course code or normalized course title.
- Added prerequisite-aware recommendation output so a recommended course can include missing prerequisite details.
- Added frontend assignment logic that can place a missing prerequisite recommendation one semester before the recommended target course when a suitable earlier choice slot exists.

### Current Recommendation Logic

- Level 1 recommendation logic is weighted keyword matching plus rule-based filtering.
- It is not AI-based ranking, collaborative filtering, graph search, ChromaDB retrieval, LangGraph reasoning, or OpenAI generation.
- For `Software Engineer`, the backend uses explicit weighted keywords such as `software`, `engineering`, `programming`, `development`, `database`, `web`, `cloud`, `distributed`, `systems`, `algorithm`, `architecture`, `testing`, and `security`.
- Candidate modules score higher when their title or description contains higher-weight career keywords.
- `SC3xxx` and `SC4xxx` choice slots only consider CSC modules at the matching module level.
- `BDE` choice slots can consider modules from the wider active module catalogue, subject to active faculty settings.
- Completed modules are excluded from recommendations.
- Fixed modules already present in the uploaded curriculum roadmap are excluded by course code and by normalized title.
- Missing prerequisites are currently surfaced as rule-based constraints after scoring; if the top suitable recommendation needs one missing prerequisite, the frontend tries to place that prerequisite one semester earlier.
- If a prerequisite cannot fit into an earlier suitable slot, that target recommendation is skipped for that slot for now.
- After the backend slot-eligibility update, the frontend sends each open choice slot with its roadmap ID, year, and semester.
- Backend recommendation logic now filters and ranks candidates per concrete slot before returning recommendations.
- BDE year-level fit now happens in the backend, while the frontend uses the returned slot ID for exact placement.

### Verified

- Backend compile check passes with `.venv/bin/python -m compileall backend`.
- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Blank-line scan passed for the edited recommendation files after the repeated style issue was fixed.

### Not Included

- No Neo4j, ChromaDB, LangGraph, OpenAI, or advanced recommendation engine yet.
- No machine-learning model, ALS scoring, or semantic embedding search yet.
- No multi-career recommendation support beyond `Software Engineer`.
- No timetable, exam clash, workload, vacancy, or student preference optimization yet.
- No backend persistence for generated recommendations yet; recommendation state is frontend runtime state.
- No manual browser verification has been recorded yet for the latest prerequisite-placement behavior.

### Next Recommended Work

- Manually test `Load Roadmap` with an uploaded curriculum guide and transcript.
- Confirm existing fixed curriculum modules no longer appear as recommended choices by code or by title.
- Confirm prerequisite recommendations appear one semester earlier when a suitable earlier choice slot exists.
- Fix any remaining display issues, such as duplicated prerequisite text or curriculum guide typos, before adding more recommendation intelligence.

## Recommendation Roadmap Polish

Status: Implemented locally

### Completed

- Made roadmap recommendation cards clickable so a selected recommended module can open the same kind of module-detail popup used by the NTU Modules page.
- Updated BDE assignment so the BDE slot year must match the recommended module level for now, such as Year 2 BDE to level 2 modules and Year 4 BDE to level 4 modules.
- Increased the number of requested recommendation candidates based on open choice slots so later Year 3 and Year 4 BDE slots are less likely to be left empty by the previous small global limit.
- Normalized BDE display text to `Broadening and Deepening Electives` so the parsed curriculum typo does not appear in the roadmap.
- Deduplicated repeated missing prerequisite labels in the roadmap locked-state display.
- Hardened prerequisite placement so a missing prerequisite is checked before being passed into slot-fit logic.

### Verified

- Backend compile check passes with `.venv/bin/python -m compileall backend`.
- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited files.

### Not Included

- No Neo4j, ChromaDB, LangGraph, OpenAI, or advanced recommendation engine.
- No backend persistence for generated recommendations.
- No manual browser verification has been recorded yet after these polish changes.

## Recommendation Slot Demand Sizing

Status: Implemented locally

### Completed

- Added frontend recommendation-limit sizing based on the actual number of open BDE and MPE slots after curriculum guide upload.
- Gave BDE slots a larger candidate multiplier because BDE assignment can skip candidates due to duplicate recommendations, year-level matching, or prerequisite-placement rules.
- Increased the backend recommendation request limit validation from `50` to `120` so the frontend can request enough candidates for multiple open choice slots.

### Verified

- Backend compile check passes with `.venv/bin/python -m compileall backend`.
- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited files.

### Not Included

- No new ranking model, AI logic, graph search, vector search, or backend persistence.
- No backend-side per-slot assignment yet; the roadmap still performs the final slot placement in the frontend.

## Recommendation Debug Logging

Status: Implemented locally

### Completed

- Added backend recommendation logs for the initial SQL candidate list before Python-side filtering and scoring.
- Added backend recommendation logs for the ranked recommendation list before the request `limit` is applied.
- Added backend recommendation logs for the final returned recommendation cut after applying `limit`.
- Kept logs compact by showing counts and course-code summaries with slot, level, score, and missing prerequisite count.

### Verified

- Backend compile check passes with `.venv/bin/python -m compileall backend`.
- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited files.

### Not Included

- No frontend debug panel yet.
- No persistent logging table or analytics storage.
- No backend-side explanation for frontend slot-placement skips yet.

## Transcript-Only Roadmap Display

Status: Implemented locally

### Completed

- Added an optional roadmap node flag for completed modules that came from the transcript but were not fixed rows in the uploaded curriculum guide.
- Extended transcript parsing to attach academic year, transcript semester, and mapped study year to completed transcript modules.
- Handled both one-column and two-column transcript layouts when matching module rows to semester headers.
- Enriched unmatched transcript module codes with the existing module detail API so the roadmap can show titles, AU values, prerequisites, and unlocks where available.
- Added fallback completed transcript cards for unmatched transcript codes that cannot be found in the module catalogue.
- Placed transcript-only completed modules into their parsed Year/Sem row when transcript term metadata is available.
- Uses the curriculum guide as the base roadmap, then lets transcript Year/Sem metadata override the display position when a completed transcript course code matches a curriculum guide course.
- Corrected transcript term matching so left-column modules map to left-column semester headers even when the header starts left of the course table.
- Kept a `Completed Outside Curriculum` fallback band only for transcript modules that do not have usable term metadata.
- Added relationship arrows from known prerequisite nodes into transcript-only modules and from transcript-only modules into known unlocked roadmap nodes.
- Treated transcript-only modules as completed when checking roadmap prerequisites, while keeping their checkboxes read-only.
- Removed special transcript-only card coloring so transcript-completed modules use the normal completed-course color state.
- Kept the lower `Curriculum Guide Courses` list limited to official curriculum guide rows.
- Changed the lower `Curriculum Guide Courses` display from a narrow vertical list into a wider responsive card grid.
- Made the lower `Curriculum Guide Courses` list read directly from the uploaded curriculum guide so transcript placement does not change this section's Year/Sem grouping.

### Verified

- Backend compile check passes with `.venv/bin/python -m compileall backend`.
- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited files.

### Not Included

- Transcript-only modules still do not automatically fill BDE or MPE slots.
- No bulk module lookup endpoint yet; the frontend currently uses the existing per-module lookup.
- No manual browser verification has been recorded yet for semester-placed transcript-only roadmap cards and arrows.

## Profile Career Goal Cleanup And AU Standing

Status: Implemented locally

### Completed

- Kept roadmap academic-standing eligibility based on completed AU instead of the profile's self-declared year or semester.
- Removed Year of Study and Current Semester from the saved profile model because they can be misleading for standing rules.
- Moved Career Goal into the main profile row so the profile form focuses on recommendation inputs.
- Placed Curriculum Guide Upload and Transcript Upload cards side by side on wider screens while keeping them stacked on small screens.
- Moved transcript completion and AU totals into the Transcript Upload card and removed the separate outside roadmap statistic strip.
- Added profile hydration cleanup so old browser-saved Year of Study and Current Semester values are not saved back into active profile records.
- Kept module-code prerequisite checks, transcript-completed modules, and recommendation placement logic unchanged.

### Verified

- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited files.

### Not Included

- No backend recommendation changes.
- No transcript parser changes.
- No database schema changes.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, or advanced recommendation logic.
- No manual browser verification has been recorded yet for the simplified wider Profile layout.

## Backend Slot Eligibility

Status: Implemented locally

### Completed

- Created the `backend-slot-eligibility` branch for the first recommendation improvement.
- Added a `choiceSlots` request field so the frontend can send each open choice slot with its roadmap node ID, year, and semester.
- Kept the existing `choiceSlotCodes` request field as a simple fallback for older or manual API calls.
- Updated backend recommendation logic to evaluate candidates against each concrete open slot instead of only unique slot labels.
- Moved BDE year-level fit into the backend so Year 2 BDE slots receive level 2 candidates and Year 4 BDE slots receive level 4 candidates before frontend placement.
- Kept MPE slot eligibility backend-side by requiring CSC modules at the matching `SC3xxx` or `SC4xxx` level.
- Ranked recommendation candidates per slot before returning the flattened recommendation list to the frontend.
- Added slot metadata to each recommendation response so the frontend can place direct recommendations by exact roadmap slot ID.
- Updated the frontend recommendation request builder and roadmap assignment logic to use backend slot IDs when available.
- Updated the roadmap so locked choice slots can still show loaded recommendations while keeping their locked styling and missing-requirement message.
- Updated backend recommendation ordering to round-robin across slots and skip duplicate course codes so later BDE slots are less likely to be starved by earlier slots.
- Added duplicate-title protection so different course codes with the same normalized title are not recommended together.
- Added frontend planning nodes for fallback recommendations with missing prerequisites, using a `Recommended Pre-Requisite` tag so students can see why an extra node appears.
- Added a one-remaining-semester guard in frontend placement: if no earlier remaining semester exists, recommendations with missing prerequisites are skipped in favor of ready modules.
- Added existing-curriculum prerequisite handling so a recommendation like `SC4055` can use an earlier roadmap module such as `SC2006` as the visible prerequisite path instead of creating extra alternative prerequisite nodes.
- Added all direct prerequisite codes to recommendation responses so the frontend can draw prerequisite arrows even when a transcript has already marked those prerequisites as completed.

### Rationale Notes

- Recommendation and eligibility are separate concepts: a module can be a good recommendation for a slot even if the student is not currently ready to take it.
- `Recommended` means the module fits the student's career goal and the slot type or level.
- `Locked` means the student has not satisfied a requirement yet, such as `Year 3 Standing` or a module prerequisite.
- Without transcript AU, MPE slots with `Year 3 Standing` can remain locked, but loaded recommendations should still be visible so students can plan ahead.
- A BDE slot could appear empty even when the backend returned candidates because the frontend previously skipped target recommendations if their missing prerequisite could not be placed in the immediately previous semester.
- The current fallback keeps the target recommendation visible when prerequisite placement fails, while leaving the slot locked or showing missing requirements.
- If a target recommendation has missing prerequisites and there is an earlier remaining semester, the roadmap can show the target recommendation and add separate `Recommended Pre-Requisite` planning nodes in the latest earlier remaining semester.
- The prerequisite graph currently stores prerequisites as a flat code list, so it cannot perfectly distinguish AND requirements from OR alternatives.
- Because of that data limitation, if any missing prerequisite code already exists earlier in the student's uploaded curriculum guide, the frontend treats that existing module as the planned prerequisite path and draws an arrow from it to the recommended slot.
- Completed prerequisites are no longer counted as missing, so the backend now returns both `prerequisites` and `missingPrerequisites`; the former supports arrows and the latter supports planning-node decisions.
- If no earlier remaining semester exists, the roadmap should avoid showing recommendations with missing prerequisites because there is no remaining semester to plan those prerequisites first.

### Verified

- Backend compile check passes with `.venv/bin/python -m compileall backend`.
- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited files.

### Not Included

- No structured score breakdown yet; that is the next recommendation improvement.
- No unlock-value or deeper prerequisite-readiness logic yet.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning recommendation logic.
- No backend persistence for generated recommendations.
- No manual browser verification has been recorded yet for the exact-slot recommendation behavior.
- Recommendation coverage still depends on enough eligible unique module candidates existing for each slot.
- The one-remaining-semester guard currently lives in the frontend placement layer; a later backend refinement can make the API avoid returning those candidates earlier.
- True AND/OR prerequisite grouping is not implemented yet because the stored prerequisite graph does not preserve grouping semantics.

## Prerequisite Readiness And Unlock Value

Status: Implemented locally

### Completed

- Added `curriculumCourses` to the recommendation request so the backend can see uploaded roadmap course positions, not only completed and excluded codes.
- Added backend readiness metadata to each recommendation: `readinessStatus`, `existingPrerequisiteCourseCodes`, `plannedPrerequisiteCourseCodes`, and `unlockValue`.
- Moved the one-remaining-semester guard into backend recommendation filtering by skipping candidates with unmet prerequisites when no earlier open slot can plan the prerequisite first.
- Reused earlier uploaded curriculum courses as prerequisite paths before creating new prerequisite planning nodes.
- Kept the current flat prerequisite-list workaround: if one listed prerequisite is completed or already planned earlier, the backend treats that path as sufficient instead of recommending every alternative code.
- Added a small unlock-value score boost when a recommended module unlocks later fixed curriculum modules.
- Updated the frontend to send displayed roadmap context, including transcript-only completed modules, and to consume backend prerequisite path fields for arrows and `Recommended Pre-Requisite` nodes.
- Strengthened duplicate-title filtering so equivalent titles using punctuation variants, such as `and` versus `&`, are not recommended when the curriculum already contains that module under another code.

### Rationale Notes

- This is not just moving logic from frontend to backend; it improves recommendation quality by filtering impossible final-semester recommendations before they reach the UI.
- The backend now has enough context to distinguish completed prerequisites, prerequisites already planned earlier in the uploaded curriculum, and prerequisites that need a new planning node.
- Prerequisites do not reduce career relevance directly; a relevant course can still be recommended if it is ready or realistically plannable before its target slot.
- Unlock value is intentionally small and rule-based so it prefers pathway-useful courses without overpowering career keyword relevance.

### Verified

- Backend compile check passes with `.venv/bin/python -m compileall backend`.
- Frontend lint passes with `npm run lint`.
- Frontend production build passes with `npm run build`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited files.

### Not Included

- No structured score breakdown UI.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning recommendation logic.
- No true AND/OR prerequisite grouping yet because the stored prerequisite graph still keeps prerequisites as a flat list.
- No backend persistence for generated recommendations.
- No manual browser verification has been recorded yet for this local change.

## Curated Course Taxonomy Tags Attempt

Status: Rolled back locally

### Attempted

- Tried a small rule-based taxonomy helper for module tags such as `software-engineering`, `web-development`, `data`, `ai-ml`, `systems`, `security`, `hardware`, `business`, `math`, and `communication`.
- Wired the helper into the existing seed flow and briefly used taxonomy tags as a recommendation relevance signal.
- Reran the seed script locally during the experiment, which updated `modules.categories` in PostgreSQL.

### Rationale Notes

- This approach was rolled back because automatic keyword-style taxonomy tagging caused confusing false positives.
- Example: broad matching could tag unrelated modules as software-related if their title or description contained ambiguous words.
- Faculty exclusions reduce some mistakes but do not solve the wider problem because relevant software-engineering vocabulary is broad and context-dependent.
- For now, the seed flow should write only original source categories from `data/modules.json`.
- Recommendation scoring should remain based on the existing keyword logic and previously completed prerequisite-readiness work.

### Verified

- The seed script was rerun after rollback so local `modules.categories` is reset from `data/modules.json`.

### Not Included

- No student preference UI yet.
- No curated module taxonomy is active yet.
- No hand-curated per-module override file.
- No separate taxonomy table or admin editing workflow.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning tagging.

## CE/CSC Recommendation Tags

Status: Implemented locally

### Completed

- Added a separate `recommendationTags` field in `data/modules.json` for only `CE` and `CSC` modules.
- Kept original NTU module `categories` unchanged so curriculum/category labels such as `CORE`, `MPE`, `BDE`, `GLOAD`, and `MLOAD` remain separate from recommendation taxonomy.
- Added a separate `recommendation_tags` JSON column to the `modules` table.
- Updated the seed script to read `recommendationTags` from `data/modules.json` and write it into `modules.recommendation_tags`.
- Added a seed-time column check because the project does not use Alembic migrations yet.
- Exposed `recommendation_tags` through the backend modules API and frontend module type.
- Updated Software Engineer recommendations to use curated `recommendation_tags` as an additional relevance signal while keeping the existing title/description keyword logic as fallback.
- Added `data/recommendation_tag_review_notes.json` to list modules tagged from title/code only because they do not have a usable description.

### Rationale Notes

- The previous attempt stored generated tags inside `categories`, which was confusing because those categories came from NTU/source catalog data.
- `recommendationTags` is intentionally separate because it is project-curated recommendation metadata, not original curriculum metadata.
- Tagging is limited to `CE` and `CSC` for now to avoid cross-faculty false positives such as unrelated `ACC`, `BUS`, `AED`, or `NIE` modules.
- The current tag pass is title-first and conservative; descriptions are used as context during review, but not as broad keyword rules that can over-tag modules.
- Modules without descriptions are explicitly flagged for manual verification instead of being treated as fully verified.

### Verified

- Reran `.venv/bin/python -m backend.database.seed`.
- Local PostgreSQL `modules` table now has 311 `CE`/`CSC` rows with a `recommendation_tags` column available.
- 296 `CE`/`CSC` modules currently have at least one non-empty recommendation tag.
- 0 non-`CE`/`CSC` modules have non-empty recommendation tags.
- Confirmed `AED28R` has no recommendation tags, while `SC2002`, `SC2302`, and `SC4052` have relevant tags.

### Not Included

- No tags were added for faculties outside `CE` and `CSC`.
- No student preference UI yet.
- No separate taxonomy admin editor.
- No LLM/OpenAI runtime integration; the tagging output is stored as reviewed static data.
- No Neo4j, ChromaDB, LangGraph, MyCareersFuture, embeddings, or machine-learning tagging.

## Student Topic Preferences

Status: Implemented locally

### Completed

- Added `preferredRecommendationTags` to the browser-saved student profile.
- Existing saved profiles hydrate with an empty preference list so old localStorage profiles still work.
- Added a searchable fixed tag selector on the Profile page.
- The student can type into the search box to filter matching allowed tags instead of scrolling through the full list.
- Hid the full tag list by default so matching tag options only appear after the student starts typing.
- Changed selected preference chips to use a small cross remove button instead of a `REMOVE` text label.
- The student cannot create custom free-text tags; selections must come from the curated tag list used by `recommendationTags`.
- Sent selected preference tags to `POST /recommendations` as `preferredRecommendationTags`.
- Updated backend recommendation ranking so matching preference tags add a small soft boost after career-goal, slot-fit, duplicate, and prerequisite-readiness checks.
- Clearing or changing preferences clears stale visible recommendations until the student clicks `Load Roadmap` again.

### Rationale Notes

- Career goal remains the primary recommendation context.
- Topic preferences refine ranking within that career goal instead of replacing it.
- For example, `Career Goal = Software Engineer` and `Preference = AI / ML` means “recommend software-engineering-relevant modules, but prefer AI/ML-related options when they fit.”
- Preferences are not a hard filter because that could hide useful software modules when no suitable preferred-tag module fits a slot.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- Blank-line scan found no repeated empty-line gaps in the edited backend files.

### Not Included

- No custom user-created tags.
- No preference weights/sliders.
- No score breakdown UI.
- No tag editor or admin workflow.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning personalization.

## Roadmap Module Detail Lookup

Status: Implemented locally

### Completed

- Fixed exact module detail lookup so roadmap modules from inactive browse faculties, such as `MH1812`, can still load details by course code.
- Kept active faculty filtering for module list browsing, filters, and recommendation candidate discovery.

### Rationale Notes

- Uploaded curriculum guides can include service modules from faculties that are not enabled for the NTU Modules browsing page.
- Exact code lookup is used after a module is already visible in the student's roadmap, so it should not reject a real module just because its faculty is inactive for browsing.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Confirmed `get_module_by_code(db, "MH1812")` returns `MH1812 MATH Discrete Mathematics`.

## Profile Layout And Load Feedback

Status: Implemented locally

### Completed

- Changed Student ID, Major, and Career Goal into one inline profile row on wider screens.
- Kept the profile row responsive so those fields stack again on narrower screens.
- Added a successful loaded state for the Load Roadmap button after recommendation loading completes.
- Reset the loaded tick when the active profile, curriculum guide, career goal, preferences, or transcript completed courses change.

### Rationale Notes

- The Student ID field did not need a full-width row, so placing the three profile fields inline reduces wasted vertical space.
- The loaded tick confirms the request finished successfully without changing the existing roadmap navigation flow.

### Verified

- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- Confirmed `data/sample_transcript.pdf` parses `SC3920 Professional Internship` as Year 3 Semester 1.

## Recommendation Preference Ranking Polish

Status: Implemented locally

### Completed

- Added conservative title-signature duplicate detection so similar database module titles such as `Database Systems` and `Database System Principles` are treated as overlapping recommendations.
- Increased the student topic preference boost so selected tags visibly influence ranking while still allowing non-preferred modules when needed.
- Kept recommendation output deterministic; pressing Load Roadmap repeatedly with unchanged profile inputs should still return the same ranking.

### Rationale Notes

- Exact duplicate-title checks were not enough because similar course titles can differ by words like `Principles` or plural forms like `Systems`.
- Preference tags are still soft ranking signals, not hard filters, but the boost now has enough weight to move matching modules above generic software/database candidates.

### Verified

- Confirmed a service-level recommendation request with `SC3020` excluded by title does not include `CSC206`.
- Confirmed an `ai-ml` preference moves AI/ML-tagged modules into Year 4 BDE recommendations.
- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Load Roadmap Button Feedback Polish

Status: Implemented locally

### Completed

- Moved the loading spinner into the Load Roadmap button instead of showing a separate loader beside it.
- Styled the Load Roadmap button with a wider rounded teal button, inline spacing, hover state, and centered content.
- Added an inline tick bubble inside the button after the roadmap recommendations finish loading successfully.
- Kept the separate `Go to roadmap...` control underneath the main button and styled it like a compact sub action.

### Rationale Notes

- Keeping loading and success feedback inside the button makes the action state easier to see.
- The tick state confirms a successful load without automatically moving the student away from the Profile page.

### Verified

- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Curriculum Guide Layout Parsing Fix

Status: Implemented locally

### Completed

- Investigated `POST /curriculum-guide` returning `422 Unprocessable Entity` for `u21-and-after_csc_2bm_bus_07-july-2025 (1).pdf`.
- Confirmed the newer guide is a different PDF layout from `data/ccds_ay23-24_csc.pdf`.
- Reworked curriculum row parsing to infer column positions from the PDF table header instead of relying only on old fixed x-coordinates.
- Added support for second-major `Business` rows in the curriculum table.
- Ignored auxiliary tables such as `Course Code Type AU Remarks` so they are not mistaken for roadmap rows.
- Added a temporary first-section-only rule for PDFs that bundle multiple `CURRICULUM FOR...` variants in one file.

### Rationale Notes

- This avoids manually accepting every curriculum guide file by name.
- Similar NTU guide variants should work as long as they keep recognizable curriculum table headers.
- Multi-variant PDFs still need a future selection UI if the student must choose a section other than the first one.

### Verified

- `data/ccds_ay23-24_csc.pdf` parses successfully.
- `data/u21-and-after_csc_2bm_bus_07-july-2025 (1).pdf` parses successfully.
- `POST /curriculum-guide` returns `200` for `data/ccds_ay23-24_csc.pdf`.
- `POST /curriculum-guide` returns `200` for `data/u21-and-after_csc_2bm_bus_07-july-2025 (1).pdf`.
- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Recommendation Prerequisite Equivalence Fix

Status: Implemented locally

### Completed

- Investigated Year 4 recommendation prerequisite cards showing fallback data such as `Recommended prerequisite` and `0 AU`.
- Confirmed the module catalog DB data is correct for examples such as `CZ2007` and `CZ2101`.
- Fixed backend readiness logic so old-code prerequisites can match equivalent earlier roadmap courses by title.
- Example: `CZ2007 Introduction To Databases` can now reuse `SC2207 Introduction to Databases` when `SC2207` is already earlier in the uploaded curriculum roadmap.
- Example: `CZ2101 Algorithm Design & Analysis` can now reuse `SC2001 Algorithm Design & Analysis`.

### Rationale Notes

- The wrong display was caused by frontend fallback rendering when backend sent a planned prerequisite code without detail data.
- The backend should avoid planning duplicate old-code prerequisite nodes when the uploaded curriculum already contains an equivalent newer-code module.
- Existing browser-saved recommendations may still show the old fallback cards until the curriculum is reuploaded and recommendations are loaded again.

### Verified

- Confirmed DB titles/AU for `BC2402`, `CZ2001`, `CZ2007`, and `CZ2101` are correct.
- Confirmed `CZ2007` and `CZ2101` map to existing earlier curriculum modules `SC2207` and `SC2001`.
- Confirmed end-to-end recommendation output has no planned prerequisite codes missing prerequisite detail data.
- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Transcript Curriculum Code Equivalence Fix

Status: Implemented locally

### Completed

- Investigated why `SC3079 Professional Internship` stayed unchecked even though the uploaded transcript clearly contains a completed professional internship.
- Confirmed the transcript parser correctly extracts `SC3920 Professional Internship`, `10 AU`, grade `A+`.
- Confirmed the issue is not the transcript parser or DB data; it is a frontend matching issue because the uploaded curriculum uses `SC3079` while the transcript uses `SC3920`.
- Updated browser-side transcript-to-curriculum matching to use exact course code first, then conservative normalized title matching.
- `SC3920 Professional Internship` can now match `SC3079 Professional Internship` in the uploaded curriculum roadmap.

### Rationale Notes

- NTU curriculum guides and transcripts may use different course codes for equivalent modules across cohorts.
- Matching by title is used only after exact code matching, so ordinary same-code matches remain simple.
- Existing browser-saved transcript/curriculum results may need re-uploading or rematching to show the newly matched checkbox.

### Verified

- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Pending Curriculum Guide Upload Guard

Status: Implemented locally

### Completed

- Fixed a confusing profile flow where selecting a new curriculum guide file did not immediately replace the active stored roadmap source.
- `Load Roadmap` is now disabled while a new selected curriculum guide file is pending upload.
- After `Upload Curriculum Guide` succeeds, the file picker is reset and the parsed guide becomes the active roadmap source.
- Added helper text so students know they must upload the newly selected PDF before loading the roadmap.

### Rationale Notes

- Choosing a file in the browser only selects it locally; it does not parse or store the curriculum guide yet.
- Without this guard, students could select a new PDF and then click `Load Roadmap`, but the app would still use the previously uploaded parsed guide.

### Verified

- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Persist Roadmap Recommendations Per Student

Status: Implemented locally

### Completed

- Investigated why recommendations disappeared after logout and login with the same Student ID.
- Confirmed recommendation results were stored only in local React state inside `App`, while curriculum, transcript, and completed-course data were persisted in the profile store.
- Added `roadmapRecommendations` to the per-student browser-saved Zustand profile record.
- Updated the roadmap page to read recommendation cards from the profile store instead of local-only component state.
- Saved fresh recommendation results after `Load Roadmap` succeeds.
- Cleared saved recommendations when recommendation inputs change, such as career goal, topic preferences, curriculum guide, transcript results, or manual completion state.

### Rationale Notes

- Recommendations are part of the active student's roadmap state, so they should follow the same per-Student-ID persistence model as uploaded curriculum and transcript data.
- Loading/error states remain local UI state because they should not persist across sessions.

### Verified

- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Same-Faculty Recommendation Boost

Status: Implemented locally

### Completed

- Added `studentFaculty` to the recommendation request payload.
- Frontend now sends the active profile major as the student faculty when loading recommendations.
- Backend recommendation scoring now applies a soft same-faculty boost.
- For a CSC profile, valid CSC modules rank above comparable CE or other-faculty modules where possible.
- Same-faculty matching is not a hard filter, so BDE can still recommend broader options if they are the best valid choices.
- Saved recommendations are cleared when the profile major changes so stale results are not shown.

### Rationale Notes

- The curriculum/profile faculty should influence ranking because students usually expect recommendations to prefer modules from their own programme.
- This is especially useful for BDE slots, where the candidate pool can include many active faculties.
- The boost remains soft because BDE is intentionally broad and may still include non-CSC courses later if they are relevant.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- Confirmed `CE4045` receives no CSC same-faculty boost while `SC4002` and `SC4050` receive the boost.

## Legacy CSC Code Recommendation Priority

Status: Implemented locally

### Completed

- Added backend score penalties for legacy CSC course-code prefixes when the active student faculty is `CSC`.
- Current `SC` course codes are preferred over legacy `CZ` options for CSC students when both are valid candidates.
- Older `CSC`-prefixed course codes are deprioritized even further than `CZ` options.
- `CZ` and `CSC`-prefixed modules remain available as fallback recommendations instead of being hard-filtered out.
- Recommendation reasons mention when an older-code option is being kept as a fallback.

### Rationale Notes

- In the CSC curriculum, `CSC` and `CZ` codes are older course codes while current equivalents generally use `SC`.
- A CSC student should normally see current `SC` recommendations first.
- Keeping older codes as fallback avoids empty slots if the active catalog lacks enough suitable `SC` options.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- Confirmed `CZ2001` and `CZ2007` receive the CSC legacy-code penalty while `SC4002` and `SC4050` do not.
- Confirmed `SC4002` receives no legacy-code penalty, `CZ2001` receives a medium legacy-code penalty, and `CSC303` receives the strongest legacy-code penalty.

## Methodology Handover Review

Status: Reviewed locally

### Useful Takeaways

- Keep the recommender as a retrieve, filter, rank, and explain pipeline instead of a generic chatbot or flat top-k list.
- Treat academic validity as hard rules before ranking: slot fit, completed/equivalent courses, prerequisites, programme rules, and AU constraints should not be solved by scoring alone.
- Keep student-specific context central: transcript, uploaded curriculum guide, remaining slots, completed AUs, career goal, and preferences should all feed the recommendation request.
- Separate immediate recommendations from pathway recommendations so students can distinguish courses they can take now from courses that need prerequisite planning.
- Add score breakdowns and evidence later so recommendations can explain slot fit, eligibility, career alignment, preference match, and caveats.
- Use job-market data later as a ranking signal only, not as a replacement for curriculum validity.
- Preserve source/provenance for extracted transcript, curriculum, course, and job-market facts so recommendations stay auditable.
- Delay Neo4j, ChromaDB, LangGraph, OpenAI, and labour-market ingestion until the current deterministic roadmap and recommendation flow is stable.

### How This Applies Now

- The current branch already follows the recommended order by filtering completed/fixed courses, checking slot fit, evaluating prerequisite readiness, and only then ranking by career and preference signals.
- The recent duplicate-title and preference-ranking fixes are a small step toward the handover's diversity and student-interest recommendations.
- The next practical improvement should be an explicit API-level score breakdown before adding heavier AI or graph tooling.

## Transcript Semester Placement Override

Status: Implemented locally

### Completed

- Fixed roadmap placement for completed transcript courses when the transcript course code differs from the curriculum guide code but the course title is equivalent.
- Roadmap display now uses transcript `study_year` and `transcript_semester` as the final placement source for matched completed courses.
- Exact course-code placement still works first, and normalized title/title-signature placement handles code changes such as `SC3920 Professional Internship` matching curriculum `SC3079 Professional Internship`.

### Rationale Notes

- The curriculum guide defines the intended study plan, but the transcript is the evidence of when the student actually completed a module.
- Completed modules should therefore appear in the transcript term on the personalised roadmap, while incomplete curriculum modules should continue following the uploaded curriculum guide.

### Verified

- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

## Recommendation Score Breakdown

Status: Implemented locally

### Completed

- Added a backend `RecommendationScoreBreakdown` schema for deterministic recommendation scoring components.
- Extended each recommendation response with `scoreBreakdown` while keeping the existing `score` field unchanged.
- Split the existing recommendation score into career/tag relevance, current-semester bonus, preference boost, same-faculty boost, legacy-code penalty, unlock contribution, and final score.
- Updated frontend recommendation types so stored recommendation results can receive the new score breakdown field.
- Kept the roadmap UI unchanged because the score breakdown should not be shown on the roadmap yet.
- Added future NTU SSO guidance to `AGENTS.md`, including that the app should not collect NTU passwords or hardcode captured SAML request URLs.

### Rationale Notes

- The score breakdown makes the current rule-based recommender easier to inspect without introducing AI, graph databases, embeddings, or job-market data.
- Keeping the breakdown out of the roadmap UI avoids clutter while preserving the explanation data for later debugging or a future detail view.
- NTU login should use an official SSO redirect/callback integration later; any stable SAML/OIDC identity claim should be stored separately from the app's internal user ID.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.

### Not Included

- No visible score breakdown on roadmap cards.
- No real NTU SSO integration, mock SSO flow, auth sessions, or backend user table.
- No recommendation ranking algorithm changes beyond exposing existing deterministic score components.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning recommendation logic.

## Prototype Security Notes

Status: Implemented locally

### Completed

- Added a README section explaining that browser storage is prototype persistence, not production-secure storage.
- Documented that localStorage profile, curriculum, transcript, completed-course, and saved recommendation data can be inspected or edited by users.
- Documented that API responses such as `/recommendations` can be inspected in browser developer tools, including score breakdowns.
- Updated project rules so future work treats frontend-submitted profile, curriculum, transcript, and completed-course data as user-controlled unless it is later stored and verified server-side.
- Repeated the NTU SSO guardrail that production login should use official redirect/callback integration and must not collect NTU passwords directly.

### Verified

- Diagnostics return no issues.
- `git diff --check` passes.

### Not Included

- No production authentication implementation.
- No backend user table or server-side student record persistence.
- No change to browser storage behavior.
- No change to recommendation API output.

## Preference-Aware Recommendation Diversity

Status: Implemented locally

### Completed

- Added a backend diversity adjustment during final recommendation selection across roadmap slots.
- Tracks selected recommendation tags so later selected recommendations receive a small penalty when they repeat already-used tags.
- Applies a much smaller repeat penalty for tags that match the student's selected topic preferences.
- Keeps hard eligibility, career relevance, prerequisite readiness, preference boosts, same-faculty boosts, and legacy-code penalties before diversity.
- Leaves the existing recommendation `score` and `scoreBreakdown` as the module quality score instead of rewriting it with the selection-time diversity adjustment.
- Kept the roadmap UI unchanged.

### How It Works

- The backend applies diversity only during final recommendation selection.
- The system tracks tags from already-selected recommendations.
- Later recommendations receive a small penalty when they repeat already-used tags.
- Repeated tags receive a much smaller penalty when they match the student's selected topic preferences.
- Existing `score` and `scoreBreakdown` remain unchanged, so they still represent the module's individual recommendation quality.

### Priority Order

- Eligibility still comes first.
- Career relevance still matters most for ranking.
- Student preferences remain strong soft boosts.
- Same-faculty and legacy-code behavior remains unchanged.
- Diversity only nudges final selection when multiple valid options exist.

### Rationale Notes

- Diversity should reduce unnecessary repetition, not force variety against the student's interests.
- If a student prefers `database`, database-related modules can still rank strongly; diversity only nudges the final selection away from excessive repeated non-preferred tags when good alternatives exist.
- This keeps the recommender deterministic and explainable without adding AI, graph databases, embeddings, or job-market signals.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- `git diff --check` passes.

### Not Included

- No frontend UI changes.
- No new recommendation settings or preference sliders.
- No diversity explanation field in the public API response.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning recommendation logic.

## Backend-Owned Recommendation Slot Assignment

Status: Implemented locally

### Completed

- Changed backend final selection so it returns at most one assigned recommendation per exact open choice slot.
- Kept `recommendations` as the existing response field, but its meaning is now final assigned recommendations rather than a large candidate pool.
- Changed the frontend recommendation request limit to match the number of open choice slots instead of requesting a large buffer such as 24, 50, or 90 candidates.
- Simplified roadmap assignment so the frontend uses backend-provided `matchedChoiceSlotId` directly instead of re-ranking candidates by score or slot type.
- Kept frontend visual rendering, module detail opening, and prerequisite planning-node rendering unchanged.

### Rationale Notes

- Recommendation ranking and allocation should live in the backend service layer, not in the frontend rendering layer.
- The backend already has the career goal, preferences, completed courses, curriculum slots, prerequisite paths, scoring, and diversity context needed to make the final assignment.
- The frontend should receive assigned recommendations and render them into the matching roadmap cards.
- If there are five open choice slots, the normal response should now contain up to five assigned recommendations, not a large candidate pool that the frontend has to interpret.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- `git diff --check` passes.

### Not Included

- No new frontend UI.
- No new API endpoint name or response field rename.
- No backend persistence for assigned recommendations.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning recommendation logic.

## Backend-Owned Roadmap Logic Refactor

Status: Merged to `main`

### Completed

- Added backend-planned recommendation roadmap artifacts to recommendation responses.
- Each assigned recommendation can now include `plannedRoadmapNodes` and `plannedRoadmapEdges`.
- Removed frontend construction of `Recommended Pre-Requisite` nodes and arrows.
- Added `POST /roadmap/readiness` so the backend evaluates course readiness states and missing requirements.
- Updated the roadmap UI to render backend readiness output, with the previous local readiness calculation kept only as a fallback if the backend is unavailable.
- Added `POST /transcript/match-curriculum` so the backend matches parsed transcript modules to uploaded curriculum rows by exact code first, then conservative title/signature matching.
- Removed transcript-to-curriculum matching logic from the browser profile store.
- Added `POST /roadmap/personalized` so the backend combines uploaded curriculum guide data, transcript placement overrides, transcript-only modules, and transcript-only prerequisite/unlock arrows into the roadmap response shape.
- Removed frontend logic that enriched transcript-only modules and built the combined personalized roadmap locally.
- Kept backend persistence intentionally out of scope because it should wait for a safe user identity/login design.

### Rationale Notes

- Recommendation ranking, exact slot assignment, prerequisite planning, readiness, transcript matching, and personalized roadmap projection now sit closer to the backend service layer.
- The frontend still owns rendering, layout, hover behavior, tab navigation, upload controls, and local prototype persistence.
- Browser storage remains inspectable and user-editable, so backend APIs must continue treating submitted profile, curriculum, transcript, completion, and recommendation state as user-controlled input.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- `git diff --check` passes.
- Manually tested the end-to-end browser flow after merge: curriculum guide upload, transcript upload, personalized roadmap generation, and recommendation loading work.

### Not Included

- No backend user table, production authentication, or server-side profile storage.
- No API rename from `recommendations` to `assignments`.
- No visible recommendation score breakdown on roadmap cards.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning recommendation logic.

## Backend Roadmap Flow Compatibility Fix

Status: Merged to `main`

### Completed

- Fixed a Python 3.9 backend startup crash introduced by the backend-owned roadmap refactor.
- Replaced new `X | None` annotations in backend roadmap services with Python 3.9-compatible `Optional[X]` annotations.
- Fixed `POST /roadmap/personalized` returning `500` by converting uploaded curriculum guide `CurriculumEdge` objects into `RoadmapEdge` objects before returning `RoadmapResponse`.
- Confirmed the curriculum guide upload and recommendation flow works again after the fix.
- Updated Swagger/OpenAPI descriptions so `/recommendations` now clearly describes backend-assigned recommendations keyed by `matchedChoiceSlotId`.
- Updated Swagger/OpenAPI descriptions so `/roadmap/personalized` explains backend roadmap projection and normalized roadmap edge output.

### Rationale Notes

- The local backend runs on Python 3.9, so Python 3.10 union syntax can crash during FastAPI import before any endpoint runs.
- `CurriculumEdge` and `RoadmapEdge` have the same fields, but Pydantic v2 treats them as different model types during response validation.
- This is a compatibility and schema-normalization fix only; it does not change recommendation ranking, slot assignment, or roadmap UI behavior.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; print('backend import ok')"`.
- Confirmed `POST /roadmap/personalized` returns `200`.
- Confirmed `POST /recommendations` returns `200` with the parsed 2025 curriculum guide and open choice slots.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Confirmed OpenAPI schema generation includes the updated summaries for `/roadmap/personalized` and `/recommendations`.
- Diagnostics return no issues.
- `git diff --check` passes.

### Not Included

- No new feature behavior.
- No backend persistence, user table, production authentication, or SSO implementation.
- No API rename from `recommendations` to `assignments`.
- No Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture, embeddings, or machine-learning recommendation logic.

## Next Recommender Improvement Decision

Status: Planned on branch `career-skill-recommendations`

### Decision

- Keep roadmap/profile polish in view, especially clearer loading states, empty states, and user-facing error messages.
- Keep API naming cleanup in view, especially whether the response field `recommendations` should eventually become `assignments`.
- Start the next recommender improvement with a small deterministic career-skill mapping step.
- Use static career-to-skill mappings first instead of adding MyCareersFuture scraping or external job-market ingestion.

### Why This Is Next

- Eligibility, scoring breakdowns, prerequisite readiness, taxonomy/preferences, preference-aware diversity, and backend-owned slot assignment are now in place.
- The next useful recommendation improvement is making career relevance less dependent on raw keyword matching.
- Static mappings are easier to understand, inspect, and test than job-market scraping or AI-generated skill extraction.

### Planned Scope

- Add a simple backend-owned mapping from supported career goals, such as `Software Engineer`, to relevant skills or recommendation tags.
- Use that mapping as an additional deterministic scoring signal alongside existing recommendation tags and keyword fallback.
- Keep student topic preferences as soft boosts, not hard filters.
- Keep diversity subordinate to eligibility, career relevance, and student preferences.
- Keep the frontend as a rendering layer for assigned recommendations.

### Out Of Scope

- No MyCareersFuture scraping or live labour-market data.
- No Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, or agent workflow.
- No production persistence, backend user table, authentication, or SSO.
- No visible score breakdown UI on roadmap cards unless explicitly requested.

## Static Career-Skill Recommendation Mapping

Status: Implemented locally

### Completed

- Added backend-owned static career-skill mappings for the current supported career goal, `Software Engineer`.
- Mapped the career goal to deterministic skill areas such as software delivery, backend/data services, systems infrastructure, secure software practice, and algorithmic problem solving.
- Matched those career skills against existing curated `recommendation_tags` instead of relying only on raw title/description keyword matches.
- Added `careerSkillScore` to the recommendation score breakdown so the new signal is inspectable through the API response.
- Kept existing curated tag relevance, keyword fallback, student topic preference boosts, same-faculty boosts, legacy-code penalties, unlock contribution, and diversity behavior in place.
- Updated the recommendations endpoint description to explain that career relevance now uses static mappings, curated tags, and keyword fallback.
- Updated the frontend recommendation response type only; the roadmap UI remains visually unchanged.
- Moved the career-skill mapping data into `backend/services/career_skill_mappings.py` so the mapping is easier to review separately from ranking logic.
- Added mapping provenance through per-skill `rationale` text that explains why each skill area matters for the Software Engineer career goal.
- Added `weight_rationale` text for each mapped skill area so the manually chosen weights are easier to inspect and calibrate later.
- Improved backend recommendation reasons so matched mapped skill areas can explain why a module supports the selected career goal.

### Rationale Notes

- This is the first small job-market-aware step without adding live job scraping or AI.
- Static mappings are easy to inspect and deterministic, which fits the current beginner-friendly recommendation pipeline.
- Career-skill matching uses the already curated module tags, so it is less brittle than scanning every module title and description for broad words.
- This is a meaningful upgrade over raw keyword/tag matching because it introduces an explicit domain model between a user's career goal and course metadata.
- The model changes career relevance from `goal -> keyword/tag overlap` to `goal -> skill area -> curated module tags`, which is a more defensible structure for an FYP recommender.
- Explanations can now be grounded in concrete rules, for example: `Recommended because this module supports the Software Engineer skill area: backend and data services.`
- Determinism is valuable here because the same student data and mapping version should produce the same result, making the logic easier to test, review, and demonstrate.
- The static mapping is a good cold-start baseline because it does not need historical ratings, prior users, collaborative filtering data, or live job-market data before recommending modules.
- Keeping the goal-to-skill mapping backend-owned preserves a clean architecture boundary: the frontend renders assigned recommendations, while the backend remains the source of truth for ranking logic.
- The main limitation is that this remains a manually maintained, one-hop taxonomy matcher. It depends on the completeness and calibration of the mappings and can be brittle across many career goals or ambiguous modules.
- Content-based recommenders can suffer from over-specialisation, vocabulary mismatch, and dependence on item-feature quality, so later improvements may need stronger provenance, broader mappings, or job-market evidence.
- Keeping provenance and weight rationale beside the mapping makes future review easier because domain assumptions are documented where the scoring inputs are defined.
- The mapping remains Python-based for now instead of JSON because typed fields, comments, and rationale strings are easier to maintain during this early backend-only iteration.

### Known Downsides And Mitigations

- Manual taxonomy maintenance remains a risk because every career goal, skill area, and tag relationship must be created and updated by people. New or renamed modules can stop matching if the mapping becomes stale, so future work should version mappings, track unmatched tags/goals, and eventually support review tooling.
- Coverage gaps can occur when a genuinely relevant module has no curated tag included in the career mapping. This can make students ask why an obviously relevant module is missing, so future work should track unmapped-but-potentially-relevant modules and review coverage metrics.
- Vocabulary mismatch can still happen if module tags and mapping tags use different labels for the same idea. A future controlled taxonomy should use canonical tag IDs or aliases rather than relying on free-text labels.
- Over-broad skill areas can match many modules with unequal value. Weights and evidence strength should keep broad matches from pushing introductory or tangential modules too high.
- Over-specialisation can happen if direct skill matches repeatedly concentrate Software Engineer recommendations around backend, web, or programming courses. Future ranking should reserve room for adjacent skills, exploration, breadth requirements, or subpath diversity.
- The current mapping does not model student-specific competence. A student already strong in backend work may still receive backend-heavy suggestions, so later profile inputs could capture self-rated confidence, grades, completed modules, and stated interests.
- Tags alone do not encode prerequisites, timetable feasibility, degree rules, or module availability. The current recommender already applies curriculum and prerequisite checks before ranking, and that boundary should remain a hard eligibility layer.
- The `Software Engineer` career label is coarse because it can mean frontend, backend, platform, mobile, security, data, or product engineering. Future work can let students choose a subpath or assign importance weights to skill areas.
- Tag quality becomes a bottleneck because the semantic layer inherits mistakes from module tagging. High-impact tags should be reviewed and eventually include confidence/provenance.
- Explanation wording can overstate certainty if it sounds like one module guarantees job readiness. Use careful language such as `builds exposure to` or `is aligned with`, and show exact matched tags or skill areas when explanations are displayed.
- The current system is popularity/outcome blind because taxonomy matching alone cannot learn which modules students value, perform well in, or find useful. Later feedback or outcome signals should be separate reranking components rather than replacements for eligibility.
- Evaluation can be misleading if offline scores only show agreement with the manually defined mapping. Future evaluation should include independent labels and student or academic-advisor judgment.

### Binary Matching Issue

- The current career-skill layer still behaves like a binary match at the tag-to-skill step: if a module has a mapped tag such as `backend-engineering`, the related skill area is treated as matched and the module receives that skill area's weight.
- This is a reasonable candidate-generation signal, but it is weak as the complete ranker because not all tag matches are equally meaningful.
- For example, `Distributed Systems`, `Database Systems`, and `Introductory Web Development` may all match Software Engineer skill areas, but their expected career relevance can differ significantly depending on student level, prior experience, and target subpath.
- A simple count or binary match can rank these modules too similarly, even though a final-year student aiming for backend or platform engineering may benefit more from distributed systems than from an introductory web module.
- Future improvements should add evidence strength, course level/context, subpath preference, and tag confidence so a match can be graded rather than treated as simply present or absent.

### Next Planned Improvement

- Replace the current binary skill-area match with a weighted relationship model while keeping the recommender deterministic and backend-owned.
- Model career fit as a composition of career goal, skill-area importance, tag-to-skill relationship strength, and optional tag confidence rather than treating every mapped tag as equally strong.
- Keep hard filters separate from ranking: completed/fixed modules, slot fit, prerequisite feasibility, near-duplicate prior learning, and later availability/AU/programme constraints should be checked before final scoring.
- Keep career relevance as one ranking factor, not the whole definition of usefulness. Ranking should continue to combine career fit, student interest fit, curriculum/pathway fit, faculty/code preferences, unlock value, and diversity.
- Preserve explanations from the strongest contributing path, for example `Software Engineer -> backend and data services -> distributed-systems -> Distributed Systems`, instead of listing every matched signal.
- Start without adding tests in this immediate follow-up if requested, but the next quality step should still be focused backend tests for scoring and explanation behavior.
- Keep UI unchanged unless explicitly requested; the roadmap should continue rendering backend-assigned recommendations by `matchedChoiceSlotId`.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; print('backend import ok'); print('RecommendationScoreBreakdown' in str(backend.main.app.openapi()))"`.
- Ran `npm run lint` from `frontend`.
- Ran `npm run build` from `frontend`.
- Diagnostics return no issues.
- `git diff --check` passes.
- Confirmed a service-level `Software Engineering` module receives both existing career tag/keyword score and the new mapped career-skill score.

### Not Included

- No MyCareersFuture scraping or live labour-market data.
- No Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, or agent workflow.
- No new frontend UI and no visible score breakdown on roadmap cards.
- No automated test suite was added in this step; verification remains compile, lint, build, diagnostics, and service-level checks.
- No API rename from `recommendations` to `assignments`.
- No backend persistence, user table, authentication, or SSO.

## Weighted Career-Skill Matching

Status: Implemented locally

### Completed

- Replaced each Software Engineer skill area's flat tag list with weighted tag relationships in `backend/services/career_skill_mappings.py`.
- Added per-tag relationship strength, tag confidence, and rationale so mapped career evidence remains auditable.
- Updated backend career-skill scoring to calculate each skill area's contribution from `skill importance * strongest matching tag relationship * tag confidence`.
- Preserved `careerSkillScore` in the existing score breakdown instead of changing the recommendation API response shape.
- Kept hard filters before ranking: completed/fixed modules, slot fit, prerequisite feasibility, and near-duplicate prior learning still run outside the score calculation.
- Updated recommendation reasons to show the strongest contributing path, for example `Software Engineer -> backend and data services -> distributed-systems -> Distributed Systems`, instead of listing every mapped skill signal.

### Rationale Notes

- Weighted tag relationships make broad tags and direct tags behave differently, so one weakly related mapped tag no longer grants the full skill-area weight.
- The score remains deterministic and backend-owned, which keeps the frontend as a rendering layer for assigned recommendation slots.
- Career relevance remains one ranking component alongside student topic preferences, same-faculty preference, current-semester availability, unlock value, code-generation fallback penalties, and diversity tiebreaking.
- Each skill area still contributes at most its strongest matching tag so modules with many related tags do not automatically dominate only because of tag count.

### Verified

- Ran `.venv/bin/python -m compileall backend`.
- Ran `.venv/bin/python -c "import backend.main; print('backend import ok'); print('RecommendationScoreBreakdown' in str(backend.main.app.openapi()))"`.
- Ran `.venv/bin/python -c "import backend.main; print('backend import ok'); print('weighted static career-to-skill mappings' in str(backend.main.app.openapi()))"`.
- Ran a service-level scoring check confirming `distributed-systems` receives a stronger career-skill score than `web-development` and the recommendation reason includes the top career-skill path.
- Diagnostics return no issues.
- `git diff --check` passes.

### Not Included

- No automated tests were added in this step, by request.
- No roadmap UI change and no visible score breakdown display.
- No MyCareersFuture scraping, live job-market data, Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML logic, or agent workflow.
- No backend persistence, user table, authentication, SSO, or API rename from `recommendations` to `assignments`.

## Old Course-Code Exclusion For Recommendations

Status: Implemented locally

### Completed

- Replaced old-code fallback penalties with a hard eligibility exclusion before slot matching and scoring.
- Excluded `CE`, `CPE`, `CSC`, and `CZ` course-code prefixes from recommendation candidates because current CE/CSC curricula use `SC` course codes.
- Kept `SC` modules eligible as the primary current course-code family.
- Left service/common/math prefixes such as `MA`, `MH`, `CC`, `CV`, and `HW` unblocked until there is a clearer reason to exclude them.

### Rationale Notes

- Old course-code families should not be recommended at all, so they are now treated as eligibility exclusions instead of ranking preferences.
- This keeps relevance scoring focused on suitable current modules rather than using large negative penalties to approximate a hard rule.
- A catalog check found the CE faculty currently uses non-`SC` prefixes `CE` and `CPE`, while CSC also contains non-`SC` prefixes such as `CZ`, old `CSC`, `MA`, `MH`, `CC`, `CV`, and `HW`.
- `CE`, `CPE`, `CSC`, and `CZ` are treated as old course-code families; `MA`, `MH`, `CC`, `CV`, and `HW` are not automatically treated as old computing-course families.

### Not Included

- No contextual fallback penalty for old code families because the current rule is exclusion, not deprioritization.
- No frontend UI change.
- No automated tests were added in this step.

## Reviewer Notes On Recommender Validation

Status: Planned

### Decisions

- Treat `SC` as the primary current course-code family for CE/CSC recommendations.
- Treat `CE`, `CSC`, `CZ`, and `CPE` as old course-code families that should be excluded from recommendation candidates.
- Keep both safer scoring metadata and safer ranking behavior in view; they are complementary, not mutually exclusive.
- Implement safer scoring metadata first if the next goal is explainability and debugging.
- Implement safer ranking behavior first if the next goal is reducing bad visible recommendations such as old-code modules appearing instead of suitable current-code modules.
- Prefer doing both before the recommender is evaluated formally, but keep each as a separate small work unit.

### Safer Ranking Behavior To Consider

- Keep old course-code families as eligibility exclusions rather than fallback ranking candidates.
- If a future dataset proves that some non-`SC` code is still valid, handle it through an explicit allowlist or module-equivalence rule instead of weakening the old-code exclusion globally.
- Longer term, use module equivalence, successor relationships, or curated topic clusters to explain why an old code was excluded and which current-code module replaces it.
- Keep the hard-filter-before-ranking boundary intact: eligibility, fixed/completed modules, slot fit, prerequisite feasibility, and near-duplicate prior learning should still be checked before scoring.

### Safer Scoring Metadata To Consider

- Keep score components separately observable even if the roadmap UI does not display them.
- Add or internally log career-skill evidence such as career goal, skill area, skill-area importance, matched tag, relationship weight, tag confidence, and rationale.
- Add or internally log old-code exclusion details such as excluded code family and exclusion reason when debugging candidate filtering.
- Version the career-skill mapping or scoring model internally so historical recommendation comparisons remain understandable after weights are tuned.
- Preserve explanation fidelity: the displayed top career-skill path should match the actual highest-contributing scoring path.

### Aggregation And Confidence Caveats

- Current career-skill scoring takes the strongest matching tag per skill area, then sums skill-area contributions.
- This max-per-skill-area approach gives a clear explanation path, but can under-reward modules with several genuinely relevant tags inside the same skill area.
- A future capped top-n aggregation could reward breadth without letting many weak tags dominate, for example `x1 + 0.25*x2 + 0.10*x3`.
- Keep `relationship_weight` and `tag_confidence` conceptually separate: relationship weight means how strongly a tag supports a skill area, while tag confidence means how reliable the module's tag metadata is.
- Consider moderating confidence rather than multiplying it directly, for example `relationship_weight * (0.7 + 0.3 * tag_confidence)`, so incomplete metadata does not completely collapse a semantically strong match.

### Evaluation Plan

- Build a fixed labelled benchmark set before making many more ranking changes.
- Suggested benchmark size: 30 to 60 cases for CSC students with Software Engineer as the career goal.
- Include completed modules, eligibility constraints, candidate pools, expected relevance labels, expected explanation paths where possible, and whether old-code modules should be excluded.
- Compare old and new rankers on the same inputs using ranking, diversity, explanation, fallback, and constraint-validity metrics.
- Useful metrics include Precision@5, nDCG@5, coverage, explanation coverage, explanation fidelity, skill-area diversity@5, fallback exposure, and constraint validity.

### Automated Test Ideas

- Given equal eligibility and other signals, a stronger tag relationship should rank higher.
- A higher tag confidence should contribute at least as much as a lower confidence for the same relationship.
- The displayed top explanation path should match the path used to calculate the career-skill score.
- `CE`, `CPE`, `CSC`, and `CZ` course-code prefixes should be excluded from recommendation candidates.
- `SC` modules should remain eligible.
- Lower-priority code-family rules should not cause an ineligible module to be returned just to fill a slot.
