---
name: scale-audit
description: Assess whether a repo and its deployment are ready to be exposed publicly and scaled, and whether scaling is warranted yet at all. Grounds every recommendation in the actual code and deployment plus current best practice for that specific stack. Use before a public launch or when traffic is expected to grow.
allowed-tools: [Read, Glob, Grep, Bash, WebSearch, WebFetch]
version: 0.1.0
---

# Scale Audit

Assess whether a repo/service is ready to be deployed publicly and scaled — and, just as
important, whether scaling is even warranted yet. Ground every recommendation in the system's
actual code + deployment, and in current best-practice documentation for its specific stack.

Read the workspace `DEPLOYMENT.md` first for how things are actually hosted.

## Stage 0 — Do we even need to scale? (gate first)

Premature scaling is a cost, not a virtue (workspace rule: simplicity first). Before recommending
anything, establish:
- **Current + realistically-expected load** — users, req/s, data volume, growth. If it's a
  personal or single-user tool, say so and stop over-engineering: the honest answer may be
  "right-sized already — add auth + a health check and move on."
- **What actually breaks first at 10× / 100×** — name the concrete bottleneck; don't hand-wave.

If scaling isn't warranted, say that plainly and give only the cheap readiness/safety items.

## Stage 1 — Understand the system

- **Stack:** language, framework, server (sync/async), DB, cache, queue, hosting model
  (docker-compose / systemd / serverless) — from the repo + `DEPLOYMENT.md`.
- **Deployment shape:** single instance? behind nginx/Cloudflare? stateful?
- **Where state lives:** in-memory, local disk, SQLite, external DB.

## Stage 2 — Assess across the scaling dimensions

For each: current status → gap → recommendation (with rough effort).

1. **Statelessness / horizontal scale** — in-memory/session/local-disk state that blocks running
   N instances; sticky-session needs.
2. **Data layer** — connection pooling, indexes, N+1 queries, hot tables; SQLite→Postgres
   threshold; read replicas; migration safety.
3. **Concurrency model** — blocking I/O on an async server, worker/thread counts, GIL-bound CPU
   work, long requests that should be async jobs.
4. **Caching** — CDN for static/assets, app-level cache for hot reads, HTTP cache headers,
   invalidation strategy.
5. **Background work** — inline work that belongs in a queue; scheduled jobs; idempotency + retries.
6. **Rate limiting, auth & abuse** — public endpoints without auth or limits (a real leak/DoS
   risk — cf. the sme-outreach exposure); per-key quotas.
7. **Resilience** — timeouts, retries w/ backoff, circuit breakers, graceful degradation, health
   checks, restart policy.
8. **Observability** — structured logs, metrics, error tracking, alerting; can you *see* the
   bottleneck under load?
9. **Infra & cost** — resource limits, autoscaling/load balancing, right-sizing, image size, cold
   starts, $ per unit of load.
10. **Data/PII at scale** — what personal data is served, retention, exposure surface
    (PDPA-relevant for SG contact data).

## Stage 3 — Absorb current best practices

For the specific stack, pull authoritative, up-to-date guidance and cite it:
- Framework scaling/deployment guide (e.g. Uvicorn/Gunicorn workers, Node clustering, Next.js).
- Database scaling docs (Postgres pooling / PgBouncer, indexing).
- The hosting platform's scaling & limits docs.
Use WebSearch/WebFetch; prefer official docs; note the publication date. Fold anything that
changes a recommendation back into Stage 2 — don't cite generically.

## Stage 4 — The report

- **Verdict** (one line): scale now / harden-then-hold / right-sized as-is.
- **Ranked actions** by impact × effort (highest leverage first) — each: change/add/adjust, why,
  rough effort, which dimension it fixes.
- **First bottleneck** you'd hit, and the single highest-value change.
- **Explicitly premature / out of scope** — what NOT to do yet, and the signal that would make it
  worth doing.
- **Docs consulted** (with dates).

Be candid (see "How to advise me" in `CLAUDE.md`): if the honest answer is "don't scale this, just
add auth and right-size," say exactly that.
