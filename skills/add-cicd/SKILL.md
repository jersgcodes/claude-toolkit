---
name: add-cicd
description: [CLI-only] Scaffold GitHub Actions CI/CD workflows for this project.
version: 0.1.0
---


Scaffold GitHub Actions CI/CD workflows for this project. Do the following steps in order:

---

**1. Detect stack**

Read `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `requirements.txt` to identify:
- Language and runtime version
- Test command (`scripts.test` in package.json, etc.)
- Build command (`scripts.build` in package.json, etc.)
- Package manager: check for `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb` → bun, else npm

Also detect frontend framework:
- `vite.config.*` → Vite (static output: `dist/`)
- `next.config.*` → Next.js
- Neither → assume API / backend service

Report: "Stack: [X] | Package manager: [X] | Output: [X]"

---

**2. Detect deployment target**

Check for these config files in the project root:
- `vercel.json` → Vercel
- `netlify.toml` → Netlify
- `fly.toml` → Fly.io
- `railway.toml` or `railway.json` → Railway
- `render.yaml` → Render
- `.github/workflows/deploy*` already exists → note it

If none found, ask the user:
> "No deployment config detected. Where does this project deploy?
> A) Vercel  B) Netlify  C) Fly.io  D) Railway/Render (auto-deploy)  E) GitHub Pages  F) Skip CD for now"

Wait for the answer before continuing.

---

**3. Create .github/workflows/ directory**

```bash
mkdir -p .github/workflows
```

---

**4. Write ci.yml**

Always create this. Adapt to detected stack:

**Node.js (npm):**
```yaml
name: CI
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test
      - run: npm run build
```

**Node.js (pnpm):**
```yaml
name: CI
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm test
      - run: pnpm build
```

**Python:**
```yaml
name: CI
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - run: pip install -r requirements.txt
      - run: python -m pytest -q
```

**Go:**
```yaml
name: CI
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: stable
      - run: go test ./...
      - run: go build ./...
```

If the project has no test script, omit the test step and add a comment:
`# TODO: add npm test once tests are written`

---

**5. Write cd.yml (based on deployment target)**

**A — Vercel:**
```yaml
# Vercel auto-deploys via GitHub integration — no workflow needed.
# Connect at: https://vercel.com/new → import this repo.
# Production deploys on push to main. Preview deploys on PRs automatically.
```
Create `.github/workflows/cd-notes.md` with this note instead of a workflow file.

**B — Netlify:**
Same as Vercel — GitHub integration handles it. Create notes file.

**C — Fly.io:**
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```
Note: user must add `FLY_API_TOKEN` to GitHub repo secrets.

**D — Railway / Render:**
```yaml
# Railway/Render auto-deploys via GitHub integration — no workflow needed.
# Railway: https://railway.app → new project → deploy from GitHub repo.
# Render: https://render.com → new service → connect GitHub repo.
# Both deploy on push to main automatically.
```
Create notes file.

**E — GitHub Pages (static sites):**
```yaml
name: Deploy
on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```
Note: enable GitHub Pages in repo Settings → Pages → Source: GitHub Actions.

**F — Skip CD:**
Skip this step, note it in summary.

---

**6. Write architecture.yml**

Always create this if `docs/` exists or if the project has a `scripts/gen-architecture.ts`:

```yaml
name: Architecture
on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run docs:architecture
        continue-on-error: true
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: regenerate architecture diagram"
          file_pattern: "docs/**"
```

If no `docs:architecture` script exists, skip this workflow and note it.

---

**7. Summary**

Print:
```
CI/CD scaffolded

Files written:
  .github/workflows/ci.yml        — runs tests + build on push/PR to main and dev
  .github/workflows/cd.yml        — <description or "notes file only">
  .github/workflows/architecture.yml — <written or skipped>

Required setup:
  - [ ] <any GitHub secrets to add>
  - [ ] <any GitHub settings to enable (Pages, etc.)>
  - [ ] <GitHub integration to connect (Vercel/Netlify/Railway)>

Next: git add .github/ && git push — CI will run on first push.
```
