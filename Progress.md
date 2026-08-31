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
