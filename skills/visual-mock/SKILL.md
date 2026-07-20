---
name: visual-mock
description: Generate a static HTML mockup to preview a UI design in the browser BEFORE committing to React/Vue/Svelte components. Bridges ASCII sketch → real implementation.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
version: 0.1.0
---



# Visual Mock

Generates a self-contained HTML file you can open in the browser to validate a layout/component design before writing framework-specific code. Inspired by Superpowers' "Visual Companion" pattern but lighter — one HTML file, no infrastructure.

The goal: close the gap between *design doc* (ASCII sketch, props table) and *built component* (JSX with state). A 5-minute browser preview catches what the sketch misses.

---

## When to use

| Situation | Use? |
|---|---|
| New page/component where you're unsure how it'll feel | YES |
| Comparing 2-3 layout options before committing | YES |
| Showing a non-technical reviewer (client, friend) what you're building | YES |
| Already have a working component — just want a code change | NO — edit the real component |
| Pure logic component (no visual output) | NO — `/component-design` covers it |

---

## Stage 1 — Frame the mock

Ask (or extract from `$ARGUMENTS`):

1. **What's the screen/component?** (e.g. "user profile card", "settings page", "checkout form")
2. **Source of design intent?** (`/component-design` doc? `/responsive-design` sketch? `/feature-design` plan?)
3. **What's the most uncertain part?** (Layout? Colors? Hierarchy? Empty state?)
4. **Single mock or comparison set?** (One file with one option vs one file with 2-3 side-by-side)
5. **Mobile, desktop, or both?** (If both, render side-by-side at different widths)

If there's an existing design doc (e.g. `docs/components/ProfileCard.md`), read it and base the mock on those decisions. Don't invent new design from scratch.

---

## Stage 2 — Choose the styling approach

Pick the cheapest path that gives realistic preview:

| Approach | When | Pros / cons |
|---|---|---|
| **Tailwind CDN** | Default — fastest | Inline `<script src="https://cdn.tailwindcss.com">`, no build, design tokens via Tailwind classes. Slightly off-spec for production but visually accurate enough. |
| **Plain CSS embedded** | Workspace `design-tokens.yaml` exists and you want to honour it precisely | Hand-write CSS variables from the tokens file, more accurate to final output |
| **Project's actual CSS** | Project already has a CSS bundle | `<link rel="stylesheet" href="../actual/styles.css">` — pixel-accurate but requires the project to be built |

**Default to Tailwind CDN** unless the project has strong existing tokens.

---

## Stage 3 — Use workspace design tokens

If `~/claude/design-tokens.yaml` exists, read it and use those palette / type / spacing choices. Don't pick arbitrary colors. The workspace standard wins over your aesthetic instincts.

If the project has its own `STYLE_GUIDE.md` or `design-tokens.json`, project tokens override workspace tokens.

---

## Stage 4 — Write the HTML

Create `mockups/<feature-name>.html` at the project root (create `mockups/` if needed, add to `.gitignore` if you don't want to track it).

> **Reference:** Full HTML scaffold template for this stage is in `references/visual-mock-ref.md`.

Critical rules for the HTML:

- **Self-contained** — one file, no asset dependencies (use inline SVG, placeholder data)
- **Multiple states visible** — render loading, empty, error, success side-by-side in the same file
- **Realistic content** — use domain-appropriate placeholder text, not "Lorem ipsum"
- **Annotate uncertainty** — yellow note boxes calling out unresolved design questions
- **Multiple sizes if responsive** — wrap each in a width-constrained container so user sees mobile + desktop at once

---

## Stage 5 — Render all states

For each state from `/component-design`'s state checklist, draw a mini section.

> **Reference:** HTML section code blocks for Loading / Success / Empty / Error states are in `references/visual-mock-ref.md`.

Seeing all states in one scroll forces you to design them all, not just the happy path.

---

## Stage 6 — Annotate uncertainties

Add yellow note boxes inline next to anything still undecided.

> **Reference:** Annotation `<aside>` snippet is in `references/visual-mock-ref.md`.

These annotations become the questions you ask the user (or yourself) before committing to code.

---

## Stage 7 — Open in browser, get feedback

After writing the file:

```bash
# macOS — opens in default browser
open mockups/<feature>.html
```

What to look for (5-minute walkthrough):
- Hierarchy clear at a glance?
- Touch targets look ≥ 44px on the mobile-width container?
- Color contrast OK? (eyeball test — `/a11y-audit` for the real check later)
- Empty state inviting, not punishing?
- Error state offers a way out, not just "something went wrong"?
- Loading skeleton matches the shape it's replacing?

If the mock surfaces an issue, edit the HTML directly — it's cheap. Iterate until the mock "feels right." Then build the real component using `/component-design` + `/tdd`.

---

## Stage 8 — Decide: keep or discard?

After feedback, two paths:

**A — Discard:** the mock served its purpose. Delete the file. The design doc captures the decisions.

**B — Keep:** add to `mockups/` directory and link from the project's `docs/components/<Name>.md` so future-you can find it.

Add a line to `.gitignore` if you decide mocks are throwaway:

```
# Visual mocks — local design artifacts
mockups/
```

Or commit if they're useful reference.

---

## Worked example

> **Reference:** Full worked example (ProjectCard walk-through) is in `references/visual-mock-ref.md`.

---

## Cost control

- Output is a single HTML file — bounded, no recursion
- Tailwind CDN is free and CDN-cached
- Don't read the project's full codebase — only the design docs that informed the mock
- Reuse Tailwind classes; don't invent custom CSS for things Tailwind covers

---

## Integration

- Pulls from: `/component-design`, `/responsive-design` (the design docs), `/feature-design` (the plan)
- Hands off to: real component build (likely `/tdd` for logic, `/style-check` after for visual identity)
- Outputs feed: `/a11y-audit plan` (mock can be a11y-audited too)
- Reads: `~/claude/design-tokens.yaml`, project-level `STYLE_GUIDE.md`

---

## Anti-patterns to flag

- **Mock that becomes production** — same trap as `/spike`. HTML mock has no logic, no tests, no state — never just "convert to JSX and ship"
- **One state only** — happy path only is the classic mistake; designs fail in their unhappy states
- **Lorem ipsum** — fake content hides real layout problems (long names, empty fields, edge cases)
- **No mobile width** — desktop-only mock misses 60% of the truth
- **Don't open in browser** — Claude can't see the rendering; you have to
- **Generic AI-style design** — rounded cards, gradient buttons, blue everywhere — use `/visual-mock` to *escape* defaults, not reproduce them
