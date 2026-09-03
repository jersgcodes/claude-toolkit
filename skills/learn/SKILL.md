---
name: learn
description: Domain-agnostic learning engine. Teaches ONE concept at a time from a course — a leveled curriculum + a fact-checked encyclopedia + Socratic guided Q&A + spaced review — grounded in that course's real-world anchor. Run `/learn <course> [topic]`. Courses live in `knowledge-base/learning/`. Generalizes the /arch-lesson pattern to any subject.
allowed-tools: [Read, Write, Edit, Grep, Glob, WebSearch, WebFetch]
version: 0.1.0
---

Teach one concept, well, from a course. This is a **general learning engine** — the subject,
grounding, teaching style, fact-check policy, and share/visibility rules all come from the course's
`course.yaml`, so the same engine drives any domain. Three layers per course, working together:
**Course** (leveled path) · **Encyclopedia** (fact-checked reference you build as you learn) ·
**Guided Q&A** (Socratic active recall + spaced review). Go at the course's stated pace. Steps in order.

---

**1. Load the course**

- `/learn <course> [topic]`. Read `knowledge-base/learning/<course>/course.yaml` (domain, `grounding`,
  `goal`, `teaching_style`, `fact_check`, `visibility`), plus `curriculum.md`, `lessons-log.md`, and
  the encyclopedia index.
- **Encyclopedia location.** Default `<course>/encyclopedia/`. If `course.yaml` sets
  `encyclopedia_dir:`, resolve it **relative to the course directory** and use that instead — this
  lets a course adopt an existing shared reference store rather than copying entries into itself.
  `signals` does exactly this, pointing at `knowledge-base/encyclopedia/`, because those 8 entries
  are already referenced from ten other files and moving them would break every one.
- If `<course>` is missing/unknown, read `knowledge-base/learning/COURSES.md` and list the options.
- Honour `teaching_style` for the whole session (e.g. "slow; define every term on first use").

**2. Spaced review** (only if prior lessons exist)

- Open with 1–2 active-recall questions on the oldest not-yet-reviewed concept from `lessons-log.md`
  ("Last time — <concept>. In your words, why does X matter?"). Wait for the answer, give brief
  feedback, and record `- reviewed <date>: <ok? / misconception noted>` on that lesson. One review per session.

**3. Pick the topic**

- A topic named in the invocation wins; else the first unchecked curriculum item.
- Report: "Lesson <id>: <topic> — <tier>, X of Y in <course>."

**4. Teach (at the course's pace)**

Plain language, define every new term on first use. Cover: **what it is** · **why it matters** ·
**the core trade-off** · **the common misconception**. Then ground it in a **real example from the
course's `grounding`** (e.g. for a materials course, a specific garment — a rain shell, a merino
layer, a denim jean; for architecture, a specific system). Teach the concept *before/while* using it;
never dump. Favor one vivid concrete example over generic description.

**5. Encyclopedia entry (build the reference as you learn)**

Write or update `<encyclopedia_dir>/<slug>.md` from that directory's `_TEMPLATE.md`
(falling back to the course's own template if the shared store has none).
- **Fact-check per `course.yaml`.** If `fact_check: required`, label every figure/claim
  **VERIFIED / ESTIMATE / UNVERIFIED**, and `WebSearch`/`WebFetch` to verify load-bearing numbers before
  writing them. Never state an invented statistic as fact. When unsure, mark UNVERIFIED and say so.
- Set the entry's `visibility:` per the course's `visibility` policy (default private; flag entries
  genuinely worth sharing as `share-candidate` — that's the growth/teaching feed, opt-in, not automatic).
- Add the entry to `<encyclopedia_dir>/_index.md`.

**6. Guided Q&A (does it stick)**

Ask 2–3 questions that test **understanding and application**, not trivia ("Given property X, why would
a designer pick fiber A over B for a running shoe?"). **Wait for the learner's answers.** Give Socratic
feedback — affirm what's right, correct gently, surface the misconception. Note anything to re-test in a
future review.

**7. Exercise (make it real)**

One concrete real-world task sized ~15–30 min, appropriate to the domain — e.g. "check the fibre-content
/ care label on a jacket you own and identify which property each material is doing." This is what step 2
reviews next time.

**8. Log & advance**

- Append to `lessons-log.md`:
  ```
  ## Lesson <id> — <topic> — <YYYY-MM-DD>
  - Concept: <one line>   - Grounded in: <real example>
  - Encyclopedia: <slug>  - Q&A: <what they got / missed>
  - Exercise: <task>      - Re-test next: <the thing to review>
  ```
- Check off the topic in `curriculum.md`; update `encyclopedia/_index.md`.
- Close: "Next: <topic> (<tier>). New entry: <slug>. Run `/learn <course>` again when ready."

---

Notes: this engine is the generalization of `/arch-lesson` (architecture's specialized version). New
courses = a new folder under `knowledge-base/learning/` with a `course.yaml` + `curriculum.md` +
`encyclopedia/` + `lessons-log.md`; register it in `COURSES.md`. Respect each course's fact-check and
visibility policy — accuracy and the private/shareable boundary are the whole point of an encyclopedia.
