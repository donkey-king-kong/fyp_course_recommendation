# Pilot Student Skills Evidence Review

Date: 2026-11-03

This is a bounded course-content review of `data/student_skill_evidence.json`, using the checked-in `data/course_catalog.json` snapshot (SHA-256 `e94466a7834bd551bf86dfbca33c5c30c2ec6e4f9dbb59df3aa7389752a61d63`) and the current static career mappings. It is not an independent supervisor/TA assessment, a transcript verification, a mastery measure, or a change to recommendation ranking.

| Course | Skill ID; applicable pilot roles | Depth judgment and catalog support |
| --- | --- | --- |
| `SC1003` | `programming-foundations`; SWE, DE | Introductory: basic program constructs and simple data structures. It is not evidence of software delivery or pipeline design; its role area is context for a prerequisite foundation only. |
| `SC2006` | `software-engineering-practice`; SWE | Introductory software-engineering practice: design/construction, testing/integration and broader process topics. No direct data-pipeline implementation claim. |
| `SC3040` | `software-engineering-practice`; SWE | Advanced *management and maintenance* practice after `SC2006`; quality, project and configuration management. This does not imply advanced coding proficiency or pipeline design. |
| `SC3020` | `data-storage`; SWE, DE | Introductory DBMS implementation and use of databases for large data sets. Direct storage foundation; not evidence of every backend or data-modelling responsibility. |
| `SC4023` | `data-storage`; SWE, DE | Advanced scalable-storage topic relative to the `SC3020` foundation: big-data management, distributed storage/processing and NoSQL stores. Depth describes the course topic, not an individual's proficiency. |
| `SC4023` | `distributed-systems`; SWE, DE | Introductory *slice* of distributed systems: distributed storage and parallel data computation. The description does not establish broad coverage of distributed algorithms or consensus, so advanced storage depth is not copied to this second skill. |
| `SC4051` | `distributed-systems`; SWE, DE | Introductory exposure to distributed-system design, despite a level-4 course and coverage of replication, consensus and fault tolerance. The catalog explicitly says it introduces the subject; these topic names alone do not establish advanced mastery. |

The SWE preview contains four IDs: programming foundations, software-engineering practice, data storage and distributed systems. The DE preview contains three: programming foundations, data storage and distributed systems. `SC2006`/`SC3040` therefore remain *unmapped for DE* in this small ledger; this does not mean their students have no useful software skills. The matched static role area is broader context, not evidence that a mapped course covers every named responsibility. Any code absent from the role's reviewed ledger is unknown, not zero skill.

All seven exact excerpts were checked as substrings of their respective catalog descriptions; all applicable role-area names exist in the current static mapping. Service checks covered introductory/advanced exposure, role-specific unmapped codes, and overlapping completed/candidate inputs. A previously captured 24-case recommendation run matched the merged policy outputs exactly; this review only changes the new preview ledger, not ranking or allocation.

Next: get expert review for contested depth or role relevance before treating these course-content labels as a ranking signal. If approved, define how *likely prior exposure* and potential next learning affect ranking while preserving hard eligibility filters, all-six-career regression coverage and the separate accepted-but-failed database-preference counterfactual review. Do not convert exposure into verified mastery or infer completion from a candidate course.
