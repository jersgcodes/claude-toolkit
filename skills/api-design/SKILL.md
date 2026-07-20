---
name: api-design
description: Design an API surface (REST/GraphQL/RPC/bot commands) before writing code. Covers resources, verbs, errors, pagination, versioning, contract-first vs code-first.
allowed-tools: [Read, Glob, Grep, Write]
version: 0.1.0
---



# API Design

Design the *shape* of an API surface before writing handler code. The goal is to lock the contract (endpoints, payloads, errors) so backend + frontend + future-you all share the same mental model.

Applies to:
- HTTP REST APIs (Express, FastAPI)
- GraphQL schemas
- gRPC / Protobuf interfaces
- **Telegram bot command surfaces** (your most common case)
- Internal Python/TS module APIs (public function signatures)

Sources: Heroku API Design Guide, Phil Sturgeon's *API Design Patterns*, Stripe API style, Google AIPs (API Improvement Proposals).

---

## When to use

| Situation | Use? |
|---|---|
| Adding 3+ new endpoints | YES |
| Adding a new bot command surface (multiple commands) | YES |
| Designing inter-service contracts | YES |
| Versioning an existing public API | YES |
| Adding one endpoint to an existing well-designed API | NO — follow existing conventions |
| Internal helper function | NO — `/refactor` covers naming |

---

## Stage 1 — Frame the API

Ask (or extract from `$ARGUMENTS`):

1. **What's the consumer?** (Web frontend, mobile app, another service, Telegram user, AI agent)
2. **What's the trust boundary?** (Public internet, authenticated user, trusted internal, machine-to-machine)
3. **What are the resources/operations?** (List the nouns + verbs in one sentence each)
4. **What state changes vs reads?** (Read-only operations cluster separately from writes)
5. **What's the cardinality?** (Operations per minute? Per day? Bursty?)
6. **Versioning expectation?** (Breaking change tolerance: zero / low / high)

---

## Stage 2 — Choose the shape

### REST (best for resource-oriented domains)

- Resources are nouns. Operations are HTTP verbs.
- `GET /users/{id}` — read
- `POST /users` — create
- `PATCH /users/{id}` — partial update
- `DELETE /users/{id}` — delete
- `GET /users/{id}/orders` — nested resource
- Avoid verbs in paths (`/getUsers` is wrong; `/users` + GET is right)
- For non-resource ops, use a `/actions` collection or `:verb` suffix: `POST /users/{id}:archive`

### GraphQL (best for read-heavy, varied query needs)

- Schema-first: define types, queries, mutations in `.graphql`
- One endpoint, many operations
- Best when frontend needs flexible joins / projections

### RPC / gRPC (best for service-to-service)

- Methods, not resources
- Strong typing via Protobuf
- Best when both sides are controlled by you

### Telegram Bot Commands (best for chat-driven UX)

- Commands are verbs prefixed with `/` (e.g. `/menu`, `/status <project>`)
- Inline buttons use callback_data prefixed with a namespace (e.g. `orch:menu`)
- Limit top-level commands to ~10 (any more, use sub-menus via inline keyboards)
- Common pattern from your workspace: `/menu` shows hamburger keyboard, `/help` lists commands

### Choosing — quick rubric

| Need | Pick |
|---|---|
| Public web API with browser/curl access | REST |
| Frontend needs flexible projections | GraphQL |
| Internal microservices with shared schema | gRPC |
| User-driven chat interaction | Telegram bot commands |
| AI agent tool calling | Function definitions (OpenAPI-shaped) |

---

## Stage 3 — Lock the conventions

Before any endpoint, decide and document:

### Authentication
- Bearer token in `Authorization` header? Cookie? API key in header?
- Where do scopes live? Tied to user or to token?

### Error envelope (CRITICAL — biggest source of drift)

Pick ONE shape and use it everywhere.

> **Reference:** Error envelope JSON example, status codes table, and pagination patterns are in `references/api-design-ref.md`.

### Filtering, sorting
- `?filter[status]=active&sort=-created_at`
- Document allowed filter/sort fields explicitly
- Default sort = stable (e.g. `-created_at`)

### Timestamps
- ISO 8601 with timezone (`2026-05-20T14:30:00+08:00`)
- Or Unix epoch seconds (`1748774400`). Pick ONE.
- Resources almost always need `created_at` and `updated_at`

### Versioning
- URL versioning: `/v1/users` (simplest, recommended)
- Header versioning: `Accept: application/vnd.app.v1+json` (cleaner but more friction)
- No versioning: only if you control all consumers AND will never break compatibility
- Document deprecation policy (e.g. "v1 supported until 2027-01-01")

---

## Stage 4 — Sketch the surface

Produce a markdown table per resource/command.

> **Reference:** Resource example tables (REST + Telegram bot) and payload examples are in `references/api-design-ref.md`.

---

## Stage 5 — Write it down

Save the design to `docs/api/<service>.md` (create dir if needed). This becomes the contract — implementation must match. Future changes get a new ADR (`/decision-record`) and a versioned update.

For Telegram bots, save to `docs/bot-commands.md` per project.

---

## Stage 6 — Validate before code

Run through these checks BEFORE writing handlers:

- [ ] **Symmetry:** all collections have both list (GET) and create (POST)?
- [ ] **Idempotency:** PUT/DELETE are safe to repeat? POST has idempotency-key support if needed?
- [ ] **Error shape:** every response has a consistent error envelope?
- [ ] **Auth:** every endpoint states its auth requirement explicitly?
- [ ] **Pagination:** every list endpoint has a cursor or explicit "no pagination needed (max N items)" note?
- [ ] **Naming:** snake_case OR camelCase consistently across all payloads (pick one)?
- [ ] **Versioning:** URL/header strategy applied uniformly?
- [ ] **Discoverability:** is there a `/health`, `/v1/`, or schema introspection endpoint?

If any check fails, fix the design BEFORE writing code. Cheaper than retroactive consistency.

---

## Cost control

- Reads existing project docs to learn conventions — cap at 5 files
- Output is markdown design doc, not implementation
- For very large APIs (20+ endpoints), split into multiple `/api-design` runs by resource cluster

---

## Integration

- Pulls from: `/feature-design` (when planning surfaces a new API contract)
- Hands off to: `/schema-design` (if backed by a database), `/tdd` (implementation), `/threat-model` (security review of the surface)
- Outputs feed: `/decision-record` (capture API choice as ADR), implementation tasks

---

## Anti-patterns to flag

- **Verbs in paths:** `/getUser`, `/createOrder` — use noun + HTTP verb instead
- **Inconsistent error shapes:** half endpoints return `{error: "..."}`, others return `{message: "..."}` — pick one
- **200 OK with `{success: false}`:** use proper status codes
- **Anonymous arrays at top level:** `[{...}]` — wrap in `{items: [...], next_cursor: ...}` for forward compat
- **No request_id:** debugging is misery without it
- **Versioning by feature flag instead of URL/header:** invisible to consumers, breaks contract
