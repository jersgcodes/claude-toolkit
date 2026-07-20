---
name: add-tasks
description: [CLI-only] Extract and write actionable tasks from the current conversation into TASKS_CURRENT.md — use when wrapping up a session, after a planning discussion, or when asked to capture next steps or to-dos.
allowed-tools: [Read, Write]
version: 0.1.0
---



Review the current conversation and extract actionable tasks into two categories: system/build tasks (things to code or configure) and user tasks (things the user needs to do or decide). Then write them to a TASKS_CURRENT.md file in the project root.

Do the following steps in order:

**1. Read context**
- Read the project's TASKS.md if it exists to understand the original task list
- Read memory files from the project memory directory if available
- Scan the recent conversation for decisions made, features discussed, issues raised, and things mentioned as "next steps"

**2. Extract tasks**

Identify two types:

**System/build tasks** — things that need to be coded, configured, or built. Examples:
- New pages or features to build
- Bugs or UX issues noted during conversation
- Data enrichment work
- Infrastructure or deployment tasks

**User tasks** — things the user needs to do, decide, or provide. Examples:
- Testing something and reporting back
- Providing research data or documents
- Making a product/design decision
- Accessing external systems (Railway, API keys, etc.)

**3. Write TASKS_CURRENT.md**

Write to `TASKS_CURRENT.md` in the project working directory with this format:

```markdown
# Current Tasks
_Last updated: <today's date>_

## System / Build Tasks

- [ ] <task> — <brief reason or context>
- [ ] <task> — <brief reason or context>

## User Tasks

- [ ] <task> — <brief reason or context>
- [ ] <task> — <brief reason or context>
```

Rules:
- Be specific — "Build Gaps & Opportunities page showing 51 gaps ranked by severity" not "improve gaps"
- Include the reason/context so future-Claude understands why
- Mark already-completed items with [x] if clearly done
- Keep it to genuinely actionable tasks — not observations or notes
- If TASKS_CURRENT.md already exists, update it (preserve completed items, add new ones, remove stale ones)

**4. Confirm**
Tell the user what was written and give a brief summary of the task counts.
