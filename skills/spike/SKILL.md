---
name: spike
description: Time-boxed exploratory spike (Pragmatic Programmer's tracer bullet). Builds a throwaway prototype to LEARN before committing to a build. Outputs lessons, not production code.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch]
version: 0.1.0
---



# Spike

A spike is a **time-boxed experiment to answer a specific question** before you commit to a build. The output is *learning*, not production code. Different from `/feature-design` (which assumes you know what to build) and from a normal feature branch (which assumes you'll merge it).

Inspired by *The Pragmatic Programmer*'s "tracer bullets" and Extreme Programming's "spike solution."

---

## When to spike vs. when to feature-design

| Situation | Use |
|---|---|
| "Can this library do X?" | Spike — build the smallest thing that proves yes/no |
| "Will this approach scale?" | Spike — measure with real data |
| "Should I use Postgres or DuckDB for this?" | Spike — build both, compare |
| "I know what to build, just need a plan" | `/feature-design` |
| "How do I solve this bug?" | Just fix it, no spike needed |

**Rule of thumb:** if you can answer the question by reading docs in 15 min, don't spike. If you need to write code to find out, spike it.

---

## Stage 1 — Frame the spike

Ask the user (or extract from `$ARGUMENTS`):

1. **What question are you trying to answer?** (must be answerable yes/no or with a measurement)
2. **What's the time budget?** (default: 2 hours. If > 4 hours, this is probably a real feature — use `/feature-design`)
3. **What's the success criteria?** (specific: "p95 latency < 200ms", "library handles 10k records without OOM")
4. **What does success unlock?** (so you remember why you did this)
5. **What does failure tell you?** (the spike is valuable either way)

If user can't answer #1 in one sentence, the question is too vague — refine it first.

---

## Stage 2 — Build the smallest possible test

Critical principles for spike code:

- **No tests.** Spike code is throwaway. Skip TDD, skip coverage. The whole point is speed.
- **No production-quality.** Hardcoded paths, plaintext secrets in env, no error handling. **Don't commit to main.**
- **Use a worktree.** Run `/worktree spike-<question>` to isolate. When done, the spike branch gets deleted.
- **One file if possible.** Resist the urge to "structure it properly."
- **Fastest path to the answer.** If the library docs have an example, copy it. If a Stack Overflow answer is close, paste and tweak.

The spike is allowed to be ugly. That's the point.

---

## Stage 3 — Run the experiment

Execute the spike code. Capture:

1. **Did it answer the question?** (yes/no)
2. **What was the measured value?** (if applicable: latency, memory, accuracy)
3. **What surprised you?** (the most valuable spike output)
4. **What broke?** (failure modes you didn't expect)
5. **What was harder than expected? Easier?**

If the spike crashes mid-way, that's a result too — record what blew up.

---

## Stage 4 — Write the spike report

Save to `docs/spikes/YYYY-MM-DD-<short-name>.md` (create directory if needed):

```markdown
# Spike: <one-line question>

**Date:** YYYY-MM-DD
**Time budget:** Xh    **Time spent:** Xh
**Status:** Conclusive | Inconclusive | Abandoned

## Question
<the specific question this spike answered>

## Approach
<one paragraph: what was built, what tools/libraries used>

## Result
**Answer:** <yes/no/measurement>

## Surprises
- <thing 1 you didn't expect>
- <thing 2>

## Failure modes
- <case where it broke>

## Recommendation
- <"yes, build this" / "no, abandon" / "yes, but with these constraints">

## What to keep, what to throw away
**Keep (port to real code):**
- <small useful function or pattern>

**Throw away (do NOT port):**
- <hacky workarounds, hardcoded values>

## Code reference
Spike branch: `feature/spike-<name>`
Worktree: `~/claude/.worktrees/<project>-spike-<name>/`
Main file: `<path>`
```

---

## Stage 5 — Decide what's next

Based on the result:

| Result | Next step |
|---|---|
| **Conclusive YES** | Run `/feature-design` to plan the real build, citing this spike. Then `/decision-record` to capture the "why" |
| **Conclusive NO** | Document the dead-end. Future-you will thank present-you when tempted to retry |
| **Inconclusive** | Either extend the time budget once (max 2x) or accept "we don't know" and move on |
| **Abandoned** | Capture why — usually the question was wrong or premature |

---

## Stage 6 — Clean up

a) Run `/worktree clean` — remove the spike worktree if not already deleted.
b) Optionally tag the commit on the spike branch with `spike-archive/<name>` so it's findable later, then delete the branch.
c) If any small useful piece deserves to survive, port it cleanly to a real feature branch (with tests this time).

---

## Anti-patterns

- **Spike that becomes production** — happens when "this is working, why not just merge?" Resist. Spike code lacks tests, error handling, and review. Always rebuild cleanly. *The Pragmatic Programmer*: "tracer bullets are not throwaway prototypes — but they're not production either; they evolve."
- **Spike with no time box** — becomes a feature build without a plan. Set the budget upfront.
- **Spike that doesn't answer the question** — ran out of time, accumulated state, but never measured the thing you were spiking. Re-frame and try again, or abandon.
- **Skipping the report** — the value of the spike is the *learning*. If it's not written down, it's lost.

---

## Cost control

- Default model: `sonnet` (fast for exploratory code)
- For research-heavy spikes (reading multiple docs/articles), use `Explore` agent for the research phase, then return to main session for code
- Cap reading external docs at 3 sources before writing code — if you need more, the question may be too broad

---

## Integration

- Pulls from: `/feature-design` (when planning surfaces unknowns)
- Hands off to: `/feature-design` (after a successful spike, plan the real build), `/decision-record` (capture the lesson), `/worktree clean` (delete spike branch)
- Related: `/explain` if you want to write up the spike for sharing/teaching content
