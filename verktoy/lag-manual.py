#!/usr/bin/env python3
"""Lager brukermanualen på nettsiden fra manualen i appen.

Kilden er ManualContent i Trax/UserManualView.swift og manual-*-bildene i
Trax/Assets.xcassets i app-repoet (stillerflaten/Trax). Skriptet lager
manual/index.html, sv/manual/index.html, en/manual/index.html,
de/manual/index.html og bildene i img/manual/. Stilen hentes fra index.html, så manualen følger resten av siden.

Bruk (fra roten av Trax-web):
    python3 verktoy/lag-manual.py ../Trax
    python3 verktoy/lag-manual.py ../Trax de     (bare ett eller flere språk)

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
    dict(code="nb", gp_title="Snart for Android", coming="Kommer i v. 2.1", swift="norwegian", lproj="nb", suffix="", dir="", short="NO", name="Norsk",
         locale="nb_NO", privacy=("personvern", "Personvern"), badge_alt="Last ned fra App Store", choose="Velg språk",
         contents_back="Til innholdet", updated="Sist oppdatert", tip="Tips", warning="Viktig",
         eyebrow="iOS-app for sportrening", nav="Manual",
         dev_by="Utviklet av Tillerflaten Digital · Org.nr. 938 657 742", logo_alt="Logo for Tillerflaten Digital",
         title="Brukermanual – Trax", desc="Brukermanual for Trax, appen for sportrening med hund: legg spor, tren hunden og følg utviklingen over tid.",
         months=["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]),
    dict(code="sv", gp_title="Snart för Android", coming="Kommer i v. 2.1", swift="swedish", lproj="sv", suffix="-sv", dir="sv/", short="SV", name="Svenska",
         locale="sv_SE", privacy=("integritet", "Integritet"), badge_alt="Hämta i App Store", choose="Välj språk",
         contents_back="Till innehållet", updated="Senast uppdaterad", tip="Tips", warning="Viktigt",
         eyebrow="iOS-app för spårträning", nav="Manual",
         dev_by="Utvecklad av Tillerflaten Digital · Org.nr. 938 657 742", logo_alt="Logotyp för Tillerflaten Digital",
         title="Användarmanual – Trax", desc="Användarmanual för Trax, appen för spårträning med hund: lägg spår, träna hunden och följ utvecklingen över tid.",
         months=["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"]),
    dict(code="en", gp_title="Coming soon to Android", coming="Coming in v2.1", swift="english", lproj="en", suffix="-en", dir="en/", short="EN", name="English",
         locale="en_US", privacy=("privacy", "Privacy"), badge_alt="Download on the App Store", choose="Choose language",
         contents_back="Back to contents", updated="Last updated", tip="Tip", warning="Important",
         eyebrow="iOS app for tracking training", nav="Manual",
         dev_by="Developed by Tillerflaten Digital · Org. no. 938 657 742", logo_alt="Tillerflaten Digital logo",
         title="User manual – Trax", desc="User manual for Trax, the app for tracking training with your dog: lay tracks, train your dog and follow your progress over time.",
         months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]),
    dict(code="de", gp_title="Bald für Android", coming="Kommt mit v2.1", swift="german", lproj="de", suffix="-de", dir="de/", short="DE", name="Deutsch",
         locale="de_DE", privacy=("datenschutz", "Datenschutz"), badge_alt="Laden im App Store", choose="Sprache wählen",
         contents_back="Zum Inhalt", updated="Zuletzt aktualisiert", tip="Tipp", warning="Wichtig",
         eyebrow="iOS-App für die Fährtenarbeit", nav="Handbuch",
         dev_by="Entwickelt von Tillerflaten Digital · Org.-Nr. 938 657 742", logo_alt="Logo von Tillerflaten Digital",
         css="/* «Handbuch» er lengre enn «Manual», så navnet ved logoen skjules litt tidligere på smal skjerm */\n@media (max-width:430px){.brand{font-size:0;gap:0}}",
         og="en",  # delebildet finnes ikke på tysk ennå
         title="Handbuch – Trax", desc="Handbuch für Trax, die App für die Fährtenarbeit mit deinem Hund: Fährten legen, den Hund trainieren und den Fortschritt verfolgen.",
         months=["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]),
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
    """Kopierer skjermbildet til nettsiden. Gir False når bildet ikke finnes i appen (som i appen vises det da ikke)."""
    src = app / "Trax/Assets.xcassets" / f"{name}.imageset" / f"{name}.jpg"
    if not src.exists():
        return False
    dst = WEB / "img/manual" / f"{name}.jpg"
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im.convert("RGB").resize((IMG_W, IMG_H), Image.LANCZOS).save(dst, "JPEG", quality=80, optimize=True, progressive=True)
    used.add(dst.name)
    return True


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
.back a{text-decoration:none;font-weight:600}
.hero .callout{margin-top:20px}
.hero .callout p{font-size:16px;color:var(--fg);max-width:none}
/* «Kommer i v. 2.1»: samme stil som «Ute nå»-merket på forsiden (.v2-merke) */
.kommer{display:inline-block;margin:0 0 10px;background:var(--deep);color:var(--on-deep);font:700 14px/1 var(--display);padding:8px 12px;border-radius:999px;white-space:nowrap}
.toc .kommer{flex:none;align-self:center;margin:0 0 0 auto;font-size:12px;padding:5px 9px}"""


