---
name: design-craft-check
description: Run the numeric craft checks (contrast, 4/8 spacing grid, type scale, colour literals) as PROGRAMS, then hand the judgement half to /design-review. The numeric floor is no longer a prompt.
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.2.0
---

**This skill used to describe the numeric checks in prose. They are programs now.**

That was the bug: six design checks existed, four were markdown, and none had ever run. The
page they guarded was 26% off its own spacing grid and the live contrast panel had been failing
14 of 16 rows since the day it was written. A prompt that restates a program is how you end up
with checks that never execute.

---

**0. Run the programs before you read anything**

Contrast, the 4/8 spacing grid, the type scale and colour-literal drift are **measured**, not
judged. There are programs for them; run those first and never re-derive by eye what a program
already reports with a number:

```bash
cd ~/claude/design-system/system
python3 check_contrast.py     # every pair, every theme, both modes -- tier 1, stdlib, <1s
python3 check_system.py       # component contract: no raw hex, radius roles only
python3 check_consumers.py    # consumer drift: colour literals, off-grid spacing, off-scale type
python3 check_rendered.py     # tier 2: measured in a real browser. Needs Chrome, ~17s
```

Report their output verbatim. Anything they cover is settled; your job starts where they stop.
If a program cannot run, say so and stop -- an unrun check reports clean forever, which is the
failure this preamble exists to prevent.

---

**1. Then hand over**

Everything the programs do not cover -- emoji as icons, placeholder copy, flat hierarchy, generic
gradient heroes, centred-hero sameness, whether the thing has a point of view -- is judgement, and
belongs to **`/design-review`**, which renders the target in a browser and scores it against
CRAFT-BAR's eight dimensions.

Run `/design-review` on the same target and report both together: the programs' numbers first,
then the judgement. Numbers settle what they can; the review starts where they stop.

---

**Why this skill still exists**

Roughly seventy files reference `/design-craft-check` -- CLAUDE.md, CRAFT-BAR.md, four surface
READMEs, other skills. Keeping the name as a shim collapses the content without leaving every one
of those references dangling.
