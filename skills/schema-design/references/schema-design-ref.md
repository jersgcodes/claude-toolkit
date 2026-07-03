# schema-design-ref.md — Reference material for /schema-design

---

## Stage 3 — Full conventions block

### Primary keys
- **ULIDs or UUIDs as TEXT** for distributed/append-only feel (recommended for new projects)
- **INTEGER PRIMARY KEY AUTOINCREMENT** only if you really need sequential ints
- Avoid composite primary keys unless natural (e.g. `(user_id, role_id)` for a join table)

### Standard columns on every entity
- `created_at` TEXT NOT NULL (ISO 8601 with timezone)
- `updated_at` TEXT NOT NULL
- `deleted_at` TEXT (NULL means active; non-null means soft-deleted)
- For multi-tenant: `tenant_id` TEXT NOT NULL on every tenant-scoped table

### Soft delete vs hard delete
- **Soft delete (deleted_at column)** for: anything user-visible, anything with foreign-key references, audit/compliance needs
- **Hard delete** for: ephemeral logs, session tokens, expired data with retention policy

### Timestamps
- SQLite has no native datetime; store as ISO 8601 TEXT with timezone
- Or INTEGER unix-seconds if you don't need human-readable. Pick ONE per project.

### Naming
- Table names: snake_case, plural (`users`, `orders`, `order_items`)
- Column names: snake_case
- Foreign keys: `<referenced_table_singular>_id` (e.g. `user_id`)
- Booleans: `is_<state>` or `has_<thing>` prefix (e.g. `is_admin`, `has_verified_email`)
- Don't suffix with type (`user_dict`, `name_text` — bad)

---

## Stage 5 — Index-strategy recipes

### Composite indexes
- For `WHERE a = ? AND b = ?`, create `INDEX(a, b)` — order matters: equality columns first, then range
- For `WHERE a = ? ORDER BY b`, create `INDEX(a, b)`

### Partial indexes (Postgres) / WHERE-clause indexes (SQLite 3.8+)
- For "soft-deleted rows" pattern: `CREATE INDEX active_users ON users(email) WHERE deleted_at IS NULL`
- Smaller, faster than indexing all rows when most queries filter out a subset

### SQLite-specific index notes
- Use `WITHOUT ROWID` for tables where the primary key is the natural lookup (saves space, faster lookups)
- Use `INTEGER PRIMARY KEY` (not just `INTEGER` PK) to make it an alias for ROWID
- Enable `PRAGMA foreign_keys = ON;` at connection time (off by default!)
- Use `PRAGMA journal_mode = WAL;` for concurrent readers + one writer

---

## Stage 6 — SQLite-specific migration notes

For SQLite specifically:
- `ALTER TABLE` is limited (can't drop columns until SQLite 3.35, can't rename columns until 3.25)
- For destructive changes: create new table → INSERT INTO new SELECT FROM old → DROP old → RENAME
- Wrap in BEGIN TRANSACTION ... COMMIT

---

## Stage 7 — Design doc template with DDL

Save to `docs/schema/<feature>.md`:

```markdown
# Schema: <feature name>

## Entities

### users
- id (TEXT PK, ULID)
- email (TEXT NOT NULL UNIQUE)
- ...

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    deleted_at TEXT
);
CREATE INDEX users_email_active ON users(email) WHERE deleted_at IS NULL;

### orders
- ...

## Relationships
- users 1:N orders (via orders.user_id)
- orders M:N products (via order_items)

## Access patterns (and supporting indexes)
- "Get user by email (active only)" → users_email_active
- "Get all orders for a user" → orders(user_id, created_at DESC)
- "Get order with line items" → join via PK lookup, no extra index

## Denormalizations
- orders.user_email — kept in sync via app code on email change (not common). Tradeoff: avoid join in hot path.

## Migration plan (expand/contract)
1. (deploy 1) Add tables: users, orders, order_items
2. Backfill from legacy users.csv
3. (deploy 2) Add code reading new tables
4. (deploy 3, later) Drop legacy users.csv reader
```
