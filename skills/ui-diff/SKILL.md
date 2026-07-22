---
name: ui-diff
description: Measure how closely a built UI matches a real reference (a Figma frame or a product screenshot) and close the gap. Extracts ground-truth tokens, renders the target headless, composes side-by-side + close-up crops, lists the exact drift, and iterates until it is indistinguishable. The loop that stops UI feeling "AI-made".
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
version: 0.1.0
---

# UI Diff

Build UI *against* a reference instead of from memory. Guessing values off a screenshot always drifts (a purple that is `#6E2586` instead of `#702F8A`, a 12px radius instead of 16px), and the eye reads that drift as "AI-made" even when it cannot name it. This skill makes the drift **objective**: render, overlay, measure, fix, repeat.

Pairs with `/visual-mock` (which *creates* the mock) and `/design-review` (which audits craft). Use this one whenever a real reference exists.

---

## When to use

| Situation | Use? |
|---|---|
| You have a Figma frame or a screenshot of the real thing to match | YES |
| A stakeholder said "this looks nothing like the design" | YES |
| Replicating a known product's screen (the real SGDS page, Stripe, Linear) | YES |
| Net-new UI with no reference to match | NO — use `/visual-mock` + `/design-review` |

---

## Stage 1 — Frame the diff

Extract from `$ARGUMENTS` or ask:
1. **Target**: the built UI (a local HTML file, a dev URL, or a component route).
2. **Reference**: the image(s) to match. If it is a Figma node, get the file key + node id (a real render beats an export). Otherwise a screenshot.
3. **Key element**: the one repeated/dominant element that must be right (a card, a row, the primary button). The close-up of *this* is the real test, not the whole-page glance.
4. **Viewport**: the reference's width + scale (e.g. 1440 @2x).

---

## Stage 2 — Get ground-truth tokens (do not eyeball)

If the reference is Figma, pull the **per-element** values, not page-wide aggregates (aggregates lie: a page can be 80% 8px radius while the card is 16px). For each element capture: fills, strokes, corner radius, effects/shadows, auto-layout padding + gap, and text style (family, size, line-height, weight, letter-spacing). Also fetch a 2x PNG **render** of the frame as the diff target. See `references/ui-diff-ref.md` for the exact Figma API recipe (nodes + images endpoints, token extraction, rate-limit backoff).

If the reference is only a screenshot, sample key colours with a pipette and measure spacings against a known-width element; note these are approximate and lean harder on Stage 4.

Write the extracted values into (or reconcile against) `~/claude/design-tokens.yaml` so the next screen starts from truth, not guesses.

---

## Stage 3 — Render the target headless

Render the built UI at the reference's viewport and scale with headless Chrome (via puppeteer-core against the local Chrome binary). Capture `fullPage`, and report any JS errors. See the reference file for the driver snippet.

---

## Stage 4 — Compose and read the diff

1. **Side-by-side**: reference | mine, scaled to equal width. Catches structural gaps (missing nav, wrong section order).
2. **Close-up crop** of the key element from both, at high resolution, stacked. This is the decisive comparison.
3. Read both images and produce a **drift checklist**, most-visible first:
   - Colour: exact hex mismatches (fill, border, text).
   - Geometry: radius, padding, gap, element size.
   - Type: family, size, line-height, weight, letter-spacing.
   - Structure: elements present in one but not the other; wrong order.
   - States/detail: shadow, iconography, real-vs-placeholder content.

**The render is ground truth over the token dump.** A component's Figma node can contain an element (e.g. a rating row) that is hidden in the published frame. If the render does not show it, it comes out. Trust what renders.

---

## Stage 5 — Fix and repeat

Apply the top drifts (tokens first, they cascade), re-render, re-crop. Stop when the close-up of the key element is indistinguishable. Track each pass so progress is visible.

---

## Stage 6 — Output

```
## UI Diff — <screen>

Reference: <figma node | screenshot path>
Target:    <file/url>   JS errors: <none | ...>

### Drift resolved (this pass)
- [x] purple #6E2586 -> #702F8A
- [x] card radius 12 -> 16px
- ...

### Drift remaining
- [ ] hero gradient hue (approx, Figma call rate-limited)
- [ ] real brand logos (placeholders)

Close-up verdict: MATCH / CLOSE / OFF
Artifacts: docs/refs/card_closeup.png, diff_sidebyside.png
```

Keep render/crop artifacts in a gitignored scratch dir (e.g. `docs/refs/`). Never commit licensed reference renders or embedded brand fonts without flagging licensing.
