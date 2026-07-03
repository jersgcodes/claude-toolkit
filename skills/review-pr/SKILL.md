---
name: review-pr
description: Review a pull request for logic, security, and style issues.
version: 0.1.0
---


Review a pull request for logic, security, and style issues. Do the following steps in order:

**1. Get the diff**
If a PR number or branch name is provided as an argument (`$ARGUMENTS`), use it.
Otherwise, run `git log main..HEAD --oneline` and `git diff main...HEAD` to review the current branch against main.

**2. Logic review**
- Does the change do what it claims (based on commit messages and PR description)?
- Are there edge cases not handled?
- Are there off-by-one errors, null/undefined risks, or unhandled exceptions?
- Does it introduce any regressions in existing behaviour?

**3. Security review**
- Any new user input that isn't validated or sanitised?
- Any secrets, tokens, or PII that could be exposed?
- Any new external API calls without error handling or timeouts?
- Any SQL/shell injection risks?

**4. Style and maintainability**
- Are new functions/methods appropriately sized (single responsibility)?
- Is anything duplicated that could be reused?
- Are variable names clear?
- Is anything over-engineered for the current need?

**5. Tests**
- Are new code paths covered by tests?
- Are there any obvious missing test cases?

**6. Summary**
Print a structured review:

**Must fix** (blocks merge):
- [list or "None"]

**Should fix** (important but not blocking):
- [list or "None"]

**Optional** (suggestions):
- [list or "None"]

**Overall**: Approve / Request changes / Approve with comments
