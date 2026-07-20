---
name: mobile-audit
description: Audit a web app for mobile compatibility issues — touch targets, iOS zoom, viewport, hover-only interactions, socket reconnect. Use before shipping or after adding new pages — "mobile audit", "check mobile UX".
allowed-tools: [Read, Grep, Glob]
version: 0.1.0
---



Audit a web app for mobile compatibility issues. Focuses on touch, layout, performance, and input UX on real phones.

Use `$ARGUMENTS` as the target directory if provided (e.g. `client/src`). Default: `client/src`.

---

**Check 1 — Viewport and safe areas**

Read `index.html` (or the main HTML entry point):
- Does `<meta name="viewport">` include `width=device-width, initial-scale=1`?
- Does it include `viewport-fit=cover` for notched phones (iPhone X+)?
- Are safe area insets applied for bottom bars? Search for `safe-area-inset` or `env(safe-area-inset-bottom)` in CSS/Tailwind:
  ```
  grep -rn "safe-area" client/src/ --include="*.tsx" --include="*.css"
  ```
- Flag if bottom action buttons (CTAs, fixed footbars) don't account for home indicator on iPhone.

---

**Check 2 — Touch target sizes**

Search all `.tsx` files for interactive elements: `<button`, `<a `, `onClick`, `onTouchStart`.

For each one, check if it has an explicit size class. Flag any that likely fall below 44×44px:
- Tailwind classes `h-6`, `h-7`, `h-8`, `w-6`, `w-7`, `w-8` on clickable elements → likely too small
- Icon-only buttons with no explicit size → flag for manual check
- Grid items that are tappable (e.g. Codenames 5×5 word grid) → check if `py-2 px-1` gives enough height at small screen sizes

Report pattern: `file:line — element description — likely size (e.g. ~32px) — fix suggestion`

---

**Check 3 — iOS input zoom**

iOS Safari zooms in when a focused `<input>` has `font-size < 16px`. This is jarring in a party game.

Search for all `<input` elements:
```
grep -rn "<input" client/src/ --include="*.tsx"
```

For each input, check if a `text-sm` or `text-xs` class is applied without an explicit `text-base` override. These map to 14px and 12px respectively — both trigger iOS zoom.

Also check: does any input use `type="number"` without `inputMode="numeric"`? The number keyboard on iOS is less ergonomic than the numeric pad.

---

**Check 4 — Hover-only interactions**

Search for `hover:` Tailwind classes on interactive elements that have no touch/active equivalent:
```
grep -rn "hover:" client/src/ --include="*.tsx" | grep -v "active:\|focus:"
```

Flag any `hover:` on elements where the hover state communicates something critical (e.g. hover to reveal, hover to see button label). Pure visual polish hovers (color change) are fine.

Also check: any `onMouseEnter`/`onMouseLeave` handlers with no `onTouchStart` equivalent.

---

**Check 5 — Scroll and overflow**

Search for fixed-height containers that might clip content on small screens:
```
grep -rn "h-screen\|min-h-screen\|overflow-hidden" client/src/ --include="*.tsx"
```

Flag patterns like `h-screen overflow-hidden` on game pages — on iPhone with browser chrome visible, `100vh` is taller than the visible area, causing content to be clipped below the fold.

Check: does the app use `dvh` (dynamic viewport height) or `svh` anywhere? If not, `h-screen` may be unreliable on mobile browsers.

---

**Check 6 — Performance — image loading**

Search for `<img` tags:
```
grep -rn "<img" client/src/ --include="*.tsx"
```

For each `<img`:
- Does it have `loading="lazy"` for below-the-fold images?
- Does it have explicit `width` and `height` to prevent layout shift?
- Are any images hotlinked from external domains (Wikipedia, flagcdn.com, etc.)? Flag these — they may load slowly on mobile data.

---

**Check 7 — Animation performance**

Search for CSS animations or transitions that may cause jank on low-end Android:
```
grep -rn "animate-\|transition-\|transform" client/src/ --include="*.tsx" | grep -v "node_modules"
```

Flag:
- `animate-pulse` / `animate-spin` on many elements simultaneously (battery drain)
- Transitions on `width`, `height`, `top`, `left` — these trigger layout reflow. Prefer `transform` and `opacity`
- Any `transition-all` — catches all properties including expensive ones

---

**Check 8 — Socket reconnect on background tab**

Mobile browsers aggressively suspend background tabs. When a player locks their phone mid-game, the Socket.IO connection drops.

Search for reconnect handling:
```
grep -rn "reconnect\|visibilitychange\|document.hidden" client/src/ --include="*.tsx" --include="*.ts"
```

Check `client/src/contexts/SocketContext.tsx` (or equivalent):
- Does the socket use `reconnection: true` with a reasonable `reconnectionDelay`?
- Is there a `visibilitychange` listener that re-joins the room when the tab becomes active again?
- Does the game UI show a "Reconnecting..." state while disconnected?

Flag if no visibility-based reconnect logic exists — players will silently drop from games when they switch apps.

---

**Check 9 — Keyboard obscuring inputs**

On mobile, the on-screen keyboard pushes the viewport up or resizes it. This can obscure input fields or break fixed-position elements.

Search for pages with both a fixed header/footer AND an `<input` or `<textarea`:
```
grep -rn "fixed\|sticky" client/src/ --include="*.tsx"
```

Cross-reference with pages that have inputs (Codenames clue input, Charades chain guess, GuessPerson text input). Flag if a fixed bottom bar + input exist on the same page — the keyboard may cover the submit button.

---

**Report format:**

```
## Mobile Audit

### Check 1 — Viewport
✅ viewport meta correct / 🟡 missing viewport-fit=cover / 🔴 missing viewport meta

### Check 2 — Touch targets
🔴 file:line — IconButton has w-6 h-6 (~24px) — add p-2 or min-w-[44px] min-h-[44px]
🟡 Codenames grid cards: py-2 px-1 on 5-col grid — ~38px tall at 375px width, borderline

### Check 3 — iOS input zoom
🔴 file:line — <input className="text-sm"> — add text-base (16px) to prevent iOS zoom

### Check 4 — Hover-only
🟡 file:line — hover:bg-primary on word card — add active:bg-primary for touch feedback

### Check 5 — Scroll/overflow
🟡 N pages use h-screen — consider switching to h-[100dvh] for mobile browser compatibility

### Check 6 — Images
🟡 ImageQuiz: external URLs (Wikipedia) — may be slow on mobile data, consider caching

### Check 7 — Animations
🟢 No layout-triggering transitions found
🟡 animate-pulse used in N places simultaneously

### Check 8 — Socket reconnect
🔴 No visibilitychange listener — players who switch apps will silently drop from games

### Check 9 — Keyboard + inputs
🟡 Codenames: fixed header + clue input on same page — test that keyboard doesn't obscure Submit button

### Summary
- 🔴 Critical (breaks experience): N
- 🟡 Warning (degrades experience): N
- 🟢 OK: N

### Priority fixes
1. ...
2. ...
```
