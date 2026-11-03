# Development Plan

Detailed milestone order, recommendation priorities, authentication planning, and evaluation options moved from the root agent instructions.

Read [current status](../STATUS.md) for the next task and current evidence. This document preserves earlier planning guidance; historical completion counts and metrics below are not current runtime claims. Verify the relevant source, official integration documentation, tenant configuration, and available reference paths before implementation.

## Milestone Order

Follow this order unless I explicitly say otherwise.

For the high-level architecture and request flow, refer to [Diagrams.md](../architecture/Diagrams.md).

Struck-through items are complete. They are kept for history.

### Phase 1: Core App Foundation

1. ~~FastAPI health check~~
2. ~~Backend schemas and router structure~~

### Phase 2: Course Recommendation MVP

3. ~~Static roadmap API~~
4. ~~Minimal React frontend~~
5. ~~Connect frontend to roadmap API~~
6. ~~Profile page and state~~
7. ~~Transcript upload~~
8. ~~Curriculum guide upload and parsed roadmap display~~
9. ~~Basic MPE/choice-slot recommendation flow~~ (chat stub was deprioritised; recommendation engine was built instead)
10. ~~Backend-owned deterministic scoring, exact-slot assignment, career-skill mapping~~
11. ~~Offline benchmark evaluator (14 cases, nDCG ~0.705)~~
12. **NTU SSO authentication** ← next major milestone
13. Migrate user data from `localStorage` to server-side storage keyed by `oid`

### Phase 3: Recommendation Depth and Evaluation

14. ~~Expand career coverage beyond Software Engineer~~
15. ~~Counterfactual sensitivity tests~~ (script done; original FAIL was invalid — base case already had the tag; corrected on career-first-preference-policy branch)
16. ~~Coverage audit (check slot-fill rate across degree/cohort combinations)~~ (script done; 180 cells, 0 invariant violations, 0 empty slots after request-shape fix; earlier reported cybersecurity SC3xxx gap was a script bug — omitting `studentFaculty` suppressed the CSC faculty bonus, giving a false empty result; 26 cells with weak-fit picks flagged as quality observations)
17. Expert review / think-aloud evaluation session
18. RAGAS evaluation layer for explanation quality

### Phase 4: AI and Data Integrations (deferred)

These are intentionally deferred. Do not start them until phases 1–3 are solid.

19. ~~MyCareersFuture scraper~~ (deprioritised; static career-skill mapping is sufficient for now)
20. Neo4j client and graph loader
21. ChromaDB client
22. LangGraph state, workflow, and nodes
23. OpenAI integration for explanation generation

## Recommendation Improvement Priority

This table tracks the improvement work on the deterministic recommendation engine specifically. It overlaps with the milestones above intentionally — the milestones track feature delivery order, this table tracks scoring/ranking improvement order within the recommendation system.

| Priority | Improvement | Status |
| --- | --- | --- |
| 1 | Backend-side eligibility and per-slot ranking | ~~Done~~ |
| 2 | Structured scoring features and score breakdown | ~~Done~~ |
| 3 | Prerequisite readiness and unlock-value logic | ~~Done~~ |
| 4 | Curated course taxonomy and student preference profile | ~~Done~~ |
| 5 | Diversity-aware assignment across slots | ~~Done~~ |
| 6 | Static career-to-skill mapping | ~~Done~~ (all 6 career goals) |
| 7 | Benchmark calibration and weak-case review | ~~Done~~ (24-case benchmark, all careers covered) |
| 8 | Expand career-skill mapping to more career goals | ~~Done~~ (AI/ML, Data Engineer, Cloud/Platform, Cybersecurity, Data Scientist) |
| 9 | Counterfactual sensitivity tests | ~~Done~~ (7/7 pass after fix; original FAIL was a no-op check — base case already had the tag) |
| 10 | RAGAS / expert review evaluation | After system is stable |
| 11 | Neo4j or graph traversal | Later — only if prerequisite/skill queries outgrow SQL |
| 12 | Embeddings or vector search | Later — only for semantic matching of messy free text |
| 13 | LLM or LangGraph | Last — for explanation generation, not core ranking |

