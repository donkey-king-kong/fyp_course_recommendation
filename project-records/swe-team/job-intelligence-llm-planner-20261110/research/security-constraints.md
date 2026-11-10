# Security Constraints: Job Intelligence and LLM Planner

Date: 2026-11-10
Flow ID: `swe-devops-security`
Parent: `orchestrator`
Scope: pre-frame discovery only; no product implementation or legal approval

## Decision

**Production release is blocked.** Planning and an offline fixture-based prototype may proceed, but production job ingestion, model-provider calls, scheduled collection, on-demand URL fetches, and user-provided LLM tokens must remain disabled until the release-blocking decisions below have named owners and evidence.

This assessment is not legal advice and does not approve any source, provider, privacy basis, or deployment.

## Repository Facts

These are observed facts, not target-state claims:

- The application is one FastAPI service. There is no job pipeline, source client, chat endpoint, conversation store, LLM dependency, or model evaluation harness. The current dependency list contains no model SDK, browser runtime, scheduler, queue, or secret-manager client. [R1] [R2]
- Runtime configuration currently loads only `DATABASE_URL` from the process environment or local `.env`; `.env.example` contains a placeholder database URL and no LLM or job-source credential. [R3]
- CORS is configured for four localhost development origins, with credentials, all methods, and all headers enabled. This is development configuration, not evidence of production authentication or tenant isolation. [R4]
- Student profile, curriculum, transcript, completion, and recommendation state is browser-controlled prototype data in localStorage. There is no authenticated backend student entity or server-side tenant boundary. [R1]
- Uploaded/transcript-derived state is untrusted and must not be represented as an authoritative academic record. The deterministic backend, not an LLM, owns filtering, ranking, eligibility checks, and slot allocation. [R1]
- Job-source permission is unresolved. Existing research rejects LinkedIn as an MVP source absent written authorization and identifies provider terms, robots policy, derivative-data rights, LLM-input rights, retention, attribution, and deletion as unresolved gates. [R5]
- Existing extraction research already recommends a provenance-first pipeline, deterministic parsing before bounded LLM fallback, exact source evidence for accepted requirements, shared versioned snapshots, and platform-managed server credentials rather than BYOK for the initial release. [R6]

## Cited External Facts

- OWASP documents SSRF as a path from attacker-controlled destinations to internal services, recommends allowlisting where destinations are known, warns about DNS rebinding, and recommends disabling redirects that could bypass validation. [E1]
- OWASP identifies remote/indirect prompt injection, HTML/Markdown injection, system-prompt extraction, data exfiltration, and RAG poisoning. Its controls include separating trusted instructions from untrusted content, validating outputs, sanitizing remote content, least privilege, and monitoring. [E2]
- OWASP recommends centralized secret management, fine-grained least-privilege access, lifecycle controls, audit, and automated rotation or short-lived credentials where possible. [E3]
- RFC 9309 defines robots.txt as a control for crawler access. A crawler that successfully retrieves it must follow parseable rules; an unreachable robots file caused by server/network errors requires complete disallow while that state applies. [E4]
- OpenAI's current API documentation states that default abuse-monitoring logs may contain prompts/responses and are retained for up to 30 days; approved retention controls have endpoint-specific limitations, and some API features retain application state until deletion. Provider and endpoint selection therefore materially affect privacy and retention. [E5]
- OpenAI's key-safety guidance says keys must not be deployed in browsers/mobile apps or committed to repositories; requests should be routed through a backend, with environment/KMS storage, monitoring, and rotation. [E6]

## Required Security Constraints

### LLM Token Custody

**Initial release:** do not accept user-provided LLM API tokens. Use one platform-managed, server-side credential per environment and service, injected from an approved secret manager. Scope provider permissions, models, spend, and network origin where supported.

**Permitted alternatives, in preference order:**

1. Provider OAuth or delegated authorization that does not expose a long-lived token to this service.
2. Customer-managed vault reference with narrowly scoped runtime access.
3. Dedicated TLS backend credential endpoint, envelope-encrypted tenant-scoped storage, and immediate delete/replace.
4. Explicit session-only server memory with short expiry and no persistence.

If BYOK is later approved, never accept it through chat, prompts, localStorage, cookies, URLs, analytics-enabled forms, ordinary configuration, support tickets, or direct browser-to-provider calls. Do not return it after submission. Display only provider, state, creation time, and a non-sensitive fingerprint. State plainly that the service can decrypt and use any stored token; encryption at rest is not end-to-end secrecy.

