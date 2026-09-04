---
name: compact-context
description: Use when context is getting full, before /clear, or to save a handoff summary. Writes the handoff to .claude/handoff.md as well as printing it. Triggers on "compact context", "save handoff", "context full", "summarise session".
allowed-tools: [Read, Bash, Write]
version: 0.2.0
---



Manage the Claude Code context window by summarising what matters and preparing a clean handoff. Do the following steps in order:

**1. Estimate context usage**
Estimate how full the context window is based on conversation length and any large files read this session. Use this to decide the action:

| Usage estimate | Recommended action |
|---|---|
| < 50% | Note it, no action needed unless user asked |
| 50–70% | Run `/compact` in-place to compress, then continue |
| 70–85% | Run `/compact`, save handoff notes, advise user to `/clear` soon |
| > 85% | Save handoff notes immediately, tell user to `/clear` now |

Default trigger threshold: **70%**. If the current task involves large files, deep context, or multi-step work in progress, treat the threshold as 60% instead.

**2. Summarise current work**
Write a concise summary of:
- What was being worked on in this session (task, file, goal)
- What was completed
- What is still in progress or blocked
- Any decisions made that aren't yet reflected in code or docs

**3. Check memory**
Check if any of the following should be saved to memory before context is cleared:
- New project decisions or context not already in CLAUDE.md or docs/
- User preferences or feedback that changed how you worked
- Any reference pointers (external systems, URLs, IDs) that will be needed again

Save any new memories to the project memory folder following the memory format (frontmatter with name, description, type), then update MEMORY.md index.

**4. Write the handoff to disk, then print it**

Never print the handoff without also writing it. A handoff that only exists in the
terminal is lost the moment the user forgets to copy it, and that is the failure this
step exists to prevent.

*4a. Resolve the target.* Write to `.claude/handoff.md` **relative to the repo root**:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

A git worktree has its own root, so each worktree gets its own handoff with no naming
scheme needed. Do not try to make the filename worktree-aware.

*4b. Keep one generation.* If `$ROOT/.claude/handoff.md` already exists, move it to
`$ROOT/.claude/handoff-prev.md` before writing. One generation back, no archive
directory. Anything older is recoverable from the session transcript in
`~/.claude/projects/<slug>/*.jsonl`.

*4c. Check it is ignored.* `.claude/` should be in `.gitignore`. If it is not, still
write the file, but tell the user in step 5 — a handoff contains session state and
should not be committed.

*4d. Write the file* with this shape:

```markdown
# Handoff — <project name>

**Written:** <YYYY-MM-DD HH:MM> · **Branch:** <branch> · **Commit:** <short sha>
**Worktree:** <root path>

## Paste this to start the next session

<the ready-to-paste prompt, in a fenced code block>

## Session summary

<the step-2 summary: completed / in progress / decisions not yet in code or docs>
```

The paste-block itself must include:
- Current branch and last commit
- What was in progress
- What to do next (the immediate next step)
- Any blockers or decisions needed

*4e. Print it too*, as a code block, so the user can copy it without opening the file.

**5. Final advice**
Tell the user clearly:
- Estimated context usage %
- Whether to `/compact` in-place, `/clear` now, or continue
- **The path to the handoff file just written**, so it can be found after `/clear`
- If clearing: confirm memories and handoff file are saved first
- If `.claude/` was not gitignored, say so
