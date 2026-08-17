# FYP Course Recommendation

Clean rebuild of a course recommendation system for NTU students.

## Contents

- [Backend Setup](#setup)
- [Frontend Setup](#setup-frontend)

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
