---
name: strategize
description: Retrieval-backed strategic brainstorm: pull what the workspace already knows about the question, explore it across several lenses, then land one clear recommendation rather than a menu of options. Use for a strategic question, a decision that keeps getting re-derived, or a brainstorm that should start from prior work rather than a blank slate.
allowed-tools: [Read, Glob, Grep, Bash]
version: 0.1.0
---

# Strategize

A structured thinking-partner pass for a strategic question, decision, or brainstorm. Reason
from what the workspace **already knows** — not a blank slate — then land a clear recommendation.
Lean by default (single context, no multi-agent fan-out) unless the user explicitly asks to go
wide.

## Stage 1 — Retrieve first (don't brainstorm from nothing)

Before reasoning, gather what already exists on this topic:
1. `KNOWLEDGE_INDEX.md` — corpora / docs relevant to the question.
2. `python3 scripts/find-past-chats.py <key terms>` — past conversations that touched this.
3. Grep the relevant repo(s) for prior work, decisions, or data.

Summarise in 3–5 bullets what we already know / have decided / have data on. If the search comes
up empty, say so explicitly — don't fill the gap with assumption.

## Stage 2 — Explore across lenses

Reason through several explicit lenses — don't stop at the first take:
- **First-principles** — strip assumptions; what's actually true / required?
- **Contrarian / kill-it** — what would make this fail or be the wrong move?
- **Second-order** — downstream effects (cost, maintenance, lock-in, time, attention)?
- **Prior art / analogy** — who's solved this shape before; what did *we* learn last time (Stage 1)?
- **Cheapest viable path** — the good-enough version; what would we cut?

Keep each lens tight. Note where they **disagree** — the tension is the signal.

## Stage 3 — Land it

- **Recommendation** — the one path you'd take, and the single most important next action.
- **Honest trade-off** — what it costs / gives up.
- **Open questions** — what only the user can decide, or what needs verifying before committing.
- **What would change the recommendation** — the key uncertainty to watch.

Be candid (see "How to advise me" in the workspace `CLAUDE.md`): lead with the answer, no
padding, push back if the premise is shaky.