Do not jump to Neo4j, embeddings, LangGraph, or OpenAI before career expansion, counterfactual tests, and evaluation are done.

## NTU SSO Authentication

**Status: Not yet implemented. This is the next major feature after benchmark review.**

NTU SSO is done via **Microsoft Azure AD** (NTU uses Microsoft 365), using the OAuth 2.0 Authorization Code flow with the `msal` Python library. Reference implementation: `NTUCourseGenie` at `/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/NTUCourseGenie/course_v2/login_utils/login_ui.py`.

### How it works

1. **App Registration**: Register an app in NTU's Azure AD tenant. Requires `APP_REG_CLIENT_ID`, `APP_REG_CLIENT_SECRET`, and `AUTHORITY` (`https://login.microsoftonline.com/<ntu-tenant-id>`).

2. **Login initiation**: Backend (or frontend redirect) calls `app.get_authorization_request_url(scopes=["User.Read"])` to get the Azure AD auth URL, then redirects the user there.

3. **Callback**: After NTU login, Azure AD redirects back to the app with `?code=<auth_code>` in the URL.

4. **Token exchange**: Backend calls `app.acquire_token_by_authorization_code(auth_code, scopes=["User.Read"])`. Returns `access_token` and `id_token_claims`.

5. **NTU email validation**: Check `"ntu.edu.sg" in id_token_claims["preferred_username"]` to reject non-NTU accounts.

6. **User identity**: Use `id_token_claims["oid"]` (Azure Object ID) as the stable unique user identifier — it never changes even if the student's email or name changes.

7. **Profile picture**: Optionally fetch from `https://graph.microsoft.com/v1.0/users/{oid}/photo/$value` with the access token.

### Key design decisions

- Use `oid` (Azure Object ID) as the primary key for the user record in the database, not the student ID or email.
- Store `email` and `name` from `id_token_claims["preferred_username"]` and `id_token_claims["name"]` as display fields only.
- Do not build a fake NTU password form, scrape NTU login pages, or hardcode captured SAML/auth URLs.
- Do not use SAML unless NTU specifically provides a SAML metadata URL; prefer OIDC/OAuth via Azure AD.
- The `oid` is stable across devices and sessions: the same student logging in from any device gets the same `oid`, enabling cross-device persistence.

### How user data persists across sessions and devices

The `oid` from Azure AD is the anchor. It is stable forever — the same value is returned every time the same student logs in, from any device or browser.

**Why `oid` and not email or student ID:**

| Identifier | Problem |
|---|---|
| Email | Can change (graduation, name change) |
| Student/matric number | Not reliably exposed as an OIDC claim |
| `oid` | Stable forever, unique per user per tenant, same on every device |

**Session token flow:**

After the OAuth code exchange succeeds, the FastAPI backend should:
1. Verify the `oid` from `msal` token claims.
2. Look up or create the user record in the database by `oid`.
3. Issue its own JWT (or signed httpOnly cookie) with the `oid` embedded.
4. Return that JWT to the frontend.

The frontend sends the JWT on every API request. The Azure access token is used once to verify identity and never sent to the frontend.

```
First login (any device):
  Azure returns oid → backend checks DB → not found → create user record → issue JWT

Any later login (same or different device):
  Azure returns same oid → backend finds existing record → issue JWT with their data
```

**Current state vs. after SSO:**

- Right now the app uses `localStorage` with a self-declared Student ID.
- After SSO: the Student ID field goes away; `oid` is the identity.
- All profile, curriculum, transcript, and recommendation data moves to server-side storage keyed by `oid`.
- `localStorage` becomes a UI cache only (e.g., last active tab), not a data store.
- A student logging in on a phone gets the exact same state as on their laptop.

