"""Felles deler for alle sider: språk, adresser, <head>, meny og bunntekst.

Brukes av verktoy/lag-sider.py (forside, undersider og personvern) og verktoy/lag-manual.py (manualen),
så menyen og bunnteksten er like overalt. Endrer du noe her, kjør begge skriptene på nytt.
"""
import html
import json

BASE_URL = "https://trax-dogtracking.no/"
APP_STORE = "https://apps.apple.com/app/id6758005408"
GOOGLE_PLAY = "https://play.google.com/store/apps/details?id=tillerflatendigital.trax.android"
EPOST = "post@trax-dogtracking.no"
VERSJON = "3"  # øk når stil.css eller side.js endres, så nettlesere henter ny fil

# Adressene til hver side på hvert språk. Personvern og manual har adressene de alltid har hatt (App Store lenker dit).
SIDER = {
    "nb": dict(forside="", funksjoner="funksjoner/", nytt="nytt/", hjelp="hjelp/", personvern="personvern/", manual="manual/"),
    "sv": dict(forside="sv/", funksjoner="sv/funktioner/", nytt="sv/nyheter/", hjelp="sv/hjalp/", personvern="sv/integritet/", manual="sv/manual/"),
    "en": dict(forside="en/", funksjoner="en/features/", nytt="en/whats-new/", hjelp="en/help/", personvern="en/privacy/", manual="en/manual/"),
    "de": dict(forside="de/", funksjoner="de/funktionen/", nytt="de/neu/", hjelp="de/hilfe/", personvern="de/datenschutz/", manual="de/manual/"),
}

SPRAK = [
    dict(code="nb", navn="Norsk", locale="nb_NO", og="nb",
         nav=dict(funksjoner="Funksjoner", nytt="Nytt", hjelp="Hjelp", last_ned="Last ned", meny="Meny", velg_sprak="Velg språk", hopp="Hopp til innholdet", hjem="Trax, til forsiden"),
         bunn=dict(tekst="Sportrening med hund for iPhone og Android.", produkt="Produkt", hjelp="Hjelp", sprak="Språk",
                   funksjoner="Funksjoner", nytt="Nytt i Trax", last_ned="Last ned", manual="Brukermanual", support="Support og spørsmål",
                   arrangorer="For arrangører", personvern="Personvern", utvikler="Utviklet av Tillerflaten Digital · Org.nr. 938 657 742",
                   logo_alt="Logo for Tillerflaten Digital"),
         as_alt="Last ned fra App Store", gp_alt="Tilgjengelig på Google Play", arr_anker="arrangorer"),
    dict(code="sv", navn="Svenska", locale="sv_SE", og="sv",
         nav=dict(funksjoner="Funktioner", nytt="Nyheter", hjelp="Hjälp", last_ned="Ladda ned", meny="Meny", velg_sprak="Välj språk", hopp="Hoppa till innehållet", hjem="Trax, till startsidan"),
         bunn=dict(tekst="Spårträning med hund för iPhone och Android.", produkt="Produkt", hjelp="Hjälp", sprak="Språk",
                   funksjoner="Funktioner", nytt="Nyheter i Trax", last_ned="Ladda ned", manual="Användarmanual", support="Support och frågor",
                   arrangorer="För arrangörer", personvern="Integritet", utvikler="Utvecklad av Tillerflaten Digital · Org.nr. 938 657 742",
                   logo_alt="Logotyp för Tillerflaten Digital"),
         as_alt="Hämta i App Store", gp_alt="Ladda ned på Google Play", arr_anker="arrangorer"),
    dict(code="en", navn="English", locale="en_US", og="en",
         nav=dict(funksjoner="Features", nytt="What’s new", hjelp="Help", last_ned="Download", meny="Menu", velg_sprak="Choose language", hopp="Skip to content", hjem="Trax, to the front page"),
         bunn=dict(tekst="Tracking training with your dog, for iPhone and Android.", produkt="Product", hjelp="Help", sprak="Language",
                   funksjoner="Features", nytt="What’s new in Trax", last_ned="Download", manual="User manual", support="Support and questions",
                   arrangorer="For organisers", personvern="Privacy", utvikler="Developed by Tillerflaten Digital · Org. no. 938 657 742",
                   logo_alt="Tillerflaten Digital logo"),
         as_alt="Download on the App Store", gp_alt="Get it on Google Play", arr_anker="organisers"),
    dict(code="de", navn="Deutsch", locale="de_DE", og="en",  # tysk delebilde finnes ikke ennå
         nav=dict(funksjoner="Funktionen", nytt="Neu", hjelp="Hilfe", last_ned="Laden", meny="Menü", velg_sprak="Sprache wählen", hopp="Zum Inhalt springen", hjem="Trax, zur Startseite"),
         bunn=dict(tekst="Fährtenarbeit mit Hund, für iPhone und Android.", produkt="Produkt", hjelp="Hilfe", sprak="Sprache",
                   funksjoner="Funktionen", nytt="Neu in Trax", last_ned="Laden", manual="Handbuch", support="Support und Fragen",
                   arrangorer="Für Veranstalter", personvern="Datenschutz", utvikler="Entwickelt von Tillerflaten Digital · Org.-Nr. 938 657 742",
                   logo_alt="Logo von Tillerflaten Digital"),
         as_alt="Laden im App Store", gp_alt="Jetzt bei Google Play", arr_anker="veranstalter"),
]
SPRAK_BY = {s["code"]: s for s in SPRAK}

