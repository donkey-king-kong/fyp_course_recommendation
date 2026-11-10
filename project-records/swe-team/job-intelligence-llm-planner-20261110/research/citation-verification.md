# Verification Report

**Mode:** Search  
**Document:** Fixed Pass 1 inventory `citation-claims.md`  
**Generated:** 2026-11-10  
**Inventory integrity:** 173 input rows; no claims added, removed, or re-extracted.

## Summary

| Metric | Count |
|---|---:|
| Total claims extracted | 173 |
| Verified | 117 |
| Numerical Error | 0 |
| Unverified | 46 |
| Citation Not Found | 0 |
| Hallucination | 1 |
| Misleading | 9 |
| Inaccessible | 0 |
| Planner-safe as written | 117 |
| Planner-safe after stated correction | 10 |
| Excluded from planner reliance | 46 |

**Overall Status:** FAIL: 56 inventory claims are not reliable as written. Ten can be retained only in the corrected form below; 46 must be excluded.

## Decision Rules Applied

- The fixed inventory was checked in ID order.
- A cited claim was marked Verified only where the cited primary source supports the exact statement or a meaning-preserving paraphrase.
- Negative conclusions inferred only from documentation silence were not treated as exact source claims.
- Internal planner defaults, launch gates, schedules, and descriptions of document contents without a cited external authority were marked Unverified. The research files were used only for citation metadata, as instructed.
- Current live source text controls. This matters for `LA046`: the page now has a stated update date.
- Mandatory search patterns applicable to academic, company/product, government/policy, and statistics claims were run in addition to direct primary-source retrieval. Secondary results were not used to elevate a claim to Verified.

## Primary Source Locations

These keys are used in the sequential ledger. Locations after `#` are page anchors or named sections.

| Key | Exact primary URL |
|---|---|
| LA-S1 | https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access |
| LA-S2 | https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/overview |
| LA-S3 | https://learn.microsoft.com/en-us/linkedin/talent/apply-connect/apply-connect-overview |
| LA-S4 | https://learn.microsoft.com/en-us/linkedin/talent/job-postings/job-posting-overview |
| LA-S5 | https://www.linkedin.com/legal/user-agreement |
| LA-S6 | https://www.linkedin.com/help/linkedin/answer/56347 |
| LA-S7 | https://www.linkedin.com/robots.txt |
| LA-S8 | https://www.linkedin.com/legal/crawling-terms |
| LA-S9 | https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits |
| LA-S10 | https://developer.linkedin.com/legal/api-terms-of-use |
| LA-S11 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/legal-grounds-processing-data/grounds-processing/when-can-personal-data-be-processed_en |
| LA-S12 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/how-much-data-can-be-collected_en |
| LA-S13 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/how-long-can-data-be-kept-and-it-necessary-update-it_en |
| LA-S14 | https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/what-information-must-be-given-individuals-whose-data-collected_en |
| LA-S15 | https://developer.adzuna.com/overview |
| LA-S16 | https://developer.adzuna.com/docs/search |
| LA-S17 | https://developers.greenhouse.io/job-board.html |
| LA-S18 | https://github.com/lever/postings-api |
| LA-S19 | https://developer.usajobs.gov/API-Reference/GET-api-Search |
| LA-S20 | https://services.onetcenter.org/ |
| LA-S21 | https://www.onetcenter.org/database.html |
| LA-S22 | https://esco.ec.europa.eu/en/use-esco/use-esco-services-api |
| LA-S23 | https://esco.ec.europa.eu/en/about-esco/what-esco |
| EO-S01 | https://www.w3.org/TR/json-ld11/ |
| EO-S02 | https://schema.org/JobPosting |
| EO-S03 | https://developers.google.com/search/docs/appearance/structured-data/job-posting |
| EO-S04 | https://json-schema.org/draft/2020-12/json-schema-core.html |
| EO-S05 | https://developers.openai.com/api/docs/guides/structured-outputs |
| EO-S06 | https://www.onetcenter.org/content.html |
| EO-S07 | https://www.onetcenter.org/database.html |
| EO-S08 | https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-api |
| EO-S09 | https://ec.europa.eu/esco/api/doc/esco_api_doc.html |
| EO-S10 | https://isco.ilo.org/en/isco-08/ |
| EO-S11 | https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html |
| EO-S12 | https://www.w3.org/TR/prov-o/ |
| EO-S13 | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls |
| EO-S14 | https://www.rfc-editor.org/rfc/rfc8785.html |
| EO-S15 | https://doi.org/10.1109/SEQUEN.1997.666900 |
| EO-S16 | https://www.rfc-editor.org/rfc/rfc9110.html |
| EO-S17 | https://www.rfc-editor.org/rfc/rfc9111.html |
| EO-S18 | https://www.sitemaps.org/protocol.html |
| EO-S19 | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap |
| EO-S20 | https://www.rfc-editor.org/rfc/rfc9309.html |
| EO-S21 | https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety |
| EO-S22 | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html |