# Avsnitt om funksjoner som ikke er i App Store ennå, med versjonen de kommer i. Avsnittet merkes
# «Kommer i v. 2.1» (teksten står i «coming» i LANGS). Tomt nå som 2.1 er ute; legg til avsnitts-id-er
# (f.eks. {"hundens-spor"}) og oppdater «coming» ved neste versjon.
COMING = set()

# Språk som har nettside, men ikke manual ennå (manualen kommer når appen er oversatt). Lenkene går til forsiden.
SITE_ONLY_LANGS = []


def nav_lang(l, here_prefix):
    """Språkvelgeren med lenker til manualen på de andre språkene."""
    items = []
    for o in LANGS:
        href = here_prefix + o["dir"] + "manual/"
        if o is l:
            items.append(f'      <li><a href="./" lang="{o["code"]}" aria-current="page">{o["name"]}</a></li>')
        else:
            items.append(f'      <li><a href="{href}" hreflang="{o["code"]}" lang="{o["code"]}">{o["name"]}</a></li>')
    for o in SITE_ONLY_LANGS:
        items.append(f'      <li><a href="{here_prefix}{o["dir"]}" hreflang="{o["code"]}" lang="{o["code"]}">{o["name"]}</a></li>')
    return ("  <details class=\"lang\">\n"
            f'    <summary aria-label="{l["choose"]}">{GLOBE}<span>{l["short"]}</span>{CHEV}</summary>\n'
            "    <ul>\n" + "\n".join(items) + "\n    </ul>\n  </details>")


