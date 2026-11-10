# LinkedIn job-data access for course recommendations

**Flow ID:** `job-data-researcher`  
**Research cutoff / access date:** 2026-11-10  
**Scope:** Official LinkedIn access, public job pages, automation boundaries,
rate/retention/privacy, and lawful MVP alternatives. Primary sources only.
This is product-planning research, not legal advice.

## Executive answer

**Confirmed facts**

1. LinkedIn's self-service API permissions cover sign-in identity fields and
   member posting, not retrieval of LinkedIn's job-search inventory. Most other
   permissions and partner programs require LinkedIn approval. [C01]
2. The documented Job Posting API lets authorized clients, applicant tracking
   systems (ATSs), and job distributors send jobs *to* LinkedIn. LinkedIn says
   it is not accepting new partnerships for that API and directs prospective
   partners to Apply Connect. [C02]
3. Apply Connect is an ATS-to-LinkedIn posting and application workflow. It is
   partner access, requires an eligible LinkedIn Recruiter license for real-time
   LinkedIn data in the ATS, and is not documented as a general job-search feed.
   [C03]
4. Some job-posting information can be visible to Visitors, but LinkedIn's User
   Agreement separately prohibits scraping/copying the Services, unauthorized
   automated access, bypassing access controls or use limits, and unconsented
   copying/use/display/distribution of information obtained from the Services.
   Public visibility therefore does not itself grant product-ingestion rights.
   [C04]
5. LinkedIn's `robots.txt` states that automated access without express
   permission is prohibited, supplies a permission contact, and disallows job
   search/guest/API paths for named major search crawlers. Its Crawling Terms
   limit ordinary permitted crawling to authorized paths and public search
   indexing unless LinkedIn separately approves another use. [C05]
6. LinkedIn's API Terms also prohibit an application from accessing, storing,
   displaying, or transferring LinkedIn content obtained outside the APIs by
   scraping/crawling or through a third party. They generally prohibit storing
   API Content, including hashed or transformed information, except where
   expressly allowed. [C06]

**Planner interpretation**

LinkedIn should **not** be the MVP's job-data source. There is no official,
self-service job-search inventory API identified in LinkedIn's current
documentation, and page scraping, logged-in browser automation, third-party
scraped datasets, or access-control workarounds conflict with the cited
contractual and crawling rules. Low request volume does not cure lack of
permission. [C01-C06]

**Recommended default**

Use a licensed cross-employer API such as Adzuna for live advertisements,
supplement with USAJOBS where US federal coverage is useful, and normalize
occupation/skill demand with O*NET and/or ESCO. Add Greenhouse or Lever feeds
only for employers that authorize the integration or after confirming that the
applicable provider terms permit the intended reuse. Keep a LinkedIn partner
application as a later, non-blocking business-development track. [C13-C18]

Do not ingest, reproduce, embed, summarize, or train on LinkedIn job-page
content unless a signed LinkedIn agreement expressly authorizes this exact
course-recommendation use, storage model, derived data, and display.

## Confirmed LinkedIn access facts

### Official APIs and partner access

| Claim | Confirmed fact | Planning consequence |
|---|---|---|
| C01 | LinkedIn uses OAuth 2.0. Only the listed Open Permissions are self-service: authenticated member `profile`, `email`, and `w_member_social`; most permissions/programs require explicit approval. Talent integrations require an application to LinkedIn's partner program. [S1] | Creating a developer app does not provide job-search data. |
| C02 | The Job Posting API is for authorized parties to post jobs to LinkedIn. The current overview says LinkedIn is not accepting new Job Posting API partnerships and points applicants to Apply Connect. [S2] | It is an outbound publishing integration, not a documented read/search API for LinkedIn inventory. Do not put it on the MVP critical path. |
| C03 | Apply Connect lets a LinkedIn partner send jobs/application questions, receive applications and skills-match data, and send applicant status. Access to real-time LinkedIn data in an ATS requires a LinkedIn Recruiter Corporate or Professional Services license. [S3] | Relevant to an ATS product or employer workflow, not to general labor-market ingestion. |
| C07 | LinkedIn documents API- and XML-feed-based ingestion of externally created jobs. Its Basic Jobs category includes jobs gathered from ATSs, job boards, distributors, and aggregators. [S4] | A provider sending jobs to LinkedIn does not imply a reciprocal right to retrieve LinkedIn's resulting inventory. |

