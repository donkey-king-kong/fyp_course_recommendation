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
For this project, keep explanatory comments above functions rather than inside them unless the comment explains a specific non-obvious line. Use one blank line between top-level function/comment blocks in project files.

## Entry Format

```text
Date:
Mistake:
What happened:
Correction:
Lesson:
```
