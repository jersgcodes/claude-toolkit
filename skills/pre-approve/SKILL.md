---
name: pre-approve
description: [CLI-only] Before starting a build session, surface all tool uses and permissions needed so the user can pre-approve them in one go.
version: 0.1.0
---


Before starting a build session, surface all tool uses and permissions needed so the user can pre-approve them in one go.

Do the following steps in order:

**1. Review the planned work**
Read TASKS_CURRENT.md (or equivalent) and the current conversation to understand what is about to be built.

**2. List every tool action required**
Group by type:

- **File edits (Edit tool)** — list each file path and briefly what will change
- **New files (Write tool)** — list each file path to be created
- **Bash commands** — list every shell command that will be run (e.g. `npm test`, `mkdir -p`, `npm run build`)
- **File reads (Read/Glob/Grep)** — these are low-risk; mention only if reading sensitive paths
- **External network (WebFetch/WebSearch)** — list if any fetches are planned

**3. Flag anything destructive or irreversible**
Highlight any command that deletes, overwrites without backup, or affects shared state (git push, DB mutations, etc.). Ask for explicit confirmation on those even if the user pre-approves the rest.

**4. Generate permission rules**
Based on the tool actions listed above, generate a `permissions.allow` block that covers EXACTLY what was listed — nothing more. Use the narrowest possible patterns:

- `Edit(/path/to/specific-file.js)` for each file to be edited
- `Write(/path/to/specific-file.js)` for each file to be created
- `Bash(npm test*)` for each bash command pattern
- Use `**` only when a directory of files is involved, never as a blanket allow

Output the block in a fenced code block labelled `PERMISSION RULES`:

```
PERMISSION RULES
Edit(/src/data/tool-registry.js)
Write(/src/data/tool-registry.js)
Write(/src/data/tool-capability-map.js)
Bash(npm test*)
Bash(npx eslint*)
Bash(npx prettier*)
Bash(node -e*)
```

**5. Ask for pre-approval**
Present the full list and permission rules, then say:
> "Approve to activate build mode and start building, or reject to approve each tool call manually."

**6. On approval — build mode ON**
When the user approves (says "approve", "yes", "go ahead", etc.):
1. Read `.claude/settings.local.json` (create with `{"permissions":{"allow":[]}}` if missing)
2. Parse the PERMISSION RULES block from step 4 into a string array
3. Write them into `permissions.allow` in `.claude/settings.local.json` (preserve other keys)
4. Print: "Build mode ON — [N] permission rules active."
5. Immediately start building — no further user action needed

**7. Build with minimal interruptions**
Proceed through all tasks in order. Surface blockers or unexpected errors in a summary at the end rather than interrupting mid-build.

**8. On build complete — build mode OFF**
When all pre-approved tasks are done (or blocked with errors):
1. Run `/wrap-up` to update TASKS.md, USER_ACTIONS.md, and CLAUDE.md
2. Set `permissions.allow` to `[]` in `.claude/settings.local.json` — build mode OFF
3. Print a final summary: what was built, what failed, what needs user action

Full flow:
```
/pre-approve → user approves → build mode ON → build runs → /wrap-up → build mode OFF
```
One approval, zero manual steps after.
