#!/usr/bin/env python3
"""Lager forsiden, Funksjoner, Nytt og Hjelp på alle fire språk, og legger personvernsidene i den nye rammen.

Kjør fra Trax-web-mappen:   python3 verktoy/lag-sider.py

- Tekstene står i verktoy/tekster.py. Meny, bunntekst og <head> står i verktoy/felles.py.
- Utseendet står i stil.css, og skriptet som legges på alle sider i side.js.
- Personvernsidene (personvern/, sv/integritet/, en/privacy/, de/datenschutz/) skrives fortsatt for hånd:
  endre teksten inne i <main> … </main> i filen, og kjør skriptet, så får siden ny meny og bunntekst.
- Skjermbildegalleriet på Funksjoner hentes fra verktoy/galleri-<språk>.html.
Skriptet kan kjøres så mange ganger du vil; det gir samme resultat hver gang.
"""
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from felles import (BASE_URL, EPOST, SIDER, SPRAK, butikker, bunn, esc, head, nav, opp)  # noqa: E402
from tekster import T  # noqa: E402
import kortbilder  # noqa: E402

WEB = Path(__file__).resolve().parent.parent
AAR = datetime.date.today().year
PIL = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def skriv(sti, innhold):
    f = WEB / sti / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(innhold.rstrip() + "\n", encoding="utf-8")
    print("skrev", f.relative_to(WEB))


def ios_merke(vis):
    return '<span class="ios">iPhone</span> ' if vis else ""


def telefon(up, l, navn, alt, klasse="", lat=True):
    k = f"telefon {klasse}".strip()
    lazy = ' loading="lazy"' if lat else ' fetchpriority="high"'
    return f'<div class="{k}"><img src="{up}img/app/{l}/{navn}.webp" width="600" height="1304" alt="{esc(alt)}" decoding="async"{lazy}></div>'


def side(l, key, tittel, beskrivelse, kropp, body_attr="", ekstra_head="", jsonld=None, app_banner=False, skript=""):
    up = opp(SIDER[l["code"]][key])
    return (head(l, key, tittel, beskrivelse, up, ekstra=ekstra_head, jsonld=jsonld, app_banner=app_banner)
            + f"\n<body{body_attr}>\n{nav(l, key, up)}\n{kropp}\n{bunn(l, key, up, AAR)}{skript}\n</body>\n</html>")


