---
name: postmortem
description: Blameless postmortem after an incident or significant bug. Captures timeline, contributing factors, and concrete action items. Outputs to docs/postmortems/.
version: 0.1.0
---


# Postmortem

A blameless postmortem captures **what happened, why, and what we'll change** — without assigning blame to individuals. The goal is system-level learning, not punishment.

Based on the Google SRE book (Chapter 15) and Etsy's blameless culture (John Allspaw, 2012). The "Five Whys" technique (Toyota) is used to drive past surface symptoms to root causes.

---

## When to write a postmortem

| Situation | Postmortem? |
|---|---|
| Production outage > 15 min | YES |
| Data loss or corruption | YES |
| Security incident (token leak, vulnerability) | YES |
| Bug that took > 4h to find | YES (the surprise itself is worth capturing) |
| Hotfix to main bypassing normal flow | YES |
| Bot/service crashed and you didn't notice | YES (alerting failed too) |
| Bug fix that took 30 min | NO — commit message is enough |
| Linting issue | NO |
| Plan went smoothly | NO |

**Rule of thumb:** if you said "wait, what?" or "how did that happen?" during the incident, write the postmortem.

---

## Stage 1 — Frame the incident

From `$ARGUMENTS` or ask:

1. **What was the impact?** (specific: "users couldn't login for 2h", "5 records corrupted", "bot offline for 2 days")
2. **When did it start?** (UTC or local timezone — be explicit)
3. **When was it detected?** (often later than start — note the gap)
4. **When was it resolved?** (define "resolved" — temporary fix vs root-fix)
5. **Severity:**
   - SEV-1 (critical, total outage, data loss)
   - SEV-2 (major, degraded service)
   - SEV-3 (minor, single feature broken)
   - SEV-4 (cosmetic, no user impact, but worth learning)

If user can't provide times, run:
```bash
git log --since="2 days ago" --pretty=format:"%h %ci %s" | head -20
```
to reconstruct timeline from commits.

---

## Stage 2 — Reconstruct the timeline

Build an ordered timeline of events. Each entry: timestamp + what happened + who/what observed it.

```bash
# Help reconstruct from git
git log --all --since="<incident_start - 24h>" --pretty=format:"%ci %h %s" | head -50

# Help reconstruct from logs (project-specific)
# - launchd logs: ~/claude/<project>/logs/
# - VPS docker logs: ssh root@... "docker logs <container> --since <start>"
# - orchestrator: ~/claude/claude-orchestrator/orchestrator.log
```

Format:
```
| Time (UTC) | Event |
|---|---|
| 14:00 | Deploy of commit abc123 to main |
| 14:15 | First user reports login failure (Telegram) |
| 14:23 | Bot heartbeat alert fires |
| 14:30 | Investigation begins |
| 14:55 | Root cause identified: env var TYPO_KEY missing |
| 15:00 | Fix deployed: commit def456 |
| 15:05 | Service restored |
```

**Detection gap:** time from start to detection. **Resolution gap:** time from detection to resolution. Both are improvement targets.

---

## Stage 3 — Five Whys (root cause)

Start with the surface symptom and ask "why" five times to drive past it.

Example:
- **Q1:** Why did login fail? **A:** Env var missing in production.
- **Q2:** Why was it missing? **A:** I forgot to add it to Coolify when adding the new feature.
- **Q3:** Why did I forget? **A:** No checklist when promoting from dev to prod.
- **Q4:** Why is there no checklist? **A:** Solo workflow, never formalized.
- **Q5:** Why does this matter now? **A:** Project complexity grew past the point where memory works.

Root cause: **missing deploy checklist for env vars**, not "user typo." This frames the action items to fix the system, not blame the person.

---

## Stage 4 — Contributing factors

Beyond the immediate cause, what else made this worse?

- **Detection delay** — was monitoring missing or too slow?
- **Knowledge gaps** — was the failure mode unfamiliar?
- **Tooling gaps** — did the deploy/recovery tools make it harder?
- **Documentation gaps** — was the system poorly documented?
- **Process gaps** — was there no checklist / review / staging environment?

List 2-4 contributing factors. The goal is to find leverage points where one fix prevents many future incidents.

---

## Stage 5 — What went well

Postmortems are not all blame. Capture what worked:
- Did monitoring catch it quickly?
- Did the rollback go smoothly?
- Did logs make it findable?
- Did anyone make a good call under pressure?

This protects the things that worked.

---

## Stage 6 — Action items (concrete)

Each action item must be:
- **Specific** — "Add a deploy checklist with env vars to verify" not "improve deploys"
- **Owned** — name + date (for solo work, just date)
- **Trackable** — added to TASKS.md as a real task
- **Bounded** — completable, not a vague aspiration

```markdown
| # | Action | Owner | By | Status |
|---|---|---|---|---|
| 1 | Add `pre-deploy-checklist.md` to repo | Jerome | YYYY-MM-DD | PENDING |
| 2 | Add Coolify env var diff alert to /vps | Jerome | YYYY-MM-DD | PENDING |
| 3 | Document the failure mode in MISTAKES.md | Jerome | YYYY-MM-DD | DONE (this session) |
```

**Anti-pattern:** action items like "be more careful" or "review more thoroughly" — these don't change the system. Reject them.

---

## Stage 7 — Write the postmortem

Save to `docs/postmortems/YYYY-MM-DD-<short-name>.md`:

```markdown
# Postmortem: <one-line summary>

**Date:** YYYY-MM-DD
**Severity:** SEV-X
**Author:** <name>
**Status:** Resolved | Mitigated | Ongoing

## Impact

<2 sentences: what users experienced, scope, duration>

## Timeline

| Time (UTC) | Event |
|---|---|
| ... | ... |

**Detection gap:** <minutes>
**Resolution gap:** <minutes>

## Five Whys

Q1: <surface question> A: <answer>
Q2: <next why> A: <answer>
... (continue to Q5)

**Root cause:** <one sentence>

## Contributing Factors

- <factor 1>
- <factor 2>

## What Went Well

- <thing 1>
- <thing 2>

## Action Items

| # | Action | Owner | By | Status |
|---|---|---|---|---|
| 1 | ... | ... | ... | PENDING |

## Related

- Commit(s): <SHA>
- Issue(s): <link>
- ADR(s): <if a decision contributed or was reversed>
- MISTAKES.md entry: <if added>
```

---

## Stage 8 — Hook into MISTAKES.md and TASKS.md

Add a one-line root-cause entry to MISTAKES.md (with postmortem link) and copy action items to TASKS.md as PENDING tasks.

---

## Stage 9 — Confirm

Print:
```
Postmortem written: docs/postmortems/<filename>
Severity: SEV-X
Root cause: <one-line>
Action items added to TASKS.md: N
MISTAKES.md updated: yes/no

Next: complete the action items in priority order to prevent recurrence.
```

---

## Blameless principle (DO NOT skip)

Every postmortem must focus on **systems and processes**, not people. Re-read the document and remove:
- "I should have known better" → "the system didn't surface this"
- "User should have noticed" → "monitoring failed to alert"
- Any phrasing that assigns moral fault to a person

Solo work doesn't escape this — be kind to past-you. The postmortem is for future-you.

---

## Cost control

- Reads commit history, log files, and code — moderate cost
- Use a subagent for deep log analysis if logs are > 1MB
- Cap timeline at 20 events. If more, summarize.

