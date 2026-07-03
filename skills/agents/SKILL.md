---
name: agents
description: [CLI-only] List all available Claude Code agent types and explain when to use each one.
version: 0.1.0
---


List all available Claude Code agent types and explain when to use each one. Do the following steps in order:

**1. Print the built-in agent catalogue**

These are the agent types available via the `Agent` tool (subagent_type parameter):

---
**Built-in Claude Code Agents:**

| Agent type | Best for | When NOT to use |
|---|---|---|
| `general-purpose` | Multi-step research, open-ended tasks, writing code across multiple files | Simple single-file reads or edits |
| `Explore` | Fast codebase exploration — finding files by pattern, searching keywords, answering "how does X work?" questions | Writing or editing files |
| `Plan` | Designing implementation strategies before coding — returns step-by-step plans, identifies files, trade-offs | Executing code (it can't write files) |
| `claude-code-guide` | Questions about Claude Code CLI, Claude API, Anthropic SDK, MCP servers, hooks, settings | General coding questions |
| `statusline-setup` | Configuring the Claude Code status line | Anything else |

---

**2. List project-specific custom skills**

Run the `/skills` command (or list files in `~/.claude/commands/`) to show all slash-command skills available for this project.

**3. Explain when to use agents vs direct tools**

Use an **agent** when:
- The task requires more than 3-4 tool calls (searching + reading + editing multiple files)
- Work can be done independently of current context (e.g. auditing a content pack while you write tests)
- You want to parallelise: send two agents in parallel for two independent sub-tasks
- The task is exploratory and may require multiple rounds of grep/glob

Use **direct tools** (Read, Grep, Glob, Edit) when:
- You know exactly which file to read or edit
- The task is a single focused operation
- You need the result immediately to inform the next step

**4. Parallelisation patterns**

Common patterns where multiple agents should be launched simultaneously:

```
# Content + tests in parallel
Agent(Explore): "audit content packs for duplicates"
Agent(general-purpose): "write tests for round engine"

# Research + plan in parallel
Agent(Explore): "find all socket event names"
Agent(Plan): "design the new game scaffold"

# Multiple audits in parallel
Agent(socket-audit skill): game A handlers
Agent(content-audit skill): game A content pack
```

**5. Print a quick-reference card**

---
**Quick Reference — Which agent for which task?**

| Task | Use |
|---|---|
| "Where is X defined?" | Explore (quick) |
| "How does feature Y work across multiple files?" | Explore (thorough) |
| "Write tests for module Z" | general-purpose |
| "Plan how to refactor the auth system" | Plan |
| "How do I configure MCP servers?" | claude-code-guide |
| "Audit all content packs" | /content-audit skill |
| "Audit socket handlers" | /socket-audit skill |
| "Review code architecture and suggest splits" | /arch-review skill |
| "Run type-check and lint at the same time" | Two Bash tool calls in parallel |
| "Write game A tests AND game B tests" | Two general-purpose agents in parallel |

---

Keep it concise. This is a reference card, not a tutorial.
