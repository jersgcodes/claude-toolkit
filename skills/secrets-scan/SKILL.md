---
name: secrets-scan
description: [CLI-only] Scan for exposed secrets, API keys, tokens, or credentials in code and git history. Use when auditing before a commit, deploy, or open-sourcing a repo.
allowed-tools: [Read, Grep, Glob, Bash]
version: 0.1.0
---



Scan for exposed secrets in code and git history. Do the following steps in order:

**1. Live code scan — grep patterns**
Search all non-test, non-vendor source files for these patterns:

```
# API keys and tokens
grep -rn --include="*.py" --include="*.ts" --include="*.js" --include="*.json" \
  -E "(api_key|api_secret|access_token|secret_key|private_key|auth_token)\s*=\s*['\"][^'\"]{8,}" \
  --exclude-dir={tests,node_modules,.venv,dist}
```

Also grep for provider-specific prefixes that look real:
- `sk-` (OpenAI)
- `tvly-` (Tavily)
- `AIza` (Google)
- `ghp_` or `github_pat_` (GitHub tokens)
- `xoxb-` or `xoxp-` (Slack)
- `SG.` (SendGrid)
- `AC` followed by 32 hex chars (Twilio)
- `key-` in context of `mailgun`

Flag any match where the value is NOT: an env var reference (`os.getenv`, `process.env`), a placeholder (`<your-key>`, `xxx`, `your_`, `REPLACE_ME`), or a test fixture.

**2. .env file audit**
- Check `.env` exists — if so, confirm it's in `.gitignore`
- Check `.env.example` exists — if not, flag it as missing (orgs need this for onboarding)
- Confirm `.env` is not tracked: `git ls-files .env`

**3. Git history scan**
If truffleHog is available (`trufflehog --version`), run:
```
trufflehog filesystem . --no-update --json 2>/dev/null | head -100
```
If not available, run:
```
git log --all --oneline | head -5
git log -p --all --since="6 months ago" -- "*.env" "*.json" 2>/dev/null | grep -E "(api_key|token|secret|password)\s*=" | head -20
```
This catches secrets that were committed then deleted — they still live in git history and can be extracted.

**4. Summary**
🔴 Critical (secrets found in live code): list file:line with redacted value
🔴 Critical (.env committed to git): immediate action required — rotate all keys, purge history
🟡 Warning (suspicious patterns in history): recommend running full truffleHog scan
🟢 Info (.env.example missing): should be created for org onboarding

If clean: print "No secrets found in code or recent history."

**Note for org deployment:** Even if clean now, recommend setting up truffleHog as a pre-commit hook so secrets are caught before they enter the repo: `pip install pre-commit trufflehog` then add to `.pre-commit-config.yaml`.
