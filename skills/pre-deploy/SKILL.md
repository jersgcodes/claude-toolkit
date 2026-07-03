---
name: pre-deploy
description: [CLI-only] Full deployment readiness check. Runs all quality and security gates in sequence.
version: 0.1.0
---


Full deployment readiness check. Runs all quality and security gates in sequence.

Use `$ARGUMENTS` as the target environment if provided (e.g. `staging`, `production`). Default: production.

---

**Gate 1 — Tests**
Run the test suite:
- Python: `python -m pytest -q`
- Node: `npm test` or `pnpm test`

Result: ✅ All pass / ❌ N failures — STOP if any failures.

---

**Gate 2 — Lint / Type check**
Detect stack first:
- If `tsconfig.json` exists → run `/type-check` (TypeScript: `tsc --noEmit`)
- Else if `pyproject.toml` or `requirements.txt` exists → run `/lint` (Python: ruff)
- Else → skip, print "No tsconfig.json or Python config found — skipping Gate 2"

Result: ✅ No errors / ⚠️ Warnings / ❌ Errors — STOP on errors.

---

**Gate 3 — Security scan**
Detect stack:
- If Python project → run `/security-check` (includes bandit)
- If TypeScript/Node project → run `/socket-audit` (Socket.IO auth and rate limiting checks)
- Both if mixed project

Result: ✅ No HIGH/Critical findings / ❌ Critical findings — STOP on Critical.

---

**Gate 4 — Secrets**
Run `/secrets-scan`.
Result: ✅ No secrets in code or history / ❌ Secrets found — STOP, rotate keys before proceeding.

---

**Gate 5 — Dependencies**
Run `/deps-audit`.
Check:
- Any CRITICAL or HIGH CVEs → ❌ STOP
- Any unpinned dependencies → ⚠️ warn
- Any copyleft licenses (GPL/AGPL) → ⚠️ warn for commercial org deployment

---

**Gate 6 — Optimization check**
Run `/optimize`.
Check:
- No O(n^2) patterns on large data
- No N+1 database queries
- No redundant computations in hot paths
- Sequential awaits that should be parallel

Result: ✅ No HIGH issues / ⚠️ Optimization opportunities / ❌ Performance-critical issues — STOP on HIGH.

---

**Gate 7 — Hardening checks**
Read the main entry point and key modules. Check:

- [ ] No `print()` debug statements in production code paths (use `logging` instead)
- [ ] No `TODO: remove before prod` or `FIXME` comments in critical paths
- [ ] All external HTTP/API calls have timeout parameters set
- [ ] Rate limiting in place if the service is publicly accessible
- [ ] Error messages shown to users don't include stack traces or internal details
- [ ] No `debug=True` in production config

---

**Final verdict**

Print a table:

| Gate | Result | Blocker? |
|------|--------|----------|
| Tests | ✅/❌ | Yes |
| Lint | ✅/⚠️/❌ | Errors only |
| Bandit | ✅/❌ | HIGH only |
| Secrets | ✅/❌ | Yes |
| Deps CVE | ✅/⚠️/❌ | CRITICAL/HIGH |
| Optimization | ✅/⚠️/❌ | HIGH only |
| Hardening | ✅/⚠️ | No |

**Gate 8 — Architecture docs (optional)**
If `scripts/gen-architecture.ts` exists, run `pnpm gen:arch` to regenerate `docs/architecture.md`.
Result: ✅ Regenerated / ⚠️ Script missing — non-blocking.

---

**Overall: READY TO DEPLOY / NOT READY — fix blockers above first**