GLOBUS = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
          '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def opp(sti):
    """Relativ vei fra siden på `sti` (f.eks. "sv/funktioner/") til roten."""
    return "../" * sti.count("/")


def head(l, side, tittel, beskrivelse, up, ekstra="", og_type="website", jsonld=None, app_banner=False):
    """<head> med canonical, hreflang for alle språk, delebilde og felles stil."""
    sti = SIDER[l["code"]][side]
    alts = "\n".join(f'<link rel="alternate" hreflang="{o["code"]}" href="{BASE_URL}{SIDER[o["code"]][side]}">' for o in SPRAK)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{BASE_URL}{SIDER["en"][side]}">'
    loc = "\n".join(f'<meta property="og:locale:alternate" content="{o["locale"]}">' for o in SPRAK if o is not l)
    ld = f'\n<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    banner = '\n<meta name="apple-itunes-app" content="app-id=6758005408">' if app_banner else ""
    return f"""<!doctype html>
<html lang="{l["code"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{banner}
<meta name="description" content="{esc(beskrivelse)}">
<title>{esc(tittel)}</title>
<link rel="canonical" href="{BASE_URL}{sti}">
{alts}
<link rel="icon" type="image/png" sizes="32x32" href="{up}img/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{up}img/icon-192.png">
<link rel="apple-touch-icon" href="{up}img/apple-touch-icon.png">
<link rel="preload" href="{up}fonter/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}fonter/inter-tight-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}stil.css?v={VERSJON}">
<meta name="theme-color" content="#f7f8f5" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111713" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{l["locale"]}">
{loc}
<meta property="og:site_name" content="Trax">
<meta property="og:title" content="{esc(tittel)}">
<meta property="og:description" content="{esc(beskrivelse)}">
<meta property="og:url" content="{BASE_URL}{sti}">
<meta property="og:image" content="{BASE_URL}img/og-image-{l["og"]}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">{ld}{ekstra}
</head>"""


def sprakvalg(l, side, up, klasse="sprak"):
    lis = "\n".join(
        f'      <li><a href="{up}{SIDER[o["code"]][side]}" hreflang="{o["code"]}" lang="{o["code"]}"'
        + (' aria-current="page"' if o is l else "") + f'>{o["navn"]}</a></li>' for o in SPRAK)
    return (f'  <details class="{klasse}">\n'
            f'    <summary aria-label="{l["nav"]["velg_sprak"]}">{GLOBUS}{l["code"].upper()}</summary>\n'
            f'    <ul>\n{lis}\n    </ul>\n  </details>')


