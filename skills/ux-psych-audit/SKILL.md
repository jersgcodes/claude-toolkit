---
name: ux-psych-audit
description: Audit an onboarding, signup, or conversion flow against 17 UX psychology principles (7 core — smart defaults, goal-gradient, reciprocity, IKEA, endowment, loss aversion, contrast — plus 10 Laws of UX) and a dark-pattern watch tier. Complements /style-check (component hygiene) by judging whether the flow is designed for how people actually decide.
allowed-tools: [Read, Grep, Glob]
version: 0.2.0
---

Audit a signup / onboarding / paywall / conversion flow against 7 behavioural-design
principles. This is a **flow-level** audit (does the experience respect how users decide),
not a component-hygiene audit — pair it with `/style-check` for the latter.

Source: the 7 principles distilled from UXPeak, "The UX Psychology Behind Apps People
Can't Stop Using". Each principle has a **greppable failure signal** plus a
**manual-review question** for what code can't confirm (copy, framing, sequencing).

Do the following steps in order.

---

**1. Scope the flow**

- Determine which flow to audit: signup, onboarding, paywall/upgrade, or a specific funnel.
- Locate files: `Glob` for `**/{onboard,signup,register,welcome,paywall,upgrade,pricing,auth,login}*.{jsx,tsx,js,ts,vue,svelte}`.
- If nothing matches, ask for the entry component/route.
- Report: "Auditing flow: <name> — files: <list>".

---

**2. Smart Defaults — reduce decision fatigue**

70–90% of users never change a default; a default reads as a recommendation.
- `<select>` / `<Select` with no `defaultValue` / `value=` / `selected` → HIGH.
- Radio groups with no `defaultChecked` / default value → MEDIUM.
- Plan/tier picker with no pre-selected "recommended" option → HIGH on a paywall.
- Manual: is the *recommended* choice pre-selected, not just any choice?

---

**3. Goal-Gradient — show progress early**

Never start the user at 0%.
- Progress/`Stepper`/`currentStep`/`%` whose initial value is `0` / `0%` / step 1-of-N with an empty bar → HIGH.
- Multi-step onboarding with no progress indicator → MEDIUM.
- Manual: does step 1 already show ~20% (count "account created" as progress)?

---

**4. Reciprocity — value before the ask** (highest-value check)

Give something useful *before* requesting signup.
- Auth gate firing on mount/before value: `redirect('/login')`, `requireAuth`, `<ProtectedRoute`,
  `if (!user) return <Login`, `getServerSession` + redirect at the entry of the core experience → HIGH.
- Signup wall rendered before any result/preview → HIGH.
- Manual: can a new user see a real, useful result before the account wall?

---

**5. IKEA Effect — let them build before signup**

- Personalization inputs (name, goal, preferences, `customize`) available **only after** auth → MEDIUM.
- Onboarding that collects nothing before creating the account → LOW/MEDIUM.
- Manual: does the user shape *something* before the ask?

---

**6. Endowment Effect — invested time raises value**

- Account creation demanded as step 1 with no prior interaction → HIGH.
- Core value locked behind auth with zero pre-auth interaction → HIGH.
- Manual: has the user invested effort before being asked to commit?
- (Overlaps Reciprocity/IKEA — count a shared root cause once, note all that apply.)

---

**7. Loss Aversion & Status-Quo Bias — frame the stakes**

- Purely gain-framed CTAs (`Get Pro`, `Upgrade now`, `Unlock`) with no loss/risk framing → MEDIUM (A/B opportunity).
- Data-loss / cancellation moments with no "what you'll lose" messaging or undo/grace → MEDIUM.
- Manual: is the message "here's what you'll lose" not only "here's what you'll get"?

---

**8. Contrast Effect — anchor the offer**

- Single price with no anchor (no crossed-out original, no adjacent tier, no yearly comparison) → LOW/MEDIUM.
- Discount stated absolute-only, never relative → LOW.
- Manual: is each price next to a reference that makes it feel small/fair?