**Interpretation:** Absence of a documented search endpoint is not proof that no
private commercial agreement can ever provide one. It means the planner should
assume **no accessible LinkedIn inventory feed** until LinkedIn grants written
access and supplies governing terms.

### Public job pages are not an ingestion license

| Claim | Confirmed fact | Planning consequence |
|---|---|---|
| C04 | LinkedIn says shared information, including job postings, may be seen by Members, Visitors, or people off the Services. The same User Agreement prohibits software/scripts/robots that scrape or copy the Services; unauthorized bots; bypassing access controls/use limits; and copying, using, displaying, or distributing information obtained from the Services without the content owner's consent. [S5, sections 2.5 and 8.2] | Human-visible or search-indexed content must not be treated as an open dataset. Do not build guest-page crawlers or logged-in collection. |
| C08 | LinkedIn's official help page says third-party software, crawlers, bots, plug-ins, and extensions that scrape or automate activity are not permitted and can lead to account restriction or shutdown. [S6] | Do not use headless browsers, browser extensions, session cookies, login automation, or employee accounts for collection. |
| C05 | `robots.txt` opens with an express-permission requirement and gives `whitelist-crawl@linkedin.com` for applications. It disallows paths including `/jobs?runSearch*`, `/jobs-guest/`, `/api/jobPostings/jobs*`, and `/jsearch*` for named major crawlers. LinkedIn's Crawling Terms prohibit unapproved automated crawling and ordinarily confine approved use to public search indexing. [S7, S8] | Robots directives are an additional boundary, not a grant. A permission request is possible, but the default crawling purpose does not fit course recommendations. |

**Boundary:** No bypasses, proxy rotation, CAPTCHA solving, user-agent spoofing,
cookie replay, rate-limit evasion, or login automation are acceptable options.
The approved-crawling channel is usable only if LinkedIn gives written
permission covering the exact paths and product purpose.

### API rate, retention, security, and privacy

| Claim | Confirmed fact | Planning consequence |
|---|---|---|
| C09 | LinkedIn API requests have application- and member-level 24-hour limits. Limits reset at midnight UTC; endpoint quotas are not publicly listed, are shown in the Developer Portal, and excess requests receive HTTP 429. [S9] | Capacity cannot be estimated from public quota numbers. A partner design must implement quota telemetry and 429 backoff using the granted endpoint limits. |
| C06 | API Terms section 3.1 prohibits trying to exceed/circumvent call limits and prohibits use of LinkedIn content obtained outside official APIs, even indirectly from a third party. Section 4.1 prohibits capture/copy/cache/storage of Content or information expressed by it, including hashed or transformed data, unless expressly permitted. [S10] | Buying a scraped dataset does not solve provenance. Skills extracted from LinkedIn text, embeddings, hashes, and summaries should be treated as covered derived information, not as a workaround. |
| C10 | Where API Content storage is permitted, it must be identifiable, segregable, selectively deletable, retained only as long as needed for the user service, and not put in a repository accessible to unrelated third parties. User-linked API Content must be deleted on request/account closure; stored Content must also be deleted on specified termination, suspension, or cessation events. [S10, sections 4.1, 4.4, 4.5] | A future integration needs source-level lineage, selective deletion, expiry, and termination purge procedures before launch. |
| C11 | The API Terms require a user agreement and privacy policy, legally valid member consent before accessing member Content, disclosure of collection/use/deletion, and security controls including access controls, monitoring, incident response, and encryption in transit and at rest. [S10, sections 5.1, 5.2, 7.1] | Avoid member/applicant data unless essential. Partner access would add consent, deletion, audit, and incident obligations. |
| C12 | Under GDPR principles, covered personal-data processing needs a legal ground, must be limited to what is necessary, should be kept for the shortest possible time with erase/review limits, and requires transparent information including purpose, legal basis, retention, recipients, rights, and source when indirectly collected. [S11-S14] | Recruiter names/emails and applicant/member data need jurisdiction-specific review. The MVP should omit them and process job attributes rather than people. |

