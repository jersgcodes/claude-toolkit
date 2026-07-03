---
name: seams
description: Find seams in untested code (Feathers). Identifies safe injection points to add behavior or characterization tests without changing existing logic.
version: 0.1.0
---


# Seams — Working with Legacy Code

Based on Michael Feathers' *Working Effectively with Legacy Code*. Definition: **legacy code = code without tests**, regardless of age.

When you need to add behavior to or change untested code, the riskiest option is "edit it directly and hope." A seam is a **place where you can alter behavior without editing the existing code**. This skill finds seams in your target.

---

## When to use this skill

| Scenario | Run /seams? |
|---|---|
| Adding new behavior to a function with no test | YES |
| Modifying a long function you didn't write | YES |
| Refactoring untested code (`/refactor` flagged it as UNSAFE) | YES |
| Function has tests AND you understand it | NO — just edit |
| Function is < 10 lines and pure | Probably NO — write a test directly |

If your gut says "I might break something I can't see," that's the signal. Run `/seams`.

---

## Step 1 — Identify the target

From `$ARGUMENTS` or ask the user:
1. Which function/method/class do you need to change or extend?
2. What behavior do you want to add or modify?
3. Have you tried running `/test-coverage` on this file? (helps confirm "no test")

Read the target. Note:
- Function signature
- All inputs (params, globals, env vars, file reads, network calls, time, randomness)
- All outputs (return value, mutations, side effects)
- Dependencies imported at module level

---

## Step 2 — Catalog seams

Feathers names six seam types. For each, check if it applies to the target:

### 1. Object Seam (most common in OOP)
**What:** A method call on an object you can replace with a test double.
**Find it:** External dependencies (DB clients, HTTP clients, file handles) passed in or instantiated inside the function.
**Test enable:** Pass a fake object in tests.

### 2. Preprocessing Seam (Python: monkeypatch / mock)
**What:** Replace a function or class at import time, before the real code runs.
**Find it:** Direct module-level imports of side-effecting functions (e.g. `from requests import get`).
**Test enable:** `pytest`'s `monkeypatch` or `unittest.mock.patch`.

### 3. Link Seam
**What:** Swap the implementation at import time via a different module file.
**Find it:** Import statements where you could substitute an alternate module (e.g. driven by env var).
**Test enable:** Less common in Python — prefer Object or Preprocessing seam first.

### 4. Subclass Seam
**What:** Override a method by creating a test subclass.
**Find it:** Methods on classes that aren't final — most Python methods qualify.
**Test enable:** Create a test subclass that overrides the side-effecting method to capture calls instead.

### 5. Parameterize Seam (introduce a parameter)
**What:** Add a parameter to make a hidden dependency explicit.
**Find it:** Hardcoded values, `datetime.now()`, `random.choice()`, `os.environ.get()` inside the function.
**Test enable:** Add `param=None` with `param = param or real_call()` — the one safe edit that unlocks tests.

### 6. Extract Method Seam (last resort, requires care)
**What:** Pull a chunk of the function out so you can test it independently.
**Find it:** Complex functions where you can isolate a pure piece (no side effects in the chunk).
**Test enable:** Write a characterization test FIRST (Step 4) before making this edit.

---

## Step 3 — Recommend the cheapest seam

For each seam type that applies, score:
- **Effort:** how invasive is the change to the existing code? (None = best, Refactor needed = worst)
- **Coverage:** how much of the new behavior can you test through this seam?
- **Risk:** chance of breaking existing behavior

Recommend the cheapest seam that gives adequate coverage. Common ranking:

1. Object Seam (already exists) — zero risk, just write the test
2. Preprocessing Seam (monkeypatch) — zero edit to source, test-only change
3. Subclass Seam — small test-only addition
4. Parameterize Seam — one tiny edit to source (default param)
5. Extract Method Seam — only after a characterization test is in place

---

## Step 4 — Characterization test (if needed)

If no seam exists without editing source code, write a **characterization test** first — a test that captures CURRENT behavior, even if that behavior includes bugs.

Steps:
1. Call the function with realistic input
2. Run it, capture the output
3. Write the test asserting that exact output
4. Now you have a safety net — the test fails the moment you change the function

Example:
```python
def test_legacy_calculate_total_characterization():
    """Captures behavior as of <date> — do NOT change without intent."""
    result = calculate_total([{"price": 10}, {"price": 20}], discount=0.1)
    assert result == 27.0  # captured from running the real function
```

This test makes the function safe to refactor with `/refactor`.

---

## Step 5 — Plan output

```markdown
## Seams Analysis — <target function/file>

### Target: `<function signature>` in `<file:line>`

### Hidden dependencies
- <dependency> at line N — <type: non-deterministic / network / env / DB>

### Seams available
| Type | Location | Effort | Test enables |
|---|---|---|---|
| <type> | <symbol> at line N | Zero / Add param / Subclass | <what it unlocks> |

### Recommended order of operations
- [ ] 1. <cheapest seam> — zero risk
- [ ] 2. <next seam if needed> — <one-line summary of edit>
- [ ] 3. Run /refactor or /tdd to add new behavior
```

---

## Step 6 — Hand-off

After analysis, suggest the next skill:
- If new behavior to add → `/tdd` to implement it test-first using the seam
- If cleanup is the goal → `/refactor` (now safe with characterization test)
- If you found multiple untested files → run `/test-coverage` to prioritize which to seam first

---

## Cost control

- Reads target file fully + grep for callers — moderate token cost.
- Cap analysis to ONE function per invocation. If multiple targets, run separately.
- Do NOT auto-write tests — propose them, let the user run `/tdd` to implement.

---

## Integration

- Pulls from: `/test-coverage` (identifies untested functions to target)
- Hands off to: `/tdd` (write tests through the seam), `/refactor` (now safe to apply transformations)
- Used by: `/refactor` blocks unsafe transformations and points here

---

## Anti-patterns

- **Don't add abstractions you won't reuse.** Parameterize Seam is fine for testability. Don't introduce a full DI container for one test.
- **Don't refactor before testing.** That's the failure mode this skill prevents. Write the characterization test first.
- **Don't seam everything.** Only seam the part you need to change. Untested-but-stable code can stay untested if you're not modifying it.
