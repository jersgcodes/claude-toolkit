---
name: decision-record
description: Capture an Architecture Decision Record (ADR) for a significant decision — context, options considered, decision, consequences. Lives in docs/adr/.
allowed-tools: [Read, Write, Edit, Glob, Bash]
version: 0.1.0
---



# Decision Record (ADR)

Architecture Decision Records capture *why* you made a choice — not just what you did. Future-you (or a teammate / a learner reading your project) reads the ADR to understand the constraints and trade-offs that led to the current code.

Based on Michael Nygard's ADR template (ThoughtWorks Technology Radar, 2011), still the de-facto standard.

---

## When to write an ADR

| Trigger | Write ADR? |
|---|---|
| Picked a database (Postgres vs SQLite vs DuckDB) | YES |
| Picked an architecture pattern (monolith vs microservices) | YES |
| Picked a deploy target (VPS vs Vercel vs Railway) | YES |
| Picked a library where alternatives existed | YES if non-trivial |
| Reversed an earlier decision (e.g. "we removed Redis") | YES — reverse-ADR |
| Renamed a function | NO — too small |
| Added a feature | NO — that's `/feature-design` |
| Fixed a bug | NO — that's a commit message + maybe `/postmortem` |

**Rule of thumb:** if you'd struggle to answer "why did we do this?" 6 months later, write an ADR.

---

## Stage 1 — Determine the decision

From `$ARGUMENTS` or ask the user:
- What's the decision? (short title, e.g. "Use Coolify on Hetzner instead of Railway")
- Is this a new decision, or are you reversing/superseding an existing one?

If reversing, locate the existing ADR (`grep -r "<old decision>" docs/adr/`) and reference its number.

---

## Stage 2 — Determine the next ADR number

Check `docs/adr/` directory:

```bash
mkdir -p docs/adr
ls docs/adr/*.md 2>/dev/null | grep -oE "[0-9]{4}" | sort -n | tail -1
```

Next number = max + 1, zero-padded to 4 digits. If empty: start at `0001`.

---

## Stage 3 — Gather context

Before writing, gather:

1. **What problem are we solving?** (the forcing function — why now?)
2. **What constraints apply?** (cost, time, existing stack, team size)
3. **What options did you consider?** (at least 2; ideally 3+)
4. **For each option:**
   - Pros (what it does well)
   - Cons (what it does poorly)
   - Cost (effort to implement, ongoing cost to maintain)
5. **What did you decide?** (the chosen option)
6. **Why this option over the others?** (the key trade-off)
7. **What are the consequences?** (positive AND negative — be honest about the downsides you're accepting)
8. **What does this NOT decide?** (often forgotten — scope clarification)

Don't invent answers. If you don't know an option's cons, write "unknown" rather than fabricating.

---

## Stage 4 — Write the ADR

Save to `docs/adr/NNNN-<kebab-case-title>.md`:

```markdown
# ADR-NNNN: <Title>

**Status:** Accepted
**Date:** YYYY-MM-DD
**Deciders:** <user name>
**Supersedes:** <ADR-XXXX, if reversing — else omit>

## Context

<2-3 sentences: the situation that forced this decision. Include relevant constraints (budget, deadline, existing tech, team skills). What problem are you solving?>

## Decision Drivers

- <constraint 1, e.g. "must run within $25/mo budget">
- <constraint 2, e.g. "deploy via git push, no manual steps">
- <constraint 3, e.g. "must support websockets for realtime features">

## Options Considered

### Option A — <name>

**Pros:**
- <specific benefit>

**Cons:**
- <specific drawback>

**Cost:**
- Setup: <hours/days>
- Ongoing: <monthly $ or ops time>

### Option B — <name>

**Pros:**
- <...>

**Cons:**
- <...>

**Cost:**
- <...>

### Option C — <name>

<...>

## Decision

We chose **Option <X>** because <one-sentence key reason>.

## Consequences

**Positive:**
- <what we gain>
- <...>

**Negative (accepted trade-offs):**
- <what we give up — be honest>
- <ongoing maintenance burden>
- <vendor lock-in / portability concerns>

**Neutral:**
- <changes that aren't strictly better or worse>

## What This Does NOT Decide

- <related question deliberately left open>
- <future decision deferred>

## Related

- ADR-XXXX (if related)
- Spike: docs/spikes/<file> (if a spike informed this)
- Issue: <github issue if any>

## Revisit Conditions

We should revisit this decision if:
- <condition that would change the calculus, e.g. "monthly cost exceeds $50">
- <e.g. "we add a 4th service that needs the same infra">
```

---

## Stage 5 — Status lifecycle

ADR statuses:
- **Proposed** — under discussion, not yet acted on
- **Accepted** — decision made, in effect
- **Deprecated** — no longer recommended, but still in use somewhere
- **Superseded by ADR-XXXX** — replaced by a newer decision

When superseding, update the OLD ADR's status to `Superseded by ADR-NNNN` and reference the new one.

Never delete ADRs. They're a historical record.

---

## Stage 6 — Confirm

Print:
```
ADR created: docs/adr/NNNN-<title>.md
Status: Accepted
Decision: <one-line summary>

If you want to share or teach from this decision, reference it directly.
Future related changes should reference this ADR number.
```

---

## How this hooks into other skills

**`/feature-design` should suggest writing an ADR when:**
- Stage 3 (Lock Decisions) produces a decision with downstream consequences
- A decision involves picking a library, framework, or service from > 1 alternative
- A decision involves architecture (monolith/services, sync/async, where data lives)

**`/wrap-up` should remind you to write an ADR when:**
- CLAUDE.md was edited (architecture-level change)
- A new dependency was added in package.json / requirements.txt
- A new external API was added to project-status.yaml

**`/postmortem` should reference relevant ADRs when:**
- An incident traces back to a decision documented in an ADR
- The postmortem may trigger a new ADR (reverse decision)

---

## Cost control

- ADRs are short — 200-400 words each. Don't bloat.
- Don't write ADRs for trivial decisions (premature documentation = noise).
- For your projects: aim for 3-8 ADRs per project total. If you have 20 ADRs, you're recording too much.

---

## For your teaching/sharing project

ADRs are excellent teaching content — they show *thinking*, not just *outcome*. When sharing a project:
- Link to the ADR folder
- Highlight 2-3 ADRs that illustrate non-obvious trade-offs
- Use them to demonstrate "here's how I reasoned about X"

Newcomers learn more from "why we picked this" than from the resulting code.
