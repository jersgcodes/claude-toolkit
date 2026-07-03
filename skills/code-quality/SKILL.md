---
name: code-quality
description: [CLI-only] Run a combined code quality check: dead code detection, complexity analysis, and linting. Produces a unified report.
version: 0.1.0
---


Run a combined code quality check: dead code detection, complexity analysis, and linting. Produces a unified report.

This skill runs `/dead-code`, `/complexity`, and `/lint` in sequence. For individual checks, use those skills directly.

---

## Step 1 — Dead Code Detection

Find unused code in the current project:

**1a. Run vulture (Python projects only)**

Check if this is a Python project (requirements.txt or .py files exist).
If yes, check: `vulture --version`. If not installed, run `pip3 install vulture`.

Run:
```bash
vulture . --min-confidence 80 --exclude "tests,node_modules,.venv,__pycache__" 2>&1
```

Parse vulture output — it reports unused imports, functions/methods, variables, classes, and unreachable code. Group by type and sort by confidence (highest first).

Note: vulture may flag false positives for framework entry points (decorators, callbacks). These are handled below.

**1b. Unused imports**
Grep for import statements and check if the imported name appears anywhere else in the file:
- Python: look for `import X` or `from X import Y` where `Y` never appears in the file body (cross-reference with vulture output if available)
- JS/TS: look for `import { X }` where `X` is unused

**1c. Unused functions and variables**
- Find all function/method definitions
- Check if each is called anywhere in the codebase (not just the same file)
- Flag any that have zero references outside their definition
- Skip: `__init__`, `main`, test functions, anything decorated with `@app.route`, `@handler`, `@callback` etc. (framework entry points)

**1d. Unused files**
- Find all `.py` / `.js` / `.ts` files
- Check if each is imported or referenced anywhere
- Flag files with no inbound references (excluding entry points like `main.py`, `index.js`)

**1e. Commented-out code**
Grep for large blocks of commented-out code (3+ consecutive comment lines that look like code, not documentation).

**1f. `.bak` and temp files**
Check for any `.bak`, `.tmp`, `.old` files in the project root or src directories.

---

## Step 2 — Complexity Analysis

**Complexity:** run `/complexity` and include its report here.

---

## Step 3 — Clean Code checks (Martin)

Beyond linting, check the *human-readable* qualities that ruff/eslint don't catch.

**3.0a. Function size (Clean Code Ch. 3)**

Find functions that exceed Clean Code's "small" guideline:
- Python: > 30 lines (excluding docstring + blank lines)
- JS/TS: > 50 lines

```bash
# Python: list functions and their line counts
grep -nE "^(def |async def |    def |    async def )" *.py src/**/*.py 2>/dev/null
```

For each oversized function, suggest: "Extract Function" (see `/refactor`).

**3.0b. Naming check**

Flag bad names — these often signal design problems:

| Anti-pattern | Example | Fix |
|---|---|---|
| Single-letter (outside loops) | `def f(d, t):` | Use intent-revealing name |
| Type encoded in name | `user_dict`, `total_int` | Drop the type suffix |
| Generic words | `data`, `info`, `manager`, `handler`, `processor` | Replace with what it actually does |
| Misleading abbreviations | `usr`, `acct`, `cfg` (when `user`, `account`, `config` are 1-2 chars longer) | Spell it out |
| Boolean without `is_/has_/can_` prefix | `def admin(self):` | Rename to `is_admin` |
| Negated booleans | `not_ready`, `disabled` | Prefer positive form (`ready`, `enabled`) |

```bash
# Quick scan: variables/params that are 1-2 chars (excluding loop vars i, j, k, x, y)
grep -nE "(def |fn |function )[a-z_]+\([a-z]{1,2},|^\s+[a-z]{1,2}\s*=" src/**/*.py 2>/dev/null | head -20
```

**3.0c. Comment audit (Clean Code Ch. 4)**

Scan for *bad* comments (signal unclear code, not helpful documentation):

- Comments that explain *what* the next line does (instead of *why*)
- Commented-out code
- Misleading or stale comments (mentions code that no longer exists)
- TODO/FIXME with no date or owner

Don't flag good comments: docstrings, license headers, `# noqa`/`# type: ignore` with reason, `# Why:` blocks explaining business reason.

**3.0d. Magic numbers**

```bash
grep -nE "(\=|\>|\<|\* |/ |\+ )\s*[0-9]{2,}" src/**/*.py 2>/dev/null | grep -vE "(test_|conftest|__init__)" | head -10
```

Flag numeric literals > 1 (excluding 0, 1, -1, 100, common HTTP codes). Suggest: extract to a named constant.

---

## Step 4 — Lint

**4a. Check ruff is available (Python)**
Run `ruff --version`. If not installed, run `pip install ruff` first.

**4b. Run linting**
```
ruff check . --statistics
```
If a `src/` or specific package directory exists, target that instead of `.`.

**4c. Run format check (no changes, dry-run)**
```
ruff format --check .
```

**4d. Interpret results**
Group findings by rule category:
- `E`/`W` — PEP 8 style errors/warnings
- `F` — pyflakes (unused imports, undefined names)
- `I` — import order
- `S` — security (if ruff-bandit rules enabled)
- `UP` — pyupgrade (outdated Python syntax)
- `B` — flake8-bugbear (likely bugs and design issues)

---

## Unified Report

```
## Code Quality Report

### Dead Code
- Files safe to delete: N
- Functions safe to remove: N
- Unused imports: N
- Commented-out code blocks: N
- .bak/.tmp/.old files: N

### Complexity
Stack: <Python|Node.js>
Average complexity: <score> (Grade <X>)

| Function | File:Line | Score | Grade | Action |
|---|---|---|---|---|
| ... | ... | ... | C | Simplify |

Top 3 refactoring priorities:
1. <function> in <file> — complexity <N>, suggest: <specific action>
2. ...
3. ...

### Clean Code (Martin)
- Functions over 30 lines (Python) / 50 lines (JS): N
- Suspicious names (single-letter, generic, type-encoded): N
- Bad comments (what-comments, commented-out code, stale TODOs): N
- Magic numbers: N

Top 3 Clean Code issues:
1. <function or var> at <file:line> — <issue>, suggest: <Extract Function | Rename | Replace with constant>

### Lint
- Total issues by category: ...
- Files with most issues: ...
- Must-fix: any F821 (undefined name) or F401 (unused import)
- Auto-fixable format issues: N (run `ruff format .`)

### Overall Verdict
- Dead code: PASS / WARN / FAIL
- Complexity: PASS / WARN / FAIL
- Clean Code: PASS / WARN / FAIL
- Lint: PASS / WARN / FAIL
- Combined: PASS / WARN / FAIL

### Suggested next skill
- High Clean Code findings → run `/refactor` for named transformations
- Untested complex code → run `/seams` then `/refactor`
- Adding new behavior → run `/tdd`
```

Note: flag issues, don't auto-fix. Let the user decide what to change.

**Pre-commit integration:** For Python projects, radon can be added as a pre-commit hook to block commits introducing high-complexity code. See `.pre-commit-config.yaml`.
