---
name: hooks
description: [CLI-only] Show active Claude Code hooks and explain what each one does. Use when debugging hook behaviour, auditing automation, or after editing settings.json — "what hooks are active", "show my hooks".
allowed-tools: [Read, Bash]
version: 0.1.0
---



Show the current hooks configuration and explain what each hook does. Do the following steps in order:

**1. Read settings files**

Read these files in parallel:
- `~/.claude/settings.json` — global user hooks
- `.claude/settings.json` — project-level hooks (if it exists in the current working directory)
- `.claude/settings.local.json` — local project hooks (if it exists)

**2. Read hook scripts**

For each `"command"` value found in the hooks, if it points to a shell script file (e.g. `~/.claude/hooks/foo.sh`), read that file to understand what it actually does.

**3. Print a summary**

Format the output as:

```
## Active Hooks

### <Event> — <Matcher or "all">
- Command: <command value>
- Timeout: <Ns or "default">
- Source: <which settings file>
- What it does: <1-2 sentence plain-English description of what the script does>

... repeat for each hook ...
```

**4. Explain the hook events**

After listing all hooks, print a brief reference:

```
## Hook Event Reference

PreToolUse   — runs BEFORE a tool call; can block it (exit 2) or modify input
PostToolUse  — runs AFTER a successful tool call
Stop         — runs when Claude finishes a response turn
PreCompact   — runs before context is compacted
PostCompact  — runs after context is compacted
SessionStart — runs once when a session starts
UserPromptSubmit — runs when the user submits a message
```

Only list events that are actually relevant (i.e. used in this config or commonly useful).

**5. Offer next steps**

Remind the user they can:
- Add or edit hooks via `/update-config`
- View hook files directly at `~/.claude/hooks/`
- Use `PreToolUse` on `Bash` to guard commands, `Stop` for end-of-session actions
