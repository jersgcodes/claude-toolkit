---
name: commit-status
description: [CLI-only] Show the current commit log state for this project.
version: 0.1.0
---


Show the current commit log state for this project. Do the following steps in order:

**1. Check for commit log**

Run:
```bash
python3 ~/.claude/hooks/commit-log.py --cwd . --cmd show
```

If the output is "No commit log for today." or "Commit log is from a previous day", print that message and stop.

---

**2. Print the output**

Print the result exactly as returned. It shows all commit blocks for today with:
- Status (in-progress / committed)
- Branch
- Each skill state (○ not-run / ⟳ running / ✓ passed / ✗ failed / ? pending-user)
- Test state
- Notes (if any)

---

**3. Interpret the state**

After the raw output, add a one-line verdict:

- All skills passed, tests passed, status committed → `All clear — ready to commit.`
- Any skill not-run → `Run /pre-commit to check skills before committing.`
- Any skill failed → `Fix reported issues, re-run failed skills, then retry commit.`
- Any skill pending-user → `Resolve pending-user items, update commit-log.md to passed, then retry.`
- Status in-progress → `Commit in progress — skills not yet all resolved.`
