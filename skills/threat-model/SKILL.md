---
name: threat-model
description: STRIDE threat model for a feature or system. Maps data flows, identifies threats per component, suggests mitigations. Outputs to docs/threats/.
version: 0.1.0
---


# Threat Model

Structured "how could this be abused or fail" analysis. Different from `/security-check` (post-build vulnerability scan) — this runs at DESIGN time to shape what gets built.

Sources: Adam Shostack *Threat Modeling: Designing for Security*, Microsoft Security Development Lifecycle (SDL), OWASP Threat Modeling.

---

## When to use

| Situation | Use? |
|---|---|
| Designing a new service handling user data | YES |
| Designing a service that talks to external APIs with credentials | YES |
| Adding a public endpoint | YES |
| Storing new sensitive data (PII, secrets, financial) | YES |
| Internal refactor with no boundary changes | NO |
| Adding a logging line | NO |

---

## Stage 1 — Identify what you're protecting

Ask:

1. **What are the assets?** (Data, money, reputation, availability, secrets)
2. **Who are the actors?** (User, admin, attacker, accidental insider, automated agent)
3. **What's the trust boundary?** (Where does untrusted input become trusted? Network edge? Auth check?)
4. **What's the impact tier?** If this fails:
   - **Catastrophic** — data loss, financial theft, regulatory violation
   - **High** — service unavailable, customer trust damaged
   - **Medium** — degraded UX, recovery is manual
   - **Low** — cosmetic issue

If the impact is Low across the board, you probably don't need a formal threat model. Document the decision and move on.

---

## Stage 2 — Draw the data flow diagram (DFD)

Identify the four DFD elements per the threat-model standard:

| Element | Symbol | Examples |
|---|---|---|
| **External entity** | rectangle | User browser, third-party API, Telegram, attacker |
| **Process** | circle | Your API handler, your worker, your Telegram bot |
| **Data store** | parallel lines | SQLite db, 1Password vault, Coolify env vars |
| **Data flow** | arrow | HTTP request, file read, DB query, env var lookup |

Use Mermaid to keep it in version control:

> **Reference:** Full Mermaid DFD example for this stage is in `references/threat-model-ref.md`.

**Trust boundaries** = dotted lines around clusters of equally-trusted elements. The most important ones:
- Network edge (anything from internet is untrusted until validated)
- Auth boundary (anonymous → authenticated)
- Privilege boundary (user → admin)
- Process boundary (your code → third-party library/API)

---

## Stage 3 — Apply STRIDE per element

For EACH process and data store, walk through STRIDE:

| Letter | Threat | Property violated | Examples |
|---|---|---|---|
| **S**poofing | Pretending to be someone else | Authentication | Forged auth header, replay attack, fake Telegram chat_id |
| **T**ampering | Modifying data in transit/rest | Integrity | SQL injection, modified DB row, tampered JWT |
| **R**epudiation | "I didn't do that" | Non-repudiation | No audit log, no signed actions |
| **I**nformation disclosure | Leaking what should be private | Confidentiality | Verbose errors leaking schema, secrets in logs, side channel |
| **D**enial of service | Making unavailable | Availability | Rate limit absent, infinite loop input, resource exhaustion |
| **E**levation of privilege | Becoming someone you're not | Authorization | IDOR (insecure direct object reference), missing role check, path traversal |

For each element, ask all 6 questions. Skip the ones that don't apply, but explicitly note WHY they don't apply.

### Example: a Telegram bot command handler

| Threat | Specific to this code | Likely? | Impact |
|---|---|---|---|
| S — Spoofing | Could anyone send `/admin-only-command` and have it accepted? | YES — bot only checks if `chat_id == admin_id`; spoofable if attacker compromises chat | High |
| T — Tampering | Can input modify the prompt structure (prompt injection)? | YES | Medium |
| R — Repudiation | If an admin runs `/dangerous-command`, is it logged? | NO logging beyond default | Medium |
| I — Info disclosure | Could the bot reply with another user's data? | Bot is single-user, so N/A | — |
| D — DoS | Can a user send 1000 commands/sec to exhaust quota? | Telegram rate-limits per chat, partial mitigation | Low |
| E — Elevation | Can a non-admin run admin commands? | Mitigated by chat_id check; no path to bypass | Low |

---

## Stage 4 — Rate and prioritize

For each identified threat, score:

- **Likelihood** (Low / Medium / High) — how easy is the attack?
- **Impact** (Low / Medium / High) — how bad is success?
- **Risk = Likelihood × Impact**

Focus the design effort on High-risk threats. Document Low-risk threats as "accepted risk" so future-you knows the decision was deliberate.

---

## Stage 5 — Propose mitigations

For each High and Medium risk threat, propose ONE concrete mitigation. Tie it to the design or code.

> **Reference:** Mitigation-patterns table for this stage is in `references/threat-model-ref.md`.

If you can't think of a mitigation, the design needs to change.

---

## Stage 6 — Specific patterns for YOUR workspace

> **Reference:** Workspace-specific threat patterns (AI/LLM, Telegram bot, SQLite, VPS) for this stage are in `references/threat-model-ref.md`.

---

## Stage 7 — Write the threat model doc

Save to `docs/threats/<feature>.md`:

```markdown
# Threat Model: <feature name>

**Date:** YYYY-MM-DD
**Reviewer:** <you>
**Scope:** <what's in / what's out>

## Assets at risk
- ...

## Trust boundaries
- ...

## Data flow diagram

[Mermaid diagram]

## STRIDE analysis

### Process: <name>

| Threat | Likely | Impact | Risk | Mitigation |
|---|---|---|---|---|
| S — ... | M | H | High | ... |
| T — ... | L | M | Low | accepted |
| ...

### Data store: <name>

[same table]

## Top mitigations (in priority order)
1. ...
2. ...
3. ...

## Accepted risks
- <Risk>: accepted because <reason>. Revisit if <condition>.

## Open questions
- ...
```

---

## Stage 8 — Hook into your existing security workflow

After the threat model:
- **Highest-risk mitigations** become tasks in TASKS.md (Status: PENDING)
- **Implementation choices** that arose may need `/decision-record` (e.g. "we chose JWT over session cookies because…")
- **Run-time checks** become `/security-check` rules (post-build verification)
- **Accepted risks** become MISTAKES.md entries if they're things you might forget

---

## Cost control

- Reads existing code to understand current flows — cap at 10 files
- Output is design doc, not code
- For very large systems, threat-model ONE service at a time

---

## Integration

- Pulls from: `/feature-design`, `/api-design`, `/schema-design` (all surface attack-able elements)
- Hands off to: `/decision-record` (capture mitigation choices), `/security-check` (run-time verification), TASKS.md (mitigation backlog)
- Related: `/postmortem` references threat model when incidents trace back to unaddressed threats

---

## Anti-patterns to flag

- **Threat model without DFD** — you're guessing at threats without seeing the surface
- **"Trust the framework"** — frameworks have CVEs; threat-model the integration points
- **One-shot — never revisited** — re-run when boundaries change or new attack patterns emerge
- **Mitigation = "be careful"** — not a mitigation; must be enforced by code/policy
- **STRIDE applied only to network** — file system, env, third-party libraries are also attack surfaces
- **"Solo project — no threats"** — your data still matters; threats include accidental loss, not just adversaries
