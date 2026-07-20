---
name: responsive-design
description: Plan responsive behavior before writing layout code. Breakpoint strategy, mobile-first thinking, fluid type, container queries, content reflow. Pre-build companion to /mobile-audit.
allowed-tools: [Read, Glob, Grep, Write]
version: 0.1.0
---



# Responsive Design

Plan how layouts adapt across screen sizes BEFORE writing CSS. `/mobile-audit` checks compatibility after build; this one prevents the problems at design time.

Sources: Ethan Marcotte *Responsive Web Design*, Brad Frost *Atomic Design*, Tailwind responsive design docs, MDN container queries spec, *Refactoring UI* (responsive chapter).

---

## When to use

| Situation | Use? |
|---|---|
| New page with content that needs to work on phone + desktop | YES |
| New component placed in different container sizes (sidebar, modal, full page) | YES |
| Email template (different rendering rules) | YES, but use email-specific patterns |
| Single-purpose modal that's only ever 400px wide | NO — fixed size is fine |
| Admin dashboard that's desktop-only | NO, but document the constraint |

---

## Stage 1 — Frame the layout

Ask:

1. **What's the content?** (List the pieces: headline, image, text body, CTA, sidebar widgets, etc.)
2. **What's the priority order?** (When space is tight, what shows first? What gets hidden?)
3. **Where will users encounter it?** (Phone in landscape? Tablet portrait? Big desktop? All three?)
4. **What's the minimum viable size?** (320px is the standard floor — iPhone SE width)
5. **What's the maximum useful size?** (Long-form text caps around 65ch; full-page hero may scale further)
6. **Is the content shape fixed, fluid, or varies dramatically?** (List of cards vs free-form article)

---

## Stage 2 — Adopt mobile-first as the default

**Why mobile-first** (vs designing for desktop and shrinking):
- Forces hierarchy decisions early (what's important enough for a small screen?)
- Performance budget is tight on mobile (forces lean default)
- Easier to add complexity than remove it
- Tailwind, Bootstrap 5, and modern frameworks default to mobile-first

In CSS terms: base styles apply to small screens; `@media (min-width: ...)` adds rules for larger.

> **Reference:** CSS code blocks (mobile-first vs desktop-first examples) for this stage are in `references/responsive-design-ref.md`.

---

## Stage 3 — Choose your breakpoint strategy

Pick ONE strategy per project. Document in CLAUDE.md.

### Strategy A — Content-based (best practice)

Add breakpoints when the LAYOUT visibly breaks, not at fixed pixel values. Resize the browser; note where the design feels wrong; add a breakpoint there.

Pros: minimal breakpoints, no waste
Cons: hard to remember, drift between developers

### Strategy B — Device-based (most common but flawed)

Match common device widths:
- 320px (iPhone SE) - mobile
- 768px (iPad portrait) - tablet
- 1024px (iPad landscape) - small desktop
- 1280px - standard desktop
- 1536px+ - large desktop

Pros: easy to communicate
Cons: device landscape ≠ width buckets; chases device specs that change

### Strategy C — Tailwind defaults (pragmatic choice)

```
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

Pros: matches popular tooling, well-tested
Cons: same as B

**My recommendation for your projects:** Strategy C with content-aware overrides. Use the defaults, but add custom breakpoints when content demands.

---

## Stage 4 — Sketch the layouts

For each major breakpoint, sketch the layout as ASCII or low-fi:

> **Reference:** ASCII layout sketches (mobile and desktop examples) for this stage are in `references/responsive-design-ref.md`.

Sketch at minimum:
- Mobile (320-640px)
- Tablet (640-1024px) — if it differs meaningfully
- Desktop (1024px+)

If tablet looks identical to mobile (just wider), say so explicitly — fewer breakpoints is better.

---

## Stage 5 — Content reflow rules

For each piece of content, decide:

| Decision | Options |
|---|---|
| Stack or stay side-by-side? | Stack on mobile, side-by-side from `md` |
| Hide entirely? | Show on `lg+` only (`hidden lg:block`) |
| Replace with simpler form? | Hamburger menu on mobile, full nav on desktop |
| Reorder? | CSS `order` to move things across breakpoints |
| Scale proportionally? | Use `clamp()` for fluid type/spacing |

**Watch out for:** hiding important content on mobile. If it matters on desktop, it usually matters on mobile too — it just needs to be presented differently.

---

## Stage 6 — Fluid type and spacing

Instead of stepped sizes per breakpoint, use `clamp()` for smooth scaling:

> **Reference:** `clamp()` CSS code blocks for fluid type and spacing for this stage are in `references/responsive-design-ref.md`.

Benefits:
- Fewer breakpoints to maintain
- Smooth transition (no jump at 768px)
- Works for in-between sizes

Use for: type scale, container padding, hero spacing. NOT for: layout direction (stack vs side-by-side — that needs a breakpoint).

---

## Stage 7 — Container queries (where supported)

Container queries respond to the PARENT's width, not the viewport. Modern browsers support them; great for reusable components.

> **Reference:** Container queries CSS code block for this stage is in `references/responsive-design-ref.md`.

Use when:
- Same component placed in sidebar vs main column
- Components shouldn't know about viewport, only their available space

Browser support: Chromium 105+, Safari 16+, Firefox 110+. Safe for most modern projects.

---

## Stage 8 — Lock the constants

Document in CLAUDE.md or design tokens:

> **Reference:** YAML design-token block for this stage is in `references/responsive-design-ref.md`.

---

## Stage 9 — Save the plan

Save to `docs/responsive/<feature>.md`:

> **Reference:** Output template for this stage is in `references/responsive-design-ref.md`.

---

## Stage 10 — Validate before coding

- [ ] Mobile sketch drawn (≤ 640px)
- [ ] Desktop sketch drawn (≥ 1024px)
- [ ] Tablet handled OR explicitly skipped with reason
- [ ] Content hierarchy survives smallest screen (no important content hidden)
- [ ] Touch targets ≥ 44px on mobile considered
- [ ] Fluid scaling chosen for type/spacing where smooth helps
- [ ] Breakpoint strategy documented (which one, why)
- [ ] No fixed pixel widths that won't shrink (`width: 800px` breaks below 800px)

---

## Cost control

- Reads existing layout/CSS files — cap at 8
- ASCII sketches keep output low-token
- For multi-page features, split into one `/responsive-design` per template

---

## Integration

- Pulls from: `/feature-design` (when a UI feature emerges), `/component-design` (component-level layout)
- Hands off to: implementation, `/mobile-audit` (post-build verification), `/a11y-audit` (responsive zoom is a WCAG criterion)
- Related: `/style-check` for visual identity consistency across breakpoints

---

## Anti-patterns to flag

- **Desktop-first CSS** with hand-coded mobile overrides — invert it
- **Fixed pixel widths** that break below the value
- **Hiding important content on mobile** instead of presenting differently
- **Breakpoints at random pixel values** with no rationale
- **Too many breakpoints** (more than 4 is usually overkill)
- **Magic numbers in CSS** (`@media (max-width: 712px)`) instead of named tokens
- **Horizontal scrolling on mobile** — never (except deliberate carousels)
- **Tap targets close together** — accidental taps on adjacent elements
- **Type that's too small on mobile** (< 16px body) — triggers iOS zoom on focus
- **Containers that don't cap** on huge screens — line lengths exceed 90ch are unreadable
