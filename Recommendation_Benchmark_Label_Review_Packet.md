# Recommendation Benchmark Label Review Packet

## Purpose

This packet summarizes the full 21-case before/after benchmark diff after the Opus-guided scoring fixes. It is intended for supervisor/TA review of benchmark labels before any further scoring changes are made.

## Compared Versions

- Before: predictions from commit `d34fdba` before the Opus-guided scoring fixes.
- After: current `data/recommendation_benchmark_predictions.json` after dimension-based preferences, MPE `max()` scoring, catalog-grounded mappings, and regenerated predictions.

## Aggregate Metrics

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `averagePrecisionAtReturned` | `0.7857142857142857` | `0.8095238095238095` | `+0.0238` |
| `averageNdcgAtReturned` | `0.7306114222717204` | `0.7634008820150107` | `+0.0328` |
| `averageExplanationFidelity` | `0.55` | `0.45` | `-0.1000` |
| `averageSlotFillRate` | `1.0` | `1.0` | `+0.0000` |
| `averageConstraintValidity` | `1.0` | `1.0` | `+0.0000` |
| `oldCodeExposure` | `0` | `0` | `+0.0000` |

## Summary

- Changed selections: `6` of `21` cases: software-engineer-csc-002, software-engineer-csc-013, ai-ml-engineer-csc-001, ai-ml-engineer-csc-002, data-engineer-csc-002, cybersecurity-engineer-csc-002.
- Ranking metric regressions: `0` cases: none.
- Explanation fidelity regressions: `2` cases: cybersecurity-engineer-csc-001, cybersecurity-engineer-csc-002.
- Cloud-platform cases did not change in selected modules or returned-ranking metrics.
- Software Engineer selections changed in `software-engineer-csc-002` and `software-engineer-csc-013`, but their returned precision/nDCG did not improve or regress.

## Full Case Diff

| Case | Before Selected | After Selected | Selection Changed | Precision Delta | nDCG Delta | Fidelity Delta |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `software-engineer-csc-001` | SC4052 (87), SC4051 (68) | SC4052 (87), SC4051 (68) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-002` | SC3020 (30), SC3040 (24), SC4025 (57), SC4061 (39) | SC3020 (30), SC3040 (24), SC4025 (69), SC4002 (46) | Yes | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-003` | SC4010 (63), SC4017 (58), SC4063 (49) | SC4010 (63), SC4017 (58), SC4063 (49) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-004` | SC3020 (63), SC3040 (24), SC4052 (79) | SC3020 (63), SC3040 (24), SC4052 (79) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-005` | SC4052 (60), SC4013 (39), SC4051 (49) | SC4052 (60), SC4013 (39), SC4051 (49) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-007` | SC4052 (87), SC4051 (68) | SC4052 (87), SC4051 (68) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-008` | SC4010 (63), SC4017 (54) | SC4010 (63), SC4017 (54) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-009` | SC4052 (60), SC4013 (39) | SC4052 (60), SC4013 (39) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-010` | SC3020 (30), SC4052 (60) | SC3020 (30), SC4052 (60) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-011` | SC3020 (51), SC3040 (24) | SC3020 (51), SC3040 (24) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-012` | SC3010 (46), SC4010 (63) | SC3010 (46), SC4010 (63) | No | +0.0000 | +0.0000 | +0.0000 |
| `software-engineer-csc-013` | SC4025 (57), SC4052 (46) | SC4025 (69), SC4020 (50) | Yes | +0.0000 | +0.0000 | n/a |
| `software-engineer-csc-014` | SC3030 (46), SC4050 (67) | SC3030 (46), SC4050 (67) | No | +0.0000 | +0.0000 | +0.0000 |
| `ai-ml-engineer-csc-001` | SC3020 (19), SC4002 (66) | SC3020 (19), SC4061 (74) | Yes | +0.0000 | +0.0000 | +0.0000 |
| `ai-ml-engineer-csc-002` | SC4064 (48) | SC4061 (62) | Yes | +0.0000 | +0.0000 | +0.0000 |
| `data-engineer-csc-001` | SC3020 (71), SC4023 (80) | SC3020 (71), SC4023 (72) | No | +0.0000 | +0.0000 | +0.0000 |
| `data-engineer-csc-002` | SC4023 (68), SC4052 (63) | SC4052 (63), SC4023 (60) | Yes | +0.0000 | +0.0754 | +0.0000 |
| `cloud-platform-engineer-csc-001` | SC3030 (49), SC4050 (64) | SC3030 (49), SC4050 (64) | No | +0.0000 | +0.0000 | +0.0000 |
| `cloud-platform-engineer-csc-002` | SC4063 (41), SC4051 (32) | SC4063 (41), SC4051 (32) | No | +0.0000 | +0.0000 | +0.0000 |
| `cybersecurity-engineer-csc-001` | SC4010 (62), SC4014 (62) | SC4010 (72), SC4014 (65) | No | +0.0000 | +0.0000 | -1.0000 |
| `cybersecurity-engineer-csc-002` | SC4014 (62), SC4017 (62) | SC4063 (71), SC4017 (66) | Yes | +0.5000 | +0.6131 | -1.0000 |

