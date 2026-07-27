---
name: design-craft-check
description: Audit a UI's NUMERIC visual craft — color (no pure black, token-based palette), typography (constrained type scale, ≤3 font weights, line length), spacing (4/8 grid), elevation (shadow tokens) — plus anti-AI-slop defaults (purple gradients, emoji-as-icons, placeholder copy, centered-hero sameness). Complements /design-review (qualitative "AI-made" judgment) and /style-check (UX behaviour); this one enforces the greppable craft rules from Refactoring UI. Use after building any UI.
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.1.0
---

Audit the numeric visual craft that separates pro UI from amateur/AI-made UI. This is the
**greppable craft layer** none of the other design tools enforce. Lanes:
- `/design-craft-check` (this) → numeric craft (the HYGIENE FLOOR): color, type, spacing, elevation + anti-slop.
- `/design-review` → the CRAFT CEILING: scores against `design-lab/CRAFT-BAR.md`'s 8 dimensions, verified in-browser. Passing this (not this linter) is "done".
- `/style-check` → UX behaviour vs the workspace style guide (buttons, forms, states).
- `/ux-psych-audit` → conversion/onboarding behavioural principles.
Rules distilled from Refactoring UI (Wathan & Schoger) + the "AI-built sites look identical"
critique. Do the steps in order.

---

**1. Detect stack & locate design tokens**

- `Glob` for the UI: `**/*.{jsx,tsx,vue,svelte,css,scss}` under `src/`/`app/`/`components/`.
- Locate the token source: `tailwind.config.{js,ts}`, a theme CSS file with `--` custom properties,
  a styled-components/`theme.ts`, or the project `STYLE_GUIDE.md`.
- Report: "Tokens: <source> | checking against it" or "No token system found — will flag hardcoded values as drift."

---

**Scoping (important — validated by the design-lab fixtures)**

All colour/gradient/font checks apply to **CSS declarations only** (the value side of
`property: value` in `<style>`, `.css`, or `style=` attributes) — **not** to code comments
(`/* … */`) or visible text content. Grepping raw will false-positive on copy (a hero that says
"no purple gradients") and comments (`/* never #000 */`). Scope patterns to `property:\s*value`
and exclude comment/text nodes, or verify each hit is inside a real declaration before flagging.

---

**2. Color**

- Pure black on text/background: `#000`, `#000000`, `black`, `rgb(0,0,0)` → **HIGH** (use a very
  dark desaturated colour, never pure black).
- Hardcoded hex/rgb values **not** drawn from the token source → **MEDIUM** (colour-system drift).
- No defined grey scale (greys invented ad-hoc across files) → **MEDIUM** (need ~8–10 greys).
- Accent colour with <5 shades defined → **LOW** (shallow palette can't build hierarchy).

---

**3. Typography**

- Count distinct `font-size` values in scope; more than ~6 arbitrary sizes not on a scale → **MEDIUM**
  (use a constrained modular scale, not one-off px).
- Distinct `font-weight` values > 3 → **MEDIUM** (limit weights; hierarchy from 2–3).
- Body-text containers with no `max-width` bounding line length to ~45–75ch → **MEDIUM**.
- Body `font-size` < 14px → **LOW**.

---

**4. Spacing**

- `padding`/`margin`/`gap` values off a 4/8 base scale (e.g. `5px`, `13px`, `17px`, `23px`) → **MEDIUM**
  (snap to 4/8: 4,8,12,16,24,32,48,64…).
- Many distinct one-off spacing values across a component (>~6) → **MEDIUM** (proliferation = no system).

---

**5. Elevation / shadow**

- Inline `box-shadow` values not from a defined token set → **MEDIUM** (define ~5 elevation levels).
- Same surface using multiple different ad-hoc shadows → **MEDIUM**.

---

**6. Hierarchy & emphasis** (light — deep judgment belongs to /design-review)

- Two or more elements sharing the same "primary" styling competing in one view → **MEDIUM**
  (emphasise one; de-emphasise the rest via colour/weight, don't amplify everything).
- Icons scaled up via `transform: scale(...)` or huge `font-size`/`width` on an icon → **LOW**
  (scale by adding surrounding space/background, not by enlarging the glyph).

---

**7. Anti-AI-slop defaults** (the "AI-built sites look identical" extraction)

Flag the tells that make a UI read as machine-generated. Purple gradient is the *emblem* of a
broader **generic-AI-default cluster** — flag the cluster, not just the colour:
- Saturated **gradient** hero — blue→purple→pink / violet / indigo (`linear-gradient` with
  `#8b5cf6`/`#6366f1`/`purple`/`violet`/`indigo`/`fuchsia` hues), especially on white/near-white
  → **LOW** but label **AI-DEFAULT**. (Purple is the meme; any loud multi-hue hero gradient counts.)
- Glassmorphism overused (`backdrop-filter: blur` on many stacked cards) or neon glow on dark
  (`box-shadow` with a saturated accent at high alpha) → **LOW** **AI-DEFAULT**.
- Type is *only* a generic system stack (`Inter`, `Roboto`, `Arial`, `system-ui`) with no distinctive
  display face anywhere → **LOW** (add character).
- **Emoji used as icons** in buttons/nav/feature cards (emoji chars inside interactive elements) → **MEDIUM**.
- Placeholder copy shipped: `Lorem ipsum`, `Your text here`, `Lorem`, `TODO copy` → **MEDIUM**.
- Generic centered-hero + exactly-three-feature-cards boilerplate with no distinctive layout → note as
  **AI-DEFAULT** (heuristic, not a hard fail).

---

**8. Summary**

```
## Design Craft Check

Token source: <path or "none found">
Files: <list>

### Findings by severity
HIGH (must fix):
- [ ] <rule> — <finding> — <file:line>
MEDIUM (should fix):
- [ ] <rule> — <finding> — <file:line>
LOW / AI-DEFAULT (consider):
- [ ] <rule> — <finding> — <file:line>

### Craft scorecard
| Dimension | Status | Note |
|---|---|---|
| Colour (no pure black, token-based) | ✅ / ⚠️ / ❌ | |
| Typography (scale, ≤3 weights, measure) | ✅ / ⚠️ / ❌ | |
| Spacing (4/8 grid) | ✅ / ⚠️ / ❌ | |
| Elevation (shadow tokens) | ✅ / ⚠️ / ❌ | |
| Anti-AI-slop | ✅ clean / ❌ tells found | |

### Top 3 highest-leverage fixes
1. <specific fix with file:line>
2. ...
3. ...

Verdict: PASS / WARN / FAIL
```

Note: several checks depend on a token source — when none exists, report hardcoded values as
drift and recommend establishing tokens first (that's the root fix). Where a grep can't confirm
intent, report it as a manual-review item, not a hard failure.
