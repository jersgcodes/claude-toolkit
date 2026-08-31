---
name: motion-check
description: Audit UI animation/motion for craft — durations ≤300ms, transform/opacity-only (no layout-thrashing animated width/height/top/left/margin), a prefers-reduced-motion fallback, and sensible easing (ease-out for enter/exit). Catches AI-slop and janky motion. Use after adding CSS transitions/animations or framer-motion. Complements /design-craft-check (static visual craft).
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.1.0
---

Audit motion/interaction craft — the animation layer none of the other design tools cover.
Complements `/design-craft-check` (static visual craft). Rules distilled from Emil Kowalski's
motion guidance ("giving agents taste") + the "zero-code scroll animation" extraction. Good
motion is fast, cheap to render, and respects accessibility. Do the steps in order.

---

**1. Detect stack & locate motion**

- `Glob` the UI (`src/`/`app/`/`components/`), then `Grep` for motion:
  - CSS: `transition`, `animation`, `@keyframes`, `transition-duration`, `animation-duration`.
  - Tailwind: `transition`, `duration-`, `ease-`, `animate-`.
  - framer-motion / motion: `motion.`, `animate=`, `transition=`, `whileHover`, `whileTap`, `variants`.
- Report: "Motion found in <N> files via <CSS | Tailwind | framer-motion>" or "No motion found — nothing to audit."

---

**2. Duration**

- Any UI micro-interaction duration > **300ms** (`transition-duration`/`duration` > `0.3s`/`300ms`,
  Tailwind `duration-[400ms]`+, framer `transition={{ duration: 0.4+ }}`) → **MEDIUM**
  (cap UI motion at ~300ms; only large/page-level transitions may exceed).
- Durations < ~80ms on visible motion → **LOW** (too fast to read).
- Exit animations the same length as or longer than entrances → **LOW** (exits should be ~20% faster).

---

**3. Animated properties** (the render-performance rule)

- Animating **layout properties** — `width`, `height`, `top`, `left`, `right`, `bottom`, `margin`,
  `padding` (in `transition`/`@keyframes`, or framer `animate` on those) → **HIGH**
  (layout thrash; animate `transform` (`scale`/`translate`) and `opacity` instead).
- `transition: all` → **MEDIUM** (over-broad; name the properties, or you'll animate layout by accident).

---

**4. Reduced motion** (accessibility — also a WCAG item)

- Any non-trivial `@keyframes`/`animation` or transition with **no** `@media (prefers-reduced-motion: reduce)`
  fallback → **MEDIUM** (provide a reduced / no-motion variant). framer: no `useReducedMotion()` guard → **MEDIUM**.
- **Scoping (validated by the design-system fixtures):** only credit a reduced-motion fallback that lives in a
  stylesheet the page/component **actually loads**. A global fallback in `tokens.css` does not cover a file
  that doesn't `@import`/`<link>` it — check the load graph, not just "does the fallback exist somewhere."

---

**5. Easing**

- Enter/exit motion using `linear` (or Tailwind `ease-linear`) → **LOW** (use `ease-out` for enter/exit).
- Motion with no easing specified (browser default `ease`) on prominent transitions → **LOW** (choose deliberately:
  enter/exit → `ease-out`; on-screen move/morph → `ease-in-out`; hover → `ease`; continuous → `linear`).

---

**6. Appearance & feedback patterns**

- Elements appearing via `scale(0)` / `opacity` from full-collapse → **LOW** (start at `scale(0.95)`, not 0).
- Interactive buttons/links with no `:active`/`whileTap` feedback (e.g. `scale(0.97)` on press) → **LOW**.
- Continuous/looping animation with no purpose (decorative infinite spin/pulse on non-loading elements) → **LOW**.

---

**7. Summary**

```
## Motion Check

Motion source: <CSS | Tailwind | framer-motion>
Files: <list>

### Findings by severity
HIGH (must fix):
- [ ] <rule> — <finding> — <file:line>
MEDIUM (should fix):
- [ ] <rule> — <finding> — <file:line>
LOW (consider):
- [ ] <rule> — <finding> — <file:line>

### Motion scorecard
| Dimension | Status | Note |
|---|---|---|
| Duration (≤300ms, exits faster) | ✅ / ⚠️ / ❌ | |
| Properties (transform/opacity only) | ✅ / ⚠️ / ❌ | |
| Reduced-motion fallback | ✅ / ⚠️ / ❌ | |
| Easing (deliberate) | ✅ / ⚠️ / ❌ | |

### Top 3 highest-leverage fixes
1. <specific fix with file:line>
2. ...
3. ...

Verdict: PASS / WARN / FAIL
```

Note: the highest-impact finding is almost always animated layout properties (HIGH) — fixing those
to `transform`/`opacity` removes jank. Where a grep can't confirm the animated property (e.g.
dynamic style), report it as manual-review, not a hard failure.