## Sequential Claim Ledger

`None` in the correction column means the inventory wording may be relied upon as written. “Exclude” means no planner reliance is permitted.

### LinkedIn Access Claims

| ID | Status | Exact source location | Confidence | Correction or planner action |
|---|---|---|---|---|
| LA001 | Unverified | No cited primary URL | - | Exclude; an internal cutoff/access-date assertion is not externally verifiable. |
| LA002 | Verified | LA-S1, introduction; Open Permissions; Talent | paraphrase | None |
| LA003 | Verified | LA-S1, introduction and Open Permissions table | exact | None |
| LA004 | Verified | LA-S1#talent | paraphrase | None |
| LA005 | Misleading | LA-S1#open-permissions-consumer and #talent | interpretation | Use: “Creating a developer app provides the documented self-service Open Permissions; job-search inventory retrieval is not among those permissions.” |
| LA006 | Verified | LA-S2, opening paragraph | paraphrase | None |
| LA007 | Verified | LA-S2, opening Important notice | exact | None |
| LA008 | Misleading | LA-S2, opening paragraph | interpretation | Use: “The Job Posting API documentation describes outbound posting to LinkedIn; that page does not document a read/search endpoint.” |
| LA009 | Verified | LA-S3, overview and Components | paraphrase | None |
| LA010 | Verified | LA-S3#requirements | exact | None |
| LA011 | Misleading | LA-S3, overview, Components, integration steps | interpretation | Use: “Apply Connect documentation describes an ATS posting-and-application workflow; it does not document a general job-search feed.” |
| LA012 | Verified | LA-S4#ingesting-jobs-on-linkedin and #job-posting-categories | paraphrase | None |
| LA013 | Unverified | LA-S4 does not state reciprocal-right consequences | - | Exclude; this is a legal/planning inference, not a source claim. |
| LA014 | Unverified | Documentation search found no primary statement proving nonexistence | - | Exclude; absence from reviewed documentation cannot prove universal nonexistence. |
| LA015 | Unverified | No cited primary source states this possibility | - | Exclude; epistemic caveat, not source-verifiable. |
| LA016 | Verified | LA-S5#rights, section 2.5 | paraphrase | None |
| LA017 | Verified | LA-S5#dos, section 8.2 | paraphrase | None |
| LA018 | Unverified | LA-S5 sections 2.5 and 8.2 do not state this abstract rights conclusion | - | Exclude or present as legal interpretation, not cited fact. |
| LA019 | Verified | LA-S6, opening paragraphs, prohibited list, final consequence paragraph | paraphrase | None |
| LA020 | Verified | LA-S7, opening notice | exact | None |
| LA021 | Verified | LA-S7, named crawler rules for `/jobs?runSearch*`, `/jobs-guest/`, `/api/jobPostings/jobs*`, `/jsearch*` | exact | None |
| LA022 | Verified | LA-S8, clauses 1-8 | paraphrase | None |
| LA023 | Verified | LA-S9, “Rate Limiting” and two limit types | exact | None |
| LA024 | Verified | LA-S9, opening paragraph | exact | None |
| LA025 | Verified | LA-S9, paragraph beginning “Your application's daily rate limit” | paraphrase | None |
| LA026 | Verified | LA-S9, paragraph beginning “Rate limited requests” | exact | None |
| LA027 | Verified | LA-S10, sections 2.3 and 3.1 general restrictions | paraphrase | None |
| LA028 | Verified | LA-S10, section 4.1 | paraphrase | None |
| LA029 | Verified | LA-S10, sections 4.1, 4.4, 4.5 | paraphrase | None |
| LA030 | Verified | LA-S10, sections 4.4 and 4.5 | paraphrase | None |
| LA031 | Verified | LA-S10, sections 5.1, 5.2, 7.1 | paraphrase | None |
| LA032 | Verified | LA-S11#answer; LA-S12#answer; LA-S13#answer; LA-S14#answer | paraphrase | None |
| LA033 | Verified | LA-S15#quickstart and #querying-the-api; LA-S16 examples and response note | paraphrase | None |
| LA034 | Verified | LA-S17#authentication and #list-jobs | paraphrase | None |
| LA035 | Verified | LA-S17, Introduction | paraphrase | None |
| LA036 | Verified | LA-S18 README, Introduction, published-state note, list/detail endpoints | paraphrase | None |
| LA037 | Verified | LA-S18 README, API limitations and site-name namespacing | interpretation | None; source allows full-text search within a site but documents no cross-employer endpoint. |
| LA038 | Verified | LA-S19, endpoint purpose, Resource, Authorization | paraphrase | None |
| LA039 | Verified | LA-S19, USAJOBS job-announcement scope; corroborated by OPM developer page | paraphrase | None |
| LA040 | Verified | LA-S20, homepage; LA-S21, overview and formats | paraphrase | None |
| LA041 | Misleading | LA-S20 and LA-S21 describe occupational reference data, not vacancies | interpretation | Use: “The cited O*NET sources expose occupational reference data and tools; they do not document a live-vacancy feed.” |
| LA042 | Verified | LA-S22, opening paragraphs and use cases; LA-S23, definition and uses | paraphrase | None |
| LA043 | Misleading | LA-S22 and LA-S23 describe a classification/API, not vacancy data | interpretation | Use: “ESCO is a European multilingual classification relevant to the EU labour market; the cited services expose classification data, not a documented live-vacancy feed.” |
| LA044 | Verified | LA-S4, opening paragraph and Job Posting Categories | paraphrase | None |
| LA045 | Verified | LA-S1, footer “Last updated on 06/26/2025”; live access 2026-11-10 | exact | None |
| LA046 | Hallucination | LA-S2, footer “Last updated on 06/03/2026” and `li-lts-2026-04` view | exact contradiction | Use: “The Job Posting API page was viewed under `li-lts-2026-04`, was last updated 2026-06-03, and was accessed 2026-11-10.” |
| LA047 | Verified | LA-S3, footer “Last updated on 09/09/2026”; live access 2026-11-10 | exact | None |
| LA048 | Verified | LA-S4, article date 05/08/2023; live access 2026-11-10 | exact | None |
| LA049 | Verified | LA-S5, “Effective on November 3, 2025”; live access 2026-11-10 | exact | None |
| LA050 | Verified | LA-S6, “Last updated: 2 years ago”; live access 2026-11-10 | exact | None |
| LA051 | Verified | LA-S7, no date field; live access 2026-11-10 | exact | None |
| LA052 | Verified | LA-S8, “Last revised on May 25, 2017”; live access 2026-11-10 | exact | None |
| LA053 | Verified | LA-S9, footer “Last updated on 08/20/2025”; live access 2026-11-10 | exact | None |
| LA054 | Verified | LA-S10, revision and effective-date notices; live access 2026-11-10 | exact | None |
| LA055 | Verified | LA-S11 through LA-S14, no page date displayed; live access 2026-11-10 | exact | None |
| LA056 | Verified | LA-S15 and LA-S16, no page date displayed; live access 2026-11-10 | exact | None |
| LA057 | Verified | LA-S17, no page date displayed; live access 2026-11-10 | exact | None |
| LA058 | Misleading | LA-S18, official repository README and commit-based repository UI | interpretation | Use: “Lever's Postings API documentation is maintained in Lever's official repository; the README states no publication date; accessed 2026-11-10.” |
| LA059 | Verified | LA-S19, no page date displayed; live access 2026-11-10 | exact | None |
| LA060 | Verified | LA-S20, footer “Site updated October 6, 2026”; live access 2026-11-10 | exact | None |
| LA061 | Verified | LA-S21, title “O*NET 31.0 Database”; no page date displayed; live access 2026-11-10 | exact | None |
| LA062 | Verified | LA-S22, no page date displayed; live access 2026-11-10 | exact | None |
| LA063 | Verified | LA-S23, “Current version: ESCO v1.2.1 (Last update 10/12/2025)”; live access 2026-11-10 | exact | None |

