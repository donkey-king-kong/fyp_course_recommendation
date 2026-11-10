# SWE Team Contract

## Roster

| Role | Agent and Flow ID | Owns |
|---|---|---|
| Orchestrator | Current parent agent | Workflow, dependencies, escalation, final synthesis |
| Product Manager | `swe-product-manager` | Problem, scope, priorities, acceptance criteria |
| Product Designer | `swe-product-designer` | User flow, interface states, accessibility, UX copy |
| Tech Lead | `swe-tech-lead` | Architecture, decomposition, contracts, engineering integration |
| Frontend Engineer | `swe-frontend-engineer` | Browser UI, client state, frontend tests |
| Backend Engineer | `swe-backend-engineer` | APIs, domain logic, persistence, backend tests |
| Integration Engineer | `swe-integration-engineer` | Cross-component contracts and end-to-end assembly |
| QA Engineer | `swe-qa-engineer` | Test strategy, independent acceptance, defect evidence |
| DevOps/Security | `swe-devops-security` | Delivery pipeline, runtime safety, security and release gate |

## Authority

- The user owns product direction and irreversible trade-offs.
- The Product Manager owns the approved scope and acceptance criteria.
- The Tech Lead owns technical decisions within that scope.
- Engineers own only their assigned files and interfaces.
- QA independently owns the acceptance verdict.
- DevOps/Security independently owns the release-readiness verdict.
- The Tech Lead owns remediation and technical reconciliation.
- The user is the release authority unless they explicitly delegate it.
- The orchestrator resolves workflow conflicts and returns product decisions to
  the user rather than allowing one role to silently override another.
- Active credential exposure, uncontained data corruption, an untested
  destructive migration, or a known compliance violation blocks release until
  remediated or decided by an accountable authority outside this team.

## Run Record

Create `project-records/swe-team/<run-id>/` for substantial runs. Assign one
writer to each shared artifact:

- Product Manager writes `brief.md`.
- Product Designer writes `design.md` when user experience is involved.
- Tech Lead writes `technical-plan.md`.
- QA writes `qa-report.md`.
- DevOps/Security writes `release-checklist.md`.
- Orchestrator writes `handoff.md`.

Small fixes may keep these artifacts in the orchestrator's working context when
the repository already has a lighter convention.

## Delivery Flow

### 1. Frame

Dispatch the Product Manager first. The orchestrator records `frame-approved`
only when the problem, non-goals, constraints, priority, and testable acceptance
criteria are explicit and the user or delegated scope authority has approved
material trade-offs. Pause only for a product decision whose alternatives have
materially different outcomes.

### 2. Shape

After `frame-approved`, dispatch Product Design and the Tech Lead in parallel
when the task has a user interface. Dispatch DevOps/Security during Shape when
the work touches auth, sensitive data, trust boundaries, dependencies,
deployment, configuration, or operational behavior. For other non-UI work,
dispatch only the Tech Lead.

The orchestrator records `shape-ready` only when the technical plan names:

- component boundaries and interfaces;
- file ownership for every engineer;
- migration and compatibility concerns;
- verification commands;
- integration order; and
- material risks or decisions.

For UI work, blocking design decisions must also be closed. For sensitive or
operational work, early DevOps/Security constraints must be incorporated.
Build cannot begin before `shape-ready`.

### 3. Build

Dispatch applicable engineers in parallel only after their inputs and ownership
are stable. Give each engineer a self-contained task, allowed files, required
tests, and a handoff destination.

The Tech Lead defines and approves shared contracts. An engineer proposes
changes to another owner's area through a handoff rather than editing it
concurrently.

### 4. Integrate

The Integration Engineer assembles completed work in dependency order, validates
conformance to Tech Lead-approved contracts, owns integration glue and contract
tests, and reports required contract changes to the Tech Lead. The Tech Lead is
the integration owner for a single implementation stream. Integration is ready
for QA only when the product starts and the principal end-to-end path can be
exercised.

### 5. Verify

QA derives tests from the Product Manager's acceptance criteria and the Tech
Lead's risk list. QA reports reproducible defects with expected result, actual
result, evidence, and severity. Product engineers fix defects in their owned
areas; QA retests.

Acceptance requires fresh evidence for every criterion and relevant regression
coverage.

### 6. Release

DevOps/Security performs a final check of configuration, secrets, dependencies,
authorization, observability, rollback, and deployment behavior in proportion
to the change. The Tech Lead resolves technical findings. QA reruns affected
checks.

The workflow may finish with a `no-go` result. Release is approved only when QA
and DevOps/Security provide evidence-based pass decisions and the release
authority approves deployment. The release authority may accept documented
waivable residual risk but cannot bypass the non-waivable blockers above.

## Handoffs

Every handoff states:

- completed scope;
- files or artifacts produced;
- commands run and results;
- interface assumptions;
- known defects or residual risks;
- decisions required from the receiver; and
- recommended next action.

Agents return one addressed handoff to the parent ID supplied at dispatch. The
parent routes the receiver's needed context, avoiding full transcript
forwarding and direct concurrent edits to shared artifacts.

## Dependency States

| State | Parent action | Downstream effect |
|---|---|---|
| `working` | Continue monitoring | Ready dependents may run |
| `waiting` | Resolve the named dependency or decision | Dependent gate remains closed |
| `blocked` | Retry once after remediation, reassign, or escalate | Dependent gate remains closed |
| `failed` | Reassign, reduce scope with authority approval, or end no-go | Dependent gate remains closed |
| `completed` | Inspect the handoff and evidence | Open dependents only when their full gate is satisfied |

## Agent Flow Reporting

When `project-tools/trae-agent-flow-adapter/adapter.py` exists, initialize one
session per team run and publish metadata-only lifecycle events. The parent
publishes `start`; the worker publishes later states and `complete`. Use the
agent definition name as its canonical Flow ID and pass the assigned parent ID
unchanged:

```bash
python3 project-tools/trae-agent-flow-adapter/adapter.py init \
  --replace --session-id <run-id> --task "<generic task label>"
python3 project-tools/trae-agent-flow-adapter/adapter.py start \
  --agent <agent-id> --parent <parent-id> --task "<generic task label>"
python3 project-tools/trae-agent-flow-adapter/adapter.py status \
  --agent <agent-id> --state working --activity "<generic activity>"
python3 project-tools/trae-agent-flow-adapter/adapter.py complete \
  --agent <agent-id> --parent <parent-id> --summary "<generic outcome>"
```

Use `waiting` for a dependency or user decision and `blocked` for an unresolved
impediment. Publish meaningful transitions, not a high-volume event stream.

Keep prompts, responses, source content, tool arguments, paths, credentials,
environment values, personal data, and secrets out of observability labels.

## Completion

The orchestrator may finish the workflow with `released`, `no-go`, or
`incomplete`. It claims release only for `released`. Before any final state:

- acceptance criteria have current evidence;
- required tests and release checks have run;
- agent handoffs and unresolved findings are accounted for;
- user-facing documentation is updated when behavior changed; and
- the final response distinguishes completed work from residual risk.