# ---------------------------------------------------------------- Forsiden
def forside(l):
    c = l["code"]
    s, t = SIDER[c], T[c]["forside"]
    up = opp(s["forside"])
    nyttlenke = f'{up}{s["nytt"]}'

    # Gamle ankre (/#support osv.) sendes videre av side.js
    gamle = []
    for anker, mal in t["gamle"].items():
        if mal == "#" + anker:
            continue
        if not mal.startswith("#"):
            sti, _, frag = mal.partition("#")
            mal = sti + "/" + ("#" + frag if frag else "")
        gamle.append(f"{anker}={mal}")

    a1, a2, a3 = t["vifte_alt"]
    hero = f"""<section class="hero"><div class="wrap">
  <div>
    <a class="nyhet" href="{nyttlenke}"><b>{t["nyhet_b"]}</b>{t["nyhet"]} {PIL}</a>
    <h1>{t["h1"][0]} <span>{t["h1"][1]}</span></h1>
    <p class="ingress">{t["ingress"]}</p>
    {butikker(l, up)}
    <p class="pris"><b>{t["pris"][0]}</b> {t["pris"][1]}</p>
  </div>
  <div class="vifte">
    {telefon(up, c, "home", a1, "t1", lat=False)}
    {telefon(up, c, "detail", a2, "t2", lat=False)}
    {telefon(up, c, "dogpage", a3, "t3", lat=False)}
  </div>
</div></section>"""

    sl = t["slik"]
    faner, steg = [], []
    for i, st in enumerate(t["steg"], 1):
        faner.append(f'<li role="presentation"><button type="button" role="tab" id="fane-{i}" aria-controls="steg-{i}" aria-selected="{"true" if i == 1 else "false"}">'
                     f'<span class="pin" aria-hidden="true">{i}</span>{st["kort"]}</button></li>')
        punkter = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in st["punkter"])
        steg.append(f"""<li id="steg-{i}" role="tabpanel" aria-labelledby="fane-{i}">
      <div class="tekst"><div class="hode"><span class="pin" aria-hidden="true">{i}</span><h3>{st["tittel"]}</h3></div>{ios_merke(st.get("ios"))}<p>{st["tekst"]}</p></div>
      {telefon(up, c, st["bilde"], st["alt"])}
      <ul class="punkter">{punkter}</ul>
    </li>""")
    slik = f"""<section class="slik" id="slik"><div class="wrap">
  <div class="tittel midt"><p class="smatittel">{sl["smatittel"]}</p><h2>{sl["h2"]}</h2></div>
  <ul class="faner" role="tablist" aria-label="{sl["faner"]}" data-start="0">
    {"".join(faner)}
  </ul>
  <ol class="steg">
    {"".join(steg)}
  </ol>
</div></section>"""

    r = t["ruter"]
    kort = []
    for k in t["kort"]:
        kort.append(f"""<article class="rute {k["k"]}">
      <div class="t">{ios_merke(k.get("ios"))}<h3>{k["tittel"]}</h3><p>{k["tekst"]}</p></div>
      <div class="utsnitt"><img src="{up}img/app/{c}/{k["bilde"]}.webp" width="{kortbilder.BREDDE}" height="{kortbilder.hoyde(k["bilde"])}" alt="{esc(k["alt"])}" loading="lazy" decoding="async"></div>
    </article>""")
    ruter = f"""<section id="treningsformer"><div class="wrap">
  <div class="tittel"><p class="smatittel">{r["smatittel"]}</p><h2>{r["h2"]}</h2><p class="ingress">{r["ingress"]}</p></div>
  <div class="ruter" data-inn>
    {"".join(kort)}
  </div>
  <p class="mer-midt"><a class="mer" href="{up}{s["funksjoner"]}">{r["mer"]}</a></p>
</div></section>"""

    o = t["om"]
    om = f"""<section class="om" id="om"><div class="wrap"><div class="kort">
  <div>
    <p class="smatittel">{o["smatittel"]}</p>
    <blockquote>{o["sitat"]}</blockquote>
    <p class="navn"><b>{o["navn"]}</b>{o["rolle"]}</p>
    <p class="ingress">{o["tekst"]}</p>
  </div>
  <figure><img src="{up}img/quatro.webp" width="720" height="720" alt="{esc(o["alt"])}" loading="lazy" decoding="async"></figure>
</div></div></section>"""

    la = t["last"]
    last = f"""<section class="last" id="last-ned"><div class="wrap"><div class="priskort">
  <div>
    <p class="smatittel">{la["smatittel"]}</p>
    <h2>{la["h2"]}</h2>
    {butikker(l, up)}
  </div>
  <div>
    <p class="belop">{la["belop"]}</p>
    <ul class="fordeler">{"".join(f"<li>{x}</li>" for x in la["fordeler"])}</ul>
  </div>
</div></div></section>"""

    hj = t["hjelp"]
    mal = {"manual": up + s["manual"], "hjelp": up + s["hjelp"], "epost": T[c]["hjelp"]["support_mailto"]}
    hjelp = f"""<section class="hjelp-forside"><div class="wrap">
  <div class="tittel"><h2>{hj["h2"]}</h2><p class="ingress">{hj["ingress"]}</p></div>
  <div class="hjelpekort" data-inn>
    {"".join(f'<a href="{mal[k]}"><b>{a}</b><span>{b}</span></a>' for k, a, b in hj["kort"])}
  </div>
</div></section>"""

    jsonld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": "Trax", "operatingSystem": "iOS, Android",
              "applicationCategory": "SportsApplication", "inLanguage": c, "description": t["jsonld"], "url": BASE_URL + s["forside"],
              "image": f'{BASE_URL}img/og-image-{l["og"]}.png', "author": {"@type": "Person", "name": "Silje Tillerflaten"},
              "publisher": {"@type": "Organization", "name": "Tillerflaten Digital"}}
    kropp = f'<main id="innhold" class="forside">\n{hero}\n{slik}\n{ruter}\n{om}\n{last}\n{hjelp}\n</main>'
    skriv(s["forside"], side(l, "forside", t["tittel"], t["beskrivelse"], kropp,
                             body_attr=f' data-gamle="{" ".join(gamle)}"', jsonld=jsonld, app_banner=True))


