# Pilot Student Skills Coverage Audit

Date: 2026-11-03

Source: the saved `data/review/weak_fit_policy_2026-11-03/benchmark_responses.json` (15 frozen Software Engineer / Data Engineer cases) and `data/student_skill_evidence.json`. This is a **read-only coverage count** over saved backend selections, not a new recommendation run, a ranking-quality measure, or proof that each selected course should be recommended. The capture's serving revision and database fingerprint are operator-declared; see its provenance and the [policy comparison](Recommendation_Weak_Fit_Policy_2026-11-03.md). The catalog description snapshot has SHA-256 `e94466a7834bd551bf86dfbca33c5c30c2ec6e4f9dbb59df3aa7389752a61d63`.

| Pilot subset | Cases | Selected-course occurrences | Covered before cloud link | Covered after cloud link |
| --- | ---: | ---: | ---: | ---: |
| Software Engineer | 13 | 31 | 11 | 19 |
| Data Engineer | 2 | 4 | 3 | 4 |
| Both roles | 15 | 35 | 14 | 23 |

Coverage is role-specific: a selected course counts once per case only if its code has at least one evidence link to a skill applicable to that case's role. `SC4023` has two skill links but counts as one selected-course occurrence. Nine `SC4052` selections (eight SWE, one DE) explain the entire increase. Its catalog explicitly introduces cloud computing and describes service models and distributed services; the new `cloud-service-platforms` link is introductory for both roles. It does **not** restore the previously removed unsupported `backend-engineering` tag, claim cloud is an AI/ML course, or alter any recommender selection.

The remaining 12 unmapped occurrences are `SC4010` (3); `SC4001`, `SC4013` and `SC4022` (2 each); and `SC3010`, `SC4012` and `SC4050` (1 each). Cases `software-engineer-csc-003`, `008` and `012` still have no mapped selection. Some course descriptions support narrow future links, but `SC4001`'s *neural* networks must not become SWE computer-networking evidence, and `SC4022`'s cybersecurity application must not be mistaken for secure-software practice. Leave these absent until their role-specific depth and applicability are reviewed; unknown is not zero skill or a reason to suppress a recommendation.

The existing request completions in these cases include only a subset of the ledger's courses, so coverage of selected courses is not student skill completeness. The next work unit should secure independent review of the provisional ledger and specify how likely prior exposure could affect ranking without treating course depth as verified mastery. Do not update frozen labels or tune the policy threshold to improve this coverage count. The accepted failed database-preference counterfactual remains a separate evaluation question.
