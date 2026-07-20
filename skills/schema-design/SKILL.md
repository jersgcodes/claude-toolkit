---
name: schema-design
description: Design a database schema before writing migrations. Covers entity modeling, normalization, indexing, migration safety, and SQLite-specific patterns.
allowed-tools: [Read, Glob, Grep, Write, Bash]
version: 0.1.0
---



# Schema Design

Design data models intentionally rather than discovering them through painful ALTER TABLE iterations. Most of your projects use SQLite — this skill is optimized for that, with notes for Postgres where they differ.

Sources: Martin Kleppmann *Designing Data-Intensive Applications*, Pramod Sadalage *Refactoring Databases*, the SQLite documentation on schema migration patterns.

---

## When to use

| Situation | Use? |
|---|---|
| Adding a new feature with 2+ new tables | YES |
| Adding 1 new table that joins existing ones | YES |
| Significant denormalization or restructuring | YES |
| Adding 1 column to an existing table | NO — write migration directly |
| Renaming a column | NO — straightforward |
| Designing a queue, audit log, or event table | YES (these have specific patterns) |

---

## Stage 1 — Frame the domain

Ask (or extract):

1. **What are the entities?** (Nouns the system tracks. List them.)
2. **What are the relationships?** (1:1, 1:N, N:M between which pairs?)
3. **What's the access pattern?** (Read-heavy? Write-heavy? Both? Time-windowed reads?)
4. **What's the volume?** (Rows after 1 year? 5 years? Sets the indexing strategy.)
5. **What's mutable vs immutable?** (Append-only vs in-place updates change the design.)
6. **What's the consistency requirement?** (Transactional? Eventually consistent?)
7. **Multi-tenant?** (`tenant_id` column needed? Or separate database per tenant?)

---

## Stage 2 — Sketch the entities

For each entity, define:

```
ENTITY: User
PURPOSE: Authenticated person who uses the app
KEY: id (text, ulid or uuid)
ATTRIBUTES:
  - email (text, unique, not null)
  - name (text, not null)
  - created_at (text, ISO 8601, not null)
  - updated_at (text, ISO 8601, not null)
  - deleted_at (text, ISO 8601, nullable)  -- soft delete
RELATIONSHIPS:
  - has_many: Orders (via Order.user_id)
INVARIANTS:
  - email is lowercase
  - deleted_at can only transition null → set, never back
```

Do this for every entity BEFORE writing CREATE TABLE statements.

---

## Stage 3 — Lock conventions (once per project)

These apply uniformly. Decide once, document in CLAUDE.md.

> **Reference:** Full conventions block (primary keys, standard columns, soft delete, timestamps, naming) is in `references/schema-design-ref.md`.

---

## Stage 4 — Normalize, then denormalize on purpose

Default to 3NF:
- **1NF:** atomic values (no comma-separated lists in a column)
- **2NF:** non-key columns depend on the full key (split composite keys when needed)
- **3NF:** no transitive dependencies (no `user.country` AND `user.country_code` derivable from each other)

Then deliberately denormalize ONE of these patterns when justified:

| Denormalization | When to use |
|---|---|
| Cached count (`user.order_count`) | Read-heavy, count is stable, must be kept in sync via trigger or app logic |
| Cached lookup (`order.user_email`) | Avoid join in hot path; accept staleness when user updates email |
| Materialized view (separate table refreshed on schedule) | Complex aggregations queried often |
| JSON column for sparse fields | Many optional attributes, no need to index them |
| Wide table (denormalized join) | Read-heavy, fixed query shape, very rarely written |

Document the denormalization in a comment AND explain how it's kept in sync.

---

## Stage 5 — Index strategy

Indexes speed reads but slow writes and use space. Be deliberate.

### Index every:
- Primary key (automatic)
- Foreign key (queried as filter in joins)
- Columns in WHERE/ORDER BY clauses of common queries

### Don't index:
- Low-cardinality columns alone (e.g. `is_active` with 50/50 split — full scan is faster)
- Columns rarely queried
- Tables under 1000 rows (full scan is fast)

> **Reference:** Composite/partial index recipes and SQLite-specific index notes are in `references/schema-design-ref.md`.

---

## Stage 6 — Migration safety (CRITICAL)

If the table exists in production, follow expand/contract:

### Expand (deploy 1)
- Add new columns (NULLABLE)
- Add new tables
- Add new indexes (CONCURRENTLY in Postgres; SQLite is single-writer so just do it)
- Backfill data
- Deploy code that writes BOTH old and new

### Migrate
- Deploy code that reads from NEW location, falls back to OLD
- Run for >= 1 week to confirm stability

### Contract (deploy 2)
- Drop reads from OLD
- Make NEW columns NOT NULL if needed
- Drop OLD columns / tables / indexes

**Rule:** never combine schema change + code logic change in the same deploy. Two deploys minimum.

> **Reference:** SQLite-specific migration notes (ALTER TABLE limits, create-copy-drop-rename pattern) are in `references/schema-design-ref.md`.

---

## Stage 7 — Write the design doc

Save to `docs/schema/<feature>.md`.

> **Reference:** Full doc template with DDL examples (entities, relationships, access patterns, denormalizations, migration plan) is in `references/schema-design-ref.md`.

---

## Stage 8 — Validate before writing migrations

- [ ] Every query in the access pattern list has an index supporting it
- [ ] All foreign keys have an index (SQLite does NOT auto-index FKs)
- [ ] Every table has created_at + soft delete (if applicable)
- [ ] Every denormalization has a sync mechanism documented
- [ ] Migration is split into safe expand/contract phases if production-affecting
- [ ] PRAGMA foreign_keys is enabled in app code
- [ ] WAL mode considered for write-concurrent SQLite
- [ ] No column called `data`, `info`, `metadata` (those are smells — be specific)

---

## Cost control

- Reads existing migration files / schemas — cap at 5 files
- Output is design doc + DDL, not implementation
- Don't run migrations — just generate the plan

---

## Integration

- Pulls from: `/feature-design` (when data model emerges), `/api-design` (resources usually map to tables)
- Hands off to: `/decision-record` (capture denormalization decisions), implementation (write migration), `/threat-model` (sensitive fields review)
- Related: `/seams` for safely refactoring an existing schema

---

## Anti-patterns to flag

- **Many tables with `metadata` JSON columns** — losing queryability for short-term flexibility
- **No `created_at`** — debugging is misery
- **Hard delete on user-visible data** — irrecoverable mistakes
- **Indexing everything** — write performance dies
- **No foreign key constraints** — invariants drift silently
- **SQLite without `PRAGMA foreign_keys = ON`** — silent reference violations
- **Booleans stored as text** ("yes"/"no") — use INTEGER (0/1)
- **Composite PKs that aren't natural keys** — usually a sign of missing surrogate ID
- **No migration plan for existing production table** — destructive ALTER on first try