def side_hode(h1, ingress):
    return f'<header class="side-hode"><div class="wrap"><h1>{h1}</h1><p class="ingress">{ingress}</p></div></header>'


def liste(punkter):
    return '<ul class="liste">' + "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in punkter) + "</ul>"


# ---------------------------------------------------------------- Funksjoner
def funksjoner(l):
    c = l["code"]
    s, t = SIDER[c], T[c]["funksjoner"]
    up = opp(s["funksjoner"])
    deler = [side_hode(t["h1"], t["ingress"])]
    for g in t["grupper"]:
        deler.append(f"""<section id="{g["id"]}"><div class="wrap"><div class="gruppe">
  <div><h2>{g["tittel"]}</h2><p class="ingress">{g["tekst"]}</p></div>
  {liste(g["punkter"])}
</div></div></section>""")
    d, se = t["deling"], t["send"]
    deler.append(f"""<section id="{d["id"]}"><div class="wrap"><div class="delbilde">
  <div><h2>{d["h2"]}</h2><p class="ingress">{d["tekst"]}</p></div>
  <img src="{up}img/delebilde.webp" width="680" height="1209" alt="{esc(d["alt"])}" loading="lazy" decoding="async">
</div></div></section>""")
    deler.append(f"""<section id="{se["id"]}"><div class="wrap"><div class="gruppe">
  <div><h2>{se["h2"]}</h2></div>
  <div><p class="ingress">{se["tekst"]}</p><div class="boks"><p>{se["merk"]}</p></div></div>
</div></div></section>""")
    ga = t["galleri"]
    galleri = (WEB / "verktoy" / f"galleri-{c}.html").read_text(encoding="utf-8").strip()
    galleri = galleri.replace('src="img/', f'src="{up}img/')
    deler.append(f"""<section id="{ga["id"]}"><div class="wrap">
  <h2>{ga["h2"]}</h2>
  {galleri}
</div></section>""")
    kropp = '<main id="innhold" class="side">\n' + "\n".join(deler) + "\n</main>"
    skriv(s["funksjoner"], side(l, "funksjoner", t["tittel"], t["beskrivelse"], kropp,
                                skript=f'\n<script src="{up}galleri.js?v=2" defer></script>'))


# ---------------------------------------------------------------- Nytt
def nytt(l):
    c = l["code"]
    s, t = SIDER[c], T[c]["nytt"]
    up = opp(s["nytt"])
    deler = [side_hode(t["h1"], t["ingress"])]
    for v in t["versjoner"]:
        smaa = f'<p class="smaa">{v["smaa"]}</p>' if v.get("smaa") else ""
        tlf = "".join(telefon(up, c, n, a) for n, a in v["bilder"])
        deler.append(f"""<section id="{v["id"]}"><div class="wrap"><div class="versjon">
  <div>
    <h2>{v["tittel"]}</h2>
    <p class="dato">{v["dato"]}</p>
    <p class="ingress">{v["tekst"]}</p>
    {liste(v["punkter"])}
    {smaa}
  </div>
  <div class="par">{tlf}</div>
</div></div></section>""")
    kropp = '<main id="innhold" class="side">\n' + "\n".join(deler) + "\n</main>"
    skriv(s["nytt"], side(l, "nytt", t["tittel"], t["beskrivelse"], kropp))


