---
name: swe-team
description: Coordinate a multi-agent software delivery team from product discovery through release. Use when the user asks to use the SWE team, run a feature team, or delegate work across product, design, engineering, QA, and release roles.
---

# SWE Team

Read [the team contract](references/team-contract.md) before dispatching work.

## Start

1. Identify the requested outcome, repository, constraints, and delivery mode.
   Default to end-to-end delivery when the user asks to build or fix something.
2. Create a short run ID and initialize Agent Flow reporting when the project
   adapter exists.
3. Tell the user which roles are being activated and why.
4. Dispatch the Product Manager to frame substantial product work. A narrow bug
   with explicit expected behavior may proceed directly to the Tech Lead.
5. Record `frame-approved` before Shape and `shape-ready` before Build. Do not
   open downstream work while a prerequisite is waiting, blocked, or failed.

## Assemble

Use the smallest complete team:

- Always use the Tech Lead for implementation spanning multiple files or agents.
- Use the Product Manager when scope or acceptance criteria need definition.
- Use the Product Designer for user-facing behavior.
- Use Frontend and Backend Engineers only where those surfaces exist.
- Use the Integration Engineer when two or more implementation streams meet.
- Use QA for every behavioral change.
- Use DevOps/Security when delivery, configuration, dependencies, auth, data,
  external boundaries, or operational behavior can change.

Run independent work in parallel only after inputs and file ownership are
stable. Keep dependency-bound work waiting until its producer hands off.
For sensitive or operational changes, use DevOps/Security once during Shape to
set constraints and again after integration for the release-readiness verdict.

## Dispatch

Prefer the project agents in `.trae/agents/` by name. Give every worker:

- one role and one concrete outcome;
- the minimum context and upstream artifacts it needs;
- exclusive files or components it may edit;
- explicit non-owned files;
- required verification;
- the receiver of its handoff; and
- canonical Agent Flow ID matching its agent name and its assigned parent ID.

Use this default reporting hierarchy:

```text
orchestrator
├── swe-product-manager
│   └── swe-product-designer
├── swe-tech-lead
│   ├── swe-frontend-engineer
│   ├── swe-backend-engineer
│   └── swe-integration-engineer
├── swe-qa-engineer
└── swe-devops-security
```

The parent publishes each `start` event. Workers publish later states and
completion with the same IDs.

When custom project-agent routing is unavailable, use a general worker and
include the relevant role definition in its task.

## Integrate

Remain the orchestrator. Track dependencies, request concise progress updates,
and route handoffs through the hierarchy. The Tech Lead integrates engineering
decisions; the orchestrator integrates the whole delivery.

Require QA and DevOps/Security to evaluate independently from the implementers.
Send defects back to the owning engineer, then require focused retesting.
The Tech Lead approves shared contracts; the Integration Engineer validates
conformance and owns assembly rather than redefining those contracts.

## Finish

Run fresh verification appropriate to the repository. Reconcile every acceptance
criterion, QA finding, release finding, and handoff before claiming completion.
Classify the result as `released`, `no-go`, or `incomplete`. Return a concise
delivery summary with evidence, outputs, release authority, and residual risks.
