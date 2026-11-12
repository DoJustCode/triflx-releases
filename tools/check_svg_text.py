#!/usr/bin/env python3
"""Проверка SVG в docs/assets: текст должен помещаться в свои блоки с запасом при любых шрифтах.

Что делает (нужен Google Chrome / Chromium; других зависимостей нет):
  1. Для каждого SVG измеряет getBBox() каждого <text> в Chrome, дважды: со стандартным системным
     шрифтом и с «широким» (Verdana, ≈15% шире Arial) — так имитируется любой шрифт на GitHub/Android.
  2. Ищет для текста самый маленький <rect> (без data-deco), в который попадает его центр. Если блока
     нет — это весь viewBox. Ширина текста увеличивается на 25% (запас), и он обязан лежать внутри
     блока с отступом не меньше 6 единиц viewBox. Иначе — ошибка и код возврата 1.
  3. Проверяет, что в колонке 358 px (телефон 390 px минус поля) размер шрифта не меньше 11 px.
  4. Рендерит PNG в 390, 768 и 1200 px, светлая и тёмная темы (ключевые кадры анимации) в --out.

Запуск:  python3 tools/check_svg_text.py [--out /tmp/svgcheck] [--no-png]
"""
import argparse, json, os, re, subprocess, sys, tempfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "assets"
CHROME = next((p for p in [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"] if os.path.exists(p)), None)
PAD, STRETCH, COLUMN, MIN_FONT = 6.0, 1.25, 358.0, 11.0
FONTS = {"system": "", "wide(Verdana)": "text,tspan{font-family:Verdana,'DejaVu Sans',sans-serif !important}"}
FRAMES = {"flow-card.svg": [0, 1, 2]}   # три шага анимации = три кадра

JS = r"""
const out=[];const svg=document.querySelector('svg');const vb=svg.viewBox.baseVal;
const rects=[...svg.querySelectorAll('rect')].filter(r=>!r.hasAttribute('data-deco')&&!r.closest('clipPath')&&!r.closest('defs')).map(r=>{const b=r.getBBox();return {x:b.x,y:b.y,w:b.width,h:b.height,g:r.closest('g')}});
for(const t of svg.querySelectorAll('text')){
  const b=t.getBBox();const cs=getComputedStyle(t);const fs=parseFloat(cs.fontSize);
  const anchor=cs.textAnchor;const ax=t.getStartPositionOfChar?t.x.baseVal[0].value:b.x;
  let l=b.x,r=b.x+b.width;const w=b.width*%STRETCH%;
  if(anchor==='middle'){l=b.x+b.width/2-w/2;r=b.x+b.width/2+w/2}else if(anchor==='end'){l=r-w}else{r=l+w}
  const cx=b.x+b.width/2,cy=b.y+b.height/2;
  let box={x:0,y:0,w:vb.width,h:vb.height,name:'viewBox'};let best=1e18;
  for(const q of rects){if((q.g===null||q.g===t.closest('g'))&&cx>=q.x&&cx<=q.x+q.w&&cy>=q.y&&cy<=q.y+q.h&&q.w*q.h<best){best=q.w*q.h;box={...q,name:'rect'}}}
  const bad=[];
  if(l<box.x+%PAD%)bad.push('слева '+(l-box.x).toFixed(1));
  if(r>box.x+box.w-%PAD%)bad.push('справа '+(box.x+box.w-r).toFixed(1));
  if(b.y<box.y+%PAD%-2)bad.push('сверху '+(b.y-box.y).toFixed(1));
  if(b.y+b.height>box.y+box.h-%PAD%+2)bad.push('снизу '+(box.y+box.h-b.y-b.height).toFixed(1));
  const eff=fs*%COLUMN%/vb.width;if(eff<%MINFONT%)bad.push('шрифт '+eff.toFixed(1)+'px');
  out.push({text:t.textContent.trim(),w:+b.width.toFixed(1),inbox:box.name,fs,eff:+eff.toFixed(1),bad});
}
document.getElementById('out').textContent=JSON.stringify(out);
"""

def chrome(args, timeout=60):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox", *args],
                          capture_output=True, text=True, timeout=timeout)

def measure(svg_path, css):
    svg = pathlib.Path(svg_path).read_text(encoding="utf-8")
    js = (JS.replace("%STRETCH%", str(STRETCH)).replace("%PAD%", str(PAD))
            .replace("%COLUMN%", str(COLUMN)).replace("%MINFONT%", str(MIN_FONT)))
    html = f"<!doctype html><meta charset=utf-8><style>{css}</style><body>{svg}<pre id=out></pre><script>{js}</script>"
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "m.html"; p.write_text(html, encoding="utf-8")
        r = chrome(["--virtual-time-budget=1500", "--dump-dom", p.as_uri()])
    m = re.search(r'<pre id="out">(.*?)</pre>', r.stdout, re.S)
    if not m: raise RuntimeError("Chrome не вернул результат: " + r.stderr[-300:])
    return json.loads(m.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"'))

def render(svg_path, outdir, tag, width, dark, frame):
    svg = pathlib.Path(svg_path)
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg.read_text(encoding="utf-8"))
    vw, vh = int(m.group(1)), int(m.group(2))
    iw = min(vw, width - 32) if width <= 768 else min(vw * 1.5, 900)
    ih = iw * vh / vw
    bg = "#0d1117" if dark else "#ffffff"
    # SVG вставляется инлайн, анимации выключены, показывается нужный кадр (у flow-card — шаг frame+1)
    css = "*{animation:none !important}svg{width:%spx;height:auto;display:block;margin:0 auto}" % iw
    if svg.name in FRAMES: css += ".step{opacity:0}g.step:nth-of-type(%d){opacity:1}" % (frame + 1)
    body = svg.read_text(encoding="utf-8")
    html = f"<!doctype html><meta charset=utf-8><style>{css}</style><body style='margin:0;background:{bg}'><div style='box-sizing:border-box;width:{width}px;padding:16px;margin:0 auto'>{body}</div>"
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "r.html"; p.write_text(html, encoding="utf-8")
        png = pathlib.Path(outdir) / f"{svg.stem}-{width}-{'dark' if dark else 'light'}{tag}.png"
        W = max(width, 500)   # headless Chrome не делает окно уже ~500 px: лишнее обрезаем ниже
        chrome([f"--window-size={W},{int(ih + 32)}", f"--virtual-time-budget=500",
                f"--blink-settings=preferredColorScheme={0 if dark else 1}", f"--screenshot={png}", p.as_uri()])
        if W != width and png.exists() and sys.platform == "darwin":
            subprocess.run(["sips", "--cropToHeightWidth", str(int(ih + 32)), str(width), str(png)], capture_output=True)
    return png

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=str(pathlib.Path(tempfile.gettempdir()) / "svgcheck")); ap.add_argument("--no-png", action="store_true")
    a = ap.parse_args()
    if not CHROME: sys.exit("Нужен Google Chrome или Chromium")
    os.makedirs(a.out, exist_ok=True)
    fails = 0
    for svg in sorted(ASSETS.glob("*.svg")):
        for fname, css in FONTS.items():
            res = measure(svg, css)
            bad = [x for x in res if x["bad"]]
            fails += len(bad)
            print(f"{'FAIL' if bad else 'ok  '} {svg.name:16} {fname:14} текстов: {len(res)}, мин. шрифт в колонке 358px: {min(x['eff'] for x in res)} px")
            for x in bad: print(f"       «{x['text']}» → {', '.join(x['bad'])}")
        if not a.no_png:
            for w in (390, 768, 1200):
                for dark in (False, True):
                    for i, b in enumerate(FRAMES.get(svg.name, [0])):
                        render(svg, a.out, f"-f{i}" if svg.name in FRAMES else "", w, dark, b)
    print("PNG:", a.out)
    print("ИТОГ:", "ошибок нет" if not fails else f"ошибок: {fails}")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
