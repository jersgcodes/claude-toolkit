---
name: wrap-up
description: [CLI-only] End-of-session wrap-up — updates TASKS.md, USER_ACTIONS.md, CLAUDE.md, and project-status.yaml. Use at the end of every build session.
allowed-tools: [Bash, Read, Grep, Glob, Write, Edit]
version: 0.2.0
---

End-of-session documentation update. Reviews what was built this session and updates TASKS.md, USER_ACTIONS.md, CLAUDE.md, and project-status.yaml.

`$ARGUMENTS` selects the scope:

| Argument | Runs |
|---|---|
| *(none)* | Every step below |
| `tasks` | Steps 1 to 3 only — capture the task list and stop. Use mid-session, after a planning discussion, or when you only want next steps written down |

Do the following steps in order:

---

**1. Orient — read current state**

Read these files in parallel:
- `TASKS.md` — current task list
- `USER_ACTIONS.md` — existing session log (first 60 lines is enough)
- `CLAUDE.md` — project rules (first 80 lines)
- `LEARNINGS.md` (if exists) — accumulated session lessons

Also run `git diff --stat HEAD` and `git status` to see what files changed this session.

Run incident detection scan:
```bash
git log --since="2 days ago" --pretty=format:"%h %s" | grep -iE "revert|hotfix|urgent|rollback|fix.*production|fix.*bug" | head -10
```

If any matches found, flag for Step 8 (postmortem suggestion).

---

**2. Update TASKS.md**

Flip completed tasks to `Status: DONE`, then scan the conversation for work that is not yet on the list: decisions made, features discussed, issues raised, anything named as a next step.

Append new build tasks (code, config, infra) in the format the file already uses. The workspace standard is:

```
- [ ] [Bnn] <task> — <sub-project or area> — Status: PENDING
```

If the project allocates task IDs, read the highest existing one and continue the sequence; if it does not, omit them. Append to the pending section only — never reformat existing entries, never rewrite the file wholesale.

Be specific: "Build Gaps & Opportunities page showing 51 gaps ranked by severity", not "improve gaps". Include the reason so future-Claude knows why. Genuinely actionable items only, not observations.

Never write to `TASKS_CURRENT.md`. Every hook and script counts `Status: PENDING` in `TASKS.md`; a task written anywhere else is invisible to the session-start summary and to `/status` in both its modes.

---

**3. Update USER_ACTIONS.md**

Everything the user must do, decide, or provide goes here rather than TASKS.md: things to test, deploy or setup steps, and decisions only they can make. Add a dated entry at the top, per workspace CLAUDE.md §End-of-build-session checklist:

```markdown
## YYYY-MM-DD — <feature name>
### Built
- ...
### Test on your device
- [ ] ...
### Deploy / setup steps
- [ ] ...
### Decisions needed
- ...
```

Preserve existing entries in both files. You are appending, not regenerating.

**If `$ARGUMENTS` is `tasks`, stop here** and report what was written to each file.

---

**4. Update CLAUDE.md (only if needed)**

Scan the conversation for:
- New patterns introduced that should be documented (e.g. new file structure, new naming convention)
- Decisions made that will affect future builds
- Checklist items that are now outdated

If anything is substantive, make the minimal targeted edit — add a section, update a path, or add a checklist item. Do NOT rewrite or restructure CLAUDE.md.

If nothing needs changing, skip this step and say so.

---

**5. Update architecture documentation**

Check if `docs/` exists in the project root. If not, skip this step and note it.

If it does, update or create `docs/architecture.md` (description paragraph, Mermaid module map, key-files table), then run the architecture generator script if the project has one.

> **Reference:** the `architecture.md` template and the generator-script rules are in `references/wrap-up-ref.md` § Step 5.

---

**6. Update project-status.yaml (API declarations for orchestrator dashboard)**

Scan the codebase for external API usage, classify each API as `paid` / `free-tier` / `free`, and write or update `project-status.yaml` at the project root. If the existing file is already accurate, update only `last_updated`.

> **Reference:** the scan list, tier definitions, YAML template and rules are in `references/wrap-up-ref.md` § Step 6.

---

**7. Worktree cleanup check**

If this session created or used git worktrees, check whether any are safe to remove.

Run:
```bash
git worktree list 2>/dev/null
```

For each non-main worktree:
- If branch is merged to main AND working tree is clean → suggest `/worktree clean` to remove
- If unmerged commits exist → note in summary, do NOT remove
- If working tree dirty → note in summary

If no worktrees exist, skip this step silently.

---

**8. Capture session learnings (LEARNINGS.md)**

Ask the user one direct question:

> "What was the most surprising, unexpected, or instructive thing about this session? (One sentence — skip if nothing stood out.)"

If they answer, append an entry to `LEARNINGS.md` at the project root, creating it if missing. If they say "nothing" or "skip", note `LEARNINGS.md: skipped` in the final summary and write nothing.

This is opt-in. Don't force a learning if there isn't one — that creates noise.

> **Reference:** the `LEARNINGS.md` entry template is in `references/wrap-up-ref.md` § Step 8.

**9. Postmortem check (incident detection)**

If Step 1 detected incident signals (revert/hotfix/urgent commits in last 2 days), suggest:

> "Recent activity suggests an incident: <brief — list the signal commits>.
> Consider running `/postmortem <name>` to capture the timeline and root cause before details fade. Skip if these were planned changes."

Don't auto-create the postmortem — let the user decide. They know context the script doesn't.

**10. Decision record check**

If significant architectural changes happened this session — detected by:
- New file in `docs/adr/` already? Skip.
- Was a new dependency added in `requirements.txt` / `package.json`?
- Was `CLAUDE.md` edited with structural changes?
- Was a new external API added to `project-status.yaml`?

If any: suggest `/decision-record <title>` for the change. List the suggested ADR titles. Don't auto-create.

---

**11. Clear build-mode permissions**

Check if `.claude/settings.local.json` exists and has `permissions.allow` entries (build-mode is ON). If so:
- Read the file
- Set `permissions.allow` to `[]`
- Write the file back (preserve other settings)
- Note in the summary: "Build mode cleared"

If build-mode was already off, skip silently.

---

**12. Confirm**

Print a one-paragraph summary:
- Tasks marked done / tasks added
- USER_ACTIONS.md entry added (date + feature name)
- CLAUDE.md: updated or unchanged
- project-status.yaml: updated / created / unchanged / skipped (no APIs)
- Worktrees: <count> active, <count> safe to clean
- LEARNINGS.md: added entry / skipped
- Postmortem suggested: yes (run /postmortem) / no
- ADR suggested: yes (titles: ...) / no
- Build mode: cleared or was already off
