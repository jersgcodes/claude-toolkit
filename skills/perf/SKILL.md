---
name: perf
description: Performance check — analyze code for optimization opportunities (static) and run profilers (dynamic). Combines former /optimize + /profile.
version: 0.1.0
---


# Perf

Two modes in one skill:
- **Analyze (static)** — scan code for known performance anti-patterns (O(n²), N+1, redundant computation, bad data structures)
- **Profile (dynamic)** — run profilers on the live entry point (cProfile, Scalene, node --prof, clinic)

Default runs both. Use `analyze` or `profile` as `$ARGUMENTS` to run just one.

---

## Step 1 — Detect stack

- `requirements.txt` or `pyproject.toml` → Python
- `package.json` → Node.js / TypeScript
- Report: "Detected stack: [X]"

---

## ANALYZE MODE — static patterns

### Python checks

**2a. Algorithmic complexity (HIGH)**

Scan all `.py` files (excluding tests, .venv, __pycache__):
- Nested `for` loops over the same or related collections — O(n²)
- `if x in list` inside a loop — should be `set` for O(1)
- Repeated `.index()` or `.count()` calls inside loops
- List comprehension inside list comprehension on large data

**2b. Redundant computation (HIGH)**
- Same function called multiple times with same args in a scope (cache it)
- `len()` called in every iteration of a loop condition
- Repeated dictionary lookups: `d["key"]["nested"]` used 3+ times → assign once

**2c. Inefficient data structures (MEDIUM)**
- `list` for membership checks → use `set` or `dict`
- Building strings with `+=` in a loop → use `"".join()`
- `dict` when `defaultdict` or `Counter` would simplify
- Sorting just to get min/max → use `min()`/`max()` directly

**2d. I/O and blocking (MEDIUM)**
- Synchronous file/network I/O in async functions
- `requests.get()` in a loop without session reuse
- Opening/closing files in a loop
- Missing `with` statement for file handles

**2e. Database patterns**
- N+1 queries (cursor.execute or ORM `.get()` inside `for`)
- `WHERE` clauses on potentially unindexed columns
- `SELECT *` when only specific columns needed
- Unbounded queries without `LIMIT`

**2f. Memory patterns**
- Loading entire file into memory when streaming would work
- Large list created just to iterate once → generator
- Unbounded global lists/dicts that grow forever

### Node.js / TypeScript checks

**3a. Algorithmic complexity (HIGH)**
- `.find()` or `.filter()` inside `.map()` or `.forEach()`
- `.includes()` on array inside a loop → use `Set`
- Nested array iterations on related data
- `.indexOf()` inside loops

**3b. React-specific (HIGH for UI)**
- Props drilling 3+ levels — consider context/composition
- `useEffect` re-running on every render (missing/broad deps)
- New callbacks in render without `useCallback` (passed to memoized children)
- Inline styles/objects creating new references each render

**3c. I/O patterns (MEDIUM)**
- Sequential `await` calls that could be `Promise.all()`
- `fetch()` in loop instead of batch API
- No request deduplication
- Missing abort controller for cancelled requests

**3d. Bundle optimization**
- Large default imports that could be tree-shaken (`import _ from 'lodash'` → `import debounce from 'lodash/debounce'`)
- Dynamic `import()` candidates
- Images not lazy-loaded

---

## PROFILE MODE — dynamic measurement

### Python profiling

**4a. Find entry point**
- `main.py`, `app.py`, `bot.py`, `server.py` in project root
- `if __name__ == "__main__"` blocks
- Ask user if unclear

**4b. Run cProfile (always available)**
```bash
python3 -m cProfile -s cumtime <entry_point> 2>&1 | head -40
```
- Top 10 functions by cumulative time
- Flag any function taking > 1s cumulative
- Flag any function called > 10,000 times

**4c. Run Scalene (if available)**
```bash
scalene --version 2>/dev/null && scalene --cpu --memory --reduced-profile <entry_point> 2>&1
```
Provides line-level CPU time (Python vs C) + memory allocation per line. If not installed: print `pip install scalene` and skip.

**4d. Memory check with tracemalloc**
```python
import tracemalloc
tracemalloc.start()
import <module>
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:10]:
    print(stat)
```

### Node.js profiling

**5a. Find entry point** — check `package.json` scripts for `start` / `dev` / `serve`. Look for `index.js`, `server.js`, `app.js`.

**5b. Built-in profiler**
```bash
node --prof <entry_point>
node --prof-process isolate-*.log 2>&1 | head -60
```

**5c. clinic.js (if available)**
```bash
npx clinic --version 2>/dev/null && npx clinic doctor -- node <entry_point>
```

---

## Step 6 — Combined report

```
## Performance Report

Stack: <Python|Node.js|TypeScript>
Mode: <analyze|profile|both>

### Static analysis findings (analyze mode)

HIGH severity:
| Issue | File:Line | Pattern | Suggested fix |
|---|---|---|---|

MEDIUM severity:
| Issue | File:Line | Pattern | Suggested fix |
|---|---|---|---|

### Profile results (profile mode)

CPU hotspots:
| Function | Cumulative time | Calls | File:Line |
|---|---|---|---|

Memory:
| Location | Allocation | File:Line |
|---|---|---|

### Top 3 priorities (combined)
1. <fix with estimated impact>
2. <fix with estimated impact>
3. <fix with estimated impact>

### Verdict
- PASS: No high-severity static issues, no functions > 1s cumulative
- WARN: Some opportunities exist
- FAIL: O(n²) on large data, N+1 queries, or function > 5s cumulative

### Suggested next skill
- HIGH static issues with tests → /refactor (Extract Function, Replace Conditional)
- HIGH static issues without tests → /seams first
- React render perf → /perf-audit (deeper React-specific checks)
```

---

## Cost control

- Profile mode reads runtime output — bounded by `head -40`/`head -60`
- Analyze mode greps codebase — cap results at 30 findings
- For long-running servers (bots, web servers), use `timeout 30` prefix or ask user duration

---

## Related skills

- `/perf-audit` — React/Vite bundle + render-specific checks
- `/arch-review` — module-level structure (different scope)
- `/code-quality` — complexity, dead code, lint
- `/refactor` — apply named transformations to fix the issues found here
