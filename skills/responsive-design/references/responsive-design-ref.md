# responsive-design-ref.md

Reference material for `/responsive-design`. Loaded on demand by the skill.

---

## Stage 2 — Mobile-first CSS code blocks

```css
/* Mobile-first: base = mobile */
.card { padding: 1rem; }

/* Add desktop affordances */
@media (min-width: 768px) {
  .card { padding: 2rem; }
}
```

NOT:
```css
/* Desktop-first (avoid for new work) */
.card { padding: 2rem; }
@media (max-width: 767px) {
  .card { padding: 1rem; }
}
```

---

## Stage 4 — ASCII layout sketches

```
Mobile (< 640px):
┌─────────────┐
│ HEADER      │
├─────────────┤
│ HERO IMG    │
├─────────────┤
│ HEADLINE    │
│ BODY TEXT   │
│             │
│ [CTA BTN]   │
├─────────────┤
│ FOOTER      │
└─────────────┘

Desktop (≥ 1024px):
┌─────────────────────────────────┐
│ HEADER                          │
├──────────────┬──────────────────┤
│ HEADLINE     │                  │
│ BODY TEXT    │   HERO IMG       │
│              │                  │
│ [CTA BTN]    │                  │
├──────────────┴──────────────────┤
│ FOOTER                          │
└─────────────────────────────────┘
```

---

## Stage 6 — Fluid type clamp() code blocks

```css
/* Fluid heading: 1.5rem on mobile, scales to 3rem on large screens */
h1 {
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);
}

/* Fluid container: 1rem padding on mobile, scales to 4rem */
.container {
  padding-inline: clamp(1rem, 4vw, 4rem);
}
```

---

## Stage 7 — Container queries code block

```css
.card-grid {
  container-type: inline-size;
}

@container (min-width: 600px) {
  .card { display: grid; grid-template-columns: 1fr 1fr; }
}
```

---

## Stage 8 — YAML design-token block

```yaml
# Breakpoints (mobile-first)
breakpoints:
  sm: 640
  md: 768
  lg: 1024
  xl: 1280
  2xl: 1536

# Container max widths per breakpoint
container_max:
  sm: 640
  md: 768
  lg: 1024
  xl: 1280
  2xl: 1400  # cap content width even on huge screens

# Spacing scale (used at all breakpoints, but with different defaults)
spacing:
  base_mobile: 16  # 1rem
  base_desktop: 24

# Type scale endpoints (for clamp())
type:
  body: clamp(1rem, 0.95rem + 0.25vw, 1.125rem)
  h1:   clamp(1.75rem, 1.25rem + 2.5vw, 3rem)
  h2:   clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem)
```

---

## Stage 9 — Output template

```markdown
# Responsive Plan: <feature>

## Layout sketches

### Mobile
[ASCII sketch]

### Tablet
[ASCII sketch — or "same as mobile" / "same as desktop"]

### Desktop
[ASCII sketch]

## Breakpoints used
- mobile → md (768px): stack becomes side-by-side
- md → lg (1024px): sidebar appears
- lg → none beyond: content cap at 1280px

## Content decisions
| Element | Mobile | Tablet | Desktop |
|---|---|---|---|
| Hero image | Below headline | Beside headline (50/50) | Beside headline (60/40) |
| Sidebar nav | Hidden behind hamburger | Hidden behind hamburger | Inline sidebar |
| Footer links | Stacked, full width | 2-column grid | 4-column grid |

## Fluid scaling
- h1 uses `clamp(1.75rem, ..., 3rem)` — no breakpoint needed
- Container padding uses `clamp(1rem, 4vw, 4rem)`

## Container queries
- `.card` adapts based on parent width — fixed for sidebar vs main column

## Min viewport tested
- 320px — must remain usable
- 1920px — content capped, comfortable reading width
```
