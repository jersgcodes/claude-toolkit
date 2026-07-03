---
name: pre-commit
description: [CLI-only] Run all pre-commit skill checks in parallel before committing.
version: 0.1.0
---


Run all pre-commit skill checks in parallel before committing. Do the following steps in order:

**1. Check for active commit block**

Run:
```bash
python3 ~/.claude/hooks/commit-log.py --cwd . --cmd active
```

If empty, there is no active commit block yet. That is fine — the pre-commit hook will create one when `git commit` is run. Proceed anyway.

If a key is returned, note it as ACTIVE_KEY.

---

**2. Launch all five checks in parallel**

Spawn five agents simultaneously using a single message with five Agent tool calls:

```
Agent 1: /test-coverage
Agent 2: /security-check
Agent 3: /secrets-scan
Agent 4: privacy-guard agent
Agent 5: ai-api-auditor agent
```

Wait for all five to complete before proceeding.

---

**3. Record results in commit-log.md**

For the three tracked skills, determine the outcome state:
- No issues found → `passed`
- Issues found but user decision required (e.g. intentional secret, low-severity finding) → `pending-user`
- Blocking issue found → `failed`

If ACTIVE_KEY is known, update each skill field:

```bash
python3 ~/.claude/hooks/commit-log.py --cwd . --cmd set --key ACTIVE_KEY --field SKILL_TEST_COVERAGE --value <state>
python3 ~/.claude/hooks/commit-log.py --cwd . --cmd set --key ACTIVE_KEY --field SKILL_SECURITY_CHECK --value <state>
python3 ~/.claude/hooks/commit-log.py --cwd . --cmd set --key ACTIVE_KEY --field SKILL_SECRETS_SCAN --value <state>
```

`privacy-guard` and `ai-api-auditor` results are reported inline but do not block the commit gate — surface any FAIL verdicts and ask the user to confirm before proceeding.

If ACTIVE_KEY is empty (no active block yet), save the results to memory — the pre-commit hook will create the block on the first `git commit`, and you should update the fields immediately after.

---

**4. Optional refactor candidates (advisory)**

After the five blocking checks above, run `/refactor` in **analysis-only mode** on the staged diff (not the whole codebase, to keep cost low). This is advisory — it never blocks the commit, but surfaces named transformation candidates for next session.

```bash
git diff --cached --name-only | head -10
```

For each staged Python/JS/TS file, run a quick smell scan (Long Method, Duplicate Code, Long Parameter List). Print the top 3 candidates if any. Do NOT block — just inform.

---

**5. Print summary**

```
Pre-commit check complete

  /test-coverage:    <state>
  /security-check:   <state>
  /secrets-scan:     <state>
  privacy-guard:     PASS / FAIL / REVIEW
  ai-api-auditor:    PASS / FAIL

  Refactor candidates: <N> (advisory, see /refactor for details)
```

Then one of:
- All passed → `All checks passed. Safe to commit.`
- Any pending-user → `Resolve pending-user items above, then update commit-log.md to passed before committing.`
- Any skill failed → `Fix the issues above, re-run the failed skill(s), update commit-log.md, then retry the commit.`
- privacy-guard or ai-api-auditor FAIL → Surface the specific violations and ask user to confirm or fix before committing.

---

**6. If any skill failed**

Do NOT proceed to commit. Fix the reported issues, re-run only the failed skill(s), update the relevant field(s) in commit-log.md, then instruct the user to retry.
