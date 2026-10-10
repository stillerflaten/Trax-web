#!/usr/bin/env python3
"""Lager brukermanualen på nettsiden fra manualen i appen.

Kilden er ManualContent i Trax/UserManualView.swift og manual-*-bildene i
Trax/Assets.xcassets i app-repoet (stillerflaten/Trax). Skriptet lager
manual/index.html, sv/manual/index.html, en/manual/index.html og bildene i
img/manual/. Stilen hentes fra index.html, så manualen følger resten av siden.

Bruk (fra roten av Trax-web):
    python3 verktoy/lag-manual.py ../Trax

Kjør på nytt hver gang manualen i appen endres, og legg inn alt som endres.
Krever Pillow (python3 -m pip install pillow) for å skalere bildene.
"""
import datetime
import html
import pathlib
import re
import sys

from PIL import Image

WEB = pathlib.Path(__file__).resolve().parent.parent
BASE_URL = "https://trax-dogtracking.no/"
IMG_W, IMG_H = 420, 913  # samme størrelse som skjermbildene på forsiden

LANGS = [
    dict(code="nb", swift="norwegian", lproj="nb", suffix="", dir="", short="NO", name="Norsk",
         locale="nb_NO", privacy=("personvern", "Personvern"), choose="Velg språk",
         contents_back="Til innholdet", updated="Sist oppdatert", tip="Tips", warning="Viktig",
         eyebrow="iOS-app for sportrening", nav="Manual",
         title="Brukermanual – Trax", desc="Brukermanual for Trax, appen for sportrening med hund: legg spor, gå spor med hunden og følg utviklingen over tid.",
         months=["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]),
    dict(code="sv", swift="swedish", lproj="sv", suffix="-sv", dir="sv/", short="SV", name="Svenska",
         locale="sv_SE", privacy=("integritet", "Integritet"), choose="Välj språk",
         contents_back="Till innehållet", updated="Senast uppdaterad", tip="Tips", warning="Viktigt",
         eyebrow="iOS-app för spårträning", nav="Manual",
         title="Användarmanual – Trax", desc="Användarmanual för Trax, appen för spårträning med hund: lägg spår, spåra med hunden och följ utvecklingen över tid.",
         months=["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]),
    dict(code="en", swift="english", lproj="en", suffix="-en", dir="en/", short="EN", name="English",
         locale="en_US", privacy=("privacy", "Privacy"), choose="Choose language",
         contents_back="Back to contents", updated="Last updated", tip="Tip", warning="Important",
         eyebrow="iOS app for tracking training", nav="Manual",
         title="User manual – Trax", desc="User manual for Trax, the app for tracking training with your dog: lay tracks, walk them with your dog and follow your progress over time.",
         months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
]

STR = r'"((?:[^"\\]|\\.)*)"'
BLOCK_RE = re.compile(
    r'\.(?P<kind>text|tip|warning)\(\s*' + STR + r'\s*\)'
    r'|\.(?P<lkind>steps|bullets)\(\s*\[(?P<items>.*?)\]\s*\)'
    r'|\.screenshot\(\s*name:\s*' + STR + r'\s*,\s*caption:\s*' + STR + r'\s*\)',
    re.S)


def unescape(s):
    return re.sub(r'\\(.)', r'\1', s)


def parse_sections(swift, var):
    start = swift.index(f"static let {var}: [ManualSection] = [")
    end = swift.find("static let ", start + 10)
    body = swift[start:end if end != -1 else len(swift)]
    parts = re.split(r'\bManualSection\(', body)[1:]
    sections = []
    for p in parts:
        sid = re.search(r'id:\s*' + STR, p).group(1)
        title = unescape(re.search(r'title:\s*' + STR, p).group(1))
        m = re.search(r'intro:\s*(?:nil|' + STR + ')', p)
        intro = unescape(m.group(1)) if m and m.group(1) else None
        blocks = []
        for b in BLOCK_RE.finditer(p[p.index("blocks:"):]):
            if b.group("kind"):
                blocks.append((b.group("kind"), unescape(b.group(2))))
            elif b.group("lkind"):
                items = [unescape(s) for s in re.findall(STR, b.group("items"))]
                blocks.append((b.group("lkind"), items))
            else:
                blocks.append(("screenshot", (b.group(5), unescape(b.group(6)))))
        sections.append(dict(id=sid, title=title, intro=intro, blocks=blocks))
    return sections


def read_strings(path):
    out = {}
    for k, v in re.findall(r'^"([^"]+)"\s*=\s*' + STR + ';', path.read_text(encoding="utf-8"), re.M):
        out[k] = unescape(v)
    return out


def esc(s):
    t = html.escape(s, quote=False)
    return re.sub(r'([\w.+-]+@[\w-]+\.[\w.]+[A-Za-z])', r'<a href="mailto:\1">\1</a>', t)


def copy_image(app, name, used):
    src = app / "Trax/Assets.xcassets" / f"{name}.imageset" / f"{name}.jpg"
    dst = WEB / "img/manual" / f"{name}.jpg"
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im.convert("RGB").resize((IMG_W, IMG_H), Image.LANCZOS).save(dst, "JPEG", quality=80, optimize=True, progressive=True)
    used.add(dst.name)


ICON_TIP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg>'
ICON_WARN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0zM12 9v4M12 17h.01"/></svg>'
GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

MANUAL_CSS = """/* Brukermanual (lages av verktoy/lag-manual.py): innholdsliste, nummererte steg, tips og skjermbilder */
nav a.l[aria-current]{color:var(--accent)}
.hero .lead{font-size:20px;color:var(--muted);margin:0;max-width:40ch}
.hero p.updated{font-size:13px;margin-top:12px;max-width:none}
.toc,.m{scroll-margin-top:64px}
.toc{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin-top:28px}
.toc ol{margin:0;padding:0;list-style:none;columns:1;column-gap:28px;counter-reset:toc}
.toc li{counter-increment:toc;break-inside:avoid;max-width:none}
.toc a{display:flex;gap:10px;padding:5px 0;text-decoration:none;color:var(--fg);font-weight:500}
.toc a::before{content:counter(toc,decimal-leading-zero);font:400 13px/1.9 var(--mono);color:var(--muted);flex:none}
.toc a:hover,.toc a:focus-visible{color:var(--accent)}
@media (min-width:600px){.toc ol{columns:2}}
.m .intro{font-size:18px;color:var(--muted)}
.m ol.steps{list-style:none;padding:0;counter-reset:st;margin:16px 0}
.m ol.steps li{counter-increment:st;position:relative;padding-left:40px;margin-bottom:10px}
.m ol.steps li::before{content:counter(st);position:absolute;left:0;top:1px;width:26px;height:26px;border-radius:50%;background:var(--accent);color:var(--accent-ink);font:700 14px/26px var(--display);text-align:center}
.m ul li{margin-bottom:6px}
.callout{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:14px 16px;margin:16px 0;max-width:65ch}
.callout svg{flex:none;width:22px;height:22px;color:var(--accent);margin-top:2px}
.callout p{margin:0}
.callout.warn{border-left-color:var(--track)}
.callout.warn svg{color:var(--track)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
figure.shot{margin:20px 0;max-width:260px}
figure.shot img{display:block;width:100%;height:auto;border-radius:18px;border:1px solid var(--line);box-shadow:0 8px 24px rgba(0,0,0,.08)}
figure.shot figcaption{font-size:14px;color:var(--muted);margin-top:8px}
.back{font-size:14px;margin:20px 0 0}
.back a{text-decoration:none;font-weight:600}"""


def nav_lang(l, here_prefix):
    """Språkvelgeren med lenker til manualen på de andre språkene."""
    items = []
    for o in LANGS:
        href = here_prefix + o["dir"] + "manual/"
        if o is l:
            items.append(f'      <li><a href="./" lang="{o["code"]}" aria-current="page">{o["name"]}</a></li>')
        else:
            items.append(f'      <li><a href="{href}" hreflang="{o["code"]}" lang="{o["code"]}">{o["name"]}</a></li>')
    return ("  <details class=\"lang\">\n"
            f'    <summary aria-label="{l["choose"]}">{GLOBE}<span>{l["short"]}</span>{CHEV}</summary>\n'
            "    <ul>\n" + "\n".join(items) + "\n    </ul>\n  </details>")


def render(l, sections, strings, style, app, used, date):
    up = "../" * (1 + l["dir"].count("/"))       # fra manualsiden til roten
    home = up + l["dir"]                          # forsiden på samme språk
    img = up + "img/manual/"
    pslug, pname = l["privacy"]
    d = f'{date.day}. {l["months"][date.month - 1]} {date.year}' if l["code"] != "en" else f'{date.day} {l["months"][date.month - 1]} {date.year}'

    out = []
    for i, s in enumerate(sections, 1):
        h = [f'  <section class="m" id="{s["id"]}">',
             f'    <p class="eyebrow">{i:02d}</p>',
             f'    <h2>{esc(s["title"])}</h2>']
        if s["intro"]:
            h.append(f'    <p class="intro">{esc(s["intro"])}</p>')
        for kind, val in s["blocks"]:
            if kind == "text":
                h.append(f"    <p>{esc(val)}</p>")
            elif kind in ("tip", "warning"):
                cls, icon, label = ("callout", ICON_TIP, l["tip"]) if kind == "tip" else ("callout warn", ICON_WARN, l["warning"])
                h.append(f'    <div class="{cls}">{icon}<p><span class="sr">{label}: </span>{esc(val)}</p></div>')
            elif kind == "steps":
                h.append('    <ol class="steps">\n' + "\n".join(f"      <li>{esc(x)}</li>" for x in val) + "\n    </ol>")
            elif kind == "bullets":
                h.append("    <ul>\n" + "\n".join(f"      <li>{esc(x)}</li>" for x in val) + "\n    </ul>")
            else:
                name, cap = val
                copy_image(app, name, used)
                h.append(f'    <figure class="shot"><img src="{img}{name}.jpg" width="{IMG_W}" height="{IMG_H}" alt="" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>')
        h.append(f'    <p class="back"><a href="#innhold">↑ {l["contents_back"]}</a></p>')
        h.append("  </section>")
        out.append("\n".join(h))

    toc = "\n".join(f'      <li><a href="#{s["id"]}">{esc(s["title"])}</a></li>' for s in sections)
    alts = "\n".join(f'<link rel="alternate" hreflang="{o["code"]}" href="{BASE_URL}{o["dir"]}manual/">' for o in LANGS)
    loc_alts = "\n".join(f'<meta property="og:locale:alternate" content="{o["locale"]}">' for o in LANGS if o is not l)
    footer_langs = " · ".join(f'<a href="{up}{o["dir"]}manual/" hreflang="{o["code"]}" lang="{o["code"]}">{o["name"]}</a>' for o in LANGS if o is not l)

    return f"""<!doctype html>
<html lang="{l["code"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{l["desc"]}">
<title>{l["title"]}</title>
<!-- Lages av verktoy/lag-manual.py fra manualen i appen. Ikke rediger for hånd; endre appen og kjør skriptet på nytt. -->
<link rel="canonical" href="{BASE_URL}{l["dir"]}manual/">
{alts}
<link rel="icon" type="image/png" sizes="32x32" href="{up}img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{up}img/icon-192.png">
<link rel="apple-touch-icon" href="{up}img/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:locale" content="{l["locale"]}">
{loc_alts}
<meta property="og:site_name" content="Trax">
<meta property="og:title" content="{l["title"]}">
<meta property="og:description" content="{l["desc"]}">
<meta property="og:url" content="{BASE_URL}{l["dir"]}manual/">
<meta property="og:image" content="{BASE_URL}img/og-image.png">
<meta property="og:image:width" content="512">
<meta property="og:image:height" content="512">
<meta name="twitter:card" content="summary">
<style>
{style}
{MANUAL_CSS}
</style>
</head>
<body>
<nav><div class="wrap">
  <a class="brand" href="{home}"><img src="{up}img/icon-192.png" width="32" height="32" alt="">Trax</a>
  <a class="l" href="./" aria-current="page">{l["nav"]}</a>
  <a class="l" href="{home}#support">Support</a>
  <a class="l opt" href="{home}#{pslug}">{pname}</a>
{nav_lang(l, up)}
</div></nav>

<main class="wrap" id="top">
  <header class="hero">
    <p class="eyebrow">{l["eyebrow"]}</p>
    <h1>{esc(strings["manual.title"])}</h1>
    <p class="lead">{esc(strings["manual.subtitle"])}</p>
    <p class="updated">{l["updated"]}: {d}</p>
    <svg class="trackline" viewBox="0 0 700 60" preserveAspectRatio="none" aria-hidden="true">
      <path d="M10 40 C 90 10, 150 55, 240 30 S 380 8, 460 38 S 600 50, 690 18"/>
      <circle cx="10" cy="40" r="6"/><circle cx="690" cy="18" r="6"/>
    </svg>
    <div class="toc" id="innhold" role="navigation" aria-labelledby="innhold-tittel">
      <p class="eyebrow" id="innhold-tittel">{esc(strings["manual.contents"])}</p>
      <ol>
{toc}
      </ol>
    </div>
  </header>

{chr(10).join(out)}
</main>

<div class="wrap">
  <footer>© {date.year} Silje Tillerflaten · <a href="./">{esc(strings["manual.title"])}</a> · <a href="{home}#support">Support</a> · <a href="{home}#{pslug}">{pname}</a> · {footer_langs}</footer>
</div>

<script>
/* Språkvelger: lukk menyen ved klikk utenfor eller Escape */
(function(){{var d=document.querySelector('.lang');if(!d)return;
document.addEventListener('click',function(e){{if(d.open&&!d.contains(e.target))d.open=false}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&d.open){{d.open=false;d.querySelector('summary').focus()}}}});}})();
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    app = pathlib.Path(sys.argv[1]).resolve()
    swift = (app / "Trax/UserManualView.swift").read_text(encoding="utf-8")
    style = re.search(r"<style>\n(.*?)\n</style>", (WEB / "index.html").read_text(encoding="utf-8"), re.S).group(1)
    style = style.split("\n", 1)[1]  # dropp forsidens layout-kommentar
    date = datetime.date.today()
    used = set()
    for l in LANGS:
        sections = parse_sections(swift, l["swift"])
        strings = read_strings(app / f'Trax/{l["lproj"]}.lproj/Localizable.strings')
        page = render(l, sections, strings, style, app, used, date)
        dst = WEB / l["dir"] / "manual/index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        shots = sum(1 for s in sections for k, _ in s["blocks"] if k == "screenshot")
        print(f'{dst.relative_to(WEB)}: {len(sections)} avsnitt, {shots} skjermbilder')
    for old in (WEB / "img/manual").glob("*.jpg"):
        if old.name not in used:
            old.unlink()
            print(f"slettet ubrukt bilde {old.name}")


if __name__ == "__main__":
    main()
