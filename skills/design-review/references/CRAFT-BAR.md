<!--
GENERATED SNAPSHOT -- DO NOT EDIT.

Authored in the design-system repo as CRAFT-BAR.md, copied here so the skill works on a
machine with no design-system checkout. Edit it there, then run:

    python3 scripts/sync-design-refs.py

Synced: 2026-09-05
-->

# The Craft Bar — the standard above hygiene

> The problem this file fixes: the "gauntlet" (`/design-craft-check` + `/motion-check` + a quick
> a11y pass) certifies **hygiene**, not **craft**. It checks for the *absence of tells* — no pure
> black, no purple gradient, no emoji icons, tokens not hardcodes, ≤3 weights, 4/8 spacing, cheap
> motion. A UI can pass every one of those and still be flat, generic, and forgettable. Passing the
> gauntlet means "not obviously machine-made." That is a **floor**. This file defines the **ceiling**.

The gauntlet answers *"is this tidy?"* This file answers *"was this designed by someone with taste?"*
The two are independent. Tidy-but-generic is the most common AI output and the exact thing Jer flagged.

**How to use it:** a surface is not "done" when it passes the linters — it's done when it clears the
bar on all eight dimensions below. Each dimension gives the **tidy floor** (what the linter already
catches), the **craft ceiling** (what excellence looks like), and a **test** you can actually apply.

---

## The one rule under all eight
**Every value is a decision you can defend.** Generic design is the accumulation of un-made decisions —
the default font stack, the default `#3b82f6` accent, the centered hero with three cards, the shadow
that came with the component library. Craft is when someone *chose* this face over that one, this
measure, this easing, and can say why. The deepest AI tell is not ugliness — it's the **absence of a
point of view.**

---

## 1. Typography — the highest-leverage dimension
**Floor (linted):** on a modular scale, ≤3 weights, body ≥14px, has a `max-width`.
**Ceiling (craft):**
- A **real type pairing that actually loads.** A "distinctive display face" that silently falls back
  to Georgia (the current bug — Fraunces is named everywhere, loaded nowhere) is worse than honestly
  using a great system stack. Load the face (`@font-face`, `font-display: swap`, subset it) or don't
  claim it.
- **Optical adjustments by size:** display sizes get **tighter tracking** (`letter-spacing: -0.02em`)
  and tighter line-height; all-caps labels get **open tracking** (`+0.06em`); body stays neutral.
- **Line-height scales inversely with size** — headings ~1.1, body ~1.5–1.6. One `line-height` for
  everything is a tell.
- **Measure:** body text 60–72ch. Not just "has a max-width" — the *right* max-width.
- **Tabular/lining numerals** (`font-variant-numeric: tabular-nums`) anywhere numbers align (tables,
  KPIs, prices). Proportional digits jittering in a column is a tell.
- **Hierarchy from type alone** should survive with color removed — size + weight + spacing carry it.
- **Test:** screenshot in grayscale. Can you still rank the information? Do headings feel *set*, not
  just *bigger*? Is any real web font actually rendering (not a fallback)?

## 2. Color — perceptual, not hand-picked
**Floor (linted):** no pure black, tokenized, ≥5 accent shades, desaturated states.
**Ceiling (craft):**
- **Perceptually even ramps.** Hand-picked hex jump unevenly in lightness. Build neutrals and accent
  in **OKLCH** so each step is a real, even perceptual increment. A ramp that's smooth to the eye is
  the difference between a system and a swatch grab.
- **A neutral temperature that's chosen** — warm greys or cool greys, consistently, and the accent
  sits in a deliberate relationship to them (complementary warmth, or a considered analogous nudge).
- **Color builds hierarchy, doesn't just decorate** — the accent appears *rarely* and always means
  "this is the one thing." An accent on five elements is an accent on none.
- **Dark mode is re-thought, not inverted.** Real dark mode lifts surface (not pure `#000`), reduces
  accent chroma (saturated colors vibrate on dark), and re-checks every contrast pair. An inverted
  light theme is a tell.
- **Test:** lay the neutral ramp out as swatches — do the lightness steps look even? Count accent
  uses on one screen — is it ≤ ~2 meaningful placements? Toggle dark mode — is it designed or flipped?

## 3. Space & composition — rhythm, not just "on the grid"
**Floor (linted):** values on a 4/8 scale.
**Ceiling (craft):**
- **Space is rhythm.** Related things sit closer; unrelated things get real air. The gaps should form
  a clear hierarchy (a section break ≫ a field gap ≫ a label gap), not a uniform `16px` everywhere.
- **Whitespace is generous and intentional** — especially around the focal point. Cramped-but-tidy is
  still cramped. Density is *calibrated to the job*: a data table earns tightness; a hero earns air.
- **Alignment to a real grid**, and deliberate use of asymmetry (optical centering, off-center focal
  points) rather than everything dead-center — the centered-everything layout is a slop signature.
- **Vertical rhythm** relates to the type's line-height, so text baselines feel like they share a beat.
- **Test:** the squint test — blur the screen. Does a clear compositional structure remain, with one
  obvious focal area and calm negative space? Or is it an even gray mush of equally-spaced boxes?

