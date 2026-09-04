---
name: data-story-check
description: Audit a chart, dashboard or data page for STORYTELLING, not chart craft — does the title state the finding, is one claim per chart, is emphasis achieved by suppression, do annotations argue rather than label, is every number compared to something, is the framing honest about what the data cannot say, does the sequence build. Judges against design-system/data-story/STORY-BAR.md. Complements the `dataviz` skill (the craft floor: mark selection, palette, axes). Use after building any results page, report, deck or dashboard — and before sharing data with a stakeholder.
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.1.0
---

Audit whether a data surface **says something**, as opposed to merely showing data correctly.
Lanes:
- `dataviz` → chart craft (the FLOOR): mark for the data shape, palette, axes, legends, tooltips.
- `/data-story-check` (this) → the STORY CEILING: `design-system/data-story/STORY-BAR.md`, 8 dimensions.
- `/design-craft-check`, `/design-review` → the surrounding UI.

The failure this catches is not an ugly chart. It is a correct chart that leaves the reader to
work out the point alone — the most common outcome of "we have the data so we showed it".

Do the steps in order.

---

**1. Locate the surface and inventory every chart**

Find the data page(s): `.html`, notebook, deck, or component tree. For each chart, table and
stat tile, record: its title/caption, its heading, its annotations, and what it plots.

```bash
# HTML data pages — every chart label in document order
grep -oE '<h[2-4][^>]*>[^<]+|<caption>[^<]+' <page> | sed 's/<[^>]*>//'
```

**2. Dimension 1 — the finding, not the cut (do this first; it is usually the whole problem)**

Classify every label as **FINDING** (a sentence stating what the data says) or **CUT** (names
the axes, segments or population). Report the ratio. A page where most labels are CUT has no
story at the evidence level, however good its section headings are.

Rewrite every CUT label as a FINDING, using the actual numbers. Keep the old label as the
subtitle — it still carries the units and population, which the finding-title should not.

> Before: `Who responded · sector`
> After: `Retail and F&B answered; construction almost didn't` / sub: `Responses by sector, n=65`

Do not invent a finding. If the data does not support a sentence, say so — that chart may not
earn its place (see step 4).

**3. Dimensions 2, 4, 5 — claim, emphasis, annotation**

For each chart:
- **One claim?** State it in one sentence with no "and". If impossible, flag it to split.
- **Emphasis by suppression?** Is exactly one element visually promoted and the rest demoted?
  A full categorical palette with no highlight almost always means no claim was chosen.
  Recommend: one accent, everything else neutral grey.
- **Annotation as argument?** Does the highlighted mark carry *why it matters*, anchored to
  the mark, not just its value in a caption? Draft the missing annotation.

**4. Dimensions 3, 6, 7 — the grill**

Run the grill from STORY-BAR.md against each chart. In practice, ask and answer in writing:
- What question does this answer? (no question → candidate for cutting)
- Compared to what? (every bare number needs a baseline)
- What is missing / silent / non-responding, and is it drawn or silently dropped?
- Is the outlier a story or an error?
- What is the counter-read, and does the chart survive it?
- Is n and the denominator visible where they change the reading?

Flag any chart that answers no question and has no baseline as **cut candidate**. Removing
charts is a legitimate and usually the highest-value finding.

**5. Dimension 8 — sequence**

Write the one sentence the reader believes after each chart, in order. Then check:
- Do adjacent charts produce the same sentence? → cut one.
- Could the order be shuffled with no loss? → there is no argument, only an inventory.
- Does any chart appear before the reader has a reason to care? → move or cut.

**6. Report**

Output, in this order:

1. **Verdict** — inventory vs argument, in one line, with the FINDING/CUT ratio as evidence.
2. **The rewrite table** — every chart, current label → proposed finding-title + subtitle.
   This is the deliverable most of the time; it is cheap and it changes the page most.
3. **Cut candidates** — charts that answer no question, with the reason.
4. **Missing annotations** — drafted, per chart.
5. **Honesty gaps** — absent denominators, undrawn non-response, unstated counter-reads.
6. **Sequence** — the belief-per-chart list and any reorder.

Rank by what changes the reader's understanding most, not by how many rules were broken.
Rewriting eleven labels usually beats every other change combined.

**Do not** rebuild the charts unless asked. The finding is almost always in the words, the
emphasis and the ordering — not in the chart type.