## Cases Needing Label Review

These are current returned recommendations whose benchmark label is either missing or below the evaluator relevance threshold. They are the safest cases to send to a reviewer before doing more scoring changes.

| Case | Returned Module | Current Label | Score |
| --- | --- | --- | ---: |
| `software-engineer-csc-002` | `SC3020` | `somewhat-relevant` | `30` |
| `software-engineer-csc-002` | `SC4025` | `unlabelled` | `69` |
| `software-engineer-csc-003` | `SC4063` | `unlabelled` | `49` |
| `software-engineer-csc-004` | `SC4052` | `unlabelled` | `79` |
| `software-engineer-csc-005` | `SC4052` | `unlabelled` | `60` |
| `software-engineer-csc-010` | `SC4052` | `unlabelled` | `60` |
| `software-engineer-csc-013` | `SC4025` | `unlabelled` | `69` |
| `software-engineer-csc-013` | `SC4020` | `unlabelled` | `50` |
| `software-engineer-csc-014` | `SC4050` | `somewhat-relevant` | `67` |
| `ai-ml-engineer-csc-001` | `SC3020` | `somewhat-relevant` | `19` |

## Networks-Tagged Relevant Candidates

These reviewed relevant candidates carry the generic `networks` tag. They are useful for checking whether the Cybersecurity-specific demotion of generic `networks` caused unintended harm.

| Case | Candidate | Label |
| --- | --- | --- |
| `software-engineer-csc-001` | `SC4052` | `relevant` |
| `software-engineer-csc-002` | `SC4001` | `highly-relevant` |
| `software-engineer-csc-003` | `SC4053` | `relevant` |
| `software-engineer-csc-007` | `SC4052` | `highly-relevant` |
| `software-engineer-csc-009` | `SC4052` | `relevant` |
| `software-engineer-csc-013` | `SC4001` | `highly-relevant` |
| `software-engineer-csc-014` | `SC3030` | `highly-relevant` |
| `software-engineer-csc-014` | `SC4030` | `highly-relevant` |
| `ai-ml-engineer-csc-001` | `SC4001` | `relevant` |
| `ai-ml-engineer-csc-002` | `SC4050` | `highly-relevant` |
| `data-engineer-csc-001` | `SC4050` | `relevant` |
| `data-engineer-csc-002` | `SC4052` | `highly-relevant` |
| `data-engineer-csc-002` | `SC4050` | `highly-relevant` |
| `cloud-platform-engineer-csc-001` | `SC3030` | `highly-relevant` |
| `cloud-platform-engineer-csc-001` | `SC4052` | `highly-relevant` |
| `cloud-platform-engineer-csc-001` | `SC4050` | `relevant` |
| `cloud-platform-engineer-csc-002` | `SC4063` | `highly-relevant` |
| `cloud-platform-engineer-csc-002` | `SC4050` | `relevant` |
| `cybersecurity-engineer-csc-001` | `SC4014` | `highly-relevant` |
| `cybersecurity-engineer-csc-002` | `SC4063` | `highly-relevant` |

## Reviewer Questions

- For each unlabelled returned module, should it be marked `relevant`, `somewhat-relevant`, or `irrelevant` for the stated profile?
- For `software-engineer-csc-013`, are `SC4025` and `SC4020` actually poor recommendations, or are they missing labels?
- For cases with `explanationFidelity = 0`, are the expected skill paths stale after the catalog-grounded mapping rewrite?
- For Software Engineer cases, should cloud/distributed/data-platform modules be treated as broadly relevant, or only when the student explicitly selects those preferences?
- For network/security cases, should generic `networks` count as weak evidence unless paired with `network-security` or `network-infrastructure`?

## Follow-Up Diligence Checks

### Changed Software Engineer Cases

- `software-engineer-csc-002` changed from `SC3020`, `SC3040`, `SC4025`, `SC4061` to `SC3020`, `SC3040`, `SC4025`, `SC4002`.
- `software-engineer-csc-002` did not regress: `precisionAtReturned` stayed `0.5`, `nDCGAtReturned` stayed `0.44859091644534477`.
- `software-engineer-csc-013` changed from `SC4025`, `SC4052` to `SC4025`, `SC4020`.
- `software-engineer-csc-013` did not regress by current labels: `precisionAtReturned` stayed `0.0`, `nDCGAtReturned` stayed `0.0`.
- These cases should be reviewed before more scoring work because both contain unlabelled returned modules and AI/ML-oriented expectations under the `software-engineer` career goal.

