---
name: arch-lesson
description: Teach one system-design / architecture concept at a time, grounded in the user's real repos, with a concrete exercise. A recurring learning loop — tracks progress so it advances instead of repeating. Distinct from /arch-review (which audits a codebase); this teaches.
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.1.0
---

Deliver ONE architecture lesson, grounded in the user's real code. Teach-then-apply,
not abstract theory. Keep each lesson ~5–8 min to read. Do the steps in order.

---

**1. Load state**

- **Pick the track.** Six tracks share this engine. Curricula and their reference files live in the
  user's private knowledge dir (`knowledge-base/arch-loop/` + `knowledge-base/arch-loop/references/`);
  read them at lesson time — this engine hardcodes no infra details, it grounds from the user's files.
  - default / `--track foundations` → `curriculum.md` (vendor-neutral principles, 24 topics).
  - `--track solution` → `solution-arch-curriculum.md` (platform/tools selection, cert-aligned,
    11 topics). Also read `references/platform-map.md` and `references/certs.md`.
  - `--track agent` → `agent-arch-curriculum.md` (AI/agent architecture, 10 topics). Also read
    `references/agent-arch.md`. Ground in the user's Claude Agent SDK usage, MCP servers, and
    Workflow/subagent patterns; lean on the reference's honest hype-vs-substance skip-list.
  - `--track networking` → `networking-curriculum.md` (how packets move, 11 topics). Also read
    `references/networking.md`. Ground in the user's real edge from their `DEPLOYMENT.md` (CDN →
    VPS → reverse proxy → containers, their DNS + TLS) — read it; don't assume a topology.
  - `--track cybersecurity` → `cybersecurity-curriculum.md` (attack/defense, 13 topics). Also read
    `references/cybersecurity.md`. Ground in the user's real attack surface from their own docs
    (their MCP auth model, executor, tool descriptions) and map each class onto their existing
    `/security-check` / `/secrets-scan` / `/threat-model` / `/deps-audit` (name what those miss).
    Defensive framing only.
  - `--track devops` → `devops-curriculum.md` (ship & operate, 13 topics). Also read
    `references/devops.md`. Ground in the user's real infra from their `DEPLOYMENT.md` + CI configs
    (their containers, reverse proxy, service manager, pipelines) — read them; don't assume.
- Read the chosen curriculum, plus `lessons-log.md` and `PRACTICES.md` (all in `knowledge-base/arch-loop/`).
- Topic selection: (a) a topic named in the invocation wins; (b) `--place` → step 1a;
  (c) else the **first unchecked** topic in the chosen curriculum.
- Report: "Lesson <id>: <topic> — <track>, <tier/domain>, X of Y".

**1a. Level placement (only on `--place`, or first-ever run)**

Don't assume novice. Skim 2–3 of the user's real repos (`ARCHITECTURE_OVERVIEW.md` +
grep a project) and judge which rungs their code already demonstrates. Recommend a
starting tier and mark clearly-mastered lower rungs as `[x]` with a one-line "already
evidenced in <file>" note in the log — judge the level from their actual code, not a default.

---

**2. Spaced review + real-world hook**

- **Spaced review:** if `lessons-log.md` has past lessons, pick the oldest one not yet
  marked reviewed and open with a one-line check: "Last time — <topic>. Did you do the
  exercise / apply P<n>?" Record the answer (append `- reviewed: <YYYY-MM-DD> — <applied? note>`
  to that lesson). One review per session; skip if nothing is due.
- **Hook:** if the user keeps an idea/signal backlog, grep it for an `architecture`-themed entry
  related to today's topic and open with it as a one-liner if one fits. Skip silently otherwise.

---

**3. Teach the concept (tight)**

In plain language: **what it is** (2–3 sentences) · **why it matters** (the failure it
prevents) · **the core trade-off** (name what the choice costs) · **the common mistake**.
Then two concrete anchors — this is where it sticks:
- **Worked example (the good):** a real snippet/decision from the user's own code that does
  this well — cite `file_path:line`.