**Watch out for multiple Azure AD tenants:** NTU may have separate tenants for students and staff. Pin the `AUTHORITY` URL to the student tenant so non-NTU Microsoft accounts are rejected at the tenant level, before the email check.

### Required env vars

```
APP_REG_CLIENT_ID=<azure app registration client id>
APP_REG_CLIENT_SECRET=<azure client secret>
AUTHORITY=https://login.microsoftonline.com/<ntu-tenant-id>
```

### Rules for implementation

- Use Microsoft MSAL (`msal` Python package) for the backend token exchange.
- The FastAPI backend should own the OAuth callback endpoint (e.g., `GET /auth/callback`).
- Issue a server-side session token (e.g., JWT or opaque token stored in an httpOnly cookie) after the token exchange succeeds; do not pass the Azure access token to the frontend.
- Keep the app's internal user ID (`oid`) separate from the student's matriculation number.
- The student's matriculation number may be derivable from their NTU email but should not be treated as a stable identity key.

## Recommendation Evaluation

### Current approach

The current offline benchmark uses a hand-reviewed set of 14 cases evaluated with precision@k, nDCG@k, explanation coverage, explanation fidelity, skill-area diversity, old-code exposure, and constraint validity. This is deterministic and fast but relies entirely on manually reviewed labels.

### RAGAS eval framework

Explore using **RAGAS** (`ragas` Python package) for a more structured evaluation layer. RAGAS was designed for RAG pipelines but its metrics transfer well to recommendation systems with LLM-generated explanations:

- **Faithfulness**: does the recommendation explanation only make claims supported by the student's actual profile and curriculum data?
- **Answer relevancy**: does the recommended module actually address the student's career goal and topic preferences?
- **Context precision / recall**: are the right signals (career-skill mappings, prerequisite chain, student preferences) being used and weighted correctly?

RAGAS needs a dataset of `(question, context, answer, ground_truth)` tuples. For this system that maps to `(student profile, curriculum + career-skill context, recommended modules + explanation, reviewed positive labels)`.

Reference implementation in a past FYP: `/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/NTUCourseGenie/course_v2/ragas_eval/`

### Other evaluation approaches to explore

| Approach | What it measures | When to use it |
|---|---|---|
| **Offline benchmark (current)** | Precision@k, nDCG@k against hand-reviewed labels | Fast iteration; catches ranking regressions |
| **RAGAS** | Faithfulness and relevancy of LLM-generated explanations | Once explanations become a key output |
| **A/B or interleaving test** | Which ranking produces more clicks/accepts from real users | If real NTU students use the system |
| **Expert review / think-aloud** | Whether a knowledgeable person (supervisor, senior student) agrees with the top recommendations | Good for FYP evaluation chapter; low sample count is fine |
| **Counterfactual sensitivity** | Does changing career goal, completed modules, or preferences actually shift the ranked list in a sensible direction? | Catches cases where scoring is correct on average but insensitive to meaningful input changes |
| **Coverage audit** | What fraction of valid MPE/BDE slots can the system fill with at least one eligible recommendation? | Ensures the system does not silently leave slots empty for certain degree/cohort combinations |
| **Constraint validity (current)** | Are all hard rules (no old codes, no completed modules, slot type match) always satisfied? | Keep as a required pass on every benchmark run |

### Rules

- Do not replace the current offline benchmark with RAGAS; add it alongside as a complementary layer.
- Expert review is the most credible evaluation for an undergraduate FYP and should be included in the final report.
- Counterfactual sensitivity tests can be written as simple assertion scripts without a full test suite.
- Do not build the RAGAS or A/B evaluation layer until the recommendation system itself is stable.

## Reference Files From Past FYP Repos

Use these only when needed:

```text
/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/NTUCourseGenie/
/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/CourseNavigator/
/Users/zacklau/Desktop/y4s1/fyp/past-fyp-github/shing-hao/
```