**Recommended controls regardless of provider**

- Store provider ID, provenance, retrieval time, source URL where licensed,
  title, employer, location, description/skill fields, and closure/expiry state.
- Exclude applicant profiles, LinkedIn member data, recruiter contact details,
  demographic inferences, and sensitive/protected attributes.
- Keep raw text only where provider terms permit it. Keep derived skills or
  embeddings only where the license clearly permits derivatives and model use.
- Use provider-specific refresh, deletion, and attribution rules. Purge jobs
  removed at source on the next refresh and define a short fallback expiry.
- Maintain per-source rate budgets, conditional requests where supported,
  exponential backoff for 429/5xx responses, and a kill switch.
- Do not train or fine-tune a model on provider content unless the provider
  agreement expressly permits training. For inference, transmit only fields
  permitted by the source agreement and the model processor agreement.

These controls are planner recommendations, not claims that every listed
provider imposes the same terms.

## Feasible source options

| Option | Primary-source evidence | Feasibility and limits | Verdict |
|---|---|---|---|
| LinkedIn Talent partner integration | Talent access requires application; Job Posting API intake is closed to new partnerships; Apply Connect is an ATS/application integration with licensing and certification requirements. [S1, S2, S3] | Possible only if LinkedIn approves a relevant commercial use. Current documented products do not expose general inventory search. | **Future track only** |
| LinkedIn approved crawling | LinkedIn accepts permission requests, but default Crawling Terms confine permitted use to authorized paths and public search indexing unless separately approved. [S7, S8] | Course recommendation requires explicit alternative-use, storage, derivation, and display permission. | **Not an MVP assumption** |
| Adzuna API (C13) | Adzuna's official developer site offers authenticated REST search over its job-ad database. Search responses include job fields and a redirect URL; public docs say descriptions are snippets. [S15, S16] | Cross-employer coverage and a fit for demand signals. Commercial plan, geography, quota, attribution, retention, derivative/LLM rights, and service terms must be confirmed in writing before production. | **Recommended live-job default, contract-gated** |
| Employer-authorized Greenhouse Job Board API (C14) | Greenhouse documents public, unauthenticated GET endpoints returning a company's published jobs as JSON; application submission is separately authenticated. [S17] | Good for an employer allowlist. Documentation frames the API around the customer's own career site, so do not assume unrestricted cross-customer aggregation rights. | **Recommended supplement with permission** |
| Employer-authorized Lever Postings API (C15) | Lever documents list/detail endpoints for published company postings and states published postings are public; its API is designed to create a job site. It does not provide global full-text search across employers. [S18] | Good for approved employers, but each company's postings are namespaced and reuse must follow applicable terms/authorization. | **Recommended supplement with permission** |
| USAJOBS Search API (C16) | The US Office of Personnel Management documents `GET /api/Search` for lightweight job-announcement consumption by commercial job boards, mobile apps, and social-media sites; it uses API-key authentication. [S19] | Authoritative US federal jobs, not private-sector coverage. | **Recommended where geography fits** |
| O*NET Web Services/database (C17) | The US Department of Labor-sponsored service exposes the O*NET database through an API; the database describes occupations and worker/work characteristics, including skill requirements. [S20, S21] | Strong occupation-to-skill baseline, but not a live-vacancy feed. Follow the stated O*NET database license/attribution. | **Recommended normalization layer** |
| ESCO API/classification (C18) | The European Commission provides ESCO APIs for occupations, skills, and their relationships, including uses such as job matching, skills intelligence, career guidance, and training suggestions. [S22, S23] | Strong multilingual EU-oriented taxonomy, but not a live-vacancy feed. | **Recommended normalization layer** |
| Direct employer feeds/contracts | LinkedIn itself documents that jobs originate in ATSs, company sites, job boards, distributors, and aggregators. [S4] | Highest provenance and clearest permission when contracted, but slower employer-by-employer coverage. | **Preferred strategic source** |

