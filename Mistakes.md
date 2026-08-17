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

## Entry Format

```text
Date:
Mistake:
What happened:
Correction:
Lesson:
```
