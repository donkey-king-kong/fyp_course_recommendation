# FYP Course Recommendation

Clean rebuild of a course recommendation system for NTU students.

## Contents

- [Backend Setup](#setup)
- [Frontend Setup](#setup-frontend)
- [NTU Course Scraper](#ntu-course-scraper)

## Current State

- Backend exposes `GET /health` and `GET /roadmap`.
- Frontend loads roadmap data from the backend.
- Frontend displays a plain roadmap summary and course list.

## Setup

Create and activate a local Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

## Run The Backend

Start the FastAPI development server:

```bash
uvicorn backend.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## Test The Health Check

Open this URL in a browser:

```text
http://127.0.0.1:8000/health
```

Or test it from the terminal:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Setup Frontend

Install frontend dependencies:

```bash
cd frontend
npm install
```

## Run The Frontend

Start the Vite development server:

```bash
npm run dev
```

The frontend will run at:

```text
http://127.0.0.1:5173
```

To load roadmap data in the frontend, run the backend and frontend at the same time.

## NTU Course Scraper

The `scraper/` folder is a standalone prototype for scraping NTU course/module information.

It is intentionally separate from `backend/` and `frontend/` while the NTU page structure is still being explored.

Install scraper dependencies from the project root:

```bash
pip install -r scraper/requirements.txt
```

Run the scraper for Computer Science Year 1 in academic semester `2026_1`:

```bash
python scraper/scrape_ntu_courses.py --acadsem 2026_1 --course-yr "CSC;;1;F"
```

Save parsed JSON and raw HTML output for debugging:

```bash
python scraper/scrape_ntu_courses.py \
  --acadsem 2026_1 \
  --course-yr "CSC;;1;F" \
  --output scraper/output/csc-year-1.json \
  --raw-html-output scraper/output/csc-year-1.html
```

Current scraper scope:

- Fetches the NTU course page using a form POST.
- Extracts course code, title, description, number of credits, and mutually exclusive courses.
- Keeps generated output in `scraper/output/`, which is ignored by Git.
- Does not add a backend endpoint, database storage, scheduled scraping, or recommendation logic yet.
