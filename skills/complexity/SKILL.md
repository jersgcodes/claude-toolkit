---
name: complexity
description: [CLI-only] Analyse cyclomatic and cognitive complexity, flag functions that need simplification. Use when code feels hard to follow, before refactoring, or standalone (not via /code-quality).
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.1.0
---



For a combined check (dead code + complexity + lint), use `/code-quality`.

Analyse code complexity and flag functions that need simplification. Do the following steps in order:

**1. Detect stack**

- `requirements.txt` or `pyproject.toml` → Python
- `package.json` → Node.js / TypeScript
- Report: "Detected stack: [X]"

---

## Python complexity analysis

**2a. Check radon is available**

Run `radon --version`. If not installed, run `pip install radon` first.

**3a. Cyclomatic Complexity**

```bash
radon cc . -a -s -n C --exclude "tests,node_modules,.venv,__pycache__"
```

Flags: `-a` = average, `-s` = show score, `-n C` = only show grade C or worse (complexity >= 11).

Grading scale:
- **A** (1-5): simple, low risk
- **B** (6-10): moderate, acceptable
- **C** (11-15): complex, should simplify
- **D** (16-20): very complex, must refactor
- **E** (21-30): extremely complex, high bug risk
- **F** (31+): unmaintainable

**4a. Maintainability Index**

```bash
radon mi . -s --exclude "tests,node_modules,.venv,__pycache__"
```

Flag any file with MI below 20 (grade C or worse).

**5a. Halstead metrics (optional)**

```bash
radon hal . --exclude "tests,node_modules,.venv,__pycache__" 2>&1 | head -40
```

Note files with high difficulty scores (>30).

---

## Node.js / TypeScript complexity analysis

**2b. Check eslint is available**

Run `npx eslint --version` or `pnpm exec eslint --version`.

**3b. Complexity via eslint**

