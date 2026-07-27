---
name: ux-psych-audit
description: Audit an onboarding, signup, or conversion flow against 17 UX psychology principles (7 core — smart defaults, goal-gradient, reciprocity, IKEA, endowment, loss aversion, contrast — plus 10 Laws of UX) and a dark-pattern watch tier. Complements /style-check (component hygiene) by judging whether the flow is designed for how people actually decide.
allowed-tools: [Read, Grep, Glob]
version: 0.1.0
---

Audit a signup / onboarding / paywall / conversion flow against 7 behavioural-design
principles. This is a **flow-level** audit (does the experience respect how users decide),
not a component-hygiene audit — pair it with `/style-check` for the latter.

Source: the 7 principles distilled from UXPeak, "The UX Psychology Behind Apps People
Can't Stop Using". Each principle below has a **greppable failure signal** plus a
**manual-review question** for the parts code can't confirm (copy, framing, sequencing).

Do the following steps in order.

---

**1. Scope the flow**

- Ask (or infer from the request) which flow to audit: signup, onboarding, paywall/upgrade,
  or a specific conversion funnel.
- Locate the relevant files: `Glob` for `**/{onboard,signup,register,welcome,paywall,upgrade,pricing,auth,login}*.{jsx,tsx,js,ts,vue,svelte}`.
- If nothing matches, ask the user for the entry component/route.
- Report: "Auditing flow: <name> — files: <list>".

---

**2. Smart Defaults — reduce decision fatigue**

Principle: 70–90% of users never change a default; a default reads as a recommendation.

