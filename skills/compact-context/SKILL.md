---
name: compact-context
description: Use when context is getting full, before /clear, or to save a handoff summary. Triggers on "compact context", "save handoff", "context full", "summarise session".
allowed-tools: [Read, Bash, Write]
version: 0.1.0
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

**4. Surface a handoff prompt**
Print a ready-to-paste prompt the user can use to start the next session cleanly. It should include:
- Current branch and last commit
- What was in progress
- What to do next (the immediate next step)
- Any blockers or decisions needed

Format it as a code block so it's easy to copy.

**5. Final advice**
Tell the user clearly:
- Estimated context usage %
- Whether to `/compact` in-place, `/clear` now, or continue
- If clearing: confirm memories and handoff prompt are saved first