### Extraction and Operations Claims

| ID | Status | Exact source location | Confidence | Correction or planner action |
|---|---|---|---|---|
| EO001 | Unverified | No cited primary URL | - | Exclude; internal document date not externally sourced. |
| EO002 | Unverified | No cited primary URL | - | Exclude; broad uncited capability limitation. |
| EO003 | Verified | Source register metadata plus EO-S01 through EO-S22 live owner pages | paraphrase | None |
| EO004 | Unverified | No cited primary URL | - | Exclude; internal document-characterization claim. |
| EO005 | Verified | EO-S01, title/status and abstract | exact | None |
| EO006 | Verified | EO-S01, abstract/features; sections 5.1-5.2; companion API reference | paraphrase | None |
| EO007 | Verified | EO-S01, `@graph`, arrays, context, expanded/compacted form sections | interpretation | None |
| EO008 | Verified | EO-S02, JobPosting property table | exact | None |
| EO009 | Verified | EO-S02, expected types for skills, qualifications, education and experience properties | paraphrase | None |
| EO010 | Verified | EO-S02, `occupationalCategory` row | paraphrase | None |
| EO011 | Verified | EO-S03, markup examples/guidelines and content-consistency troubleshooting | paraphrase | None |
| EO012 | Verified | EO-S03#remove-job-postings, three listed expiry mechanisms | exact | None |
| EO013 | Verified | EO-S03, “Keep Google informed” | paraphrase | None |
| EO014 | Verified | EO-S04, Abstract | paraphrase | None |
| EO015 | Verified | EO-S05#structured-outputs-vs-json-mode and refusal documentation | paraphrase | None |
| EO016 | Misleading | EO-S02 defines available fields/types but makes no publisher-behavior guarantee | interpretation | Use: “Schema.org defines fields for expressing job requirements; the specification does not require publishers to populate them or to use typed values.” |
| EO017 | Verified | EO-S02 rows for `experienceRequirements`, `educationRequirements`, `qualifications` | exact | None |
| EO018 | Verified | EO-S03#remove-job-postings | interpretation | None |
| EO019 | Verified | EO-S06, Worker Requirements, Experience Requirements, Occupational Requirements, Occupation-Specific Info | paraphrase | None |
| EO020 | Verified | EO-S07, format links: Excel/CSV/JSON, SQL, RDF, Web Services | exact | None |
| EO021 | Verified | EO-S07, “Primary Source of Occupational Information” and release/update paragraphs | paraphrase | None |
| EO022 | Verified | EO-S08, definition; EO-S09, API documentation | paraphrase | None |
| EO023 | Misleading | EO-S08 sections 1-2 and EO-S09 API docs support web/local APIs, not the full downloadable-data wording | interpretation | Use: “The European Commission provides an ESCO web-service API and a downloadable local API.” |
| EO024 | Verified | EO-S08, versions paragraph and URI example; EO-S09 versioned API docs | paraphrase | None |
| EO025 | Verified | EO-S10, opening paragraph | exact | None |
| EO026 | Verified | EO-S10, opening paragraph, structure, skill model, downloads | paraphrase | None |
| EO027 | Verified | EO-S02, `occupationalCategory` row | exact | None |
| EO028 | Unverified | No cited primary URL | - | Exclude; internal planner default. |
| EO029 | Unverified | No cited primary URL | - | Exclude; internal planner threshold. |
| EO030 | Verified | EO-S01, expanded form and companion processing-algorithm specification | interpretation | None |
| EO031 | Verified | EO-S05#structured-outputs-vs-json-mode | exact | None |
| EO032 | Verified | EO-S05, Explicit refusals and Supported models | paraphrase | None |
| EO033 | Verified | EO-S11#remoteindirect-prompt-injection | paraphrase | None |
| EO034 | Verified | EO-S11, prevention pipeline, trusted/untrusted separation, tool boundary, least privilege | paraphrase | None |
| EO035 | Unverified | No cited primary URL | - | Exclude; internal repair default. |
| EO036 | Verified | EO-S12, ontology overview and term index for Entity, Activity, Agent, `wasGeneratedBy`, `wasDerivedFrom`, timestamps, `hadPrimarySource` | paraphrase | None |
| EO037 | Verified | EO-S02, inherited `identifier` property row | paraphrase | None |
| EO038 | Verified | EO-S13, ordered canonicalization methods | exact | None |
| EO039 | Verified | EO-S13, duplicate/similar-page scope and signal language | interpretation | None |
| EO040 | Verified | EO-S14, Abstract | paraphrase | None |
| EO041 | Verified | EO-S15, abstract and paper text on resemblance, containment, shingles and sampling | interpretation | None |
| EO042 | Verified | EO-S15 DOI/IEEE bibliographic record, 1997 | exact | None |
| EO043 | Verified | EO-S03#remove-job-postings | exact | None |
| EO044 | Verified | EO-S03, “Keep Google informed” | paraphrase | None |
| EO045 | Verified | EO-S16 sections 8.8, 13, 15.4.5; EO-S17 validation sections | paraphrase | None |
| EO046 | Verified | EO-S17 sections 1, 4.2, 4.3 | paraphrase | None |
| EO047 | Verified | EO-S18, `<lastmod>` definition | exact | None |
| EO048 | Verified | EO-S19, XML sitemap notes | exact | None |
| EO049 | Unverified | No cited primary URL | - | Exclude; internal closure policy. |
| EO050 | Unverified | No cited primary URL | - | Exclude; internal recheck policy. |
| EO051 | Unverified | No cited primary URL | - | Exclude; internal recheck policy. |
| EO052 | Unverified | No cited primary URL | - | Exclude; internal recheck policy. |
| EO053 | Unverified | No cited primary URL | - | Exclude; internal retry policy. |
| EO054 | Unverified | No cited primary URL | - | Exclude; internal recheck policy. |
| EO055 | Unverified | No cited primary URL | - | Exclude; internal lifecycle recommendation. |
| EO056 | Verified | EO-S20, Abstract | paraphrase | None |
| EO057 | Verified | EO-S18, protocol/discovery fields; EO-S19#rss | paraphrase | None |
| EO058 | Unverified | No cited primary URL | - | Exclude; internal polling default. |
| EO059 | Unverified | No cited primary URL | - | Exclude; internal reuse default. |
| EO060 | Unverified | No cited primary URL | - | Exclude; internal ladder count/ranking. |
| EO061 | Unverified | No cited primary URL | - | Exclude; internal pilot composition. |
| EO062 | Unverified | No cited primary URL | - | Exclude; internal pilot minimum. |
| EO063 | Unverified | No cited primary URL | - | Exclude; internal annotation policy. |
| EO064 | Unverified | No cited primary URL | - | Exclude; uncited generalization about F1. |
| EO065 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO066 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO067 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO068 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO069 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO070 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO071 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO072 | Unverified | No cited primary URL | - | Exclude; internal launch target. |
| EO073 | Unverified | No cited primary URL | - | Exclude; internal characterization of targets. |
| EO074 | Verified | EO-S21, sections 2-6 | paraphrase | None |
| EO075 | Verified | EO-S22 sections 2.2-2.7 | paraphrase | None |
| EO076 | Unverified | No cited primary URL | - | Exclude; internal ranking of BYOK patterns. |
| EO077 | Unverified | No cited primary URL | - | Exclude; uncited security assertion. |
| EO078 | Unverified | No cited primary URL | - | Exclude; uncited security assertion. |
| EO079 | Unverified | No cited primary URL | - | Exclude; internal mapping threshold. |
| EO080 | Unverified | No cited primary URL | - | Exclude; internal repair default. |
| EO081 | Unverified | No cited primary URL | - | Exclude; internal freshness default. |
| EO082 | Unverified | No cited primary URL | - | Exclude; internal lifecycle default. |
| EO083 | Unverified | No cited primary URL | - | Exclude; internal reuse default. |
| EO084 | Unverified | No cited primary URL | - | Exclude; internal polling default. |
| EO085 | Verified | EO-S01 through EO-S22 live retrieval/search records dated 2026-11-10 | exact | None |
| EO086 | Verified | EO-S01, title, abstract, features, processing reference | paraphrase | None |
| EO087 | Verified | EO-S02, title and property table | paraphrase | None |
| EO088 | Verified | EO-S03, title, markup and expiry/removal sections | paraphrase | None |
| EO089 | Verified | EO-S04, Draft 2020-12 Core title and Abstract | paraphrase | None |
| EO090 | Verified | EO-S05, title, JSON-mode comparison, refusals | paraphrase | None |
| EO091 | Verified | EO-S06, content-model categories | paraphrase | None |
| EO092 | Verified | EO-S07, U.S. taxonomy, releases and formats | paraphrase | None |
| EO093 | Verified | EO-S08, web/local APIs, URI identifiers, versions | paraphrase | None |
| EO094 | Verified | EO-S09, REST API title and resource endpoints | paraphrase | None |
| EO095 | Verified | EO-S10, hierarchy and definitions | paraphrase | None |
| EO096 | Verified | EO-S11, remote content and prevention guidance | paraphrase | None |
| EO097 | Verified | EO-S12, ontology classes and derivation relations | paraphrase | None |
| EO098 | Verified | EO-S13, canonicalization methods | paraphrase | None |
| EO099 | Verified | EO-S14, RFC title and Abstract | paraphrase | None |
| EO100 | Misleading | EO-S15 bibliographic record and paper; “original” priority is not established by the cited source | interpretation | Use: “S15 is A. Z. Broder's 1997 paper *On the Resemblance and Containment of Documents* and presents a shingling-and-sampling approach to near-duplicate documents.” |
| EO101 | Verified | EO-S16 sections 8.8, 13 and 15 | paraphrase | None |
| EO102 | Verified | EO-S17 sections 4.2-4.3 | paraphrase | None |
| EO103 | Verified | EO-S18, protocol and `<lastmod>` definition | paraphrase | None |
| EO104 | Verified | EO-S19, XML sitemap notes | paraphrase | None |
| EO105 | Verified | EO-S20, Abstract | paraphrase | None |
| EO106 | Verified | EO-S21, sections 2-6 | paraphrase | None |
| EO107 | Verified | EO-S22 sections 2.2-2.7 | paraphrase | None |
| EO108 | Unverified | No primary source can establish that a prior checking action occurred | - | Exclude. |
| EO109 | Unverified | No cited primary URL; internal document-wide characterization | - | Exclude. |
| EO110 | Unverified | No cited primary URL; proving the negative would require content re-audit outside the allowed metadata-only use | - | Exclude. |