### Secret Logging and Redaction

- Use structured allowlisted logging. Do not log request/response bodies by default for credential, transcript, chat, source-fetch, or model endpoints.
- Redact `Authorization`, cookies, provider keys, database URLs, signed URLs, query credentials, webhook secrets, prompt bodies, model responses, fetched HTML, and queue/dead-letter payloads before logs, traces, metrics labels, error reports, or support exports.
- Redaction must run at ingress and again at each telemetry/export sink. Pattern matching is defense in depth, not the primary control.
- Audit secret access by tenant, actor/workload, purpose, secret identifier, outcome, and time, never by value. Test representative provider-key formats and database URLs against logs before release.
- Suspected exposure response: disable/revoke first, rotate second, preserve only secret-free evidence, and inspect downstream logs and queues.

### Tenant and Identity Boundaries

- No production multi-user LLM or job-personalization release before authenticated server identity exists. Use the validated Azure tenant and stable Azure `oid` described by repository policy; never use browser `studentId`, email, or matriculation number as the authorization key.
- Every student-owned row, object, conversation, credential, cache entry, queued job, audit event, and deletion request must carry a server-derived tenant/user scope. Ignore tenant identifiers supplied in request bodies.
- Enforce tenant scope in service and data-access layers, including background workers and retries. Add negative cross-tenant tests for direct IDs, pagination, exports, cache keys, job status, and audit retrieval.
- Shared job snapshots may be global only when they contain no student data and their source license permits shared reuse. Never mix student prompts/history into shared caches or deduplication keys.
- Admin source controls, faculty mutation, provider configuration, kill switches, and policy overrides must not be LLM tools and require separate authorization.

### URL Fetching, SSRF, and Hostile HTML

- Prefer contracted APIs/feeds and an allowlisted source registry. Do not expose a general-purpose fetcher to the LLM.
- For on-demand URLs: allow `https` only; normalize once; reject credentials, fragments, nonstandard schemes, literals, ambiguous encodings, and disallowed ports; resolve DNS and block loopback, private, link-local, multicast, reserved, metadata, and internal ranges for IPv4 and IPv6.
- Pin connection-time destination validation. Revalidate every redirect and DNS result; default to no redirects unless a source policy explicitly permits bounded redirects. Apply the same checks to retries and alternate addresses.
- Egress-filter ingestion workers from databases, control planes, metadata services, internal DNS, and the application network. Set strict connect/read/total timeouts, byte limits, decompression limits, content-type allowlists, and redirect limits.
- Fetch and parse in an isolated, disposable worker with no secrets, student data, application session, shared filesystem, or internal network access. Static parsing is the default.
- If JavaScript rendering is source-approved, use a sandboxed disposable browser with downloads, extensions, popups, service workers, WebRTC, local network access, and unnecessary subresources blocked. Never reuse cookies or authenticated browser sessions.
- Store fetched bytes as untrusted evidence. Do not execute scripts, active documents, macros, or embedded resources, and do not render source HTML in the student UI without a proven sanitizer and restrictive CSP.

### Terms, Robots, and Source Policy

- A source-policy registry is mandatory before any fetch. Each entry must record approved hosts/paths, purpose, legal/contract owner, terms/version, robots result, authentication method, rate limits, permitted fields, attribution, raw/derived storage, LLM use, training prohibition, retention, deletion, and review/expiry date.
- Enforce both contract/terms and robots policy. Robots permission does not establish contractual reuse rights; contractual access does not waive applicable robots controls unless the agreement expressly says so.
- Fail closed on absent, expired, conflicting, or indeterminate policy. Never bypass login, CAPTCHA, paywall, access control, or rate limits.
- LinkedIn ingestion remains disabled unless a signed agreement expressly covers this product's collection, storage, derived skills, model processing, display, and deletion. Public visibility and low request volume are not approval. [R5]
- Recheck live terms and robots rules before first production use and on a scheduled policy-review cadence. Record the policy decision used for every fetch.

### Privacy and Retention