### AI/ML Changed Case

- `ai-ml-engineer-csc-002` changed from `SC4064` to `SC4061`.
- It did not regress by current labels: `precisionAtReturned` stayed `1.0`, `nDCGAtReturned` stayed `0.6666666666666666`.
- Current returned module `SC4061` is labelled `relevant`.
- The expected top candidates remain `SC4062` and `SC4050`, so this case should still be reviewed for whether exact-slot/prerequisite constraints explain the returned choice.

### Cloud Sanity Check

- `cloud-platform-engineer-csc-001` selected modules did not change: `SC3030`, `SC4050`.
- `cloud-platform-engineer-csc-001` returned metrics did not change: `precisionAtReturned = 1.0`, `nDCGAtReturned = 0.7956176024115139`.
- `cloud-platform-engineer-csc-002` selected modules did not change: `SC4063`, `SC4051`.
- `cloud-platform-engineer-csc-002` returned metrics did not change: `precisionAtReturned = 1.0`, `nDCGAtReturned = 0.8710490642551529`.
- The MPE `sum()` to `max()` change did not cause an observed Cloud Platform regression.

### Explanation-Fidelity Review

- `cybersecurity-engineer-csc-001` explanation fidelity changed from `1.0` to `0.0`.
- `cybersecurity-engineer-csc-002` explanation fidelity changed from `1.0` to `0.0`.
- This appears to be a stale benchmark-label issue, not a ranking regression.
- The mapping rewrite changed the top evidence path from dead semantic tags such as `computer-security` / `computer-network` toward real catalog tags such as `cybersecurity`, `network-security`, and `network-infrastructure`.
- Do not silently edit the benchmark labels. Ask the reviewer to approve these expected-skill-path updates.

### Proposed Expected-Skill-Path Updates For Review

| Case | Module | Current Expected Path | Proposed Review Path | Reason |
| --- | --- | --- | --- | --- |
| `cybersecurity-engineer-csc-001` | `SC4016` | `Cybersecurity Engineer -> security analysis and defence -> computer-security -> Cyber Threat Intelligence` | `Cybersecurity Engineer -> security analysis and defence -> cybersecurity -> Cyber Threat Intelligence` | `computer-security` was a dead semantic tag; `cybersecurity` is the real catalog tag. |
| `cybersecurity-engineer-csc-001` | `SC4012` | `Cybersecurity Engineer -> cryptography and secure implementation -> computer-security -> Software Security` | Review needed: likely `Cybersecurity Engineer -> security analysis and defence -> cybersecurity -> Software Security`, unless the reviewer prefers a cryptography/secure-implementation rationale. | The old path used dead `computer-security`; the correct skill area should be reviewer-approved because the winning skill area may have changed. |
| `cybersecurity-engineer-csc-001` | `SC4013` | `Cybersecurity Engineer -> cryptography and secure implementation -> computer-security -> Application Security` | Review needed: likely `Cybersecurity Engineer -> security analysis and defence -> cybersecurity -> Application Security`, unless the reviewer prefers secure-implementation rationale. | The old path used dead `computer-security`; update only after reviewer confirms the intended skill rationale. |
| `cybersecurity-engineer-csc-002` | `SC4063` | `Cybersecurity Engineer -> networks and systems security -> computer-security -> Network Security` | `Cybersecurity Engineer -> networks and systems security -> network-security -> Network Security` | `SC4063` directly carries `network-security`, which is now the catalog-grounded specific signal. |
| `cybersecurity-engineer-csc-002` | `SC4013` | `Cybersecurity Engineer -> networks and systems security -> computer-security -> Application Security` | Review needed: likely `Cybersecurity Engineer -> security analysis and defence -> cybersecurity -> Application Security`, unless the reviewer considers it primarily network/systems security. | The old path used dead `computer-security` and may also point to the wrong skill area. |
| `cybersecurity-engineer-csc-002` | `SC4016` | `Cybersecurity Engineer -> security analysis and defence -> computer-security -> Cyber Threat Intelligence` | `Cybersecurity Engineer -> security analysis and defence -> cybersecurity -> Cyber Threat Intelligence` | `computer-security` was a dead semantic tag; `cybersecurity` is the real catalog tag. |

## Recommendation

Do not tune scoring further until these labels are reviewed. The latest structural fixes improved aggregate ranking while preserving slot fill and constraint validity, so remaining weak cases may reflect draft-label gaps rather than algorithm defects.
