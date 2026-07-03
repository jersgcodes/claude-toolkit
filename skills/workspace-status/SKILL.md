---
name: workspace-status
description: [CLI-only] Show pending tasks across all projects in the workspace.
version: 0.1.0
---


Show pending tasks across all projects in the workspace. Do the following steps in order:

**1. Find all projects**

List all directories under `~/claude/` that contain a `TASKS.md` file:

```bash
find ~/claude -maxdepth 2 -name "TASKS.md" | sort
```

Exclude `~/claude/` itself (workspace-level file, not a project).

---

**2. For each project, extract task counts**

Read each `TASKS.md` and count:
- `Status: PENDING` tasks
- `Status: DONE` tasks

Also grab the title of each pending task (the `### Task N — <title>` line).

---

**3. Check for active commit blocks**

For each project that has a `.claude/` directory, run:
```bash
python3 ~/.claude/hooks/commit-log.py --cwd <project_path> --cmd active
```

Note any project with an in-progress commit block.

---

**4. Print workspace summary**

```
Workspace Status — <date>

<project-name>/        N pending, N done
  PENDING: Task 3 — Add export feature
  PENDING: Task 5 — Fix mobile layout
  [commit in progress: 20260319-1430]

<project-name>/        N pending, N done
  PENDING: Task 1 — Initial setup

<project-name>/        all done ✓

Total: N pending tasks across N projects
```

---

**5. Highlight**

- Projects with 0 pending tasks: mark as `all done`
- Projects with an active commit block: flag clearly
- Projects with more than 5 pending tasks: flag as `backlog heavy`
