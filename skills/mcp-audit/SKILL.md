---
name: mcp-audit
description: Audit an MCP server project for correctness, security, and deploy-readiness. Catches the 8 common gotchas that bite when shipping MCP behind a tunnel/proxy (FastMCP DNS-rebinding, hardcoded log paths, port conflicts, etc.). Use before deploying any MCP server, or when an MCP "sho
version: 0.1.0
---


# MCP Server Audit

Validates an existing MCP server project against the patterns that actually work in production (lessons from a reference MCP server deploy).

Different from `/security-check` (generic OWASP scan) — this is **MCP-specific**, focused on what makes an MCP server work behind tunnels and with Claude.ai's custom-connector model.

---

## When to use

| Situation | Use? |
|---|---|
| Before first deploy of an MCP server to production | YES |
| MCP "should work" but Claude.ai shows "Couldn't reach the MCP server" | YES |
| After major refactor of auth or transport layer | YES |
| Adding a new MCP server to an existing infra | YES |
| Pure stdio MCP (Claude Desktop only) — no HTTP | Skip the auth/tunnel sections |
| Tool authoring quality (descriptions, schemas) | Use the protocol section here, OR `/style-check` for UX angle |

---

## Audit checklist

For each item: locate the relevant code, decide PASS / WARN / FAIL, explain the *why*. Output as a structured report at the end.

### A. Transport + binding

1. **Bound to 127.0.0.1 (not 0.0.0.0)** — server must bind loopback only; cloudflared or your reverse proxy is the only inbound path
   - Find: `--host`, `host=`, `uvicorn.run`, etc.
   - PASS if explicit `127.0.0.1`; WARN if `0.0.0.0` (open to LAN); FAIL if bound publicly with no proxy

2. **Endpoint path is `/mcp` (streamable HTTP), not `/sse`** — `/sse` is the deprecated transport. Modern FastMCP uses `mcp.streamable_http_app()` which serves `/mcp`.
   - Find: `streamable_http_app`, `sse_app`, custom routes
   - FAIL if docs/configs reference `/sse` as the connector URL (Claude.ai will 404)

3. **FastMCP DNS-rebinding protection is configured for the deploy host** — when `FastMCP()` is bound to `127.0.0.1`, it auto-enables `TransportSecuritySettings` allowing ONLY `127.0.0.1`/`localhost` as Host headers. Tunneled requests arrive with `Host: <public-hostname>` → 421 Misdirected Request.
   - Find: `FastMCP(...)` call, `transport_security=`, `TransportSecuritySettings`
   - PASS if `allowed_hosts` includes the public hostname; FAIL if not set and the server is bound to 127.0.0.1 (which is the right binding anyway — fix by adding `TransportSecuritySettings`, not by changing the bind)
   - Symptom in journal: `WARNING mcp.server.transport_security: Invalid Host header: ...`

4. **Port doesn't collide with common services** — 8080 commonly taken by Docker/Coolify/Traefik. Default to **8082** or a service-specific port.
   - Find: `--port`, `port=`, systemd unit `ExecStart`, cloudflared `service:` URL
   - WARN if port is 8080 or 3000 (common collisions); recommend changing
   - Bonus check: do all three (app code default, systemd unit, cloudflared config) agree on the port? A mismatch is the #1 cause of 502 from CF.

### B. Auth

5. **Auth is appropriate for the consumer model**:
   - **Bearer token** — fine for personal/internal MCP servers, one consumer
   - **OAuth 2.1 with PKCE** — required for Claude.ai Custom Connectors (their backend does server-to-server discovery, no browser cookies). Per MCP 2025 spec.
   - **CF Access / human-in-browser session auth** — WORKS FOR HUMANS, NOT FOR MCP CLIENTS. Claude.ai's MCP backend can't navigate cookie-based 302 redirects. If you see CF Access in front of an MCP server intended for Claude.ai, FLAG IT.
   - **None** — only acceptable if endpoint has no money-burning tools and the URL doesn't matter being leaked