## Corrected Claims

Only these corrected forms may replace the ten non-safe inventory wordings:

| ID | Planner-safe corrected claim |
|---|---|
| LA005 | Creating a developer app provides the documented self-service Open Permissions; job-search inventory retrieval is not among those permissions. |
| LA008 | The Job Posting API documentation describes outbound posting to LinkedIn; that page does not document a read/search endpoint. |
| LA011 | Apply Connect documentation describes an ATS posting-and-application workflow; it does not document a general job-search feed. |
| LA041 | The cited O*NET sources expose occupational reference data and tools; they do not document a live-vacancy feed. |
| LA043 | ESCO is a European multilingual classification relevant to the EU labour market; the cited services expose classification data, not a documented live-vacancy feed. |
| LA046 | The Job Posting API page was viewed under `li-lts-2026-04`, was last updated 2026-06-03, and was accessed 2026-11-10. |
| LA058 | Lever's Postings API documentation is maintained in Lever's official repository; the README states no publication date; accessed 2026-11-10. |
| EO016 | Schema.org defines fields for expressing job requirements; the specification does not require publishers to populate them or to use typed values. |
| EO023 | The European Commission provides an ESCO web-service API and a downloadable local API. |
| EO100 | S15 is A. Z. Broder's 1997 paper *On the Resemblance and Containment of Documents* and presents a shingling-and-sampling approach to near-duplicate documents. |