## 4. Hierarchy & focus — one clear path for the eye
**Floor (linted):** one primary action, no two competing primaries.
**Ceiling (craft):**
- A **deliberate focal order** — the eye lands 1st / 2nd / 3rd where you intend. Built from *all* of
  size + weight + color + space + position acting together, not one lever.
- **Secondary and tertiary actions genuinely recede** (ghost/text buttons, muted ink) so the primary
  reads instantly. Three buttons of equal visual weight = no hierarchy.
- **Progressive disclosure** — the screen shows what matters now; detail is one interaction away.
- **Test:** show it to someone for 3 seconds, hide it, ask "what was the main thing / what would you
  click?" If they can't answer, the hierarchy failed regardless of how tidy it was.

## 5. Depth & surface — a coherent light model
**Floor (linted):** shadows from a token set, not ad-hoc.
**Ceiling (craft):**
- **One consistent light source.** All shadows fall the same way; elevation is a *semantic* scale
  (resting / raised / overlay / modal), not three random blurs.
- **Border vs shadow vs background-shift used deliberately** to separate layers — often a hairline
  border + a whisper of shadow reads more crafted than a heavy drop shadow.
- Shadows tuned per theme (softer, lower-opacity, and often a subtle border instead, in dark mode).
- **Test:** do all shadows agree on where the light is? Does elevation *mean* something consistent, or
  is depth decorative?

## 6. Motion — choreographed, not just non-broken
**Floor (linted):** <300ms, no layout-prop animation, `prefers-reduced-motion`, `:active` feedback.
**Ceiling (craft):**
- **Choreography:** when multiple things appear, they enter in a considered order/stagger, not all at
  once. Motion has a *sequence*.
- **Motion reinforces the spatial model** — a drawer slides in from the edge it lives on; a popover
  scales from its trigger; a deleted row collapses. Movement explains the change.
- **Easing has character and matches direction** — enter with a decelerating ease-out, exit faster;
  the same curve everywhere is a tell.
- **Felt, not seen** — good motion is barely noticed; you'd miss it if removed. Bouncy/showy motion on
  a productivity UI is a slop signature.
- **Test:** does each transition *explain* a change of state or spatial relationship? Remove all
  motion — is the product harder to understand? (If motion was purely decorative, it was wrong.)

## 7. States & content — the part slop skips
**Floor (linted / current):** states *documented in markdown*, real copy (no Lorem).
**Ceiling (craft):**
- **Every state is built and designed**, not described: **empty** (teaches the first action, never a
  sad blank), **loading** (a skeleton matching the final layout, not a spinner), **error**
  (recoverable, says what to do next), **success**, **partial/edge** (long names, zero/huge numbers,
  one item vs a thousand). The **designed empty state is one of the clearest craft signals** there is.
- **Content is real and has a voice.** Microcopy that sounds like a product with a personality, not
  "Welcome back!" / "Something went wrong." Numbers, names, and dates that are plausible and specific.
- **Test:** can you screenshot the empty, loading, and error states and have each look *intentional*?
  Read the copy aloud — does it sound like a person wrote it for this product, or like a placeholder?

## 8. Point of view — the thing that can't be linted
**Floor:** inoffensive; could be any SaaS template.
**Ceiling (craft):**
- A **committed aesthetic stance.** Editorial-warm (serif display, generous measure, paper tones)?
  Technical-precise (mono accents, tight grid, hairlines)? Soft-calm (low contrast, rounded, muted)?
  Pick one, commit, and let it show in *every* decision. Half-committing (warm off-white + the single
  most-defaulted "designer teal" + a display font that never loads) reads as generic with good posture.
- The POV should make some things **deliberately unusual** — a distinctive empty state, an unexpected
  but right accent placement, a typographic flourish that's clearly a choice. Safe-everywhere = generic.
- **Test:** could you tell this apart from ten other dashboards in a lineup? If a stranger described it
  back to you, would the description include an adjective that isn't "clean"?

---

## The bar, in one paragraph
A surface clears the craft bar when: a real type pairing is *actually loaded* and optically tuned;
the color ramps are perceptually even with a chosen temperature and a rarely-used accent; space forms
a clear rhythm around generous, intentional whitespace; the eye has one obvious path; depth follows a
single light model; motion choreographs and explains state changes; **every** state is built and the
copy has a voice; and the whole thing has a **point of view** you could name in one adjective that
isn't "clean." Tidy is the floor you pass on the way to that — not the finish line.

## What changes because of this file
1. `tokens.css` → **v2**: add a radius scale, real font tokens **and actually load the faces**,
   perceptually-even OKLCH ramps, a designed dark mode, fluid type. (Fixes the gaps the audit found:
   no radius scale, thin ramps, unloaded Fraunces, no dark mode, no font tokens.)
2. Surfaces get **rebuilt to this bar**, not just re-linted — starting with one flagship exemplar
   that proves the ceiling, with **every state built** (no more states-only-in-markdown) and the
   `aria-sort` bug fixed.
3. The **`/design-review` skill** scores a surface against these eight dimensions, **verified
   in-browser** (light + dark, every state) — the qualitative judge the linters defer to. It is the
   "done" gate: a surface clears the bar when `/design-review` scores it CRAFTED, not when the linters
   pass. (Built 2026-07-27; pairs with the `design-review` agent for the code-level tell sweep.)
