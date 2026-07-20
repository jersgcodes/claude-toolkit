---
name: a11y-audit
description: Accessibility audit against WCAG 2.1 AA. Two modes — pre-build planning (design intent) or post-build verification (existing component/page). Extends /style-check with depth.
allowed-tools: [Read, Glob, Grep, Bash]
version: 0.1.0
---



# Accessibility Audit

WCAG 2.1 AA compliance check. Use at design time (intent) AND at audit time (verification). `/style-check` covers the lighter pass against your workspace UX style guide; this one goes deeper into WCAG specifics.

Sources: WCAG 2.1 (W3C), WebAIM accessibility checklist, A11y Project, Deque University guides, Inclusive Components by Heydon Pickering.

---

## Modes

| Mode | When | What it does |
|---|---|---|
| **plan** (default for new work) | Before writing components/screens | Walks WCAG criteria as design questions, produces an a11y checklist for the feature |
| **audit** | After build, before deploy | Scans code for known patterns, flags violations |

Use `/a11y-audit plan <feature>` or `/a11y-audit audit <path>`.

---

## WCAG 2.1 — the four principles (POUR)

Every check maps to one of:

| Principle | Means | Examples |
|---|---|---|
| **P**erceivable | User can perceive the info | Contrast, alt text, captions |
| **O**perable | User can interact | Keyboard nav, no time traps, sufficient touch targets |
| **U**nderstandable | User can comprehend | Predictable behavior, clear errors |
| **R**obust | Works with assistive tech | Valid HTML, ARIA correctness |

---

## Stages 1–4 — POUR checklists

> **Reference:** the full WCAG 2.1 AA checklists for Stages 1–4 (Perceivable, Operable, Understandable, Robust) are in `references/a11y-checklist-ref.md` — read it before working through any stage.

---

## Stage 5 — Audit tooling (if mode == audit)

Run automated checks alongside manual review. Automated catches ~30% of issues — humans needed for the rest.

```bash
# axe-core via CLI (Node-based)
npx @axe-core/cli https://yourapp.com

# Lighthouse a11y category
npx lighthouse https://yourapp.com --only-categories=accessibility --output=json --output-path=./lighthouse-a11y.json

# Pa11y
npx pa11y https://yourapp.com

# For local dev (no live URL):
# Install browser extension: axe DevTools, WAVE, or use Lighthouse in DevTools
```

For each tool output, group findings by severity:
- **Critical** (legal/compliance risk, blocks users with assistive tech): fix before deploy
- **Serious** (significant barrier, fix this week)
- **Moderate** (annoying, fix this sprint)
- **Minor** (nice-to-have)

---

## Stage 6 — Manual checks the tools can't do

Automated tools miss these — must be manually verified:

- [ ] **Keyboard-only walkthrough** — unplug mouse, navigate the entire feature with Tab/Enter/Space/Esc
- [ ] **Screen reader test** — VoiceOver (Cmd+F5 on Mac) or NVDA (Windows), navigate the feature
- [ ] **Zoom test** — Cmd+Plus to 200%, check no content lost
- [ ] **High contrast mode** — Mac: System Settings → Accessibility → Display → Increase Contrast
- [ ] **Touch test** — actual phone, not just narrow window
- [ ] **Slow connection** — DevTools throttle to Slow 3G, confirm loading states show

---

## Stage 7 — Report

```markdown
# A11y Audit: <feature/page>

**Date:** YYYY-MM-DD
**Standard:** WCAG 2.1 AA
**Mode:** plan | audit
**Auditor:** <you>

## Summary
- <N> critical issues
- <N> serious issues
- <N> moderate issues
- <N> minor issues

## Critical (block deploy)

### <Issue 1>
- WCAG criterion: 1.4.3 Contrast (Minimum)
- Location: button.submit in src/components/Submit.tsx
- What's wrong: button text contrast is 3.2:1 against background
- How to fix: change button background from #777 to #595959 OR text from #fff to a darker base

## Serious / Moderate / Minor
[same format]

## Manual checks passed
- [x] Keyboard walkthrough
- [x] VoiceOver navigation
- ...

## Open questions
- ...
```

Save audits to `docs/a11y/YYYY-MM-DD-<feature>.md`.

---

## Cost control

- Audit mode reads HTML/JSX/CSS — cap at 20 files per run, prioritize entry points
- Plan mode is a checklist walk, low token use
- For full-site audits, run per page/route in separate sessions

---

## Integration

- Pulls from: `/feature-design` (a11y considered at design time), `/component-design` (component-level a11y already partially covered)
- Hands off to: TASKS.md (fix items by severity), `/decision-record` (capture a11y trade-offs if any)
- Related: `/style-check` (overlaps on visual identity), `/mobile-audit` (overlaps on touch targets)

---

## Anti-patterns to flag

- **`outline: none` without replacement** — kills keyboard focus indicator
- **Placeholder-as-label** — disappears on focus, screen readers don't always announce
- **`<div onclick>` instead of `<button>`** — loses keyboard, focus, role for free
- **Color as the only signal** — red text without an icon, "click the green button" instructions
- **Tiny touch targets** — under 44×44 px on mobile
- **`aria-label` that doesn't match visible text** — confuses screen readers
- **Modals without focus trap** — keyboard users escape to background
- **Skip links missing** — keyboard users tab through every nav item on every page
- **Hover-only tooltips** — keyboard/touch users never see them
- **Auto-playing media with audio** — disorienting and accessibility-failing
- **Generic link text** ("click here") — screen reader users browse by link list
