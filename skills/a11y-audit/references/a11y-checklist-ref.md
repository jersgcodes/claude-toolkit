# a11y-audit reference material — WCAG 2.1 AA checklists

---

## Stage 1 — Perceivable

### 1.1 Text alternatives
- [ ] Every `<img>` has `alt` attribute
  - Decorative: `alt=""` (NOT missing — present-but-empty)
  - Informative: describes content/function in context
  - Functional (logo in link): describe destination, not visual
- [ ] Every `<svg>` has `<title>` or `aria-label`
- [ ] Icons have accessible names (aria-label) or paired text
- [ ] No important info conveyed through image of text

### 1.2 Time-based media (skip if no video/audio)
- [ ] Video has captions
- [ ] Audio has transcript
- [ ] Auto-playing video has no audio OR plays under 3 seconds

### 1.3 Adaptable
- [ ] Semantic HTML used (h1/h2/.../nav/main/article/aside/section/header/footer)
- [ ] Heading hierarchy correct: one `<h1>` per page, no skipping levels (h1 → h3 is wrong)
- [ ] Tables use `<th scope="...">` when they're real tables
- [ ] Form fields have associated `<label>` (`for` attribute matching field `id`)
- [ ] Reading order makes sense without CSS (visual order = DOM order, generally)

### 1.4 Distinguishable
- [ ] **Text contrast ≥ 4.5:1** against background (3:1 for text ≥ 18pt or 14pt bold)
- [ ] **UI component contrast ≥ 3:1** (button borders, focus indicators, form field borders)
- [ ] Color is NEVER the only signal (error state needs icon + text, not just red)
- [ ] Text resizable to 200% without loss of content/functionality
- [ ] No fixed text inside images (allows zoom + screen reader access)
- [ ] Page works at 320px width zoomed to 400% (= 1280px content at base zoom)
- [ ] Line spacing ≥ 1.5× font size, paragraph spacing ≥ 2× font size (for text content)

---

## Stage 2 — Operable

### 2.1 Keyboard accessible
- [ ] ALL functionality available via keyboard alone (Tab, Shift+Tab, Enter, Space, arrows, Escape)
- [ ] Tab order is logical (matches visual order)
- [ ] No keyboard trap (can always Tab/Esc out of any control)
- [ ] Visible focus indicator on every focusable element (NEVER `outline: none` without replacement)
- [ ] Custom controls re-implement keyboard model of native (e.g. custom listbox = arrow keys + Enter)
- [ ] Skip link to main content for keyboard users

### 2.2 Enough time
- [ ] No session timeout < 20 hours without warning + extend option
- [ ] No auto-refresh that disorients (or has pause/stop)
- [ ] Animations under 5 seconds OR pause/stop control
- [ ] No content that flashes > 3 times/second (seizure risk)

### 2.3 Seizures and physical reactions
- [ ] No flashing > 3 times/second
- [ ] Animation can be disabled via `prefers-reduced-motion`

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 2.4 Navigable
- [ ] Page has a descriptive `<title>` (unique per page)
- [ ] Headings describe content of section
- [ ] Link text describes destination (NEVER "click here", "read more")
- [ ] Multiple ways to find pages (nav + search + sitemap, etc.)
- [ ] Current location indicated (active nav item, breadcrumb)

### 2.5 Input modalities
- [ ] **Touch targets ≥ 44×44 px** (WCAG 2.5.5 AAA, but workspace standard)
- [ ] Click target larger than visible button is OK; smaller is not
- [ ] No motion-only activation (shake-to-undo needs alternative)
- [ ] No drag-only operation (drag-and-drop needs click alternative)

---

## Stage 3 — Understandable

### 3.1 Readable
- [ ] `<html lang="en">` (or whatever language)
- [ ] Language changes in text marked with `lang` attribute
- [ ] Reading level appropriate to audience (avoid jargon; explain on first use)

### 3.2 Predictable
- [ ] Focus doesn't trigger context change (a select focus shouldn't navigate)
- [ ] Input doesn't trigger context change without warning (typing in search shouldn't auto-navigate)
- [ ] Navigation is consistent across pages
- [ ] Identical components labeled identically (don't call the same button "Save" and "Submit")

### 3.3 Input assistance
- [ ] Errors identified (which field, what's wrong)
- [ ] Error message text describes the problem AND how to fix
- [ ] Error message announced to screen readers (`aria-live="polite"` for soft, `assertive` for blocking)
- [ ] Labels visible on focus (NOT placeholder-as-label — placeholder disappears on focus)
- [ ] Help text associated via `aria-describedby`
- [ ] For legal/financial/data-modification actions: confirm step before commit
- [ ] Auto-complete attributes on common fields (`autocomplete="email"`, `autocomplete="name"`, etc.)

---

## Stage 4 — Robust

### 4.1 Compatible
- [ ] Valid HTML (no duplicate IDs, properly nested tags)
- [ ] ARIA used only when semantic HTML doesn't suffice
- [ ] ARIA roles match the implementation behavior
- [ ] Live regions used for dynamic updates (`aria-live`)
- [ ] Status messages announced (`role="status"`, `role="alert"`)

### Common ARIA anti-patterns to flag
- `role="button"` on `<a>` — use `<button>` instead
- `<div onclick>` — replace with `<button>`
- `aria-hidden="true"` on focusable elements — they'll be hidden but reachable, very confusing
- Missing `aria-label` on icon-only buttons
- `aria-label` on elements with visible text (redundant, may confuse screen readers)