- Complete a privacy review and provider data-processing assessment before sending any student or job content externally. Record purpose, data categories, recipients/subprocessors, processing/storage regions, retention, deletion, security controls, and approved endpoint/features.
- Default model input to the minimum structured facts. Do not send raw transcript/curriculum PDFs, student identifiers, recruiter/applicant/member data, source credentials, full browser state, or unrelated conversation history.
- Define separate retention schedules for raw source snapshots, normalized job evidence, model inputs/outputs, chat history, audit metadata, BYOK metadata, and deletion tombstones. “Until deleted” is not an acceptable default without an owner and expiry process.
- Keep raw source text only when terms permit it. Delete or re-derive source-dependent records when license, source deletion, retention, or consent requires it; provenance must support selective purge.
- Treat provider “not used for training” and “zero retention” as distinct claims. Verify the exact endpoint, feature, project setting, contract, and exceptions before relying on either. [E5]
- Conversation persistence should remain off until authenticated server storage and deletion/export behavior are designed. Browser history remains user-controlled and untrusted.

### Prompt Injection and Data Exfiltration

- Treat job descriptions, HTML, PDFs, uploaded documents, retrieved text, model output, and prior chat content as untrusted data, never instructions.
- Deterministic parsers own network metadata, typed fields, evidence offsets, schema validation, hashes, and policy decisions. Invoke an LLM only for bounded unresolved prose.
- The extraction model receives no secrets, raw student documents, browsing capability, arbitrary URL fetch, shell/code execution, database access, write tools, or admin endpoints.
- Use a versioned prompt and strict schema with closed enums, bounded arrays/strings, `additionalProperties: false`, refusal/error variants, application-side validation, exact quote/offset verification, and one repair attempt before abstention.
- Tool permissions and tenant scope are fixed by server code, not prompt text. Model output is a proposal; it cannot change preferences, ranking, eligibility, source policy, or stored data without deterministic validation and explicit user confirmation where applicable.
- Prevent exfiltration through URLs, Markdown images/links, tool arguments, error messages, citations, and rendered output. The UI must not auto-fetch model-generated remote resources.
- Maintain adversarial fixtures for indirect instructions, encoded/obfuscated instructions, malicious HTML/Markdown, poisoned structured data, cross-tenant references, system-prompt requests, and secret-exfiltration attempts.

### Rate, Cost, Cron, and On-Demand Abuse

- Authenticate all non-public ingestion/model endpoints. Apply per-user, per-tenant, per-IP, per-source-host, and global limits with bounded queues and concurrency.
- Enforce daily/monthly token and currency budgets, model allowlists, maximum input/output size, maximum tool steps, timeouts, retry caps, and circuit breakers. Reject before calling the provider when a budget is exhausted.
- Meter accepted, rejected, cached, failed, and retried work by tenant/source/model without logging content. Alert on spend velocity, denial spikes, source `429/403`, repeated model failures, and queue growth.
- Scheduled ingestion must use an idempotency key such as `(source, policy_version, query/window, scheduled_at)` plus a distributed lease. On-demand refresh uses the same governed pipeline, coalesces normalized URLs, serves a fresh cached result when allowed, and never bypasses source policy or quotas.
- Do not expose unrestricted “run now,” cron-expression, bulk URL, or query fan-out controls to ordinary users. Bound role/query scope to the approved pilot.
- Backoff must honor source/provider retry guidance and must not turn retries into quota amplification. Dead-letter records contain IDs and sanitized failure metadata, not tokens, prompts, or full source payloads.

### Provenance and Audit

- Every accepted job assertion must resolve through extraction/normalization activities to an exact evidence locator in an immutable source snapshot/hash. Record source/policy version, retrieval time, parser/prompt/schema/model/taxonomy versions, validator outcomes, and reviewer decision. [R6]
- Record model request IDs, latency, token counts, cost, finish/refusal state, and sanitized error class. Do not put raw prompts/responses in general logs; any approved replay store requires separate access control and retention.
- Audit events must cover policy decisions, source fetches, model calls, secret access, admin changes, user-confirmed mutations, deletions, exports, kill-switch changes, and release/config versions.
- Audit records are append-only or tamper-evident, access-controlled, time-synchronized, searchable by non-secret IDs, and tested for selective deletion linkage without erasing required operational evidence.

### Kill Switches and Recovery

Provide independently operable, audited switches for:

- all model calls;
- each model/provider/model version;
- all ingestion;
- each source/host/policy;
- scheduled jobs;
- on-demand fetch;
- JavaScript rendering;
- BYOK use and decryption;
- model-suggested mutations;
- market-informed ranking, with static deterministic fallback.

