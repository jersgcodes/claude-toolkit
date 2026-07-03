---
name: mcp-scaffold
description: Bootstrap a new MCP server project with battle-tested defaults — OAuth 2.1 or bearer auth, FastMCP transport-security configured, systemd + cloudflared templates, smoke test, unit tests. Saves you from the 8 gotchas /mcp-audit catches.
version: 0.1.0
---


# MCP Server Scaffold

Generates a new MCP server project pre-wired with the patterns that took a reference MCP server a marathon session to discover. Companion to `/mcp-audit` (which catches problems in existing code).

---

## When to use

| Situation | Use? |
|---|---|
| New MCP server, even just for personal use | YES |
| You'll deploy it behind a tunnel (CF / Tailscale / nginx) | YES |
| Pure stdio MCP (Claude Desktop only, no HTTP) | Skip OAuth, use the lightweight stdio template |
| Forking an existing MCP for a tweak | Use the existing repo, run `/mcp-audit` instead |
| MCP wrapping a workplace API | YES — but get internal infra review on the auth choice first |

---

## Before scaffolding — decisions to lock

Walk the user through these. **Don't generate code until all are answered.**

### 1. Project name + location
- `<name>` — used for package name (`<name>_mcp`), repo name, systemd service name, etc.
- Convention: lowercase, hyphens for project, underscores for Python package
- Target dir: usually `~/claude/<name>/`

### 2. Transport
- **stdio only** — Claude Desktop local use, no deploy. Smallest scope. Skip auth, tunnels, OAuth entirely.
- **HTTP behind a tunnel** — accessible from Claude.ai web + mobile + other clients. Need auth.
- **Both** — same codebase serves stdio and HTTP via `--transport` flag (a reference MCP server pattern, recommended)

### 3. Auth (HTTP transport only)
- **Bearer token** — simplest. One static token, set in `.env` and pasted into Claude.ai connector. Fine for single-user personal MCP.
- **OAuth 2.1 with PKCE** — required by MCP 2025 spec; supports multi-user, mobile-friendly, real per-user identity. ~500 lines of code. Use if you'll ever have more than one user or want production-grade auth.
- **No auth** — only if the endpoint has nothing sensitive. Don't pick this for anything that spends money or holds private data.

### 4. Upstream IdP (if OAuth)
- **GitHub** — easiest, you probably have an account, supports Passkeys
- **Google** — wider audience, Passkeys via Google account settings
- **Microsoft** — if your work uses M365
- **DIY email PIN** — no external dep but you implement the email flow
- For v1: pick one, add others later (Phase 2 work)

### 5. Hosting target
- **Hetzner / DigitalOcean / similar VPS** — assume Ubuntu 24.04
- **Cloudflare Tunnel** — recommended (no inbound ports)
- **Custom (Tailscale-only, etc.)** — adjust the deploy templates accordingly
- **Local-only (Claude Desktop stdio)** — skip the deploy layer entirely

### 6. Default port
- Avoid 8080 (Docker/Traefik), 3000 (common Node default)
- Suggest **8082** as a sensible default if hosting on a shared box

---

## Scaffold structure