## Planner-Safe Claims

The planner may rely on the following inventory claims **as written**:

- `LA002-LA004`, `LA006-LA007`, `LA009-LA010`, `LA012`, `LA016-LA017`, `LA019-LA040`, `LA042`, `LA044-LA045`, `LA047-LA057`, `LA059-LA063`
- `EO003`, `EO005-EO015`, `EO017-EO022`, `EO024-EO027`, `EO030-EO034`, `EO036-EO048`, `EO056-EO057`, `EO074-EO075`, `EO085-EO099`, `EO101-EO107`

The planner may also rely on the ten statements in **Corrected Claims**, but only in those corrected forms.

The following claims are blocked and must not be relied upon:

- `LA001`, `LA013-LA015`, `LA018`
- `EO001-EO002`, `EO004`, `EO028-EO029`, `EO035`, `EO049-EO055`, `EO058-EO073`, `EO076-EO084`, `EO108-EO110`

## Blocking Issues

1. Forty-six uncited internal or negative-existence claims lack an authoritative primary source and are excluded.
2. `LA046` contradicts the current primary page: the Job Posting API page now states “Last updated on 06/03/2026.”
3. Nine claims overstate what their cited sources directly establish. They are usable only after replacement with the exact corrections above.
4. No cited primary source was inaccessible, and no citation was fabricated or missing.

## Search Coverage

| Source class | Mandatory patterns applied | Result |
|---|---|---|
| Academic citation | Author/year/title; full title on Semantic Scholar/arXiv; author/year/venue; DOI | Broder paper and DOI confirmed through IEEE/DOI and bibliographic indexes. |
| Company/product | Company + topic + announcement; official-domain topic; official announcement; SEC pattern where applicable | Official LinkedIn, Adzuna, Greenhouse, Lever, Google, and OpenAI sources found; SEC searches did not replace product documentation. |
| Government/policy | Policy/source on government domain; official statistics; agency report | European Commission GDPR/ESCO, OPM/USAJOBS, U.S. DOL/O*NET, and ILO/ISCO sources confirmed. |
| Statistics/version claims | Exact value/topic/year; official report/domain; original source | O*NET 31.0, ESCO v1.2.1, source dates, RFC numbers, and enumerated mechanisms checked against primary pages. |

