---
name: security-check
description: [CLI-only] Scan the codebase for security vulnerabilities.
version: 0.1.0
---


Scan the codebase for security vulnerabilities. Do the following steps in order:

**1. Hardcoded secrets**
Search for patterns that suggest hardcoded credentials:
- Grep for: `api_key`, `secret`, `password`, `token`, `sk-`, `Bearer` in `.py`, `.js`, `.ts`, `.json` files (excluding test files and node_modules)
- Flag any that appear to contain real values (not placeholders like `<your-key>` or `os.environ`)

**2a. Bandit scan (Python projects only)**
Check if this is a Python project (`.py` files or `requirements.txt` exist). If yes:

Check bandit is available: run `bandit --version`. If not installed, run `pip install bandit` first.

Run scan:
```
bandit -r . -f txt -ll --exclude ./tests,./node_modules,./.venv
```
Flags: `-ll` = medium and high severity only (skip low noise), `-r` = recursive.

Interpret findings by severity:

HIGH severity — must fix before any deployment:
- B102: `exec()` usage
- B103: `chmod` setting permissive permissions
- B105/B106/B107: hardcoded passwords
- B301/B302: pickle deserialisation (arbitrary code execution)
- B320/B602/B603: shell injection via subprocess
- B501/B502: weak TLS/SSL

MEDIUM severity — should fix for org deployment:
- B101: `assert` used for security checks (stripped in optimised builds)
- B110: `try/except/pass` silencing exceptions
- B112: `try/except/continue`
- B311: non-cryptographic random used for security purposes
- B324: weak hash (MD5, SHA1) for security

LOW severity — informational:
- Overly broad exception handling
- Use of `tempfile.mktemp` instead of `mkstemp`

Report bandit summary:
- Count by severity: HIGH / MEDIUM / LOW
- List all HIGH items with file:line
- Deployment verdict:
  - Any HIGH → Not deployable
  - MEDIUM only → Deployable with documented risk acceptance
  - Clean → Security scan passed

**2b. OWASP Top 10 — relevant to this stack**
Check for:
- **Injection**: f-strings or `.format()` used to build SQL queries or shell commands. Flag any `os.system()`, `subprocess` with user input, or raw SQL string building.
- **Broken auth**: hardcoded admin checks, missing auth gates on sensitive routes/handlers
- **Sensitive data exposure**: PII logged to console or stored unencrypted, API keys in error messages
- **Security misconfiguration**: debug mode enabled in production config, overly permissive CORS

**3. Dependency check**
Run `pip list --outdated` (if Python project) or `npm outdated` (if Node project) and flag any packages with known CVEs or that are significantly outdated (>2 major versions behind).

**4. Environment variable audit**
- Check that all secrets are loaded via `os.environ` or a secrets manager, not from committed files
- Verify `.env` files are in `.gitignore`
- Check Railway/deployment env var list if `CLAUDE.md` documents what vars are required

**5. Summary**
Print a prioritised list:
- Critical: exposed secrets, injection vulnerabilities, bandit HIGH findings
- Warning: outdated packages, missing auth checks, bandit MEDIUM findings
- Info: minor improvements

If no issues found, print "No security issues found."
