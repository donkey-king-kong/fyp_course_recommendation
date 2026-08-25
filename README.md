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

Scrape all configured academic semester and course-year combinations:

```bash
python scraper/scrape_ntu_courses.py --all
```

The batch scraper currently includes:

- Academic semesters from `2022_1` to `2026_1`, excluding special terms.
- Computer Science Year 1 to Year 4.
- Computing Year 1 to Year 3.
- Data Science & Artificial Intelligence Year 1 to Year 4.
- Economics & Data Science Year 1 to Year 4.
- Computer Engineering Year 1 to Year 4.
- Renaissance Engineering (CE) Year 2 to Year 4.
- Renaissance Engineering (CSC) Year 2 to Year 4.
- Accountancy and Data Science & Artificial Intelligence Year 1 to Year 5.
- Business and Computer Engineering Year 1 and Year 4.
- Business and Computing Year 1 to Year 4.
- Computer Engineering and Economics Year 1 to Year 5.
- Computer Science and Economics Year 1 to Year 5.
- One JSON output file per academic semester and course-year combination in `scraper/output/`.

Current scraper scope:

- Fetches the NTU course page using a form POST.
- Extracts course code, title, description, number of credits, grading type, prerequisites, mutually exclusive courses, and programme availability restrictions.
- Keeps generated output in `scraper/output/` so the scraped JSON files can be committed.
- Does not add a backend endpoint, database storage, scheduled scraping, or recommendation logic yet.

## Normalize Scraped Course Data

After scraping, build normalized app-ready data:

```bash
python scraper/build_course_data.py
```

This creates:

- `data/course_catalog.json`: one unique record per course code.
- `data/course_offerings.json`: one record per academic year, semester, programme, study year, and course code.

The catalog answers what each course is.

The offerings file answers where and when each course appears.
