# component-design-ref.md

Reference material for `/component-design`. Loaded on demand by the skill.

---

## Stage 3 — TypeScript Props interface example

```typescript
interface Props {
  // Data
  user: User;                          // required, the entity
  orders?: Order[];                    // optional, omit if not needed

  // State
  isLoading?: boolean;                 // boolean for binary states
  status?: 'idle' | 'pending' | 'error' | 'success';  // enum for multi-state

  // Behavior callbacks (name as event: onX, never handleX)
  onSubmit?: (data: FormData) => void;
  onCancel?: () => void;

  // Customization (slots)
  header?: ReactNode;
  emptyState?: ReactNode;

  // Variants (not "themes" — specific design system options)
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'secondary' | 'ghost';

  // Accessibility
  'aria-label'?: string;
  'aria-describedby'?: string;
}
```

---

## Stage 5 — States checklist table (all 11 rows)

| State | Trigger | What user sees |
|---|---|---|
| **Initial / first-use** | Component renders with no data ever | Onboarding hint, "Add your first X" CTA |
| **Loading** | Fetch in progress | Skeleton / spinner / progress; not blank |
| **Empty** | Loaded successfully but zero items | Friendly empty state with action |
| **Partial** | Some data, more loading | Show what's there, indicator for more |
| **Error** | Fetch failed | Specific message + retry button |
| **Success** | Data loaded, items exist | The main state — usually all you draw first |
| **Stale** | Showing cached, refresh failed | Show data + subtle "couldn't update" warning |
| **Saving** | Mutation in progress | Disable inputs, show pending indicator |
| **Saved** | Mutation succeeded | Brief confirmation, return to normal |
| **Validation error** | Input invalid | Inline error per field, focus first error |
| **Permission denied** | Auth ok but action not allowed | Clear "you don't have access" — different from generic error |

For an interactive component, also:
- **Hover** — visual change for discoverability
- **Focus** — keyboard focus ring (a11y required)
- **Active / pressed** — touch/click feedback
- **Disabled** — visually distinct, NOT just lower opacity (a11y)

---

## Stage 6 — Composition pseudo-JSX examples

```
// Standard use
<UserCard user={user} />

// Loading state (parent fetches)
<UserCard isLoading />

// With custom action area
<UserCard user={user} actions={<Button>Edit</Button>} />

// Error state — replace, not append
<UserCard error="Failed to load" onRetry={refetch} />
```

---

## Stage 8 — Doc template

```markdown
# Component: UserCard

## Purpose
Single-line description.

## Where used
- src/pages/Profile.tsx
- src/pages/Admin.tsx (with `compact` variant)

## Props

[TypeScript interface from Stage 3]

## States

| State | Trigger | Visual |
|---|---|---|
| ... | ... | ... |

## Composition

[Examples from Stage 6]

## Accessibility

[Checklist results from Stage 7]

## Open questions

- ...
```