Run eslint with the complexity rule **layered on top of the project's own
config** (so the TS parser is already wired — raw espree can't parse TS types):
```bash
# Adjust the path(s) to your source dir(s): src/ — or client/src/ server/ for a monorepo
npx eslint --rule '{"complexity": ["warn", 10]}' src/ 2>&1
```

This flags any function with cyclomatic complexity > 10. This is the eslint
equivalent of `radon cc` (cyclomatic only).

> **eslint 9+/flat-config note:** do NOT use `--no-eslintrc` or `--ext` — both
> were removed in flat config and the command will error
> (`Invalid option '--eslintrc'`). Layering `--rule` onto the project config (as
> above) is the correct approach and reuses the project's TS parser. `--plugin`
> still works (used in 4b).

**4b. Cognitive Complexity (the practical MI-equivalent for TS)**

`radon mi` (Maintainability Index) has no clean TypeScript port — the JS tools
that compute MI (escomplex et al.) parse JavaScript, not TS *types*. The modern,
TS-native equivalent is **cognitive complexity** (SonarSource's metric: counts how
hard code is to *follow* — nesting, breaks in flow — not just paths). It is
usually more actionable than MI/Halstead.

```bash
# Layers onto the project config (reuses its TS parser); adjust src/ as needed
npx eslint \
  --plugin sonarjs \
  --rule '{"sonarjs/cognitive-complexity": ["warn", 15]}' \
  src/ 2>&1
```

If the plugin isn't installed it will error — install once with
`pnpm add -D eslint-plugin-sonarjs` (or `npm i -D`), then re-run.

Thresholds (SonarSource defaults):

- **≤ 15** — acceptable
- **16–25** — review, consider simplifying
- **> 25** — refactor; the function is hard to reason about

**5b. Maintainability Index + Halstead (optional — true radon `mi`/`hal` parity)**

Only worth running if you specifically need MI/Halstead numbers for a TS/JS project.
See `references/complexity-ref.md` for the full escomplex + sucrase script.

**6b. File size check**

Find all source files over 300 lines:
```bash
find src/ -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" | xargs wc -l | sort -rn | head -20
```

Flag files over 300 lines as candidates for splitting.

**7b. Function length check**

Search for functions longer than 50 lines. These are candidates for extraction.

---

## Module depth analysis (Ousterhout — *A Philosophy of Software Design*)

Beyond cyclomatic complexity, check the *cognitive load* per module. Ousterhout's principle: **modules should be deep** — small, simple interfaces hiding substantial implementation.

A "shallow module" is the opposite: a module whose interface is nearly as complex as its implementation. Shallow modules force callers to know internal details.

**6a. Interface vs implementation ratio**

For each module (file), measure:
- **Interface size** — public functions + public class methods + their parameter counts
- **Implementation size** — total lines of code (excluding blanks/comments)
- **Depth ratio** = implementation_lines / interface_complexity

```bash
# Python: count public defs and their params per file
grep -nE "^(def |class )[a-z]" src/**/*.py | head -30
```

Flag modules where:
- Many public functions (> 8) for a small file (< 200 lines) — suggests **shallow module**, interface bloat
- Few public functions (≤ 3) but very large file (> 500 lines) — suggests **deep module** (good!)

**6b. Pass-through code**

Look for functions that just delegate to another function with the same parameters. This is a hallmark of shallow modules — the indirection adds no value.

```bash
# Find one-line functions that just call another
grep -A1 "^def " src/**/*.py | grep -B1 "return.*(.*)" | head -10
```

If `def foo(x, y): return bar(x, y)` exists with no transformation, flag it.

**6c. Information leakage**

A module leaks information when its interface forces callers to know internal data structure / file format / encoding. Heuristic: search for functions that return raw dicts/tuples instead of named objects.

```bash
grep -nE "def [a-z_]+\([^)]*\) -> (dict|tuple|list)" src/**/*.py | head -10
```

Suggest: replace dict returns with dataclass / named tuple where the structure has meaning.

**6d. Over-eager configuration**

Functions with many optional parameters often signal a missing abstraction. If a function has 5+ keyword args with defaults, the caller has to know all of them to use it well.

Suggest: introduce Parameter Object (per `/refactor`) or split into multiple intent-revealing functions.

---

## Summary (both stacks)

```
## Complexity Analysis

Stack: <Python|Node.js>

### Cyclomatic Complexity
| Function | File:Line | Score | Grade | Action |
|---|---|---|---|---|
| ... | ... | ... | C | Simplify |
| ... | ... | ... | D | Must refactor |

### Cognitive Complexity (TS only — how hard to follow)
| Function | File:Line | Cognitive | Action |
|---|---|---|---|
| ... | ... | 18 | Review |
| ... | ... | 27 | Refactor |

### File-level metrics
| File | Lines | Maintainability | Action |
|---|---|---|---|
| ... | ... | B (45) | OK |
| ... | ... | C (18) | Review |

> Python MI from `radon mi`; TS MI from the optional escomplex pass (5b). If the
> escomplex pass wasn't run, report cognitive complexity (4b) as the TS
> maintainability signal instead.

### Average complexity: <score> (Grade <X>)

### Top 3 refactoring priorities
1. <function> in <file> — complexity <N>, suggest: <specific action>
2. <function> in <file> — complexity <N>, suggest: <specific action>
3. <function> in <file> — complexity <N>, suggest: <specific action>

### Module depth (Ousterhout)
- Shallow modules (interface-heavy, few internals): N
- Deep modules (small interface, rich implementation): N
- Pass-through functions (no value-add): N
- Functions returning raw dicts/tuples: N
- Functions with > 4 optional params: N

### Verdict
- PASS: Average complexity A-B, no functions above D, modules well-balanced
- WARN: Some C-grade functions, or some shallow modules
- FAIL: D+ functions exist OR average complexity is C+ OR many shallow modules

### Suggested next skill
- High complexity → `/refactor` (Extract Function, Replace Conditional with Polymorphism)
- Shallow modules → `/refactor` (Inline Function, Extract Class to consolidate)
- Both → run `/code-quality` for full picture
```

**Pre-commit integration:** For Python projects, radon can be added as a pre-commit hook to block commits introducing high-complexity code. See `.pre-commit-config.yaml`.
