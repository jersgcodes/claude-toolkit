---
name: stack-detect
description: [CLI-only] Identify the current project's tech stack and list applicable quality/profiling tools.
version: 0.1.0
---


Identify the current project's tech stack and list applicable quality/profiling tools. Do the following steps in order:

**1. Detect project type**

Check the current directory for these markers:

| Marker | Stack |
|---|---|
| `requirements.txt` or `pyproject.toml` or `setup.py` | Python |
| `package.json` with `typescript` dep or `tsconfig.json` | Node.js + TypeScript |
| `package.json` without TypeScript | Node.js (JavaScript) |
| `Cargo.toml` | Rust |
| `go.mod` | Go |

If multiple markers exist (e.g. Python backend + JS frontend), report both.

**2. Read key config files**

- Python: read `requirements.txt` or `pyproject.toml` for dependencies. Note frameworks (Flask, Django, FastAPI, telegram, etc.)
- Node: read `package.json` for dependencies and scripts. Note frameworks (React, Next.js, Express, etc.)
- Check for existing quality tooling: `.pre-commit-config.yaml`, `ruff.toml`, `.eslintrc*`, `.prettierrc*`, `mypy.ini`, `pyrightconfig.json`

**3. Report applicable tools**

Based on the detected stack, print a table of tools and their status:

### Python projects

| Tool | Purpose | Status |
|---|---|---|
| **ruff** | Lint + format | Installed? Check `ruff --version` |
| **bandit** | Security analysis | Installed? Check `bandit --version` |
| **radon** | Complexity analysis | Installed? Check `radon --version` |
| **mypy** | Static type checking | Installed? Check `mypy --version` |
| **scalene** | CPU + memory profiling | Installed? Check `scalene --version` |
| **vulture** | Dead code detection | Installed? Check `vulture --version` |
| **pytest** | Testing | Installed? Check `pytest --version` |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` exists? |

### Node.js / TypeScript projects

| Tool | Purpose | Status |
|---|---|---|
| **eslint** | Lint | In devDependencies? |
| **prettier** | Format | In devDependencies? |
| **tsc** | Type check (TS only) | `tsconfig.json` exists? |
| **vitest** / **jest** | Testing | In devDependencies? |
| **clinic** / **0x** | Profiling | Installed globally? |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` exists? |

**4. Recommend missing tools**

For each tool that is NOT installed/configured, print a one-line install command:

```
Missing tools — install commands:
  pip install ruff bandit radon mypy scalene   # Python
  npm install -D eslint prettier               # Node.js
  pip install pre-commit && pre-commit install  # Git hooks
```

**5. List applicable skills**

Print which Claude Code skills are available for this stack:

- **All projects**: `/lint`, `/dead-code`, `/security-check`, `/secrets-scan`, `/test-coverage`, `/deps-audit`
- **Python**: `/bandit`, `/profile`, `/complexity`
- **Node/TS**: `/type-check`, `/perf-audit`
- **All**: `/pre-commit`, `/commit`, `/diff-review`

**6. Pre-commit status**

Check if `.pre-commit-config.yaml` exists and if pre-commit hooks are installed (`ls .git/hooks/pre-commit`).
Report: "Pre-commit: INSTALLED" or "Pre-commit: NOT CONFIGURED — run `/pre-commit` setup or copy template."