- **Anti-pattern (the trap):** the recognizable wrong version, ideally spotted in the wild or
  in an earlier state of their own code (e.g. a duplicated module that later drifted).
Close the teach with a one-line **canon pointer** from `references/canon.md` for the topic
("Go deeper: <source>") — don't lecture the source, just name it.

---

**4. Ground it in the user's real repos — incl. their own ADRs**

- Read `ARCHITECTURE_OVERVIEW.md` for the cross-project map.
- **Mine their ADRs/docs as case studies:** `Glob` for `**/docs/adr/*.md` and the canonical
  docs in the overview table; if one of their real decisions embodies today's concept, teach
  *from that decision* — what they chose, what they traded, what it would've cost to choose otherwise.
- Use `Grep`/`Glob` to show where the concept **appears** (`file:line`) or is **absent**.
- Reference their real projects by name and the concrete dependency between them (a shared library
  and its consumers, an MCP server, their deploy). One strong tie-in beats three vague ones.

---

**5. One exercise + apply-back**

- Give a single concrete ~15–30 min thing to inspect/try in a real repo (not a big refactor).
- **Apply-back:** offer to open a matching task in that project's `TASKS.md` /
  `TASKS_CURRENT.md` (e.g. `- [ ] [arch] <exercise> (from Lesson N)`) so the learning drives
  a real repo improvement. Only write it on a yes. This exercise is what step 2's spaced
  review will check next time.

---

**Solution-track variant** (`--track solution`) — adapt steps 3–5:
- **Teach** around the *decision*, not a definition: name the **job-to-be-done** and the
  **selection axes** (scale profile · consistency need · ops burden · cost model · lock-in ·
  team familiarity · failure blast-radius). The "anti-pattern" is choosing the wrong tool
  class for the job (e.g. a queue where you needed a stream; NoSQL where you needed a join).
- **Platform map:** show the AWS / GCP / Azure options **and** the self-hosted equivalent from
  `references/platform-map.md`. Teach the portable model, not one vendor.
- **Cert lens:** one line on how the exams frame/weight this domain (from `references/certs.md`)
  — e.g. "SAA weights Security 30% — an SA is a security thinker first."
- **Grounded call:** tie it to a real choice in their stack (e.g. SQLite vs Postgres for a given
  service; which object store; private-network-only vs public exposure). The exercise is a real
  selection decision to write up ADR-style (job → axes → options → choice → what it trades).

---

**6. Log, bolster practices, and advance**

- Append the lesson entry to `knowledge-base/arch-loop/lessons-log.md`:
  ```
  ## Lesson N — <topic> — <YYYY-MM-DD>
  - **Concept:** <one line>   - **Grounded in:** <project / file:line>
  - **Exercise:** <the exercise>   - **Takeaway:** <the single thing to remember>
  ```
- **Bolster the handbook:** append one distilled, imperative rule to `PRACTICES.md`
  (next `P<n>`, under the right heading), with a *why* and a real workspace anchor.
- **Bolster real standards:** if the lesson exposed a genuine gap or repeated bug class,
  propose a one-line entry for the workspace `MISTAKES.md` (show it; don't write it without
  a nod) and/or a `CLAUDE.md` checklist line. Skip if nothing concrete surfaced — no filler.
- Check off the topic in `curriculum.md` (`[ ]` → `[x]`).
- Close: "Next up: <next topic> (Tier <t>). New practice logged: P<n>. Run `/arch-lesson` again."

---

Notes:
- If `curriculum.md` / `lessons-log.md` don't exist, create them (curriculum seed is in
  `knowledge-base/arch-loop/`).
- The user can jump the queue: `/arch-lesson caching` teaches that topic regardless of order.
- Honesty over flattery — if their code already does something well, say so; if a concept
  genuinely doesn't apply to their workspace yet, say that and pick the next relevant one.