def nav(l, side, up):
    s, n = SIDER[l["code"]], l["nav"]

    def lenke(key, tekst):
        cur = ' aria-current="page"' if key == side else ""
        return f'<a href="{up}{s[key]}"{cur}>{tekst}</a>'
    ned = f'{up}{s["forside"]}#last-ned'
    sm = "".join(f'<a href="{up}{SIDER[o["code"]][side]}" hreflang="{o["code"]}" lang="{o["code"]}"' + (' aria-current="page"' if o is l else "") + f'>{o["navn"]}</a>' for o in SPRAK)
    return f"""<a class="hopp" href="#innhold">{n["hopp"]}</a>
<header class="topp"><div class="wrap"><nav class="bar" aria-label="{n["meny"]}">
  <a class="merke" href="{up}{s["forside"]}" aria-label="{n["hjem"]}"><img src="{up}img/icon-192.png" width="32" height="32" alt="">Trax</a>
  <ul class="lenker">
    <li>{lenke("funksjoner", n["funksjoner"])}</li>
    <li>{lenke("nytt", n["nytt"])}</li>
    <li>{lenke("hjelp", n["hjelp"])}</li>
  </ul>
{sprakvalg(l, side, up)}
  <a class="knapp" href="{ned}" data-last-ned>{n["last_ned"]}</a>
  <details class="meny">
    <summary aria-label="{n["meny"]}"><span></span></summary>
    <div class="panel">
      {lenke("funksjoner", n["funksjoner"])}
      {lenke("nytt", n["nytt"])}
      {lenke("hjelp", n["hjelp"])}
      {lenke("manual", l["bunn"]["manual"])}
      <hr>
      <div class="sm" lang="">{sm}</div>
    </div>
  </details>
</nav></div></header>"""


def butikker(l, up, hoyde=52):
    b = round(hoyde * 120 / 40), round(hoyde * 135 / 40)
    return (f'<div class="butikker">'
            f'<a href="{APP_STORE}"><img src="{up}img/app-store-{l["code"]}.svg" width="{b[0]}" height="{hoyde}" alt="{l["as_alt"]}"></a>'
            f'<a href="{GOOGLE_PLAY}"><img src="{up}img/google-play-{l["code"]}.svg" width="{b[1]}" height="{hoyde}" alt="{l["gp_alt"]}"></a>'
            f'</div>')


def bunn(l, side, up, aar):
    s, b = SIDER[l["code"]], l["bunn"]

    def lenke(href, tekst, key=None):
        cur = ' aria-current="page"' if key and key == side else ""
        return f'<li><a href="{href}"{cur}>{tekst}</a></li>'
    langs = "".join(lenke(f'{up}{SIDER[o["code"]][side]}', f'<span lang="{o["code"]}">{o["navn"]}</span>') for o in SPRAK)
    return f"""<footer class="bunn"><div class="wrap">
  <div class="rad">
    <div>
      <a class="merke" href="{up}{s["forside"]}"><img src="{up}img/icon-192.png" width="32" height="32" alt="">Trax</a>
      <p>{b["tekst"]}</p>
      {butikker(l, up, 40)}
    </div>
    <div><h2>{b["produkt"]}</h2><ul>{lenke(up + s["funksjoner"], b["funksjoner"], "funksjoner")}{lenke(up + s["nytt"], b["nytt"], "nytt")}{lenke(up + s["forside"] + "#last-ned", b["last_ned"])}</ul></div>
    <div id="support"><h2>{b["hjelp"]}</h2><ul>{lenke(up + s["manual"], b["manual"], "manual")}{lenke(up + s["hjelp"], b["support"], "hjelp")}{lenke(up + s["hjelp"] + "#" + l["arr_anker"], b["arrangorer"])}{lenke("mailto:" + EPOST, EPOST)}</ul></div>
    <div><h2>{b["sprak"]}</h2><ul>{langs}</ul></div>
  </div>
  <div class="nederst">
    <span class="utvikler"><img src="{up}img/tillerflaten-digital.png" width="24" height="24" alt="{b["logo_alt"]}">© {aar} {b["utvikler"]}</span>
    <a href="{up}{s["personvern"]}">{b["personvern"]}</a>
  </div>
</div></footer>
<script src="{up}side.js?v={VERSJON}" defer></script>
<script data-goatcounter="https://trax-dogtracking.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>"""
