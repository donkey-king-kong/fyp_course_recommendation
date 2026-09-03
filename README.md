# FYP Course Recommendation

Clean rebuild of a course recommendation system for NTU students.

## Start Backend

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`. Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Start Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://127.0.0.1:5173`.

## Module Data

The module data currently comes from the standalone NTU scraper in `scraper/`. The scraper fetches NTU course pages, parses module information, and saves raw scraped output under `scraper/output/`.

Run the full configured scrape from the project root:

```bash
python scraper/scrape_ntu_courses.py --all
```

After scraping, normalize the scraped data into app-ready JSON:

```bash
python scraper/build_course_data.py
```

This creates `data/course_catalog.json` for unique module details and `data/course_offerings.json` for where and when modules are offered. The backend seed script then loads normalized module data into PostgreSQL for the module catalog and recommendation APIs.

## Recommendation Logic

- The supported career goal is currently `Software Engineer`.
- The frontend sends the uploaded curriculum roadmap, open choice slots, completed modules, profile major, career goal, and topic preferences to `POST /recommendations`.
- The backend owns recommendation filtering, ranking, and exact slot assignment.
- Hard filters run before scoring: already completed modules, fixed curriculum modules, old CE/CSC code families, slot-level mismatch, prerequisite feasibility, and near-duplicate prior learning.
- MPE slots such as `SC3xxx` and `SC4xxx` receive current CSC `SC` modules at the matching level.
- BDE slots can use broader active-faculty module candidates, subject to slot fit and ranking rules.
- Career relevance is deterministic, not AI-based: `Software Engineer` maps to weighted skill areas, and those skill areas map to curated recommendation tags.
- Student topic preferences are soft boosts, not hard filters.
- Broad-default and specialist metadata helps no-preference Software Engineer recommendations prefer generally useful modules before niche ones.
- Missing prerequisites can be returned as planned prerequisite roadmap nodes and arrows when useful for planning.
- Recommendation score breakdowns are returned by the API for inspection, but the roadmap UI does not display them yet.
- Roadmap readiness is handled by `POST /roadmap/readiness`, including academic-standing requirements based on completed AU.
- This project does not use Neo4j, ChromaDB, LangGraph, OpenAI, embeddings, ML ranking, MyCareersFuture scraping, backend user persistence, or production auth yet.
