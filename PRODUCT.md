# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary users are NTU students planning degree modules and future course choices. They use the product while setting up a profile, uploading curriculum guide and transcript PDFs, reviewing their personalized roadmap, and deciding which open MPE or BDE slots to fill next.

Academic advisers or reviewers may inspect the system, but they are not the primary design audience unless later confirmed.

## Product Purpose

FYP Course Recommendation helps NTU students understand their curriculum roadmap, match completed transcript modules against that roadmap, and receive suitable next-course recommendations.

Success means a student can see what curriculum structure applies to them, what they have already completed, which slots remain open, and why recommended modules fit their profile, prerequisites, curriculum constraints, and career goal.

## Positioning

The product combines three mechanisms that future work should preserve:

- Roadmap-first planning from an uploaded NTU curriculum guide rather than a generic static roadmap.
- Parser-backed completion matching from uploaded transcripts rather than only self-declared completed courses.
- Backend-owned deterministic recommendation logic that assigns eligible modules to exact open curriculum slots using constraints, career-skill mapping, preferences, prerequisite readiness, unlock value, and diversity.

## Operating Context

Students currently use the app as a local web prototype with a React frontend and FastAPI backend. The frontend collects browser-side profile, curriculum, transcript, completion, and recommendation state, then sends user-controlled state to backend APIs for parsing, matching, readiness, and recommendations.

The expected student workflow is:

- Set or update profile fields such as major, career goal, and topic preferences.
- Upload a curriculum guide PDF to define the roadmap structure.
- Upload a transcript PDF to extract completed or exempted modules.
- View a personalized roadmap that reflects the uploaded curriculum guide and matched transcript completions.
- Request recommendations for open MPE or BDE slots.

## Capabilities and Constraints

Current capabilities include FastAPI routes and services, a PostgreSQL-backed module catalog, static CSC roadmap sample data, curriculum guide PDF parsing, transcript PDF parsing, personalized roadmap matching, roadmap readiness checks, and deterministic recommendations for Software Engineer-oriented skill mapping.

The frontend is a Vite React TypeScript app with ReactFlow kept as a graph visualization dependency and Zustand for browser-side state. The backend uses Python, FastAPI, Pydantic, PyMuPDF, SQLAlchemy, PostgreSQL support, and Uvicorn.

Confirmed constraints:

- The backend owns recommendation filtering, ranking, and exact slot assignment.
- Completed modules, fixed curriculum modules, old CE/CSC code families, slot mismatch, prerequisite infeasibility, and near-duplicate prior learning are hard-filtered before ranking.
- Browser `localStorage` is prototype persistence only and must not be treated as trusted production storage.
- If no curriculum guide is uploaded, the roadmap page should show an empty state rather than defaulting to static sample data as the student's roadmap.
- The static roadmap JSON is sample/test data, not the final source of truth for a student's uploaded roadmap.
- NTU SSO is planned through Microsoft Azure AD OAuth using MSAL, with Azure Object ID (`oid`) as the stable internal user identity.
- Neo4j, ChromaDB, LangGraph, OpenAI, MyCareersFuture scraping, embeddings, ML ranking, and LLM explanation generation are intentionally deferred.

Open decisions:

- How broad the career-skill mapping should become beyond Software Engineer.
- When user data should move from browser storage to server-side persistence keyed by `oid`.
- Whether future explanation quality needs RAGAS, expert review, or both.

## Brand Commitments

The product name in the repository is FYP Course Recommendation. Existing UI copy has also used NTU Course Recommender. Future naming should avoid implying official NTU ownership unless that status is confirmed.

The project should remain beginner-friendly for the builder, with simple milestones, readable code, and explanations of why files exist.

## Evidence on Hand

Real evidence and source materials include:

- `README.md` for run instructions and recommendation logic summary.
- `Diagrams.md` for product architecture and student-context flow.
- `Progress.md` and `Progress2.md` for completed feature history and next steps.
- `AGENTS.md` for rebuild rules, architecture style, milestone order, and constraints.
- `data/test_csc_roadmap.json` and related roadmap data as sample/test data.
- Uploaded curriculum guide and transcript PDFs during local prototype use.

Do not fabricate production users, deployment status, NTU endorsement, expert validation, or benchmark claims beyond the repository's recorded evaluation results.

## Product Principles

- Uploaded curriculum guide data should define the student's roadmap before recommendations are shown.
- Transcript-derived completions should enrich the roadmap but not replace curriculum structure.
- Recommendations should be explainable, deterministic, and constraint-valid before adding AI.
- The UI should help students understand planning consequences without exposing unnecessary scoring internals.
- The rebuild should favor small understandable steps over broad architecture jumps.

## Accessibility & Inclusion

The product should be usable by students reviewing dense academic planning information, including long course titles, technical module codes, missing data, empty states, and error states. Future UI work should preserve keyboard access, readable contrast, responsive layouts, and clear non-color-only status indicators.