---

**8b. Extended principles — Laws of UX (all greppable)**

- **Hick's Law** — `<form>` >7 controls, or nav/plan picker >7 ungrouped siblings, or 3+ SSO + full email form with no primary path → MEDIUM.
- **Miller's Law** — single `<form>` >7 `<input>` with no `<fieldset>`; long numeric inputs with no chunking / missing `inputmode`/`autocomplete` → MEDIUM.
- **Doherty (<400ms)** — async `onSubmit`/`onClick` with no `isLoading`/spinner/skeleton, or button not disabled in-flight → HIGH.
- **Von Restorff** — 2+ elements with same primary class in one view; all buttons identical → MEDIUM.
- **Zeigarnik** — wizard with `step`/`currentStep` but no progress/"Step X of Y" → MEDIUM.
- **Fitts's** — tap targets <44px (48px for buttons, 8px gap), control `font-size` <12px, icon-only no-min-size; CTA far from its field → MEDIUM.
- **Tesler's** — required fields no `autocomplete=`, "confirm email" fields, no session prefill, manual country/timezone with no auto-detect → MEDIUM.
- **Jakob's** — password before email in DOM; auth only in footer/hamburger; custom `<div onClick>` replacing native controls → LOW/MEDIUM.
- **Aesthetic-Usability** — unstyled `<input>`/`<button>` in onboarding routes; default browser forms → LOW.
- **Serial Position** — "recommended"/primary item at a middle index of a nav/pricing array → LOW.

---

**8c. Dark-pattern watch (audit for MISUSE, not absence)**

- **Social Proof** — hardcoded counts, constant `rating={5}`, fake live-activity → DARK PATTERN.
- **Anchoring** — `line-through` "original" price never actually charged → DARK PATTERN.
- **Hooked** — infinite-scroll no stop cue / anxiety streaks / post-signup dead-end → MEDIUM or DARK PATTERN.
- **Commitment** — small commitment escalating into hidden billing (roach motel) → DARK PATTERN.
- **Labor Illusion** — fake `setTimeout` faking work that's instant → DARK PATTERN.

---

**9. Ethics gate (mandatory)**

These principles persuade and can slide into dark patterns. Every recommended fix must be
**honest**: real value in reciprocity, truthful loss-aversion (no fake scarcity/countdowns),
genuine defaults (not pre-checked upsells). Flag existing manipulation (fake urgency,
pre-ticked paid add-ons, confirm-shaming) as HIGH under a **DARK PATTERN** label — remove, don't add.

---

**10. Summary**

```
## UX Psychology Audit

Flow audited: <name>
Files: <list>

### Findings by severity
HIGH (must fix):
- [ ] <principle> — <finding> — <file:line>
MEDIUM (should fix):
- [ ] <principle> — <finding> — <file:line>
LOW (consider / A-B test):
- [ ] <principle> — <finding> — <file:line>
DARK PATTERN (remove):
- [ ] <finding> — <file:line>

### Principle scorecard
| Principle | Status | Note |
|---|---|---|
| Smart Defaults | ✅ / ⚠️ / ❌ | |
| Goal-Gradient | ✅ / ⚠️ / ❌ | |
| Reciprocity | ✅ / ⚠️ / ❌ | |
| IKEA Effect | ✅ / ⚠️ / ❌ | |
| Endowment | ✅ / ⚠️ / ❌ | |
| Loss Aversion | ✅ / ⚠️ / ❌ | |
| Contrast | ✅ / ⚠️ / ❌ | |

### Top 3 highest-leverage changes
1. <specific change with file:line and which principle it unlocks>
2. ...
3. ...

Verdict: PASS / WARN / FAIL
```

Weight Reciprocity, Goal-Gradient, and Endowment highest — they drive activation/retention most.
When a grep can't confirm intent, report it as a manual-review item, not a hard failure
(mirroring how /style-check handles colour contrast).
