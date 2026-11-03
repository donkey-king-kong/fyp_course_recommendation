# Mistakes

This file tracks mistakes made during the rebuild so they can be reviewed and avoided later.

## Log

### 2026-08-17

Mistake:
Included extra guidance text and unwanted scope wording in the PR body.

What happened:
The PR body included PR title examples and wording that should not have appeared in the submitted PR description.

Correction:
Removed the extra examples from the PR body and updated the PR description to focus only on the actual backend change.

Lesson:
PR templates can include guidance while drafting, but submitted PR bodies should be concise and contain only reviewer-facing information.

### 2026-08-17

Mistake:
Used the word `milestone` in PR-related text.

What happened:
The PR description mentioned `Milestone 1`, even though commit messages and PR content should not include the word `milestone`.

Correction:
Removed the milestone wording from the PR description.

Lesson:
Do not mention `milestone` or milestone-related wording in commit messages, PR titles, or PR descriptions. Keep Git and PR text focused on the concrete code change.

### 2026-08-25

Mistake:
Added explanatory comments/docstrings inside functions and unnecessarily used two empty lines after functions in newly created backend files.

What happened:
Some module API comments were placed inside function bodies instead of above the function. I also kept adding two empty lines after functions, even though the preferred project style is one blank line. A patch also briefly left malformed comment text and duplicated a module lookup call in `backend/routers/modules.py` / `backend/services/module_service.py`.

Correction:
Moved function explanations above the functions, removed the malformed comment text, restored the exact module lookup function, and normalized spacing to one blank line between top-level comment/function blocks.

Lesson:
For this project, keep explanatory comments above functions rather than inside them unless the comment explains a specific non-obvious line. Use exactly one empty line between top-level function/comment blocks in project files. Do not leave two consecutive empty lines between imports, constants, comments, functions, or classes.

### 2026-08-27

Mistake:
Repeatedly created PR titles that did not follow the required Conventional Commit-style format.

What happened:
The PR title was created as `Add curriculum guide upload flow` instead of using the expected typed format such as `feat: add curriculum guide upload flow`. This repeated the earlier PR-formatting issue where submitted PR text did not match the project's preferred Git/PR conventions.

Correction:
Update the PR title to `feat: add curriculum guide upload flow` and record this rule explicitly so future PR titles are checked before submission.

Lesson:
Before creating or updating any PR, verify the PR title follows the same Conventional Commit-style format as commits: `<type>: <short lowercase summary>`. Examples: `feat: add curriculum guide upload flow`, `fix: handle empty transcript uploads`, `docs: update architecture notes`. Do not use untitled sentence case such as `Add curriculum guide upload flow`.

### 2026-08-27

Mistake:
Created a PR without assigning it to the repository owner/user.

What happened:
PR #20 was created but the assignee field was left empty, showing `No one`. This means the PR was not clearly owned for review and follow-up.

Correction:
Assign PR #20 to the current GitHub user. For future PRs, always assign the PR to the user immediately after creating it.

Lesson:
Whenever creating a PR with `gh pr create`, also assign it to the user. Use `gh pr edit <number> --add-assignee @me` after PR creation unless the user explicitly asks for a different assignee.

### 2026-08-27

Mistake:
Created a PR description that did not follow `PR_template.md`.

What happened:
PR #20 was created with custom sections named `Summary`, `Verification`, and `Not included`. The repository template requires the sections `Description`, `Why This Change Is Needed`, `How To Test`, `Expected Result`, and `Checklist`.

Correction:
Update PR #20 so its description follows `PR_template.md` exactly, including the required checklist items.

Lesson:
Before creating or updating a PR description, read `PR_template.md` and use its exact section headings. Do not invent alternate headings, even if the content is similar. Use the template format first, then fill in project-specific details.

### 2026-08-28

Mistake:
Repeated offence: added two blank lines between imports/classes/functions again in newly created recommendation files.

What happened:
`backend/schemas/recommendation.py`, `backend/services/recommendation_service.py`, and `backend/routers/recommendations.py` were created with repeated double blank lines between top-level blocks, despite this exact style mistake already being recorded on 2026-08-25.

Correction:
Removed the extra blank lines and checked the newly changed recommendation files for the same spacing issue.

Lesson:
Do not make this mistake again. For this project, use one blank line between top-level comment/function/class blocks, not two. Before committing any newly created or edited Python file, explicitly scan imports, constants, classes, functions, and router decorators for accidental double blank lines.

### 2026-08-31

Mistake:
Repeated offence: created a PR without assigning it and without following `PR_template.md`.

What happened:
PR #27 was created with a custom `Summary`/`Verification` body instead of the required `Description`, `Why This Change Is Needed`, `How To Test`, `Expected Result`, and `Checklist` sections. It was also left unassigned. This is the 2nd recorded time a PR was created without an assignee, and the 2nd recorded time a PR description did not follow `PR_template.md`.

Correction:
Updated PR #27 to use the exact `PR_template.md` section headings and assigned it to `@me`.

Lesson:
Before creating any PR, first read `PR_template.md`, prepare the body using its exact headings, create the PR, then immediately run `gh pr edit <number> --add-assignee @me`. After creation, verify the PR with `gh pr view <number> --json title,assignees,body,url` before telling the user it is done.

### 2026-09-01

Mistake:
Repeated offence again: created PR #33 without following `PR_template.md` and without assigning it.

What happened:
PR #33 was created with custom `Summary` and `Verification` headings instead of the required `Description`, `Why This Change Is Needed`, `How To Test`, `Expected Result`, and `Checklist` headings. The PR was also left with no assignee even though this exact process mistake had already been recorded multiple times.

Correction:
Update PR #33 to use the exact `PR_template.md` sections, assign it to `@me`, and verify the PR metadata with `gh pr view`.

Lesson:
Do not create PRs from memory. Before every `gh pr create`, read `PR_template.md`, draft the body with the exact required headings, include the checklist, create the PR, immediately assign `@me`, and verify title/body/assignee before reporting completion.

## Entry Format

```text
Date:
Mistake:
What happened:
Correction:
Lesson:
```
