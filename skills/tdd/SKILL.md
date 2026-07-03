---
name: tdd
description: Test-Driven Development cycle (Beck). Enforces red → green → refactor before writing implementation code.
version: 0.1.0
---


# TDD — Test-Driven Development

Based on Kent Beck's *Test-Driven Development by Example*. Three rules, in order:

1. **Red** — Write a failing test that defines the desired behavior
2. **Green** — Write the simplest code that makes the test pass
3. **Refactor** — Clean up the code with the test as your safety net

This is different from `/test-coverage` (which checks AFTER) and `/feature-design` (which plans). TDD is the *implementation discipline itself*.

---

## When to use TDD vs not

**USE TDD when:**
- Adding a new pure function with clear inputs/outputs
- Fixing a bug (regression test FIRST, then fix)
- Building a data transformation, parser, validator
- Implementing an algorithm or business rule

**SKIP TDD when:**
- UI layout / styling (visual feedback loop is faster)
- Exploratory spike to learn an API (write a tracer bullet, then TDD the cleanup)
- Glue code with no logic (e.g. wiring a route to a handler)
- One-off scripts

If unsure, default to TDD for any function with branching logic, math, or string manipulation.

---

## Step 1 — Define the unit under test

Ask the user (or extract from `$ARGUMENTS`):

1. **What's the function/class name?** (e.g. `parse_invoice`, `EventDispatcher`)
2. **What's its single responsibility?** (one sentence — if it can't fit in one sentence, split it)
3. **What's the simplest happy-path example?** (concrete inputs → expected output)
4. **What edge cases matter?** (empty input, error case, boundary)

If the user can't answer #2 in one sentence, stop and run `/feature-design` first.

---

## Step 2 — RED: write the failing test first

Before writing ANY production code:

a) Locate or create the test file (`test_<module>.py` or `<module>.test.ts`)
b) Write the simplest test for the happy path. Use the function name even though it doesn't exist yet.
c) Run the test. Confirm it FAILS — and fails for the right reason (NameError, ImportError, AssertionError on expected output). Not for syntax errors.
d) State the failure: "RED: test fails because `parse_invoice` is not defined."

Test shape:
```python
def test_parse_invoice_extracts_total():
    raw = "Invoice #123\nTotal: $42.50"
    result = parse_invoice(raw)
    assert result.total == Decimal("42.50")
```

**Critical rule:** If the test PASSES on the first run, the test is wrong (it's not actually testing the new behavior). Rewrite it.

---

## Step 3 — GREEN: simplest possible implementation

Write the **fakest, simplest code** that makes the test pass. Even if it's literally `return Decimal("42.50")`.

This feels wrong but it's the discipline:
- It proves the test is hooked up correctly
- It forces you to write more tests (because the fake won't survive case #2)
- It prevents over-engineering

Run the test. Confirm it PASSES.

State: "GREEN: test passes with stub implementation."

---

## Step 4 — Add the next test

Before improving the code, add a SECOND test that the fake won't satisfy:

```python
def test_parse_invoice_handles_different_total():
    raw = "Invoice #456\nTotal: $99.00"
    result = parse_invoice(raw)
    assert result.total == Decimal("99.00")
```

Run. Confirm RED. Now you're forced to write real logic to make BOTH tests pass.

Iterate Step 2-3-4 until the function is fully specified by tests:
- Edge case: empty input
- Edge case: malformed input (raises ValueError)
- Edge case: multiple totals (uses last one? errors? — DECISION)

---

## Step 5 — REFACTOR with test safety

Once tests are green and cover the cases:
- Extract repeated logic into helpers (Extract Function from `/refactor`)
- Rename variables for clarity
- Remove duplication between tests via fixtures
- Run tests after EACH change. If they break, revert.

Do NOT add untested behavior during refactor. If you discover a missing case, write the test first (back to Step 2).

---

## Step 6 — Confirm

```
TDD Cycle Complete — <function_name>

Tests written: <N>
Coverage: happy path + <list edge cases>
Implementation: <line count>
Refactorings applied: <list, or "none">

Next:
- Run /test-coverage to confirm no missing branches
- Run /code-quality to check naming + complexity
```

---

## Anti-patterns (warn the user if you see these)

- **Writing tests after the code** — that's not TDD, that's coverage. Useful but different. Use `/test-coverage` instead.
- **Testing implementation details** — tests should describe behavior, not internal structure. If a refactor breaks a test that didn't change behavior, the test is too tightly coupled.
- **Skipping the RED step** — if you don't see the test fail first, you don't know it's actually testing your code.
- **Multiple assertions per test** — one test, one behavior. Split.
- **Mocking everything** — in this workspace, prefer real dependencies (per the workspace MISTAKES.md "integration tests must hit a real database" rule).

---

## Cost control

- TDD cycles produce many test runs. Cache test invocation if pytest takes > 5s — use `pytest -x --ff` (stop on first fail, fail-first ordering) to keep cycles fast.
- Don't read full test output every cycle. Just the pass/fail summary.

---

## Integration

- Pulls from: `/feature-design` (when you have a plan but need implementation discipline)
- Hands off to: `/test-coverage` (final coverage check), `/refactor` (cleanup with test safety)
- Hook-triggered: a PreToolUse hook on Write/Edit can prompt TDD when creating a new function in src/
