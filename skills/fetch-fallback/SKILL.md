---
name: fetch-fallback
description: Recover a web page when WebFetch or WebSearch fails, AND avoid misreading one that succeeded. Diagnoses the failure mode first (403 bot-wall, JS-rendered, 404, blocked domain, paywall) then routes to the right recovery; also covers reading state (ticks, crosses, greyed rows) out of comparison tables and pricing cards, where text-only extraction silently reports every option as including everything. Use whenever a fetch errors, returns thin content, or when scraping any table of what is included or supported.
allowed-tools: [Bash, WebFetch, WebSearch, Read, Write]
version: 0.2.0
---

A failed fetch is not one problem. It is at least six, and they need different fixes. Diagnose
before reaching for a tool, or you will run a scraper at a page that was never there.

## Step 1: classify the failure

Get the real status code first. Never infer it from a tool's error text.

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" -A "$UA" -L --max-time 25 "<URL>"
```

Compare against what the fetch tool reported. The gap tells you which branch to take.

| Symptom | Likely cause | Go to |
|---|---|---|
| Tool errors, curl with UA returns 200 | UA / bot wall | Step 2 |
| 200 but content is empty, a shell, or a cookie banner | JS-rendered | Step 3 |
| 404 from both tool and UA curl | Wrong URL, moved, or removed | Step 4 |
| Tool refuses the domain outright | Domain blocked for the fetch tool | Step 5 |
| 401, 402, or a login or paywall interstitial | Authenticated or paid | Step 6 |
| 429 | Rate limited | Back off, retry once with delay, then stop |
| Content-Type is application/pdf | PDF | Step 7 |

## Step 2: bot wall or UA gate (403, or tool-only failure)

Fetch with a browser UA via `curl` and parse the HTML yourself. Many government and vendor sites
serve full SSR HTML to a browser UA and 403 to everything else.

```bash
curl -s -A "$UA" -L --max-time 30 "<URL>" | python3 -c "
import sys,re,html
t=sys.stdin.read()
t=re.sub(r'(?is)<(script|style|noscript).*?</\1>',' ',t)
t=re.sub(r'(?s)<[^>]+>',' ',t)
print(re.sub(r'\n\s*\n+','\n',re.sub(r'[ \t]+',' ',html.unescape(t))))
"
```

If the project has a hardened version of this, use it rather than rewriting. Example in
`sme-solution-radar`: `scripts/psg_directory_fetch.py` (GoBusiness 403 bypass).

## Step 3: JS-rendered page

Content only exists after script execution. `curl` cannot help. Use a headless browser.
Example in `sme-solution-radar`: `scripts/vendor_pricing_browser.py` (Playwright).

Tell-tale signs: a near-empty `<body>`, a root div with an app id, or a summary that describes
navigation chrome and nothing else.

## Step 4: 404 (this is where most time gets wasted)

A 404 means the URL is wrong or the page moved or it was removed. Work that order, because the first
two are cheap and the third loses information.

**4a. Is the URL wrong?** Most likely cause when the URL was guessed, reconstructed from a filename,
or copied from a search-result snippet rather than clicked. Check for a stale path segment, a
missing query string, or an invented slug.

**4b. Find the current URL.** Cheapest first:

1. **Site-filtered search.** `WebSearch` with `allowed_domains: ["example.gov.sg"]` and distinctive
   page text rather than the slug. Search snippets often carry the live URL.
2. **Sitemap.** `curl -s <origin>/sitemap.xml` and grep the slug. Check `robots.txt` first, it often
   names several sitemaps including a separate one for documents.
3. **Hub page link scrape.** Fetch the parent or index page you know exists and read its links. This
   beats guessing when a file has been reorganised into a new directory.
   ```bash
   curl -s -A "$UA" -L "<hub URL>" | grep -oE 'href="[^"]+\.(pdf|xlsx?|docx?)"' | sort -u
   ```
4. **Wayback CDX API, the highest-yield move for documents.** It lists every archived URL under a
   path with wildcards and filters, so it finds renamed and re-dated files that no search engine
   still indexes. This is what recovers rotated government PDFs.
   ```bash
   curl -s "http://web.archive.org/cdx/search/cdx?url=example.gov.sg*\
   &filter=original:.*keyword.*&fl=timestamp,original,statuscode&collapse=digest&limit=40"
   ```
   Read the `statuscode` column. A row with 404 means the archive captured the error page, not the
   document, so take the most recent row with 200.

**Filename patterns matter.** Government document URLs commonly carry a cache-busting query
(`?sfvrsn=...`) and a date in the slug (`-(updated-18-may-2024)`). When a document is refreshed, the
date in the slug changes and every published link to the old one dies. Search on the stable part of
the name, never the dated part.

**Documents may have moved host entirely.** If *every* document URL under a site 404s while the HTML
pages still work, suspect a platform migration rather than individual deletions. Singapore
government sites on the Isomer platform serve HTML from `agency.gov.sg` but documents from
`isomer-user-content.by.gov.sg/<id>/<uuid>/<filename>`, so no amount of guessing at the old
`/docs/default-source/...` path will ever work. The hub-page link scrape (step 3 above) is what
finds this, because the live page carries the real href. When you see this pattern, scrape the hub
page first and skip the archive entirely, since the archive holds the dead host too.

**4c. If it truly is gone, go to the archive.** Query the availability API, then retrieve the
snapshot itself with `curl`, because WebFetch is blocked from `web.archive.org`.

```bash
curl -s "http://archive.org/wayback/available?url=<URL without scheme>"
# then, with the returned snapshot URL:
curl -s -A "$UA" -L --max-time 45 "<snapshot URL>" | python3 -c "<same strip script as Step 2>"
```

**Always record that a fact came from an archived copy, with the snapshot date.** Archived pages go
stale silently. Check the archived copy for internal date cues (referenced schemes, years, prices)
and state how old the content looks, not just when the snapshot was taken.

## Step 5: domain blocked for the fetch tool

Some domains are refused by WebFetch regardless of status. `web.archive.org` is one. Use `curl`.
If the domain is blocked at the network level too, say so and stop.

## Step 6: authenticated or paywalled

Stop. Do not attempt to circumvent. Options, in order: an authenticated MCP tool or CLI for that
service if one exists (`gh` for GitHub, for example), a public mirror of the same fact, or tell the
user what is behind the wall and let them decide.

## Step 7: PDF

Try WebFetch first, it handles many PDFs. If it fails, `curl -o` then extract locally. If the PDF
URL itself 404s, treat it as Step 4: PDF paths on government sites rotate often and the same
document usually exists under a new filename.

## Step 8: record what happened

Whatever you recover, write down in the research note:

- the URL, the access date, and whether it came from live or archive
- for archived content, the snapshot date **and** how old the content appears
- the failure mode you hit, so the next session does not repeat the diagnosis
- confidence, and specifically whether a claim is verified verbatim, inferred, or an absence finding

An absence finding ("no notice of X was found") is weaker than a positive one and must be labelled
as such.

## Step 9: the fetch SUCCEEDED and the answer is still wrong

The failure modes above are all about access. The more expensive ones come after it, because a
misread page returns a confident wrong answer where a blocked page returns nothing. Nothing warns
you. Run this check whenever the page describes **state** — what is included, allowed, active,
supported, in stock, required.

**The words are not the state.** A pricing card, a comparison grid, a compatibility matrix and a
feature table all list every item on every option and mark each one with a tick, a cross, a colour
or a greyed-out row. `innerText` returns the item and discards the mark, so every option reads as
having everything.

> Measured case: a vendor printed "Download videos with no watermark" on all four of its plan cards.
> The icon was `check-circle-x` on the first two and `check-circle` on the third. Text extraction
> reported the FREE tier as including what is not granted until the second PAID tier.

So:

1. **Capture the mark, not the line.** Read the icon's `href`, `class`, `aria-label`; test negatives
   first, because `check-circle-x` contains `check`.
2. **An explicit glyph outranks styling.** Use opacity or strikethrough only when the glyph is
   silent. The same `opacity-60` meant "excluded" on one card and "dark theme" on another, and
   letting it override the icon reported the top option as excluding everything.
3. **Ask what a tick would mean here.** Polarity is not universal: ticked "Watermark removal" clears
   the problem, ticked "Watermark" is the problem. Where the word is neutral, only the value decides
   ("all resolutions" passes, "480p only" does not).
4. **Before writing "the page does not state X", prove your detector fires** on a line you can see
   with your own eyes. `\bresolution\b` never matches "all resolutions"; that one character was
   reported as missing vendor data.
5. **Suspect the reader before the source.** Across the cases behind this skill, the large majority
   of "the site does not publish it" turned out to be our extraction. It is the most tempting label
   and the rarest true cause.
6. **Let unknown be an answer.** Silence must never become a pass. Record `unknown` and say what
   would settle it.

Cheapest way to check any of this: open the HTML around the fact, not the text dump. Both findings
above took one look at the element wrapping the line.

## What this skill is not

It is not a way past access controls. If a site requires payment or login, or its terms forbid
automated retrieval, the answer is to stop and say so.
