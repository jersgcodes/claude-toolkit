---
name: diff-review
description: [CLI-only] Review changed code before it lands, for bugs, security, privacy, debug leftovers, style and missing tests. Scope follows the argument: no argument or `staged` reviews the staged diff, `branch` reviews the whole branch against main including its commit messages, and a PR number or branch name reviews someone else's work. Use before /pre-commit or before merging a feature branch.
allowed-tools: [Read, Grep, Bash, Glob]
version: 0.2.0
---

Review changed code before it lands. `$ARGUMENTS` selects the scope:

| Argument | Reviews | Typical use |
|---|---|---|
| *(none)* or `staged` | `git diff --staged` | Before `/pre-commit` |
| `branch` | `git diff main...HEAD` plus `git log main..HEAD --oneline` | Before merging a feature branch |
| a PR number or branch name | That PR or branch | Reviewing someone else's work |

**1. Get the diff**

For `staged`, run `git diff --staged` and `git diff --staged --stat`. If nothing is staged, print "Nothing staged — run `git add` first." and stop.

For `branch`, run `git log main..HEAD --oneline` and `git diff main...HEAD`. Read the commit messages: they state what the change claims to do, which step 2 checks it against.

---

**2. Bugs and logic**

Greppable patterns:
- Array/object mutation on state variables (`state.push(`, `state[i] =`)
- Missing `await` on async calls
- Off-by-one errors in loops or slice indices
- Returning inside a loop where the intent looks like continue
- A conditional that is always true or always false

Judgement (weight these more heavily on `branch` and PR scope, where intent is stated):
- Does the change do what its commits claim?
- Unhandled edge cases, null/undefined risks, uncaught exceptions
- Regressions in existing behaviour

**3. Security**
- New user input that is not validated or sanitised
- Secrets, tokens or PII that could be exposed
- New external API calls with no error handling or timeout
- SQL or shell injection risk

For a dedicated pass rather than a spot check, run `/security-check`.

**4. Privacy (project-specific)**
- Free-text fields (company name, URL, product names, workflow descriptions) passed to `localStorage.setItem` or a storage wrapper
- Any new field added to a session or library save object — flag for privacy review

**5. Debug leftovers**
- `console.log(`, `console.error(`, `debugger`
- Commented-out code blocks over 2 lines
- TODO/FIXME introduced in this diff

**6. Style and maintainability**
- New functions appropriately sized, single responsibility
- Anything duplicated that could be reused
- Unclear variable names
- Anything over-engineered for the current need

**7. Tests**
- Source files changed with no corresponding test file in the diff — name each one
- New code paths with no test coverage
- Obvious missing test cases

---

**8. Report**

```
Diff Review (<scope>) — <N> files changed, <+X/-Y> lines

Must fix (blocks):
  - <file>:<line> — <what and why>

Should fix (important, not blocking):
  - <file>:<line> — <what and why>

Optional:
  - <file>:<line> — <suggestion>

Verdict: CLEAN / WARN / BLOCK
```

- `CLEAN` — nothing found
- `WARN` — debug leftovers, style or missing tests only
- `BLOCK` — a bug, a security issue or a privacy violation

**9. Next step**

- `BLOCK` — list the exact lines to fix. Do not proceed until they are resolved.
- Staged scope, `CLEAN` or `WARN` — print "Ready for /pre-commit".
- Branch or PR scope — state Approve / Request changes / Approve with comments.
