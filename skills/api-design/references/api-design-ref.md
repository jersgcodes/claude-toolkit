# api-design-ref.md — Reference material for /api-design

---

## Stage 3 — Error envelope JSON example

```json
{
  "error": {
    "code": "validation_failed",
    "message": "email is required",
    "details": [{"field": "email", "issue": "missing"}],
    "request_id": "req_abc123"
  }
}
```

- `code` is machine-parseable (snake_case enum, stable contract)
- `message` is human-readable, can change
- `details` is optional, structured
- `request_id` is required for support/debugging

Document the full enum of `code` values. Treat as a versioned contract.

---

## Stage 3 — Status codes table

| Code | Meaning |
|---|---|
| `200` | OK with body |
| `201` | Created (return resource in body) |
| `204` | No Content (success, no body — DELETE) |
| `400` | Bad Request (validation, malformed) |
| `401` | Unauthorized (no/bad credentials) |
| `403` | Forbidden (auth ok, not allowed) |
| `404` | Not Found |
| `409` | Conflict (state collision, idempotency mismatch) |
| `422` | Unprocessable Entity (semantic validation) |
| `429` | Rate Limited |
| `500` | Server Error (your bug) |
| `503` | Service Unavailable (upstream down) |

---

## Stage 3 — Pagination patterns

- **Cursor-based** (recommended): `?cursor=xxx&limit=20` returns `{items, next_cursor}`. Stable under writes.
- **Offset/limit**: `?offset=40&limit=20`. Simple but breaks if data shifts.
- **Page-number**: `?page=3`. Almost always cursor-or-offset in disguise.

---

## Stage 4 — Resource example tables and payload examples

```markdown
## Resource: User

| Method | Path | Purpose | Auth | Status |
|---|---|---|---|---|
| POST | /v1/users | Create user | none (public signup) | 201 / 400 / 409 |
| GET | /v1/users/{id} | Get one user | owner or admin | 200 / 401 / 403 / 404 |
| PATCH | /v1/users/{id} | Update fields | owner | 200 / 400 / 401 / 404 |
| DELETE | /v1/users/{id} | Soft-delete user | owner | 204 / 401 / 404 |
| GET | /v1/users/{id}/orders | List user's orders | owner or admin | 200 (cursor) / 401 |

### Payloads

POST /v1/users (request):
{
  "email": string (required, RFC 5322),
  "name": string (required, 1-100 chars)
}

POST /v1/users (response 201):
{
  "id": "usr_abc123",
  "email": "...",
  "name": "...",
  "created_at": "2026-05-20T14:30:00+08:00"
}
```

For Telegram bot commands, use a similar table:
```markdown
| Command | Args | Purpose | Output |
|---|---|---|---|
| /menu | — | Main menu | Message + inline keyboard |
| /status <project> | required | Project deep-dive | Message |
```
