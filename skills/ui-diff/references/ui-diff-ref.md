# ui-diff reference recipe

Concrete, tested snippets for the loop. Adapt paths per project. Keep scratch files in a gitignored dir.

## 1. Figma: extract per-element tokens

Needs a Figma REST token (store as `FIGMA_TOKEN` in a gitignored `.env`, never echo it). File key + node id come from the Figma URL: `figma.com/design/<KEY>/...?node-id=13542-302151` (the node id uses `:` in the API, so `13542:302151`).

```python
import os, json, urllib.request, time
tok=[l.split("=",1)[1].strip().strip('"').strip("'") for l in open(".env") if l.startswith("FIGMA_TOKEN=")][0]
KEY="<file-key>"
def api(p):
    for a in range(4):
        try:
            r=urllib.request.Request("https://api.figma.com/v1/"+p, headers={"X-Figma-Token":tok})
            return json.load(urllib.request.urlopen(r))
        except urllib.error.HTTPError as e:
            if e.code==429 and a<3: time.sleep(15); continue   # rate-limit backoff
            raise
hx=lambda c:"#%02X%02X%02X"%(round(c['r']*255),round(c['g']*255),round(c['b']*255))+("" if c.get('a',1)>=0.999 else "/a%.2f"%c['a'])

# per-element walk of ONE component (find it by name), dumping the values that matter
data=api(f"files/{KEY}/nodes?ids=13542:302151&depth=10")
doc=data["nodes"]["13542:302151"]["document"]
def sty(n):
    out=[]
    if n.get("layoutMode"): out.append("gap%s pad(%s,%s,%s,%s)"%(n.get("itemSpacing"),n.get("paddingTop"),n.get("paddingRight"),n.get("paddingBottom"),n.get("paddingLeft")))
    if "cornerRadius" in n: out.append("r%s"%n["cornerRadius"])
    for f in n.get("fills",[]) or []:
        if f.get("type")=="SOLID" and f.get("visible",True): out.append("fill "+hx(f["color"]))
    for s in n.get("strokes",[]) or []:
        if s.get("type")=="SOLID": out.append("stroke %s w%s"%(hx(s["color"]),n.get("strokeWeight")))
    for e in n.get("effects",[]) or []:
        if e.get("type")=="DROP_SHADOW" and e.get("visible",True):
            o=e.get("offset",{}); out.append("shadow x%s y%s blur%s %s"%(round(o.get('x',0)),round(o.get('y',0)),round(e.get('radius',0)),hx(e["color"])))
    if n.get("type")=="TEXT":
        st=n.get("style",{}); out.append("TXT %s %s/%s w%s ls%s '%s'"%(st.get("fontFamily"),st.get("fontSize"),round(st.get("lineHeightPx",0)),st.get("fontWeight"),round(st.get("letterSpacing",0),2),n.get("characters","")[:30]))
    return "  ".join(map(str,out))
def walk(n,d=0):
    print("  "*d+f"[{n.get('type')}] {n.get('name','?')[:22]:22} {sty(n)}")
    for c in n.get("children",[]) or []: walk(c,d+1)
walk(doc)
```

- **Gradients**: a fill with `type=="GRADIENT_LINEAR"` has `gradientStops` (`color`,`position`) and `gradientHandlePositions` (direction). Convert the handle vector to a CSS `deg`.
- **Aggregate scan** (all colours/type/radii across a frame, to build the token file) = same walk but with `collections.Counter` on the values; use it for the token palette, never for a specific component's radius.

## 2. Figma: fetch the reference render

```python
img=api(f"images/{KEY}?ids=13542:302151&format=png&scale=2")
urllib.request.urlretrieve(img["images"]["13542:302151"], "docs/refs/ref.png")
```

The rendered PNG is the diff target and the source of truth. Prefer it over a hand "export".

## 3. Render the target headless

puppeteer-core drives the installed Chrome (no Chromium download). Install once in a gitignored `_qa/`: `npm i puppeteer-core`. Run the driver from that dir so `require` resolves.

```js
const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'; // macOS
(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
  const p=await b.newPage(); await p.setViewport({width:1440,height:1200,deviceScaleFactor:2});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file:///abs/path/target.html',{waitUntil:'load'});
  await new Promise(r=>setTimeout(r,500));
  await p.screenshot({path:'docs/refs/mine.png',fullPage:true});
  console.log('JS ERRORS:', errs.length?errs.join('|'):'NONE'); await b.close();
})();
```

For interaction flows, drive real clicks (`p.click(sel)`), assert visible selectors, and screenshot each step. Watch `pageerror` — silent JS errors are a common cause of "the animation does nothing".

## 4. Compose side-by-side + close-up (PIL)

```python
from PIL import Image
ref=Image.open("docs/refs/ref.png"); mine=Image.open("docs/refs/mine.png")
W=380
sc=lambda im: im.resize((W,int(im.height*W/im.width)))
# whole-page side-by-side
a,b=sc(ref),sc(mine); H=max(a.height,b.height)
c=Image.new("RGB",(W*2+16,H),"white"); c.paste(a,(0,0)); c.paste(b,(W+16,0)); c.save("docs/refs/side.png")
# close-up: crop the SAME element region from each (boxes differ by y-offset), then stack
rc=ref.crop((280,1360,1060,2300)); mc=mine.crop((290,1010,1060,1780))
# ...resize to equal width and paste as above -> card_closeup.png
```

Then Read both composed PNGs and list the drift.

## 5. Font weight mapping

When embedding a brand font you only have some weights of, map Figma weights to the nearest file: e.g. Avenir has Roman(≈400), Medium(≈500), Heavy(≈800). If Figma says `w700`, declare the `@font-face` at 700 using the Heavy file so bold renders bold. Base64-embed woff2 so it survives inside a gated/sandboxed iframe.

## 6. Common drift causes (check these first)

- Close-but-wrong hex from eyeballing → always transcribe.
- Page-aggregate radius applied to a component whose radius differs.
- An element present in the Figma component but hidden in the published frame (trust the render).
- System font falling back because the brand font failed to load.
- `deviceScaleFactor` mismatch making everything look soft/misaligned.
- Emoji standing in for real icons; placeholder "Company A" content instead of realistic lengths.