## Recommended MVP source contract

1. **Live demand:** procure Adzuna API access only after the agreement confirms
   commercial display, caching/retention, attribution, derivatives/skill
   extraction, LLM inference, and deletion requirements.
2. **Public-sector demand:** add USAJOBS if US federal roles are in scope.
3. **Skill normalization:** map extracted terms to O*NET for US occupation
   coverage and/or ESCO for multilingual European coverage.
4. **High-quality employer data:** onboard Greenhouse/Lever employers through an
   allowlist backed by employer authorization or provider terms that clearly
   permit this product's use.
5. **LinkedIn:** show no LinkedIn job content, copied descriptions, derived
   embeddings, or LinkedIn-sourced records. Do not make automated requests.
   Revisit only after written LinkedIn approval and legal review.
6. **Recommendation behavior:** recommend courses from aggregated skill demand,
   not from personal/member profiles, and retain evidence links to the licensed
   source records.

**Go/no-go gate:** If no live-job provider grants commercial derivative and LLM
rights, launch with O*NET/ESCO occupation-skill mappings plus manually
contracted employer feeds. Do not substitute LinkedIn scraping.

## Claim-to-source map

| Claim | Exact support |
|---|---|
| C01 | S1, introductory access rules, Open Permissions table, and Talent section |
| C02 | S2, opening notice and first paragraph |
| C03 | S3, overview, Components, Requirements, and integration steps |
| C04 | S5, sections 2.5 and 8.2 |
| C05 | S7 opening notice and named crawler path rules; S8 clauses 1-8 |
| C06 | S10, sections 3.1 and 4.1 |
| C07 | S4, “Ingesting Jobs on LinkedIn” and “Job Posting Categories” |
| C08 | S6, opening paragraphs, prohibited list, and account consequence |
| C09 | S9, “Rate Limiting” and application/member limit sections |
| C10 | S10, sections 4.1, 4.4, and 4.5 |
| C11 | S10, sections 5.1, 5.2, and 7.1 |
| C12 | S11 GDPR Article 6 summary; S12 Article 5(1)(c); S13 Article 5(1)(e); S14 Articles 12-14 summary |
| C13 | S15 API purpose/quickstart; S16 Search endpoint and response fields |
| C14 | S17 Introduction, Authentication, and Jobs/List jobs |
| C15 | S18 Introduction and “Get a list of job postings” |
| C16 | S19 endpoint purpose, authorization, and query parameters |
| C17 | S20 API purpose; S21 database overview and usage-license section |
| C18 | S22 API purpose; S23 classification description and current-version statement |

## Primary sources