Grep signals (in the flow's forms):
- `<select>` / `<Select` with no `defaultValue` / `value=` / `selected` option → HIGH (user forced to choose from scratch).
- Radio groups (`type="radio"`, `<Radio`) with no `defaultChecked` / default `value` → MEDIUM.
- Plan/tier pickers with no pre-selected (e.g. "recommended") option → HIGH on a paywall.

Manual question: Is the *most common / recommended* choice pre-selected, not just any choice?

---

**3. Goal-Gradient — show progress early**

Principle: motivation rises as a goal feels closer; never start the user at 0%.

Grep signals:
- Progress components (`Progress`, `Stepper`, `step`, `currentStep`, `progress`, `%`) whose
  initial value is `0`, `0%`, or step `1 of N` with an empty bar → HIGH.
- Multi-step onboarding with **no** progress indicator at all → MEDIUM.

Manual question: Does step 1 already show ~20% done (e.g. counting "account created" as progress)?

---

**4. Reciprocity — value before the ask**

Principle: give something genuinely useful *before* requesting signup; it creates obligation.

Grep signals (the highest-value check):
- Auth gate firing on mount / before any value: `redirect('/login')`, `redirect('/signup')`,
  `requireAuth`, `<ProtectedRoute`, `getServerSession` + redirect, `if (!user) return <Login`
  at the **entry** of the core experience → HIGH.
- Signup wall rendered before any result/preview component → HIGH.

Manual question: Can a brand-new user see a real, useful result (score, preview, output)
*before* hitting the account wall?

---

**5. IKEA Effect — let them build before signup**

Principle: people value what they helped create; customization pre-signup raises commitment.

Grep signals:
- Personalization inputs (name, goal, preferences, theme, `customize`, `preferences`) that
  appear **only after** auth → MEDIUM (move some before the wall).
- Onboarding that collects nothing from the user before creating the account → LOW/MEDIUM.

Manual question: Does the user shape *something* (a project, profile, goal) before the ask?

---

**6. Endowment Effect — invested time raises perceived value**

Principle: merely having spent time on something makes users value it more (Duolingo pattern).

Grep signals:
- Account creation demanded as **step 1** with no prior interaction → HIGH.
- Core value (lesson, editor, result) locked behind auth with zero pre-auth interaction → HIGH.

Manual question: Has the user invested any effort (completed a lesson/step, generated output)
before being asked to commit?

*(This overlaps with Reciprocity/IKEA — count a shared root cause once, but note all that apply.)*

---

**7. Loss Aversion & Status-Quo Bias — frame the stakes**

Principle: fear of losing outweighs desire to gain; frame around what's at risk.

Grep signals (copy in paywall/upgrade/delete flows):
- Purely gain-framed CTAs: `Get Pro`, `Upgrade now`, `Unlock features` with **no**
  loss/risk framing → MEDIUM (note as an A/B opportunity, not a hard bug).
- Data-loss / cancellation moments with no "what you'll lose" messaging or grace/undo → MEDIUM.

Manual question: At the decision point, is the message "here's what you'll lose" rather than
only "here's what you'll get"? (Use honestly — dark-pattern framing is out of scope; see Ethics.)

---

**8. Contrast Effect — anchor the offer**

Principle: value is judged relative to a nearby reference point.

Grep signals (pricing/paywall):
- A single price shown with no anchor (no crossed-out original, no adjacent higher tier,
  no "$X/mo billed yearly" comparison) → LOW/MEDIUM.
- Discounts stated as absolute only, never relative (e.g. "$50 off" with no % or ratio) → LOW.

Manual question: Is each price positioned next to a reference that makes it feel small/fair?

---

**8b. Extended principles — Laws of UX (all have greppable signals)**

Audit these alongside the core 7. Each is a codified heuristic (lawsofux.com / NN/g).

- **Hick's Law** — decision time grows with choice count. Signal: a `<form>` with >7 interactive
  controls, or a nav/plan picker with >7 ungrouped siblings, or 3+ SSO buttons beside a full
  email form with no visual primary path → MEDIUM.
- **Miller's Law** — working memory ≈ 7±2. Signal: single `<form>` with >7 `<input>` and no
  `<fieldset>` grouping; long numeric inputs (phone/card/OTP) with no chunking / missing
  `inputmode`/`autocomplete` → MEDIUM.
- **Doherty Threshold** — keep response <400ms. Signal: `onSubmit`/`onClick` calling
  `fetch`/`await` in a component with no `isLoading`/`isPending`/spinner/skeleton, or button
  not disabled in-flight (also a double-submit) → HIGH.
- **Von Restorff (Isolation)** — the standout is remembered/clicked. Signal: 2+ elements sharing
  the same primary class (`btn-primary`, `variant="primary"`) in one view; all buttons identical → MEDIUM.
- **Zeigarnik Effect** — unfinished tasks pull to completion. Signal: wizard with
  `step`/`currentStep` state but no `ProgressBar`/`Stepper`/"Step X of Y" → MEDIUM. (Pairs with Goal-Gradient.)
- **Fitts's Law** — target speed scales with size/proximity. Signal: tap targets <44px,
  control `font-size` <12px, icon-only buttons with no min-size; primary CTA far from the field
  it submits → MEDIUM.
- **Tesler's Law** — complexity is conserved; absorb it for the user. Signal: required fields with
  no `autocomplete=`, manual "confirm email" fields, no `defaultValue`/session prefill, manual
  country/timezone selectors with no auto-detect → MEDIUM.
- **Jakob's Law** — users expect conventions. Signal: password field before email in DOM order;
  auth entry only in footer/hamburger; custom `<div onClick>` replacing native `<select>`/checkbox → LOW/MEDIUM.
- **Aesthetic-Usability** — polish is perceived as usability. Signal: `<input>`/`<button>` with no
  class/style in onboarding routes; default browser-styled forms top-of-funnel → LOW.
- **Serial Position** — first/last are best remembered. Signal: "recommended"/primary item at a
  middle index in a nav or pricing-tier array → LOW.

---

**8c. Dark-pattern watch tier (audit for MISUSE, not absence)**

These persuade and are easily abused. Do **not** flag their absence — flag deceptive *presence*.

- **Social Proof** — hardcoded counts (`"10,000+ users"`, constant `rating={5}`), fake
  live-activity ("someone in London just signed up") → DARK PATTERN. Genuine counts must map to a real source.
- **Anchoring** — `<del>`/`line-through` "original" price that was never actually charged →
  DARK PATTERN (illegal in many jurisdictions). Real struck-through prices are fine.
- **Hooked / Investment loop** — infinite-scroll with no stopping cue, anxiety-based streaks,
  post-signup dead-ends with no next-action → flag (missing stop cue = MEDIUM; manipulative loop = DARK PATTERN).
- **Commitment & Consistency** — a small early commitment silently escalating into hidden billing
  ("roach motel") → DARK PATTERN. A low-friction first step before signup is the *honest* version.
- **Labor Illusion** — fake `setTimeout` delay simulating work that's actually instant → DARK PATTERN.
  Real staged progress ("Checking availability…") for genuinely slow ops is fine.

---

**9. Ethics gate (mandatory)**

These principles persuade; they can slide into dark patterns. For every finding, confirm the
recommended fix is **honest**: real value in reciprocity, truthful loss-aversion (no fake
scarcity/countdowns), genuine defaults (not pre-checked upsells). Flag any *existing* code that
already crosses into manipulation (fake urgency, pre-ticked paid add-ons, confirm-shaming) as
HIGH under a **DARK PATTERN** label — that's a fix-to-remove, not a fix-to-add.

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
| Hick's / Miller's | ✅ / ⚠️ / ❌ | choice count / chunking |
| Doherty | ✅ / ⚠️ / ❌ | <400ms feedback |
| Von Restorff | ✅ / ⚠️ / ❌ | one dominant CTA |
| Zeigarnik | ✅ / ⚠️ / ❌ | progress cue |
| Fitts's | ✅ / ⚠️ / ❌ | target size/proximity |
| Tesler's | ✅ / ⚠️ / ❌ | prefill/auto-detect |
| Jakob's / Aesthetic / Serial | ✅ / ⚠️ / ❌ | conventions/polish/order |
| Dark-pattern watch | ✅ clean / ❌ found | misuse of proof/anchor/loop |

### Top 3 highest-leverage changes
1. <specific change with file:line and which principle it unlocks>
2. ...
3. ...

Verdict: PASS / WARN / FAIL
```

Notes on judgement:
- Weight **Reciprocity, Goal-Gradient, and Endowment** highest — they drive activation/retention most.
- Many signals are heuristic; when a grep can't confirm intent, report it as a *manual-review*
  item rather than a hard failure, mirroring how `/style-check` handles colour contrast.