def render(l, sections, strings, style, app, used, date):
    up = "../" * (1 + l["dir"].count("/"))       # fra manualsiden til roten
    home = up + l["dir"]                          # forsiden på samme språk
    img = up + "img/manual/"
    pslug, pname = l["privacy"]
    d = f'{date.day}. {l["months"][date.month - 1]} {date.year}' if l["code"] != "en" else f'{date.day} {l["months"][date.month - 1]} {date.year}'

    # Valgfri beskjed øverst, f.eks. når manualen kommer før appen er oversatt (fjern «note» i LANGS når den ikke trengs)
    note = f'    <div class="callout">{ICON_TIP}<p>{esc(l["note"])}</p></div>\n' if l.get("note") else ""

    out = []
    for i, s in enumerate(sections, 1):
        h = [f'  <section class="m" id="{s["id"]}">',
             f'    <p class="eyebrow">{i:02d}</p>',
             *([f'    <span class="kommer">{l["coming"]}</span>'] if s["id"] in COMING else []),
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
                if not copy_image(app, name, used):
                    continue
                h.append(f'    <figure class="shot"><img src="{img}{name}.jpg" width="{IMG_W}" height="{IMG_H}" alt="" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>')
        h.append(f'    <p class="back"><a href="#innhold">↑ {l["contents_back"]}</a></p>')
        h.append("  </section>")
        out.append("\n".join(h))

    toc = "\n".join(f'      <li><a href="#{s["id"]}">{esc(s["title"])}' + (f' <span class="kommer">{l["coming"]}</span>' if s["id"] in COMING else "") + '</a></li>' for s in sections)
    alts = "\n".join(f'<link rel="alternate" hreflang="{o["code"]}" href="{BASE_URL}{o["dir"]}manual/">' for o in LANGS)
    loc_alts = "\n".join(f'<meta property="og:locale:alternate" content="{o["locale"]}">' for o in LANGS if o is not l)
    footer_langs = " · ".join(f'<a href="{up}{o["dir"]}manual/" hreflang="{o["code"]}" lang="{o["code"]}">{o["name"]}</a>' for o in LANGS if o is not l)
    footer_langs += "".join(f' · <a href="{up}{o["dir"]}" hreflang="{o["code"]}" lang="{o["code"]}">{o["name"]}</a>' for o in SITE_ONLY_LANGS)

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
<meta property="og:image" content="{BASE_URL}img/og-image-{l.get("og", l["code"])}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<style>
{style}
{MANUAL_CSS}
{l.get("css", "")}
</style>
</head>
<body>
<nav><div class="wrap">
  <a class="brand" href="{home}"><img src="{up}img/icon-192.png" width="32" height="32" alt="">Trax</a>
  <a class="l" href="./" aria-current="page">{l["nav"]}</a>
  <a class="l" href="{home}#support">Support</a>
  <a class="l opt" href="{home}{pslug}/">{pname}</a>
{nav_lang(l, up)}
  <a class="kj" href="https://apps.apple.com/app/id6758005408"><img src="{up}img/app-store-{l["code"]}.svg" width="120" height="40" alt="{l["badge_alt"]}"></a>
  <span class="gp" title="{l["gp_title"]}"><img src="{up}img/google-play-{l["code"]}.svg" width="135" height="40" alt="Google Play: {l["gp_title"]}"></span>
</div></nav>

<main class="wrap" id="top">
  <header class="hero">
    <p class="eyebrow">{l["eyebrow"]}</p>
    <h1>{esc(strings["manual.title"])}</h1>
    <p class="lead">{esc(strings["manual.subtitle"])}</p>
    <p class="updated">{l["updated"]}: {d}</p>
{note}    <svg class="trackline" viewBox="0 0 700 60" preserveAspectRatio="none" aria-hidden="true">
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
  <footer>© {date.year} Silje Tillerflaten · <a href="./">{esc(strings["manual.title"])}</a> · <a href="{home}#support">Support</a> · <a href="{home}{pslug}/">{pname}</a> · {footer_langs}
    <p class="utvikler"><img src="{up}img/tillerflaten-digital.png" width="24" height="24" alt="{l["logo_alt"]}"> {l["dev_by"]}</p>
  </footer>
</div>

<script>
/* Språkvelger: lukk menyen ved klikk utenfor eller Escape */
(function(){{var d=document.querySelector('.lang');if(!d)return;
document.addEventListener('click',function(e){{if(d.open&&!d.contains(e.target))d.open=false}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&d.open){{d.open=false;d.querySelector('summary').focus()}}}});}})();
</script>
<script data-goatcounter="https://trax-dogtracking.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    app = pathlib.Path(sys.argv[1]).resolve()
    only = set(sys.argv[2:])
    if only - {l["code"] for l in LANGS}:
        sys.exit(f"ukjent språk: {', '.join(sorted(only))}")
    swift = (app / "Trax/UserManualView.swift").read_text(encoding="utf-8")
    style = re.search(r"<style>\n(.*?)\n</style>", (WEB / "index.html").read_text(encoding="utf-8"), re.S).group(1)
    style = style.split("\n", 1)[1]  # dropp forsidens layout-kommentar
    date = datetime.date.today()
    used = set()
    for l in LANGS:
        if only and l["code"] not in only:
            continue
        sections = parse_sections(swift, l["swift"])
        strings = read_strings(app / f'Trax/{l["lproj"]}.lproj/Localizable.strings')
        page = render(l, sections, strings, style, app, used, date)
        dst = WEB / l["dir"] / "manual/index.html"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(page, encoding="utf-8")
        shots = sum(1 for s in sections for k, _ in s["blocks"] if k == "screenshot")
        print(f'{dst.relative_to(WEB)}: {len(sections)} avsnitt, {shots} skjermbilder')
    if only:
        return  # bildene til de andre språkene er ikke lest inn, så ingenting slettes
    for old in (WEB / "img/manual").glob("*.jpg"):
        if old.name not in used:
            old.unlink()
            print(f"slettet ubrukt bilde {old.name}")


if __name__ == "__main__":
    main()