Generate this layout (omit deploy/* if stdio-only):

```
<name>/
├── README.md                            # what it does + how to run (stdio + HTTP)
├── CLAUDE.md                            # project-specific build rules
├── TASKS.md                             # build backlog
├── USER_ACTIONS.md                      # post-session log
├── project-overview.yaml                # workspace metadata standard
├── pyproject.toml                       # deps + project.scripts entry point
├── requirements.txt                     # for pip-tools / readability
├── .env.example                         # documented env vars
├── .gitignore                           # standard Python + .env + data/*
├── .pre-commit-config.yaml              # ruff + bandit + detect-secrets + pytest
├── .secrets.baseline                    # detect-secrets baseline
├── .github/workflows/ci.yml             # run tests on push/PR
├── <name>_mcp/                          # the MCP server package
│   ├── __init__.py
│   ├── __main__.py                      # `python -m <name>_mcp`
│   ├── server.py                        # FastMCP instance + main()
│   ├── oauth.py                         # OAuth 2.1 server (if HTTP+OAuth picked)
│   └── logging_mw.py                    # tool-call logger middleware
├── deploy/                              # (skip if stdio-only)
│   ├── README.md                        # step-by-step VPS walkthrough
│   ├── install.sh                       # idempotent installer
│   ├── systemd/<name>-mcp.service       # ProtectHome=true + ReadWritePaths
│   └── cloudflared/config.yml.example   # port 8082, 10min keep-alive
├── scripts/
│   └── smoke_test_mcp.py                # post-deploy gate (7-check)
└── tests/
    ├── test_server.py                   # MCP protocol introspection
    ├── test_oauth.py                    # auth unit tests (if OAuth)
    └── test_smoke.py                    # local smoke (skip if CI runs the script)
```

---

## Critical files — what each must contain

### `<name>_mcp/server.py` — FastMCP instance

> **Reference:** the TransportSecuritySettings snippet for this file is in `references/mcp-scaffold-ref.md` — read it when you reach this step.

**Why each piece matters:** see `/mcp-audit` checklist items 1-3.

### `<name>_mcp/oauth.py` (if OAuth) — reference implementation

For a complete RS256 + GitHub OAuth implementation, copy from a reference MCP server:
```bash
cp <your-reference-mcp-project>/kitchen_mcp/oauth.py <name>_mcp/oauth.py
```
Then adapt:
- Rename references from "kitchen_mcp" → "<name>_mcp"
- Update the `OAUTH_ALLOWED_GITHUB_USERS` env var name if you want per-project naming
- Path-prefix the OAUTH_KEY_DIR default to your project

### `deploy/systemd/<name>-mcp.service`

> **Reference:** the full systemd unit file template is in `references/mcp-scaffold-ref.md` — read it when you reach this step.

**Important:** any log/data path the app writes MUST be under `/opt/<name>/data/` (or whatever's in `ReadWritePaths=`). Never `Path.home() / ".something"` — that crashes under `ProtectHome=true`.

### `.env.example`

Document **every** env var the code reads.

> **Reference:** the `.env.example` template with all required vars is in `references/mcp-scaffold-ref.md` — read it when you reach this step.

### `scripts/smoke_test_mcp.py`

Copy + adapt from a reference MCP server:
```bash
cp <your-reference-mcp-project>/scripts/smoke_test_mcp.py scripts/
```
Change `DEFAULT_BASE_URL` to your project's deployed URL.

### `deploy/install.sh` — idempotency rule

> **Reference:** the idempotency snippet and explanation are in `references/mcp-scaffold-ref.md` — read it when you reach this step.

### `deploy/README.md` — the actual gotchas to document

> **Reference:** the five required gotchas for the deploy README are in `references/mcp-scaffold-ref.md` — read it when you reach this step.

---

## Execution flow when this skill is invoked

1. **Gather inputs** — walk user through the 6 decisions above. Don't write files until all are answered. Save them as variables.

2. **Confirm scope** — list what will be generated and roughly the line count. Get explicit go-ahead.

3. **Generate files** — write each file. Substitute the project name and other variables. Skip deploy/* if stdio-only.

4. **Run sanity checks** —
   - `python -m py_compile <name>_mcp/*.py` (syntax)
   - `pip install -e .` works (deps resolve)
   - `python -m <name>_mcp --help` runs (entry point wired)
   - Smoke test script syntax-checks
   - Stub tests exist

5. **Don't auto-commit** — show the user the file tree, ask if they want a commit + initial push. Respect the workspace `[allow-direct]` token convention for the initial-bootstrap commit.

6. **Next steps for the user** — explicit list:
   - Set up GitHub OAuth App (if OAuth) — provide the URL + the fields
   - Create the `.env` from `.env.example` with real values
   - Run `/mcp-audit` once after first deploy to verify everything
   - Configure the Claude.ai connector with the right URL

---

## Reference architecture

Working example with every pattern correctly implemented:
- `<your-reference-mcp-project>/`
- Key files: `kitchen_mcp/server.py:70-95` (transport security), `kitchen_mcp/oauth.py` (OAuth 2.1 server), `deploy/README.md` (gotcha-documented walkthrough), `scripts/smoke_test_mcp.py` (post-deploy gate)

When in doubt about a generated piece of code, diff against the a reference MCP server equivalent.

---

## What this skill does NOT do

- **Doesn't write your actual MCP tools** — that's the unique-to-your-project code. The skill scaffolds the *server*, not the *tools*.
- **Doesn't set up the GitHub OAuth App, CF Tunnel, or DNS** — those are dashboard actions. The skill outputs a README that walks the user through them.
- **Doesn't deploy** — only generates the artifacts. User runs the deploy manually.
