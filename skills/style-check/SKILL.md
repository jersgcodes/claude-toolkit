---
name: style-check
description: Audit a component or page against the workspace UX style guide — buttons, forms, loading states, error handling, accessibility, and responsive layout.
allowed-tools: [Read, Grep, Glob]
version: 0.1.0
---

Audit a component or page against the workspace UX style guide. Do the following steps in order:

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

**1. Detect stack and load style guides**

- Check for `package.json` → React/Next.js project
- Read `your project's STYLE_GUIDE.md` (workspace UX fundamentals)
- Read project-level `STYLE_GUIDE.md` or `CLAUDE.md` visual style section (if exists)
- Report: "Checking against: workspace UX guide + [project visual guide | no project guide found]"

---

**2. Button behavior audit**

Search all `.jsx` / `.tsx` / `.js` / `.ts` files in `src/` for button elements:
- `<button`, `<Button`, `onClick`

For each button found, check:
- Does it have a loading/disabled state when triggering async actions?
- Does it prevent double-submit? (look for `disabled={loading}` or similar)
- Destructive actions (delete, remove): is the button styled differently from primary?
- Touch target: is there explicit min-height/min-width or padding >= 10px?

Flag buttons missing loading state on async actions as HIGH.

---

**3. Form behavior audit**

Search for `<form`, `<input`, `<select`, `<textarea`, `onSubmit`:

- Labels: are inputs linked to labels via `htmlFor`/`id` or wrapping `<label>`?
- Placeholder-only labels: flag any input where placeholder is the only label (no visible `<label>`)
- Validation: is there error display (`error`, `helperText`, red border)?
- Submit button: does it show loading state during submission?
- Required fields: are they marked with `*` or `required`?

Flag placeholder-only labels as HIGH (accessibility violation).

---

**4. Loading state audit**

Search for async patterns: `fetch(`, `await`, `useEffect`, `useMutation`, `callAI`:

- Is there a loading indicator (spinner, skeleton, "Loading..." text)?
- Are there empty/blank states while data loads?
- For lists: is there an empty state ("No items found") vs loading state?

Flag any async data fetch without a loading indicator as MEDIUM.

---

**5. Error handling audit**

Search for `catch`, `.catch`, `onError`, `error`, `isError`:

- Are errors shown to the user? (not just `console.error`)
- Is the error message user-friendly? (not raw error objects)
- Is there a recovery action (retry button, back link)?

Flag `console.error` without user-facing feedback as MEDIUM.

---

**6. Accessibility audit**

Check all files in scope:

- `<img` without `alt` → HIGH
- `<button` or clickable `<div` without text content or `aria-label` → HIGH
- `onClick` on non-interactive elements (`<div`, `<span`) without `role="button"` and `tabIndex` → MEDIUM
- Color contrast: flag any hardcoded color values and note they should be checked (can't auto-verify contrast ratios)
- `<a` without `href` → MEDIUM

---

**7. Responsive audit**

Search for:
- Hardcoded pixel widths on containers (`width: 800px`, `width: "800px"`) → flag, should use max-width or responsive units
- Tables without responsive treatment (no mobile card view or horizontal scroll wrapper)
- Missing viewport meta tag in index.html

---

**8. Summary**

```
## Style Check

Workspace guide: your project's STYLE_GUIDE.md
Project guide: <path or "none">

### Findings by severity

HIGH (must fix):
- [ ] <finding> — <file:line>
- ...

MEDIUM (should fix):
- [ ] <finding> — <file:line>
- ...

LOW (consider):
- [ ] <finding> — <file:line>
- ...

### Category breakdown
| Category | Issues |
|---|---|
| Button behavior | N |
| Form behavior | N |
| Loading states | N |
| Error handling | N |
| Accessibility | N |
| Responsive | N |

### Top 3 priority fixes
1. <specific fix with file:line>
2. <specific fix with file:line>
3. <specific fix with file:line>

Verdict: PASS / WARN / FAIL
```
