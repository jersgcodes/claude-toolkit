# mcp-scaffold reference material

---

## server.py — TransportSecuritySettings snippet

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# Derive Host/Origin allowlist from OAUTH_BASE_URL so HTTP transport behind
# Cloudflare Tunnel passes FastMCP's DNS-rebinding protection.
import os
from urllib.parse import urlparse

_oauth_base = os.environ.get("OAUTH_BASE_URL", "").strip().rstrip("/")
_transport_security: TransportSecuritySettings | None = None
if _oauth_base:
    _public_host = urlparse(_oauth_base).netloc
    _transport_security = TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            _public_host, f"{_public_host}:*",
            "127.0.0.1:*", "localhost:*", "[::1]:*",
        ],
        allowed_origins=[
            _oauth_base, "https://claude.ai",
            "http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*",
        ],
    )

mcp = FastMCP("<name>", transport_security=_transport_security, instructions="...")
```

**Why each piece matters:** see `/mcp-audit` checklist items 1-3.

---

## systemd unit file template

```ini
[Unit]
Description=<name> MCP server (HTTP)
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=<service-user>
Group=<service-user>
WorkingDirectory=/opt/<name>
EnvironmentFile=/opt/<name>/.env
ExecStart=/opt/<name>/.venv/bin/python -m <name>_mcp --transport http --host 127.0.0.1 --port 8082
Restart=on-failure
RestartSec=5

# Hardening — note ProtectHome=true means /home is invisible to the process
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/opt/<name>/data

[Install]
WantedBy=multi-user.target
```

**Important:** any log/data path the app writes MUST be under `/opt/<name>/data/` (or whatever's in `ReadWritePaths=`). Never `Path.home() / ".something"` — that crashes under `ProtectHome=true`.

---

## .env.example template

Document **every** env var the code reads. At minimum:

```
# Required for the app's primary work (replace with your actual deps)
# ANTHROPIC_API_KEY=sk-ant-...

# Required on the VPS — systemd ProtectHome=true blocks /home access
<NAME>_LOG_DIR=/opt/<name>/data/logs

# Required for HTTP transport (OAuth or bearer)
OAUTH_BASE_URL=https://<name>.<your-domain>
OAUTH_GITHUB_CLIENT_ID=
OAUTH_GITHUB_CLIENT_SECRET=
OAUTH_ALLOWED_GITHUB_USERS=your-gh-username

# Local dev escape hatch — skip OAuth (NEVER set in prod)
# KITCHEN_MCP_DEV=1
```

---

## deploy/README.md — gotchas list

At minimum, the README must call out:

1. `cloudflared service install` reads `/etc/cloudflared/config.yml`, NOT `/root/.cloudflared/config.yml`
2. Port must match in 3 places: systemd `--port`, cloudflared `service:`, app default
3. CNAME for the tunnel, not an A record (delete leftover A records first)
4. systemd `ProtectHome=true` means logs go to `/opt/<name>/data/`, not home
5. Restart cloudflared with full `stop` + `start`, not `restart` (sometimes doesn't reload ingress)

---

## deploy/install.sh — idempotency snippet

```bash
# Clone if missing
if [ ! -d "${INSTALL_DIR}" ]; then
    sudo git clone "${REPO_URL}" "${INSTALL_DIR}"
fi
# ALWAYS chown — fixes the case where someone pre-cloned as root
sudo chown -R "${SERVICE_USER}:${SERVICE_USER}" "${INSTALL_DIR}"
```

Common bug: putting `chown` inside `[ ! -d ]` so pre-clone case leaves files root-owned, then `git pull --ff-only` as the service user fails with "dubious ownership". **Chown unconditionally.**
