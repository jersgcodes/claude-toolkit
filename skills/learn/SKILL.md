---
name: learn
description: Domain-agnostic learning engine. Teaches ONE concept per run as a mechanism (cause -> effect) with one worked example and one mandatory exercise, surfaces overdue reviews first, and logs a short fixed-format entry. Run `/learn <course> [topic]`. Courses live in `knowledge-base/learning/`. Generalizes the /arch-lesson pattern to any subject.
allowed-tools: [Read, Write, Edit, Grep, Glob, WebSearch, WebFetch]
version: 0.2.0
---

One concept per run, taught as a mechanism, checked by an exercise the learner actually does.
Short beats thorough: a lesson the learner sits through and retains one mechanism from is a
success; a long one they stop opening is not. Steps in order.

**Why these rules** (from the 2026-09 logs, where lessons stopped being used): entries ran
60-120 lines of tutor notes; the learner kept prescriptions ("do X") but no mechanisms ("X
because Y"); exercises were required and never logged; groundings sat in repos untouched for
months; reviews fell due and never ran.

---

**1. Load the course**

Read `knowledge-base/learning/<course>/course.yaml` (`grounding`, `goal`, `teaching_style`,
`fact_check`, `visibility`, optional `encyclopedia_dir`, resolved relative to the course dir;
default `<course>/encyclopedia/`), `curriculum.md`, `lessons-log.md`. Unknown course: list
`knowledge-base/learning/COURSES.md`. Honour `teaching_style` throughout.

**2. Overdue reviews first, every run**

Scan `lessons-log.md` for `review due:` (and legacy `next review:`) dates on or before today.
- If any are overdue, open with: "Overdue: <n> reviews. Oldest: <concept>, due <date>."
- Run the oldest one before teaching anything new: ask the learner to state its **mechanism**
  closed-book ("what causes what, and why?"). Wait. One line of feedback.
- Append to that entry: `- reviewed <date>: <mechanism recalled / prescription only / blank>`
  and set a new `review due:` (recalled: double the last gap; otherwise: 2 days).
- The learner may skip; log `- review skipped <date>` so it stays visible.

**3. Pick the topic and check the grounding**

A named topic wins, else the first unchecked curriculum item. Say: "Lesson <id>: <topic>."

The example must come from something the learner **uses or deals with now** (a repo touched this
week, their own money, their own job, a business they actually buy from). Not something chosen
because it illustrates well. If you are not sure they still use it, **ask before teaching**:
"I'd ground this in <X>. Do you still work with it?" A stale grounding decays faster than the
concept, and the review then tests the example instead of the idea.

**4. Teach: one mechanism, one worked example**

- **The mechanism, in one sentence**: cause -> effect. "Fixed costs don't change with volume, so
  each extra sale past break-even is mostly profit." Not a rule to follow; the reason the rule holds.
- Define each new term the first time it appears. No more than three new terms.
- **One worked example** in the grounding, with real numbers where the subject has them, shown
  step by step so the cause -> effect is visible. One example, not a survey.
- One line on the common misconception, if there is a well-known one.
- Keep it to a few short paragraphs. Stop there; do not add a quiz.

**5. Exercise (mandatory; the lesson is not done without it)**

One task the learner does now, in this session, that forces them to **use the mechanism**, not
recite it. Same shape as the worked example with something changed, e.g. different numbers
("price rises 10%, costs stay: what happens to break-even units?"), or a new case from their own
life to explain with the mechanism. Numeric subjects: ask for the number and one sentence on why.

Wait for the answer. Give short feedback: right/wrong, and the mechanism step they missed.
If the learner cannot do it now, the lesson stays **open**: log it with `exercise: pending`,
do not check off the curriculum item, and the next run asks for the answer before new material.

**6. Encyclopedia (only if the concept is new to it)**

Write or update `<encyclopedia_dir>/<slug>.md` from its `_TEMPLATE.md` and add it to `_index.md`.
If `fact_check: required`, label figures VERIFIED / ESTIMATE / UNVERIFIED and verify load-bearing
numbers with WebSearch/WebFetch first; never state an invented statistic as fact. Set
`visibility:` per the course policy (default private; `share-candidate` is opt-in). Depth,
sources and caveats go here, not in the log.

**7. Log (fixed format, at most ~25 lines)**

Append exactly this block to `lessons-log.md`. This format overrides any older format described
inside a course's log.

```
## <id> — <concept> — <YYYY-MM-DD>
- mechanism: <cause -> effect, one line>
- example: <the worked example, 1-3 lines, in the learner's grounding>
- exercise: <the task>
- answer: <what the learner actually said/produced, verbatim or close; or "pending">
- result: <correct / partly: missed <step> / wrong: <misconception>>
- encyclopedia: <slug or none>
- review due: <YYYY-MM-DD, 2 days out>
```

Only the learner's own output and what to re-test go in the log. **No tutor-method notes**
(how you taught, what to do differently, rules for future lessons). If a lesson teaches you
something about teaching, put it in the course's `README.md` or `course.yaml` notes, in one line.

Then check off the curriculum item (only if the exercise has an answer) and close:
"Done: <concept>. Review due <date>. Next: <topic>."

---

New course = a folder under `knowledge-base/learning/` with `course.yaml`, `curriculum.md`,
`lessons-log.md`, an encyclopedia, and a line in `COURSES.md`. `/arch-lesson` is the
architecture-specific sibling of this engine.
