---
name: status
description: [CLI-only] Project status check — tasks, user actions, and architecture alignment.
version: 0.1.0
---


Project status check — tasks, user actions, and architecture alignment. Do the following steps in order:

**1. Read task files**
Look for TASKS.md, TASKS_CURRENT.md in the project root. Read both if they exist. Extract all PENDING tasks (not DONE). Group by priority if labelled.

**2. Read user actions**
Read USER_ACTIONS.md. Show only the most recent dated entry (the one at the top).

**3. Print status**

```
## Pending Tasks
<numbered list of PENDING tasks, or "None" if all done>

## Latest User Actions (<date>)
<built items and any open decisions/next steps from the most recent entry>
```

**4. Staleness review (background)**
Spawn a background agent to do the following:
- Read TASKS.md, USER_ACTIONS.md, and CLAUDE.md (project-level)
- Read the src/ directory structure (one level deep)
- Run `git log --oneline -20` to see recent commits

For each PENDING task, assess:
- **STALE**: task is already done (code exists, merged in recent commits) but not marked complete
- **OUTDATED**: task references files, patterns, or decisions that have since changed
- **SUPERSEDED**: task has been replaced by a different approach already in the codebase
- **OK**: task is still relevant and actionable

For USER_ACTIONS.md, check the 3 most recent dated entries:
- Flag any "Test on your device" items that reference UI/features that have been significantly reworked since that entry (making the test instructions inaccurate)
- Flag any "Decisions needed" that have already been decided (visible in later commits or TASKS.md completed items)
- Flag any "Deploy / setup steps" that are no longer accurate

For architecture alignment, for each PENDING task assess whether it:
- Fits cleanly within the current architecture (no flag needed)
- Requires a new file, module, or pattern not yet present (flag as GAP)
- Conflicts with or changes an existing architectural decision (flag as CHANGE)

The agent should return a combined report. If everything is OK (no stale tasks, no outdated user actions, no architecture flags), return the single string "OK".

**5. Print review findings**
- If the background agent returns "OK": print nothing (suppress this section entirely).
- If it returns findings, print applicable sections:

```
## Staleness Flags
<one line per flagged item: item → STALE/OUTDATED/SUPERSEDED → one sentence explanation>

## User Actions — Needs Update
<one line per flagged item: date + section → reason it needs updating>

## Architecture Flags
<one line per flagged task: task name → GAP or CHANGE → one sentence explanation>
```

Only print sections that have at least one finding. Keep the entire output under 60 lines.
