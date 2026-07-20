---
name: component-design
description: Design a UI component's API before writing code. Props shape, state vs derived, composition, slots, controlled vs uncontrolled, and empty/error/loading state checklist.
allowed-tools: [Read, Glob, Grep, Write]
version: 0.1.0
---



# Component Design

Design the *shape* of a UI component before writing JSX/TSX. The goal is to lock the props API and the state model so the component is reusable, testable, and doesn't grow accidental coupling.

Applies to: React, Vue, Svelte, Astro components, Web Components. Examples here use React, but the principles transfer.

Sources: Kent C. Dodds on component design, *Refactoring UI* (Adam Wathan + Steve Schoger), React docs on "Thinking in React", Brad Frost's *Atomic Design*.

---

## When to use

| Situation | Use? |
|---|---|
| New component that other components will use | YES |
| Component with > 4 props | YES |
| Component that handles user input | YES |
| Component that fetches/displays remote data | YES |
| One-off layout wrapper used in one place | NO |
| Bug fix to existing component | NO |

---

## Stage 1 — Frame the component

Ask:

1. **What does it do?** (One sentence. If it takes more, split the component.)
2. **What's its single responsibility?** (Display? Input? Layout? Behavior trigger? Mix is a smell.)
3. **Who renders it?** Where in the tree?
4. **How many times will it appear on one screen?** (0..1, 0..N, exactly 1)
5. **Does it own state, or is it pure presentational?**

If the answer to "what does it do" needs "and" — split. e.g. "Shows the user's name AND lets them edit it" → split into `UserName` + `UserNameEditor`.

---

## Stage 2 — Decide the API shape

### Props vs Context vs Composition

| When | Use |
|---|---|
| Direct parent passes data | Props |
| Many descendants need same data, no intermediate cares | Context |
| Parent wants to customize what's inside | Slots / children / render props |
| Parent doesn't know the structure | Composition (compound components) |

### Controlled vs Uncontrolled

For input components (text fields, toggles, etc.):

| Pattern | When to use |
|---|---|
| **Uncontrolled** (`defaultValue`) | Form-level state, no per-keystroke logic needed |
| **Controlled** (`value` + `onChange`) | Parent needs to validate, transform, or react per change |
| **Hybrid** (`defaultValue` + `onChange`) | Common for inputs that mostly self-manage but report changes |

Default to controlled — it's more flexible. Add uncontrolled mode if forms become noisy.

### Compound components (advanced)

For components with related parts (like `Select` with `Option`):

```jsx
<Select value={...} onChange={...}>
  <Select.Option value="a">A</Select.Option>
  <Select.Option value="b">B</Select.Option>
</Select>
```

Use when:
- Parts are tightly coupled but parent wants to choose which/order
- Avoids props explosion (`options={...}`, `renderOption={...}`)

---

## Stage 3 — Sketch the props

Write a TypeScript interface (even if your project is JS — the type sketch forces clarity):

> **Reference:** TypeScript Props interface example for this stage is in `references/component-design-ref.md`.

Naming rules:
- Booleans: `isX`, `hasX`, `canX` — never `loading`/`disabled` alone (use `isLoading`, `isDisabled`)
- Callbacks: `onX` (DOM-style), never `handleX`
- Multi-state: enum string union, not multiple booleans
- Variants: limited set, not arbitrary CSS overrides
- Required vs optional: lean toward required; make optional only if there's a sensible default

---

## Stage 4 — State model

For each piece of state in this component, classify:

| Class | Examples | Where it lives |
|---|---|---|
| Server state | User's profile, list of orders | TanStack Query / SWR / lifted to parent + props |
| URL state | Current page, filters, search query | URL params (router) |
| Form state | Input values, validation errors | useState or react-hook-form |
| UI state | Modal open, accordion expanded | useState |
| Derived | "Has unsaved changes" computed from form vs initial | Computed inline, NOT state |

**Default to deriving, not storing.** If a value can be computed from existing state/props, don't store it separately.

---

## Stage 5 — The states checklist (CRITICAL — most-forgotten step)

Every component that displays data must handle ALL of these. Sketch each:

> **Reference:** States table (11 rows) and interactive state notes for this stage are in `references/component-design-ref.md`.

If you can't describe what the user sees in any state, the design isn't done.

---

## Stage 6 — Composition examples

For each major prop/state combination, sketch how it's used. ASCII or pseudo-JSX:

> **Reference:** Composition pseudo-JSX examples for this stage are in `references/component-design-ref.md`.

If a use case feels awkward (lots of conditional props, mutually exclusive booleans), refactor the API.

---

## Stage 7 — Accessibility

For a11y requirements, run `/a11y-audit plan <component>` after this stage.

---

## Stage 8 — Write the design doc

Save to `docs/components/<ComponentName>.md`:

> **Reference:** Doc template for this stage is in `references/component-design-ref.md`.

---

## Stage 9 — Validate before coding

- [ ] Single responsibility (Stage 1 description in one sentence)
- [ ] No more than 7 props (8+ is a smell — extract sub-components or use composition)
- [ ] All booleans use `is/has/can` prefix
- [ ] All callbacks named `onX`
- [ ] Every displayed state has a sketch
- [ ] Every interactive state (hover/focus/active/disabled) considered
- [ ] Accessibility checklist confirmed
- [ ] No mutually exclusive boolean props (use enum union instead)
- [ ] Slot/composition pattern chosen over render props where possible

---

## Cost control

- Reads neighbour components to infer conventions — cap at 5
- Output is design doc, not implementation
- For a large form/page, design as a composition of sub-components, each via `/component-design`

---

## Integration

- Pulls from: `/feature-design` (UI feature → component sketch)
- Hands off to: `/tdd` (implementation), `/a11y-audit` (post-build verification), `/style-check` (visual identity check), `/responsive-design` (layout planning if needed)
- Outputs feed: `/decision-record` (capture component API choices)

---

## Anti-patterns to flag

- **God components** — `<UserDashboard />` doing fetching, layout, business logic, and rendering
- **Boolean props for state machines** — `isLoading + isError + isSuccess + isIdle` (4 booleans, 16 combos, most invalid)
  - Fix: single `status: 'idle' | 'pending' | 'error' | 'success'`
- **Anonymous render props** — `<Foo render={(x) => ...} />` when composition would do
- **Skipping empty/error/loading state** — only the happy path designed
- **`disabled` without explanation** — user needs to know WHY (tooltip, helper text)
- **`children` as the only API** — no docstring on what children should be
- **CSS classes leaking** as props (`className="text-red-500"`) instead of variant enum
- **Prop drilling 3+ levels** — sign you need Context or composition
