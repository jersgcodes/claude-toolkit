---
name: status
description: [CLI-only] Show status over TASKS.md and USER_ACTIONS.md: pending tasks, the latest user actions, and architecture alignment flags. With no argument it reports this project and runs a background staleness review; `--all` sweeps every project in the workspace and reports counts. Use when resuming work, or when asked "what's next" or "where are we".
allowed-tools: [Read, Glob, Bash, Task]
version: 0.2.0
---

Status check over `TASKS.md` and `USER_ACTIONS.md`. `$ARGUMENTS` selects the scope:

| Argument | Scope |
|---|---|
| *(none)* | This project, with a background staleness and architecture review |
| `--all` / `all` | Every project under `~/claude/`, counts only. Use for a workspace overview |

---

# Mode: `--all` (workspace sweep)

**1. Find all projects**

```bash
find ~/claude -maxdepth 2 -name "TASKS.md" | sort
```

Exclude `~/claude/TASKS.md` itself — that is workspace-level, not a project.

**2. Count per project**

Read each `TASKS.md` and count `Status: PENDING` and `Status: DONE`. Extract the text of each pending task from its line; the workspace format is `- [ ] [Bnn] <task> — <area> — Status: PENDING`, so the task text sits between the ID and the first `—`. Some projects omit IDs; do not assume they are present.

**3. Check for active commit blocks**

For each project with a `.claude/` directory:
```bash
python3 ~/.claude/hooks/commit-log.py --cwd <project_path> --cmd active
```

**4. Print**

```
Workspace Status — <date>

<project>/        N pending, N done
  PENDING: <task text>
  PENDING: <task text>
  [commit in progress: 20260319-1430]

<project>/        all done

Total: N pending across N projects
```

Mark projects with 0 pending as `all done`, flag any active commit block, and flag more than 5 pending as `backlog heavy`.

---

# Mode: default (this project)

**1. Read task files**

Read `TASKS.md` in the project root and extract all `Status: PENDING` tasks (not DONE). Group by priority if labelled. If a legacy `TASKS_CURRENT.md` exists, read it too and flag that it should be folded into TASKS.md — no hook or script reads it.

**2. Read user actions**

Read `USER_ACTIONS.md`. Show only the most recent dated entry.

**3. Print status**

```
## Pending Tasks
<numbered list of PENDING tasks, or "None" if all done>

## Latest User Actions (<date>)
<built items and any open decisions/next steps from the most recent entry>
```

**4. Staleness review (background)**

Spawn a background agent to:
- Read `TASKS.md`, `USER_ACTIONS.md` and project-level `CLAUDE.md`
- Read the `src/` structure one level deep
- Run `git log --oneline -20`

For each PENDING task, assess:
- **STALE** — already done (code exists, merged in recent commits) but not marked complete
- **OUTDATED** — references files, patterns or decisions that have since changed
- **SUPERSEDED** — replaced by a different approach already in the codebase
- **OK** — still relevant and actionable

For the 3 most recent `USER_ACTIONS.md` entries, flag:
- "Test on your device" items referencing features reworked since, making the instructions inaccurate
- "Decisions needed" already decided (visible in later commits or completed tasks)
- "Deploy / setup steps" no longer accurate

For architecture alignment, for each PENDING task assess whether it fits the current architecture (no flag), needs a file/module/pattern not yet present (**GAP**), or conflicts with an existing decision (**CHANGE**).

Return a combined report, or the single string "OK" if nothing is flagged.

**5. Print review findings**

If the agent returns "OK", print nothing for this section. Otherwise print only the sections that have findings:

```
## Staleness Flags
<item → STALE/OUTDATED/SUPERSEDED → one sentence>

## User Actions — Needs Update
<date + section → why it needs updating>

## Architecture Flags
<task → GAP or CHANGE → one sentence>
```

Keep the entire output under 60 lines.
