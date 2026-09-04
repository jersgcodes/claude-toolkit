---
name: pre-approve
description: [CLI-only] Surface every tool use a build will need so they can be approved in one go, then hold those permissions for the build and clear them after. Modes: no argument runs the full analyse-approve-activate flow, `on` re-activates the last rule block, `off` restores prompt-for-everything, `status` reports what is active. Permissions are always written to the gitignored .claude/settings.local.json, never the shared settings.json.
allowed-tools: [Read, Glob, Grep, Write, Bash, Edit]
version: 0.2.0
---

Pre-approve a build session's tool calls, then hold those permissions for the duration of the build.

`$ARGUMENTS` selects the mode:

| Argument | Does |
|---|---|
| *(none)* | Full flow: analyse the planned work, emit permission rules, get approval, activate, build |
| `on` | Re-activate the most recent PERMISSION RULES block without re-analysing |
| `off` | Clear all permissions, restoring prompt-for-everything |
| `status` | Report which permissions are currently active |

**Permissions always go to `.claude/settings.local.json`** (gitignored, per-machine). Never write to `.claude/settings.json` — that file is shared and committed.

---

## Mode: `status`

Read `.claude/settings.local.json`. If `permissions.allow` has entries, list them and print "Build mode is ON with [N] rules." If it is empty or the file is missing, print "Build mode is OFF."

## Mode: `off`

Read `.claude/settings.local.json`, set `permissions.allow` to `[]`, preserve every other key, write it back. Print: "Build mode OFF — all build permissions cleared. Tool calls will prompt for approval again."

## Mode: `on`

Scan the conversation for the most recent `PERMISSION RULES` block. If there is none, stop and say: "No permission rules found. Run `/pre-approve` first to generate them." Otherwise apply them as in step 6 below.

---

## Full flow (no argument)

**1. Review the planned work**
Read `TASKS.md` and the current conversation to understand what is about to be built.

**2. List every tool action required**
Group by type:

- **File edits (Edit tool)** — each file path and briefly what will change
- **New files (Write tool)** — each file path to be created
- **Bash commands** — every shell command that will run (e.g. `npm test`, `mkdir -p`)
- **File reads (Read/Glob/Grep)** — low-risk; mention only if reading sensitive paths
- **External network (WebFetch/WebSearch)** — list if any fetches are planned

**3. Flag anything destructive or irreversible**
Highlight any command that deletes, overwrites without backup, or affects shared state (git push, DB mutations). Ask for explicit confirmation on those even if the user pre-approves the rest.

**4. Generate permission rules**
Cover EXACTLY what step 2 listed, nothing more, using the narrowest patterns:

- `Edit(/path/to/specific-file.js)` per file to be edited
- `Write(/path/to/specific-file.js)` per file to be created
- `Bash(npm test*)` per bash command pattern
- `**` only when a whole directory is genuinely involved, never as a blanket allow
- Never a bare `Edit`, `Write` or `Bash` with no path or command restriction

Output in a fenced block labelled `PERMISSION RULES`:

```
PERMISSION RULES
Edit(/src/data/tool-registry.js)
Write(/src/data/tool-capability-map.js)
Bash(npm test*)
Bash(npx eslint*)
```

**5. Ask for pre-approval**
Present the full list and the rules, then say:
> "Approve to activate build mode and start building, or reject to approve each tool call manually."

**6. On approval — build mode ON**
1. Read `.claude/settings.local.json` (create as `{"permissions":{"allow":[]}}` if missing)
2. Parse the PERMISSION RULES block into a string array
3. Merge into `permissions.allow`, preserving every other key — merge, do not overwrite
4. Print: "Build mode ON — [N] permission rules active. Local to this machine; `/pre-approve off` when done."
5. Start building immediately, no further user action

**7. Build with minimal interruptions**
Work through the tasks in order. Collect blockers and unexpected errors into an end-of-build summary rather than interrupting.

**8. On build complete — build mode OFF**
1. Run `/wrap-up` to update TASKS.md, USER_ACTIONS.md and CLAUDE.md
2. Set `permissions.allow` to `[]` — build mode OFF
3. Print a final summary: what was built, what failed, what needs user action

```
/pre-approve → approve → build mode ON → build → /wrap-up → build mode OFF
```

One approval, zero manual steps after. Always show the user exactly which permissions are being set before writing them.
