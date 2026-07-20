---
name: type-check
description: [CLI-only] Run static type checking (mypy / tsc). Use when you want to catch type errors, before committing, or after adding new types or refactoring.
allowed-tools: [Bash, Read, Grep, Glob]
version: 0.1.0
---



Run static type checking for the current project. Auto-detects stack. Do the following steps in order:

**Step 1 — Detect stack**

Check for:
- `tsconfig.json` → TypeScript (use tsc)
- `requirements.txt` or `pyproject.toml` or `*.py` files → Python (use mypy)
- If both exist, run both.

Report: "Detected stack: [Python|TypeScript|Both]"

---

## Python type checking (mypy)

**Step 2a — Check mypy is available**

Run `mypy --version`. If not installed, run `pip3 install mypy` first.

**Step 3a — Run mypy**

```bash
mypy . --ignore-missing-imports --no-strict-optional --exclude 'tests|node_modules|\.venv|__pycache__' 2>&1
```

If there's a `mypy.ini` or `[mypy]` section in `pyproject.toml`, respect that config instead of the flags above.

**Step 4a — Parse results**

- Count total errors
- Group by file: list each file with its error count and first error
- Categorise errors:
  - `[arg-type]` / `[assignment]` — type mismatches (HIGH — likely bugs)
  - `[return-value]` — wrong return type (HIGH)
  - `[attr-defined]` — accessing non-existent attribute (HIGH — runtime error)
  - `[name-defined]` — undefined name (CRITICAL — will crash)
  - `[import]` — can't find module (LOW — usually missing stubs)
  - `[no-untyped-def]` — missing type annotations (INFO — improve over time)

**Step 5a — Report**

```
## Python Type Check (mypy)

PASS: No type errors   OR   FAIL: N errors across M files

### Errors by severity
CRITICAL: N (name-defined, will crash at runtime)
HIGH: N (arg-type, return-value, attr-defined)
LOW: N (import, missing stubs)

### Errors by file
- src/foo.py (3 errors)
  - Line 42: Argument 1 has incompatible type "str"; expected "int" [arg-type]
  - ...

### Missing type stubs
If import errors for third-party packages, suggest:
  pip install types-requests pandas-stubs types-openpyxl ...

### Next steps
- Fix CRITICAL/HIGH errors first (these are likely bugs)
- Install missing stubs for LOW import errors
- Add type annotations gradually for no-untyped-def warnings
```

---

## TypeScript type checking (tsc)

**Step 2b — Detect tsconfig**

Check for `tsconfig.json` in the current directory and common subdirectories (`client/`, `server/`, `src/`).
If multiple tsconfigs exist, run each separately.

**Step 3b — Run tsc**

For each tsconfig found:
```bash
npx tsc --noEmit -p tsconfig.json 2>&1
```
Or if pnpm is the package manager:
```bash
pnpm exec tsc --noEmit 2>&1
```

**Step 4b — Parse results**

- Count total errors
- Group by file: list each file with its error count and the first error message
- Flag files with >3 errors (likely structural issues, not just typos)

**Step 5b — Report**

```
## TypeScript Check (tsc)

PASS: No type errors   OR   FAIL: N errors across M files

### Errors by file
- src/foo.ts (3 errors)
  - Line 42: Type 'string' is not assignable to type 'number'
  - ...
- server/bar.ts (1 error)
  - Line 17: Property 'x' does not exist on type 'Y'

### Next steps
- Fix structural errors first (files with many errors)
- Re-run after fixes to confirm clean
```

---

## Combined summary (if both stacks)

```
## Type Check Summary

Python (mypy):  PASS / FAIL — N errors
TypeScript (tsc): PASS / FAIL — N errors

Overall: PASS / FAIL
```

If no tsconfig found and no Python files: print "No typed project detected — skipping."
If tsc not available: print "tsc not found. Run: npm install -g typescript"
If mypy not available: print "mypy not found. Run: pip3 install mypy"
