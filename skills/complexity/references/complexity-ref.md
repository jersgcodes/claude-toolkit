# complexity-ref — Node.js MI/Halstead via escomplex + sucrase

Referenced from `/complexity` step 5b. Run this only when you specifically need Maintainability Index / Halstead numbers for a TypeScript/JavaScript project (not just cyclomatic or cognitive complexity).

Because `typhonjs-escomplex` parses JS (not TS types), transpile first with sucrase (fast, type-stripping), then analyse the emitted JS:

```bash
npx --yes typhonjs-escomplex --version >/dev/null 2>&1 || pnpm add -D typhonjs-escomplex sucrase
node --input-type=module <<'EOF'
import escomplex from 'typhonjs-escomplex';
import { transform } from 'sucrase';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

function walk(dir, out = []) {
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (e === 'node_modules' || e.startsWith('.')) continue;
    if (statSync(p).isDirectory()) walk(p, out);
    else if (['.ts', '.tsx', '.js', '.jsx'].includes(extname(p))) out.push(p);
  }
  return out;
}

const rows = [];
for (const f of walk('src')) {
  try {
    const js = transform(readFileSync(f, 'utf8'), {
      transforms: ['typescript', 'jsx'],
    }).code;
    const r = escomplex.analyzeModule(js);
    rows.push({ f, mi: r.maintainability.toFixed(1) });
  } catch { /* skip files sucrase/escomplex can't parse */ }
}
rows.sort((a, b) => a.mi - b.mi);
console.log('Maintainability Index (lower = worse; <65 review, <50 refactor):');
for (const { f, mi } of rows.slice(0, 20)) console.log(`  ${mi}\t${f}`);
EOF
```

MI scale (escomplex, 0–171; comparable to radon's 0–100 after normalisation):
flag files **< 65** for review, **< 50** for refactor.

> **Exclude data files.** MI penalises file *length* heavily, so large content/
> data/fixture files (big arrays/objects, no logic) score "unmaintainable" and
> drown out real offenders. Skip them in `walk()` (add the dir name to the
> exclude check, e.g. `e === 'content'`) and ignore `*.test.*`. For data-heavy
> repos, function-level cyclomatic (3b) + cognitive (4b) are the trustworthy
> signals; per-file MI is mostly noise.
