---
name: refactor
description: Smell-driven, test-guarded refactoring (Fowler). Identifies code smells and proposes named transformations that preserve behavior.
allowed-tools: [Read, Glob, Grep, Bash]
version: 0.1.0
---



# Refactor

Refactoring without breaking behavior. Based on Martin Fowler's *Refactoring* (2nd ed.) — find a smell, apply a named transformation, verify tests still pass.

This skill is **analysis-only by default**. It produces a refactoring plan with named transformations. The user decides what to apply. Use `--apply` to execute the top transformation after confirming.

---

## Step 1 — Determine scope

If `$ARGUMENTS` is a file or directory, focus there. Otherwise, ask the user which file/module to refactor, or scan the whole project.

Run `/code-quality` first if you haven't this session — its output (complex functions, dead code, lint issues) feeds Step 2.

---

## Step 2 — Detect code smells

Scan for these specific smells. Report each with file:line.

**Bloater smells:**
- **Long Method** — function > 30 lines (Python) or > 50 lines (JS/TS)
- **Large Class** — file > 300 lines or class with > 10 methods
- **Long Parameter List** — function with > 4 parameters (excluding `self`)
- **Primitive Obsession** — many primitive args that move together (e.g. always `(start, end, name, type)` together)

**Object-orientation abusers:**
- **Switch Statements** — `if/elif` chains > 4 branches on type/string
- **Refused Bequest** — subclass overrides nearly all parent methods

**Change preventers:**
- **Divergent Change** — single class modified for many unrelated reasons (check git log per file: many distinct concerns in commit messages)
- **Shotgun Surgery** — single concern requires editing many files (check: feature added across > 5 files)

**Dispensables:**
- **Duplicate Code** — same/similar code blocks in 2+ places (>= 6 lines)
- **Dead Code** — already covered by `/code-quality`; reference its output
- **Speculative Generality** — abstract classes / hooks / params with single concrete user
- **Comments** — long comment blocks that explain *what* (sign code is unclear) — Clean Code overlap

**Couplers:**
- **Feature Envy** — method uses another object's data more than its own
- **Inappropriate Intimacy** — class accesses internals of another class

---

## Step 3 — Map smells to named transformations

For each smell, propose ONE named refactoring from Fowler's catalog:

| Smell | Transformation | What it does |
|---|---|---|
| Long Method | Extract Function | Pull a coherent block into a new named function |
| Long Method (returns multiple things) | Split Phase | Separate calculation from output |
| Large Class | Extract Class | Move a cohesive subset of fields/methods into a new class |
| Long Parameter List | Introduce Parameter Object | Bundle related params into a dataclass / dict |
| Primitive Obsession | Replace Primitive with Object | Wrap a primitive in a small class with behavior |
| Switch Statements | Replace Conditional with Polymorphism | Move per-case logic into subclass methods |
| Switch Statements (data) | Replace Type Code with Subclasses | Or with strategy pattern / dispatch dict |
| Duplicate Code (same class) | Extract Function | Pull duplicate into shared method |
| Duplicate Code (across classes) | Pull Up Method | Move to common parent / mixin |
| Feature Envy | Move Function | Move method to the class whose data it uses |
| Speculative Generality | Inline Class / Inline Function | Collapse the abstraction back |
| Comments explaining what | Extract Function (with intent-revealing name) | Replace `// step 3: compute total` with `compute_total()` |
| Divergent Change | Extract Class (per concern) | Split file by what changes together |
| Shotgun Surgery | Move Function / Inline Class | Consolidate the scattered concern |

---

## Step 4 — Test safety check

For each proposed transformation, verify the **safety net**:

```bash
# Find the test file for the target
test_file=$(find . -path '*/test*' -name "test_${target_module}*" -o -name "${target_module}*test*" | head -3)
```

State for each refactoring:
- **TEST EXISTS** — safe to refactor; tests will catch regressions
- **NO TEST** — UNSAFE; recommend `/seams` first to add a characterization test, OR add a test before refactoring

If `--apply` flag is used, BLOCK the apply when NO TEST exists. Force the user to acknowledge the risk explicitly.

---

## Step 5 — Produce the plan

```markdown
## Refactoring Plan — <scope>

### Smells found: <count>

| # | File:Line | Smell | Severity |
|---|---|---|---|
| 1 | src/foo.py:42-95 | Long Method (53 lines) | High |
| 2 | src/foo.py:120-140 | Duplicate Code (with bar.py:88) | Medium |
| ... | | | |

### Proposed transformations

#### 1. Extract Function — `src/foo.py:42-95`
- **Smell:** Long Method (53 lines, complexity 14)
- **Transformation:** Extract lines 60-78 into `_validate_input(payload)`. Extract lines 80-95 into `_persist(record)`.
- **Test coverage:** TEST EXISTS (`test_foo.py::test_process_payment` covers this path)
- **Behavior preserved:** Yes — pure extraction, no logic change
- **Estimated effort:** 5 min

#### 2. Replace Conditional with Polymorphism — `src/foo.py:200-240`
- **Smell:** Switch Statement (6 branches on `event_type`)
- **Transformation:** Create `EventHandler` base class with subclasses `LoginHandler`, `LogoutHandler`, etc. Replace if/elif with handler dispatch.
- **Test coverage:** NO TEST — UNSAFE without seams
- **Recommendation:** Run `/seams` first to add a characterization test, then refactor

### Refactoring order (recommended)

1. ✅ **Safe & high impact:** transformation #1
2. ⚠️ **Needs test first:** transformation #2 — run `/seams`
3. ✅ **Safe & medium impact:** transformation #3
```

---

## Step 6 — Apply (only with `--apply` flag)

If user runs `/refactor --apply`:

1. Pick ONLY the top safe transformation (TEST EXISTS)
2. Run tests first to capture baseline: `python -m pytest -q` or `pnpm test`
3. Apply the transformation via Edit tool
4. Run tests again
5. If tests pass → report success, ask if user wants to apply the next safe transformation
6. If tests fail → revert the change, report what broke

Do NOT apply multiple transformations in one pass. One at a time, verified each step.

---

## Cost control

- This skill reads many files. Use a subagent (`Explore`) for codebase-wide smell detection if scope > 5 files.
- Default to analysis-only. Apply mode is opt-in.
- Cap smell detection at 20 smells per scope to avoid overwhelming output.

---

## Integration

- Pulls from: `/code-quality` output (complexity, dead code, lint)
- Hands off to: `/seams` (when test missing), `/tdd` (when adding new behavior during refactor)
- Used by: `/pre-commit` (in `--check-only` mode to flag candidates)