# ---------------------------------------------------------------- Hjelp
def hjelp(l):
    c = l["code"]
    s, t = SIDER[c], T[c]["hjelp"]
    up = opp(s["hjelp"])
    m, pv, arr = t["manual"], t["personvern"], t["arr"]
    faq = "".join(f"<li><h3>{q}</h3><p>{a}</p></li>" for q, a in t["faq"])
    kropp = f"""<main id="innhold" class="side">
{side_hode(t["h1"], t["ingress"])}
<section id="kontakt"><div class="wrap"><div class="kontakt">
  <div><p class="ingress">{t["kontakt_tekst"]}</p><a class="epost" href="{t["support_mailto"]}">{EPOST}</a></div>
  <div class="boks"><h3>{m[0]}</h3><p>{m[1]}</p><a class="mer" href="{up}{s["manual"]}">{m[2]}</a></div>
</div></div></section>
<section id="sporsmal"><div class="wrap">
  <h2>{t["faq_tittel"]}</h2>
  <ul class="sporsmal">{faq}</ul>
</div></section>
<section id="personvern-kort"><div class="wrap"><div class="gruppe">
  <div><h2>{pv[0]}</h2></div>
  <div><p class="ingress">{pv[1]}</p><a class="mer" href="{up}{s["personvern"]}">{pv[2]}</a></div>
</div></div></section>
<section id="{l["arr_anker"]}"><div class="wrap"><div class="gruppe">
  <div><h2>{arr[0]}</h2></div>
  <div><p class="ingress">{arr[1]}</p><a class="mer" href="{arr[3]}">{arr[2]}</a></div>
</div></div></section>
</main>"""
    skriv(s["hjelp"], side(l, "hjelp", t["tittel"], t["beskrivelse"], kropp))


# ---------------------------------------------------------------- Personvern (håndskrevet innhold, ny ramme)
def personvern(l):
    c = l["code"]
    sti = SIDER[c]["personvern"]
    gammel = (WEB / sti / "index.html").read_text(encoding="utf-8")
    tittel = html_unescape(re.search(r"<title>(.*?)</title>", gammel, re.S).group(1))
    beskrivelse = html_unescape(re.search(r'<meta name="description" content="(.*?)">', gammel, re.S).group(1))
    innhold = re.search(r"<main[^>]*>\n?(.*?)\n?</main>", gammel, re.S).group(1)
    # Første gang: gammel overskrift-ramme og klassenavn byttes til de nye
    innhold = re.sub(r'<header class="hero">\s*(<h1>.*?</h1>)\s*</header>', r"\1", innhold, flags=re.S)
    innhold = innhold.replace('class="updated"', 'class="oppdatert"')
    kropp = f'<main id="innhold" class="wrap les">\n{innhold.strip(chr(10))}\n</main>'
    skriv(sti, side(l, "personvern", tittel, beskrivelse, kropp))


def html_unescape(s):
    import html
    return html.unescape(s)


def sitemap():
    linjer = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in ["forside", "funksjoner", "nytt", "hjelp", "manual", "personvern"]:
        for l in SPRAK:
            linjer.append(f'  <url><loc>{BASE_URL}{SIDER[l["code"]][key]}</loc>')
            for o in SPRAK:
                linjer.append(f'    <xhtml:link rel="alternate" hreflang="{o["code"]}" href="{BASE_URL}{SIDER[o["code"]][key]}"/>')
            linjer.append("  </url>")
    linjer.append("</urlset>")
    (WEB / "sitemap.xml").write_text("\n".join(linjer) + "\n", encoding="utf-8")
    (WEB / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8")
    print("skrev sitemap.xml og robots.txt")


if __name__ == "__main__":
    for l in SPRAK:
        forside(l)
        funksjoner(l)
        nytt(l)
        hjelp(l)
        personvern(l)
    sitemap()
