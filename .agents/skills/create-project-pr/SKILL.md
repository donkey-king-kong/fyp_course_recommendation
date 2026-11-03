---
name: create-project-pr
description: Prepare, create, or update pull requests for this course recommendation repository using its shared template, title conventions, assignee rule, and final metadata verification.
---

# Project Pull Requests

Use this workflow for PR preparation, creation, or updates in this repository. Read the root [AGENTS.md](../../../AGENTS.md) and the single shared [PR template](../../../docs/workflows/PR_template.md) before drafting each PR. Resolve those links relative to this skill; shell paths below are relative to the repository root.

## Prepare The Reviewable Change

- Inspect the current branch, working tree, intended base, and complete branch diff. Describe the final changes for a reviewer who has not read the conversation.
- Use `<type>: <short lowercase description>` for the PR title. Do not include milestone wording in the title, body, or commit messages.
- Read `docs/workflows/PR_template.md` and use its exact headings and checklist. Fill in concrete behavior, purpose, verification commands or steps, and expected results. Remove drafting examples and instructions from the submitted body.
- Mark checklist items only when verified. Report material limitations and distinguish checks performed now from historical results. Do not claim application tests for a documentation-only change.
- Keep the template in its shared document; do not copy it into this skill or create a competing format.

## Publish Within Authorization

- Preparing a body does not authorize commits, pushes, PR creation, or updates. Honor explicit authorization already given in the conversation; do not ask again for actions already authorized. If publication is not authorized, finish the draft and report it as prepared.
- Check whether the branch already has a PR before creating another. Use the authorized base and draft status; do not publish to an unrelated repository or update an unrelated PR.
- For multiline bodies, use a structured tool argument, or write the exact body to a temporary file and pass it to `gh pr create` / `gh pr edit` with `--body-file`. Preserve actual newlines and avoid shell interpolation of the body.
- Assign the PR to the current GitHub user with `--assignee @me` during creation, or immediately run `gh pr edit <number> --add-assignee @me`, unless the user requests a different assignee.
- Verify the result with `gh pr view <number> --json title,assignees,body,url`. Check the title, exact template headings, checklist accuracy, requested assignee, and URL before reporting completion.
- If a mutation returns an ambiguous result, inspect the current PR state before retrying to avoid duplicate publication. Stop and report unresolved authorization or permission failures after preparing the reviewable result.
