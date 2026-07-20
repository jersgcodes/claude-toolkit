---
name: subagent-task
description: Orchestrate parallel subagents for a large task. Split → spawn N agents → synthesize. Use for bulk migrations, multi-project audits, parallel codebase exploration.
allowed-tools: [Read, Glob, Grep, Agent, TodoWrite]
version: 0.1.0
---



# Subagent Task

Standardizes the pattern of using parallel subagents to tackle one large task in less time and with less main-context pollution. Inspired by Superpowers' subagent-driven-development discipline.

The 3-phase pattern:
1. **SPLIT** — decompose the task into N independent subtasks
2. **SPAWN** — launch N subagents in parallel, each with focused scope
3. **SYNTHESIZE** — main agent reads subagent reports and produces a single output

When done right: main context stays clean, work happens in parallel, total time is roughly the longest single subtask not the sum.

---

## When to use

| Situation | Use? |
|---|---|
| Audit pattern across many projects (e.g. "check every project for X") | YES |
| Parallel research on multiple unrelated questions | YES |
| Migration that applies same pattern to many files | YES |
| Code review that touches many files | YES |
| Task where you'd otherwise read 20+ files in main context | YES |
| Sequential task with strong dependencies between steps | NO — use main context |
| Trivial task (< 5 file reads) | NO — overhead not worth it |
| Task that requires the user mid-stream | NO — subagents are autonomous |

---

## Stage 1 — Frame the task

Ask (or extract from `$ARGUMENTS`):

1. **What's the overall goal?** (One sentence.)
2. **Is the work parallelizable?** (Independent units, or sequential dependencies?)
3. **How many subtasks naturally fall out?** (Aim for 3-8 — too few wastes the pattern; too many overwhelms)
4. **What does each subtask produce?** (Concrete artifact: a file, a report, a finding list)
5. **How will you synthesize?** (Diff, merge, summary, decision matrix?)

If the work is sequential (step B depends on step A's result), do NOT use this pattern. Subagents shine on **embarrassingly parallel** problems.

---

## Stage 2 — Split into focused subtasks

Decompose the work. Each subtask MUST be:

- **Self-contained** — runs without needing other subtasks' results
- **Bounded** — limited file reads, clear stopping point
- **Specific** — narrow enough to fit comfortably in a subagent's context
- **Verifiable** — main agent can tell if the output is right

Bad split (too vague):
- "Audit project X"
- "Audit project Y"

Good split (specific):
- "In project X, find all files importing `anthropic` and list each call site with file:line and the model name used"
- "In project Y, find all files importing `anthropic` and list each call site with file:line and the model name used"

Document the split as a list before spawning:

```
SPLIT PLAN — <overall task>
1. <subtask description> → produces <artifact>
2. <subtask description> → produces <artifact>
3. ...
```

---

## Stage 3 — Pick the right subagent type per subtask

See CLAUDE.md §Agent usage for the agent selection rules. Run `/agents` for the full type list.

---

## Stage 4 — Spawn in parallel

Send ALL subagents in a SINGLE message with multiple Agent tool calls. The harness runs them concurrently.

Critical rules for the spawn:

- **Self-contained prompt per subagent** — subagent has no memory of your conversation. Brief like a new colleague.
- **Specify scope breadth** for Explore agents (`quick`, `medium`, `very thorough`).
- **Tell subagent the artifact shape** — what to return, in what format.
- **Cap output length** if you don't need long prose ("report under 200 words").
- **Don't ask subagents to make decisions** that affect other subagents — that's main-agent's job in Stage 5.

Template prompt for a research subagent:
```
You are auditing one specific aspect of one specific project.

PROJECT: <path>
QUESTION: <specific question>
SCOPE: <which files / which patterns to look for>

Return a structured report:
- Findings: list of file:line + one-line description
- Counts: how many matches by type
- Surprises: anything unexpected

Cap response under 300 words.
```

---

## Stage 5 — Synthesize

When subagents return, MAIN agent (you, this conversation):

1. Read each report
2. Note any cross-cutting findings ("these 3 projects all use the same pattern")
3. Produce ONE unified output:
   - A merged report
   - A decision matrix
   - A prioritized backlog
   - Or whatever the original goal needed

The synthesis is where intelligence lives. Subagents do the gathering. Main agent does the *thinking*.

If a subagent failed or returned garbage:
- Don't re-spawn blindly — diagnose why (prompt too vague? scope too wide?)
- Re-spawn with corrected prompt if needed
- Or fall back to main-context execution for that subtask

---

## Stage 6 — Report

Print a one-paragraph summary: overall task, subtask counts (succeeded/partial/failed), key synthesized findings, and suggested next action.

---

## Cost control

- Each subagent has its own context — main context only sees the report
- Cap subagent count at 10 per spawn (>10 gets unwieldy to synthesize)
- For very large tasks, do multiple rounds: spawn 8, synthesize, decide, spawn next 8
- Use `Explore` (cheapest, fastest) when grep-and-report suffices
- Use specialized agents only when their tools genuinely help

---

## Anti-patterns to flag

- **Sequential disguised as parallel** — "subtask 2 needs subtask 1's output" → not actually parallel
- **Subagent making decisions** — main agent decides; subagents gather
- **Vague subagent prompts** — "audit project X" with no specifics → garbage in, garbage out
- **No synthesis step** — just dumping subagent outputs back to user is lazy
- **Reading subagent output as if it's main-context work** — defeats the purpose; main context bloats
- **Too many subagents (15+)** — synthesis becomes the bottleneck
- **Spawning subagents serially instead of in one message** — loses the parallelism gain

---

## Integration

- Pulls from: `/feature-design` (when a large task surfaces)
- Hands off to: depends on synthesis output — usually `/decision-record`, TASKS.md, or direct implementation
- Related: `/agents` lists available subagent types
- Pattern complement: `/spike` for exploratory single-track work; this for parallel multi-track work