6. **For OAuth servers**: check spec compliance with MCP 2025 auth requirements
   - Has `/.well-known/oauth-authorization-server` (RFC 8414)
   - Has `/.well-known/oauth-protected-resource` (RFC 9728)
   - Has `/.well-known/jwks.json` (for verification by external services)
   - Implements `/register` for Dynamic Client Registration (RFC 7591) — Claude.ai uses this
   - PKCE S256 required (don't accept `plain` method)
   - Token endpoint accepts `authorization_code` grant
   - Bearer middleware returns 401 with `WWW-Authenticate: Bearer realm="..."` header on missing/bad token
   - JWT contains: `iss`, `sub`, `aud`, `iat`, `exp` (all required)
   - RSA keys persisted on disk so tokens survive restart (NOT generated fresh on each startup)

7. **Auth bypass for local dev exists + is loud about it** — `KITCHEN_MCP_DEV=1` or similar env var that skips auth. WARN in startup logs when dev mode is active. NEVER default-on in production.

### C. Configuration + environment

8. **No hardcoded paths under `Path.home()` for runtime files**
   - systemd units commonly set `ProtectHome=true` which makes `/home` unreachable
   - If app crashes with `PermissionError: [Errno 13] Permission denied: '/home/...'` in journalctl → this gotcha
   - PASS if log/data paths read from env var; FAIL if hardcoded `Path.home()` in any imported module

9. **systemd unit follows the hardening pattern**
   - Find: `deploy/systemd/*.service`
   - Required: `User=` non-root, `ProtectHome=true`, `ProtectSystem=full`, `NoNewPrivileges=true`, `PrivateTmp=true`
   - `ReadWritePaths=` includes the dirs the app actually writes (data, logs)
   - `EnvironmentFile=` points to the `.env` file
   - `Restart=on-failure` with `RestartSec=` ≥ 5 (avoid restart-loop CPU burn)

10. **`.env.example` lists EVERY env var the app reads** — grep the codebase for `os.environ.get(` / `os.getenv(` and cross-check against `.env.example`. Missing docs = silent prod failures.

### D. Tunnel + DNS (if behind Cloudflare Tunnel)

11. **cloudflared config is in `/etc/cloudflared/config.yml`, NOT `/root/.cloudflared/config.yml`** — `cloudflared service install` reads from `/etc`. Edits to `/root/.cloudflared/` look like they work but the systemd service ignores them.
    - Document this in the deploy README; check that install.sh references the right path

12. **DNS uses CNAME to `<UUID>.cfargotunnel.com`, not an A record** — `cloudflared tunnel route dns ...` creates the right record, but a leftover A record from a prior nginx setup will conflict
    - Document the conflict + how to resolve in the deploy README

13. **Port consistency** — cloudflared's `service:` URL must match the app's listening port AND the systemd unit's `--port`. A mismatch silently 502s.

### E. Tests + smoke

14. **Has a smoke test script for the live deployed server** — script that hits `/.well-known/*`, `/healthz`, /register, validates `/mcp` returns 401 + WWW-Authenticate. Use as post-deploy gate.
    - Look for: `scripts/smoke_test*.py`, `scripts/smoke.sh`, etc.
    - FAIL if no smoke test — easy to add, high value

15. **Has unit tests for auth components** (if non-trivial auth)
    - JWT roundtrip, PKCE verification, bearer middleware behavior
    - FAIL if OAuth/bearer code exists with zero tests

16. **MCP protocol introspection** — at minimum, a test that lists tools and verifies each has a name, description, and inputSchema
    - LLMs choose tools by description; missing/empty descriptions = degraded tool use

17. **install.sh idempotency** — running install.sh twice should not break things
    - Common bug: `chown` only inside the `[ ! -d ]` block → manual-pre-clone case leaves files owned by root
    - chown should happen unconditionally

### F. Tool quality (LLM-facing)

18. **Every `@mcp.tool()` has a non-trivial docstring** — that docstring IS the tool description shown to the LLM. "Lists dishes" is too thin; "Lists curated dishes in the user's kitchen corpus. Call this first when the user asks about cooking, recipes, or what to cook." is right.

19. **Input schemas are typed** — use Python type annotations + pydantic models for inputs. FastMCP auto-generates schemas from these.

20. **Errors are surfaced to the LLM** — custom exception classes that produce clean messages, not stack traces. Look for `_= (Error1, Error2, ...)` style surfacing or explicit try/except in tool bodies.

---

## Output format

After running all checks, output a structured report:

```markdown
# MCP Audit — <project>

## Summary
- PASS: <count>
- WARN: <count>
- FAIL: <count>

## Critical (fix before deploy)
1. <issue> — <location> — <fix>

## Warnings
1. <issue> — <location> — <suggestion>

## Passes (for the record)
- <item>: <how verified>

## Reference architecture
For a working example with all of these in place, see `<your-reference-mcp-project>/` (especially `kitchen_mcp/oauth.py`, `kitchen_mcp/server.py:70-95` for TransportSecuritySettings, and `deploy/README.md` for the deploy walkthrough).
```

---

## Common gotchas (deeper context)

These are documented at `<your Claude memory dir>` with full diagnosis + fix patterns. Read that file as input when running the audit — it has the actual symptom→cause→fix mappings from the a reference MCP server deploy.

---

## What this skill does NOT cover

- Generic security (use `/security-check`)
- Code quality / dead code (use `/code-quality`)
- Performance / profiling (use `/perf`)
- Dependency vulnerabilities (use `/deps-audit`)
- Secrets in code or git history (use `/secrets-scan`)

Layer this skill ON TOP of those for an MCP-specific audit.