| ID | Source title | Owner | Source date | Access date | URL |
|---|---|---|---|---|---|
| S1 | Getting Access to LinkedIn APIs | LinkedIn, published on Microsoft Learn | Updated 2025-06-26 | 2026-11-10 | https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access |
| S2 | Job Posting API | LinkedIn, published on Microsoft Learn | Current documentation view `li-lts-2026-04`; page date not stated | 2026-11-10 | https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/overview |
| S3 | Apply Connect overview | LinkedIn, published on Microsoft Learn | Updated 2026-09-09 | 2026-11-10 | https://learn.microsoft.com/en-us/linkedin/talent/apply-connect/apply-connect-overview |
| S4 | Job Posting Overview | LinkedIn, published on Microsoft Learn | 2023-05-08 | 2026-11-10 | https://learn.microsoft.com/en-us/linkedin/talent/job-postings/job-posting-overview |
| S5 | User Agreement | LinkedIn | Effective 2025-11-03 | 2026-11-10 | https://www.linkedin.com/legal/user-agreement |
| S6 | Prohibited software and extensions | LinkedIn Help | Page gives relative “2 years ago”; exact date not stated | 2026-11-10 | https://www.linkedin.com/help/linkedin/answer/56347 |
| S7 | robots.txt | LinkedIn | No date stated; live control file | 2026-11-10 | https://www.linkedin.com/robots.txt |
| S8 | LinkedIn Crawling Terms and Conditions | LinkedIn | Revised 2017-05-25 | 2026-11-10 | https://www.linkedin.com/legal/crawling-terms |
| S9 | Rate Limiting | LinkedIn, published on Microsoft Learn | Updated 2025-08-20 | 2026-11-10 | https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits |
| S10 | API Terms of Use | LinkedIn | Revised 2022-12-13; effective for existing developers 2023-01-13 | 2026-11-10 | https://developer.linkedin.com/legal/api-terms-of-use |
| S11 | When can personal data be processed? | European Commission | No page date stated; summarizes GDPR Article 6 | 2026-11-10 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/legal-grounds-processing-data/grounds-processing/when-can-personal-data-be-processed_en |
| S12 | How much data can be collected? | European Commission | No page date stated; summarizes GDPR Article 5(1)(c) | 2026-11-10 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/how-much-data-can-be-collected_en |
| S13 | For how long can data be kept and is it necessary to update it? | European Commission | No page date stated; summarizes GDPR Article 5(1)(e) | 2026-11-10 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/how-long-can-data-be-kept-and-it-necessary-update-it_en |
| S14 | What information must be given to individuals whose data is collected? | European Commission | No page date stated; summarizes GDPR Articles 12-14 | 2026-11-10 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/what-information-must-be-given-individuals-whose-data-collected_en |
| S15 | Build with Adzuna / API Overview | Adzuna | No page date stated | 2026-11-10 | https://developer.adzuna.com/overview |
| S16 | Search | Adzuna | No page date stated | 2026-11-10 | https://developer.adzuna.com/docs/search |
| S17 | Job Board API | Greenhouse Software | No page date stated | 2026-11-10 | https://developers.greenhouse.io/job-board.html |
| S18 | Lever Postings API | Lever | Living official repository; page date not stated | 2026-11-10 | https://github.com/lever/postings-api |
| S19 | API Reference: GET `/api/Search` | USAJOBS, US Office of Personnel Management | No page date stated | 2026-11-10 | https://developer.usajobs.gov/API-Reference/GET-api-Search |
| S20 | O*NET Web Services | National Center for O*NET Development / US Department of Labor Employment and Training Administration | Site updated 2026-10-06 | 2026-11-10 | https://services.onetcenter.org/ |
| S21 | O*NET 31.0 Database | National Center for O*NET Development / US Department of Labor | Version 31.0; page date not stated | 2026-11-10 | https://www.onetcenter.org/database.html |
| S22 | Use ESCO Services (API) | European Commission, DG Employment, Social Affairs and Inclusion | No page date stated | 2026-11-10 | https://esco.ec.europa.eu/en/use-esco/use-esco-services-api |
| S23 | What is ESCO? | European Commission, DG Employment, Social Affairs and Inclusion | ESCO v1.2.1, updated 2025-12-10 | 2026-11-10 | https://esco.ec.europa.eu/en/about-esco/what-esco |

## Unresolved before procurement

- Obtain the full commercial terms for the chosen job provider; public API
  documentation alone does not settle quotas, retention, redistribution,
  model-input, training, or derivative-data rights.
- Confirm launch jurisdictions and complete privacy review for any remaining
  personal data.
- Define source-specific deletion SLAs and test removal propagation.
- Require provenance warranties for any brokered dataset; reject data whose
  origin or collection permission cannot be demonstrated.
- Re-check all live terms immediately before contracting or launching because
  LinkedIn and provider access programs can change.
