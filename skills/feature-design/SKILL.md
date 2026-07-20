---
name: feature-design
description: Structured feature/build discussion — scope, architecture, decisions, then lock a plan before writing code
allowed-tools: [Read, Glob, Grep, TodoWrite]
version: 0.1.0
---



# Feature Design Discussion

Use this skill when you have a new feature, build, or significant change to think through before writing code. It structures the conversation into four stages: context, options, decisions, and a locked plan.

## Stage 1 — Understand the Context

Read any relevant existing files to understand current state before asking questions. Then ask:

1. What is the **goal** of this feature? What user problem does it solve?
2. Who uses it and in what context (personal tool, shared tool, production)?
3. What already exists that this connects to or replaces?
4. Are there any **hard constraints** (API limits, storage, hosting, budget, timeline)?

## Stage 2 — Map the Options

For each significant decision point, present 2–3 concrete options with honest trade-offs:

- Label each option (A / B / C)
- State the key trade-off in one line per option
- **Estimate cost/effort per option** (Pragmatic Programmer: "good-enough software"):
  - Build effort: hours/days to implement
  - Maintenance cost: monthly $ + ongoing ops time
  - Reversibility: easy / moderate / hard to change later
- Give a recommendation with a reason — explicitly weighing value vs. cost
- Do NOT ask the user to choose yet — present first, then ask

Format each option:
```
### Option A — <name>
**Trade-off:** <one-line summary>
**Cost:** Build ~Xh, maintain ~$Y/mo, reversibility: easy/moderate/hard
**Pros:** <2-3 specific benefits>
**Cons:** <2-3 specific drawbacks>
```

## Stage 3 — Lock Decisions

Go through each open decision and get explicit answers:

- Confirm or override each recommendation
- Note any decisions that have downstream consequences
- Flag anything that would need to change if a decision is reversed later

Once all decisions are confirmed, summarise them in a **Locked Decisions** block:

```
LOCKED DECISIONS
----------------
[Decision area]: [Choice made] — [one-line reason]
```

**Decision Record check:** for each locked decision, ask:
- Is this a significant architectural choice (library/framework/service/pattern)?
- Did we consider alternatives that someone might revisit later?
- Would future-you struggle to remember WHY in 6 months?

If yes to any — flag it as **ADR-worthy**. Print: "Suggest running `/decision-record <title>` after Stage 4 to capture: <list of ADR-worthy decisions>." 

Don't auto-create the ADR — the user invokes `/decision-record` separately. This keeps cost low and gives the user the choice.

## Stage 4 — Write the Plan

After locking decisions, produce:

1. **Feature spec** — what it does, what it does NOT do
2. **Implementation order** — sequenced steps, each independently deliverable
3. **Files to create / modify** — with brief reason for each
4. **Open questions** — anything still unclear that will need a decision during implementation
5. **Pre-implementation design skills** — before writing code, check if any apply:

   *Backend / contracts:*
   - 3+ new endpoints OR new bot command surface OR inter-service contract → `/api-design`
   - 2+ new tables OR significant schema restructuring → `/schema-design`
   - New service handling user data / external API credentials / public endpoint → `/threat-model`

   *Frontend / UI:*
   - New UI component with > 4 props OR user input OR remote data display → `/component-design`
   - New page/feature needing responsive layout across phone+desktop → `/responsive-design`
   - Anything shareable / public-facing → `/a11y-audit plan <feature>` at design time

   *Exploratory:*
   - "Can this approach work?" question with unknown answer → `/spike` first to learn before designing

6. **Implementation skill routing** — once design is locked, for each step:
   - New pure function (parser, validator, business rule) → `/tdd`
   - Modifying untested existing code → `/seams` first, then `/tdd` or direct
   - UI / styling / glue → direct implementation, no TDD
   - Long parallel work or experimental spike → `/worktree` for isolation

7. **Branch + worktree decision:**
   - Single feature, < 1 day work → feature branch (already standard)
   - Multi-day or experimental → suggest `/worktree <feature-name>` for isolation
   - Multiple parallel ideas → multiple worktrees, one per idea

Ask the user: "Ready to start building, or any changes to the plan?"

Do NOT write any code until the user confirms the plan.

## Arguments

If `$ARGUMENTS` is provided, treat it as the feature name or description and skip the initial "what are we building?" question — jump straight to Stage 1 context questions.
