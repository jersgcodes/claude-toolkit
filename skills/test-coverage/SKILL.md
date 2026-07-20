---
name: test-coverage
description: [CLI-only] Identify untested code paths and suggest test cases. Use when checking coverage gaps, before a PR, or when tests feel thin.
allowed-tools: [Bash, Read, Grep, Glob]
version: 0.1.0
---



Identify untested code paths and suggest test cases. Do the following steps in order:

**0. Show current test state (from TESTING.md)**

Check if `TESTING.md` exists in the current working directory. If it does:

Read it and count how many items are:
- `[x]` = done
- `[!]` = broken / failing
- `[?]` = fix attempted, needs retest
- `[~]` = skipped
- `[ ]` = not yet tested

List any `[!]` items under **Broken** and any `[?]` items under **Needs retest** so they're visible immediately.

Print a quick summary:
```
Manual testing progress: X/Y done  (exclude skipped from denominator)
Broken: N  |  Needs retest: N  |  Skipped: N  |  Remaining: N
```

If TESTING.md does not exist, skip this step and note "No TESTING.md found."

---

**1. Detect project type**

Check for these files to determine the stack:
- `package.json` → Node.js project; check `scripts.test` for runner (vitest, jest, mocha, etc.)
- `pyproject.toml` or `setup.py` or `requirements.txt` → Python project
- `go.mod` → Go project
- `Cargo.toml` → Rust project
- `pom.xml` or `build.gradle` → Java/Kotlin project
- `*.csproj` → .NET project

Within Node.js, further detect:
- `next.config.*` → Next.js (pages or app router)
- `vite.config.*` → Vite (React/Vue/Svelte)
- Express routes in `server/` or `src/server/` → Node/Express API
- `trpc` in dependencies → tRPC router
- `socket.io` in dependencies → Socket.IO server
- `fastify` in dependencies → Fastify API

Report: "Detected stack: [X]" before proceeding.

---

**2. Run existing tests**

Run the test command for the detected stack:

| Stack | Command |
|---|---|
| Node (npm) | `npm test` |
| Node (pnpm) | `pnpm test` |
| Node (yarn) | `yarn test` |
| Python | `python -m pytest -q` |
| Go | `go test ./...` |
| Rust | `cargo test` |
| Java (Maven) | `mvn test -q` |
| Java (Gradle) | `./gradlew test` |

Report pass/fail count. If zero tests exist, flag it as a critical gap.

---

**3. Check for duplicate tests**

Scan test files for describe block names or test/it() names that appear in more than one file. Report duplicates and which file has the more thorough version.

---

**4. Map untested paths**

For each non-test, non-config, non-generated source file:
- List exported functions, classes, or route handlers
- Check if they appear in any test file
- Flag anything with no test coverage

**Priority order by risk (adapt to detected stack):**

| Priority | What to check | Why |
|---|---|---|
| 1 | Auth / permission guards | Silent failures = security holes |
| 2 | Data mutation functions (DB writes, file writes, API calls) | Hard to reverse if wrong |
| 3 | Input validation / parsing | Edge cases cause silent corruption |
| 4 | Event/message handlers (Socket.IO, queues, webhooks) | Async, hard to trace |
| 5 | API route handlers | Entry points for all external input |
| 6 | Data transformation functions | Logic bugs, easy to unit test |
| 7 | Error handling branches | Often untested, reveals unexpected states |
| 8 | UI components with logic (React/Vue) | State transitions, conditional renders |

---

**5. Identify test layer gaps**

Show which layers are present, thin, or missing. Adapt table to detected stack:

**For Node.js / TypeScript APIs:**

| Layer | What it covers | Tool | Status |
|---|---|---|---|
| Unit | Pure functions, utilities, data transforms | vitest / jest | ? |
| Route / controller | Input validation, auth guards, response shape | vitest + supertest or similar | ? |
| Integration | DB interactions, external API calls | vitest + real DB or mocks | ? |
| Socket / event | Real-time event routing, room isolation | vitest + socket.io-client | ? |
| E2E | Full user flows | Playwright / Cypress | ? |

**For React / Vite frontend:**

| Layer | What it covers | Tool | Status |
|---|---|---|---|
| Unit | Pure functions, hooks, utils | vitest | ? |
| Component | Render, props, user interactions | @testing-library/react | ? |
| Integration | Multi-component flows, state transitions | @testing-library/react | ? |
| E2E | Full browser flows | Playwright / Cypress | ? |

**For Python:**

| Layer | What it covers | Tool | Status |
|---|---|---|---|
| Unit | Functions, classes, utilities | pytest | ? |
| API | Route handlers, auth, request/response | pytest + httpx / TestClient | ? |
| Integration | DB queries, external service calls | pytest + real DB or mocks | ? |
| E2E | Full request flows | pytest + httpx or Playwright | ? |

**For Go:**

| Layer | What it covers | Tool | Status |
|---|---|---|---|
| Unit | Functions, structs, interfaces | go test | ? |
| HTTP handler | Route handlers, middleware | go test + httptest | ? |
| Integration | DB, external calls | go test + testcontainers | ? |

Fill in Status as: Present / Thin (< 3 tests) / Missing

---

**6. Suggest test cases**

For the top 3-5 most important untested paths, write suggested test cases in plain English:

```
Function / route: <name>
File: <path>
Test cases:
- Happy path: <what normal input should produce>
- Edge case: <boundary condition or unusual input>
- Error case: <what bad input or failure should produce>
- Auth/permission: <what happens if unauthenticated or unauthorised>
```

Tailor examples to the actual functions found — do not use generic placeholder names.

---

**7. Suggest what to test next (from TESTING.md)**

If TESTING.md exists, prioritise `[?]` items (verify fixes) before `[ ]` items. List 2-3 specific items to test next using the Priority Order from TESTING.md for untested items.

---

**8. Summary**

- Total functions / handlers / routes identified
- Estimated coverage % (rough: tested / total)
- Which test layer is most thin
- Top 3 priority functions to test next
- One-line verdict: `PASS — coverage acceptable` / `WARN — gaps present` / `FAIL — critical paths untested`
