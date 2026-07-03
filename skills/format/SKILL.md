---
name: format
description: [CLI-only] Auto-format code in the current project.
version: 0.1.0
---


Auto-format code in the current project. Do the following steps in order:

**1. Detect stack**

- `requirements.txt` or `pyproject.toml` → Python
- `package.json` → Node.js / TypeScript
- Report: "Detected stack: [X]"

---

## Python formatting

**2a. Check ruff is available**

Run `ruff --version`. If not installed, run `pip install ruff` first.

**3a. Run format**

```bash
ruff format .
```

**4a. Run import sorting**

```bash
ruff check --select I --fix .
```

**5a. Report changes**

```bash
git diff --stat
```

Show which files were modified and how many lines changed.

---

## Node.js / TypeScript formatting

**2b. Check prettier is available**

Run `npx prettier --version` or `pnpm exec prettier --version`.
If not installed, check `package.json` devDependencies. If missing: `npm install -D prettier`.

**3b. Run format**

```bash
npx prettier --write "src/**/*.{js,jsx,ts,tsx,json,css}" 2>&1
```

Or if pnpm:
```bash
pnpm exec prettier --write "src/**/*.{js,jsx,ts,tsx,json,css}" 2>&1
```

**4b. Run eslint auto-fix (if available)**

```bash
npx eslint --fix src/ 2>&1 || true
```

**5b. Report changes**

```bash
git diff --stat
```

---

## Summary

```
## Format Results

Stack: <Python|Node.js>
Tool: <ruff format|prettier>

Files modified: N
Lines changed: +N / -N

Modified files:
- <file1>
- <file2>
- ...

Next steps:
- Review changes with `git diff`
- Run tests to confirm nothing broke: `pytest` / `pnpm test`
- Commit when ready
```

**Tip:** Use `/lint` to check formatting without applying changes (dry-run mode). Use `/format` to apply fixes.
