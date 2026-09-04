---
name: security-check
description: Security scan: bandit for Python plus an OWASP review of the things static tools miss (injection, auth and access control, data exposure, misconfiguration). Deliberately does NOT scan for hardcoded secrets or dependency CVEs; /secrets-scan and /deps-audit own those, and duplicating them ran the same grep up to four times in one commit-to-deploy sequence. Use before a commit or deploy.
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.2.0
---

Scan the codebase for security vulnerabilities.

**This skill does not scan for secrets or dependency CVEs itself.** Two other skills already do that better, and duplicating them meant the same grep ran up to four times in one commit-to-deploy sequence:

| Concern | Owner | Why not here |
|---|---|---|
| Hardcoded secrets, `.env` hygiene, git history | `/secrets-scan` | Runs trufflehog and scans history, which a flat grep cannot |
| Dependency CVEs, pinning, licences, env-var audit | `/deps-audit` | Runs `pip-audit` and `safety`, real CVE data rather than "outdated" |

If the caller has not already run those (`/pre-commit` and `/pre-deploy` both do), say so in the summary and recommend them. Do not re-implement them.

Do the following steps in order:

---

**1. Bandit scan (Python projects only)**

If this is a Python project (`.py` files or `requirements.txt` exist), check bandit is available (`bandit --version`, `pip install bandit` if not), then run:

```
bandit -r . -f txt -ll --exclude ./tests,./node_modules,./.venv
```

`-ll` = medium and high only (skips low noise), `-r` = recursive.

HIGH — must fix before any deployment:
- B102 `exec()` usage
- B103 `chmod` setting permissive permissions
- B105/B106/B107 hardcoded passwords
- B301/B302 pickle deserialisation (arbitrary code execution)
- B320/B602/B603 shell injection via subprocess
- B501/B502 weak TLS/SSL

MEDIUM — should fix for org deployment:
- B101 `assert` used for security checks (stripped in optimised builds)
- B110 `try/except/pass` silencing exceptions
- B112 `try/except/continue`
- B311 non-cryptographic random used for security
- B324 weak hash (MD5, SHA1) for security

LOW — informational: overly broad exception handling, `tempfile.mktemp` instead of `mkstemp`.

Report counts by severity, list every HIGH with `file:line`, and give a verdict:
- Any HIGH → **Not deployable**
- MEDIUM only → Deployable with documented risk acceptance
- Clean → Security scan passed

---

**2. OWASP review — what static tools miss**

Bandit catches patterns; this step catches intent. Read the code, do not just grep.

- **Injection** — f-strings or `.format()` building SQL queries or shell commands. Any `os.system()`, `subprocess` with user input, raw SQL string building.
- **Broken auth** — hardcoded admin checks, missing auth gates on sensitive routes or handlers, authorisation decided client-side.
- **Sensitive data exposure** — PII logged to console or stored unencrypted, API keys or stack traces in error messages returned to users.
- **Security misconfiguration** — debug mode enabled in production config, overly permissive CORS, default credentials left in place.

---

**3. Summary**

Prioritised list:
- **Critical** — injection vulnerabilities, bandit HIGH findings, missing auth on a sensitive route
- **Warning** — missing auth checks elsewhere, bandit MEDIUM findings, misconfiguration
- **Info** — minor improvements

State plainly whether `/secrets-scan` and `/deps-audit` have been run this session; if not, recommend them rather than guessing at their findings.

If nothing is found, print "No security issues found."
