---
name: fact-check
description: Fact-check data files for hallucinated claims, unsourced estimates, and stale figures. Classifies every data point as VERIFIED, ESTIMATE, or UNVERIFIED.
version: 0.1.0
---


# Fact Check (Data Source Audit)

Scan data files for hallucinated claims, unsourced estimates, and stale data. Classifies every data point as VERIFIED, ESTIMATE, or UNVERIFIED. Flags hallucination risks.

## Classification system

Every data point in the system falls into one of three tiers:

- **VERIFIED** — backed by a URL, official source, or scraped data. Trustworthy.
- **ESTIMATE** — reasonable approximation, clearly marked as such in code (comment, `basis` field, or `estimate` field). Acceptable as long as it's labelled.
- **UNVERIFIED** — specific dollar amount, percentage, or regulatory claim with no source and no "estimate" marker. Hallucination risk. Must be either verified, marked as estimate, or removed.

The goal is zero UNVERIFIED items. Estimates are fine — hallucinations pretending to be facts are not.

## Steps

**1. Scan upgrade-paths for opportunity costs**

Read all area files in `src/data/upgrade-paths/` (excluding index.js, dependencies.js). For each file:
- Find every `annualLoss` field. Classify:
  - VERIFIED: has a `source` or `basis` field, or a comment citing a reference
  - ESTIMATE: has an `estimate` field that provides reasoning (e.g., "8-12 hrs/month at $25/hr")
  - UNVERIFIED: bare dollar amount with no `estimate`, `source`, or `basis` — **flag as hallucination risk**
- Find every `monthlyCost` field. Cross-check against `pricingActual` in `src/data/tool-registry.js`. Flag mismatches.
- Count and report: X verified, Y estimates, Z unverified

**2. Scan tool-registry for pricing accuracy**

Read `src/data/tool-registry.js`:
- Flag tools where `pricingSource` is "estimated" — acceptable but note them
- Flag tools where `pricingAsOf` is older than 6 months from today — **stale, may be wrong**
- Flag tools with no `pricingActual` field — **unverified pricing**
- For tools with `pricingSource: "manual"` or `"scraped"`, classify as VERIFIED

**3. Scan sector data for regulatory claims**

Read `src/data/sg-sectors.js`:
- For each sector's `regs` array:
  - VERIFIED: has a URL field or references a specific act/regulation by name
  - ESTIMATE: general guidance (e.g., "food safety training required")
  - UNVERIFIED: specific penalty amounts, thresholds, or deadlines with no source — **hallucination risk** (e.g., "$5,000 fine" with no reference to the actual act)
- For `commonPitfalls`: classify enforcement examples as VERIFIED (cites case/agency) or UNVERIFIED

**4. Scan constants for magic numbers**

Read `src/data/sg-constants.js`:
- Flag any dollar amount, percentage, or threshold (e.g., CPF rates, salary thresholds, penalty amounts)
- VERIFIED: has an inline comment citing the source (e.g., `// MOM.gov.sg as of 2025`)
- UNVERIFIED: bare number with no comment — **hallucination risk for regulatory figures**

**5. Verify verifiable claims (where possible)**

For items classified as VERIFIED that include a URL:
- Use WebFetch to check if the URL returns 200 (not 403/404)
- If URL is dead, downgrade to UNVERIFIED and flag: "source URL broken"
- Skip .gov.sg URLs that are known to block bots (note in report)

For regulatory dollar amounts (CPF rates, EP salary thresholds, GST rate):
- Cross-check against known current values if you have them
- Flag any that look outdated (e.g., EP salary threshold changed in 2025)

**6. Generate fix suggestions**

For each UNVERIFIED item, suggest one of:
- **Add source:** "Add `// Source: [url]` comment" — if you can find the actual source
- **Mark as estimate:** "Add `basis: 'estimated from industry average'`" — if the number is reasonable but can't be sourced
- **Remove or replace:** "This figure appears fabricated" — if the number is suspiciously specific with no basis

**7. Print report**

```
## Source Audit Report

### Tier Summary
- VERIFIED: X items (backed by source/URL)
- ESTIMATE: X items (marked as approximations)
- UNVERIFIED: X items (hallucination risk — needs action)

### Hallucination Risks (UNVERIFIED)
<file:line — field — value — suggested fix>
...

### Stale Data
<file:line — field — value — last verified date — "older than 6 months">
...

### Broken Source URLs
<file:line — URL — HTTP status>
...

### Estimates (acceptable, for awareness)
<file:line — field — value — basis>
...

### Verified Items (no action needed)
Total: X items across Y files
```

Keep the report actionable. UNVERIFIED section first — those need immediate attention. Estimates section is informational only.

**8. If `--fix` argument is provided**

For each UNVERIFIED item where the fix is "mark as estimate":
- Add an inline comment: `// estimate — [basis]`
- This converts UNVERIFIED → ESTIMATE, which is acceptable

Do NOT auto-fix items that need actual source verification. Only mark clearly reasonable approximations as estimates.