Switches must fail closed, take effect without redeploy where practical, stop new work, and define treatment of in-flight work. Operators need a runbook for credential exposure, hostile-source discovery, source permission withdrawal, cross-tenant access, cost spike, provider outage, and bad model/prompt rollout. Roll back to the last versioned static snapshot and deterministic recommendation behavior; never silently continue with stale market evidence.

## Release-Blocking Decisions

| Gate | Required evidence | Owner decision |
|---|---|---|
| Source authorization | Signed terms or written authorization for collection, robots handling, storage, derivatives, LLM input, display, attribution, retention, and deletion | Product/legal authority; **no approval inferred here** |
| Provider/privacy | Chosen provider and endpoint, data-flow inventory, processor terms, region, retention settings/exceptions, deletion test, and approved minimum payload | Product/privacy/security |
| Identity/tenancy | Authenticated server identity, server-derived tenant scope, cross-tenant negative tests, worker/cache/object scoping | Tech lead/security |
| Secrets | Approved secret manager, per-environment credentials, redaction tests, access audit, rotation/revocation drill; BYOK either disabled or separately approved | DevOps/security |
| Fetch isolation | SSRF tests, egress policy, redirect/DNS validation, sandbox evidence, size/time limits, hostile HTML fixtures | Backend/DevOps/security |
| Prompt/tool boundary | Fixed tool allowlist, strict schemas, evidence validation, injection/exfiltration tests, no LLM ranking authority | Backend/ML/security |
| Abuse/cost | Tenant/source/provider limits, budgets, queue/concurrency caps, alerts, idempotency/coalescing tests | Product/DevOps |
| Provenance/deletion | End-to-end evidence trace, source-policy audit, selective purge, retention expiry, tamper-evident audit | Data/backend/security |
| Operations | Kill-switch test, deterministic fallback, rollback runbook, telemetry ownership, incident contacts, monitoring window | DevOps/release authority |

No blocker may be waived implicitly. Any explicit risk acceptance must identify the release authority, affected scope, compensating controls, expiry date, and follow-up owner.

## Release Posture

- **Offline planning and fixture evaluation:** ready with conditions. Use synthetic or legally retained fixtures, no live source fetching, no real secrets, no student documents, and no external model call unless separately approved.
- **Read-only deterministic chat stub:** potentially ready after a bounded contract and adversarial contract tests; it must use existing structured facts and make no mutations.
- **Live job ingestion or scheduled/on-demand fetching:** blocked pending source authorization, policy enforcement, SSRF/HTML isolation, rate controls, provenance, and kill-switch evidence.
- **External LLM synthesis:** blocked pending provider/privacy, secret, prompt/tool, cost, audit, and fallback gates.
- **BYOK:** blocked for the initial release. Reconsider only after a validated need and a separate custody design review.
- **Market-informed ranking or LLM-controlled ranking:** blocked. Market ranking requires separate deterministic evaluation; LLM-controlled ranking conflicts with repository policy.

## Reproduction Evidence

Repository observations can be reproduced with:

```bash
git status --short --branch
rg -n 'API_KEY|TOKEN|SECRET|OPENAI|LLM|cron|scheduler|DATABASE_URL|CORSMiddleware' .env.example backend
cat .env.example backend/main.py backend/database/connection.py backend/requirements.txt
```

## Sources

### Repository Evidence

- **R1:** `research/repo-analysis.md`, especially lines 10-35, 53-72, 109-167, 242-330, and 330-365.
- **R2:** `backend/requirements.txt`, lines 1-7.
- **R3:** `.env.example`, line 1; `backend/database/connection.py`, lines 5-17.
- **R4:** `backend/main.py`, lines 14-40.
- **R5:** `research/linkedin-access.md`, especially lines 9-107, 135-178, and 208-214.
- **R6:** `research/extraction-and-operations.md`, especially sections 4-6, 9, 11-13, and lines 746-817.

Paths under `research/` are relative to this file's directory; other paths are repository-root-relative.

### External Primary Sources

Accessed 2026-11-10:

- **E1:** OWASP, [Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).
- **E2:** OWASP, [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).
- **E3:** OWASP, [Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).
- **E4:** IETF, [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309.html).
- **E5:** OpenAI, [Data controls in the OpenAI platform](https://platform.openai.com/docs/guides/your-data).
- **E6:** OpenAI, [Best Practices for API Key Safety](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).
