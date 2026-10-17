# Trax

Nettside for iOS-appen Trax: forside med support, egne sider for personvernerklæringen, og brukermanual.

Norsk (`index.html`):
- Support: `/#support`
- Personvern: `/personvern/` (gamle `/#personvern` sendes dit, App Store lenker dit)

Svensk (`sv/index.html`):
- Support: `/sv/#support`
- Integritet: `/sv/integritet/` (gamle `/sv/#integritet` sendes dit)

Engelsk (`en/index.html`):
- Support: `/en/#support`
- Privacy: `/en/privacy/` (gamle `/en/#privacy` sendes dit)

Tysk (`de/`):
- Forside: `/de/`
- Datenschutz: `/de/datenschutz/`

Den tyske siden sier tydelig at appen kommer på tysk med versjon 2.1 (boksen `.de-hinweis` i toppen, en linje under App Store-merket og et avsnitt under versjon 2.0). Til da bruker den de engelske skjermbildene (App Store-merket er Apples tyske, `img/app-store-de.svg`), og den tyske manualen (`/de/manual/`, «Handbuch») viser appen på tysk med en beskjed om at appen er på engelsk til 2.1. Når appen er på tysk: lag tyske skjermbilder til galleriet, fjern `note` og `og` for tysk i `LANGS` i `verktoy/lag-manual.py` (lag `img/og-image-de.png` først), kjør skriptet og fjern 2.1-beskjedene.

Språksidene har samme stil. Endrer du tekst eller utseende på én av dem, gjør det samme på de andre. Forsiden har `<body class="forside">` med bred layout og flater; reglene for den står samlet nederst i stilen. Personvernsidene og manualen bruker samme stil uten klassen, som lesesider. Ankeret `#personvern`/`#integritet`/`#privacy` finnes fortsatt på forsiden (kort sammendrag med lenke) i tilfelle skript er slått av.

Språkvelgeren i menyen (`<details class="lang">`) har én linje per språk. Nytt språk: lag `xx/index.html`, legg til en linje i språkvelgeren, bunnteksten og `hreflang`/`og:locale:alternate` på alle sidene.

## Skjermbildegalleri

Forsiden har et sveipbart galleri med sju skjermbilder: hjemskjerm, detaljkort, valg av øvelse (sportypene), feltsøk, blodspor, kryss-spor og nattmodus (`img/galleri/galleri-<språk>-<nr>-<navn>.webp`, 640 × 999). Bildene er laget fra skjermbildene i det nye designet (`appstore-bilder/kilde/nytt-design/<språk>/`, fra skjermbilde-workflowen i app-repoet), satt i en telefon på samme bakgrunn som App Store-bildene, uten piler og merkelapper. Teksten under hvert bilde står i HTML-en. Toppbildet på forsiden er bilde 2 (detaljkortet). Bildene er fra versjon 2.0. På den tyske siden står en setning over galleriet (`.ny-tekst`) om at bildene er på engelsk til 2.1. `galleri.js` legger til piler og prikker og er felles for alle språk. Nytt språk: lag sju nye bilder og kopier `<div class="galleri">` med oversatt tekst.

## Lanseringsvideo

I «Nytt i versjon 2.0» på forsiden står lanseringsvideoen for 2.0 (`<div class="v2-film">`), én per språk: `img/video/trax-2-<nb|sv|en>.mp4` (720 × 1280, 30 fps, ca. 3 MB) med plakatbilde `.jpg`. Den tyske siden bruker den engelske til appen er på tysk. `film.js` spiller videoen lydløst i loop mens den er synlig, og knappen slår på lyd fra starten. Uten skript vises vanlige videokontroller, og med «Reduser bevegelse» starter den ikke av seg selv. Videoene lages i videoprosjektet (`video/trax-2-lansering/kilde/` i prosjektmappa, `scripts/web_version.sh`).

## Brukermanual

Brukermanualen ligger på `/manual/`, `/sv/manual/`, `/en/manual/` og `/de/manual/`, med bilder i `img/manual/`. Den lages automatisk fra manualen i appen (`ManualContent` i `Trax/UserManualView.swift` og `manual-*`-bildene i app-repoet), så nettmanualen og appen sier det samme. Ikke rediger manualsidene for hånd.

Når manualen i appen er endret, kjør fra roten av dette repoet (med app-repoet klonet ved siden av):

```
python3 verktoy/lag-manual.py ../Trax
# eller bare noen språk, f.eks.:
python3 verktoy/lag-manual.py ../Trax de
```

Skriptet henter stilen fra `index.html`, så endringer i utseendet på forsiden følger med neste gang det kjøres. Nytt språk: legg til en linje i `LANGS` øverst i skriptet.

## App Store-knapp og pris

Lanseringsdatoen står i `data-lansering` på `<body>` i alle tre sidene (format `ÅÅÅÅ-MM-DD`), nå `2026-10-16`. Uten dato, eller før datoen, vises «Snart i App Store».

Forsidene har også Smart App Banner (`<meta name="apple-itunes-app" content="app-id=6758005408">`), som viser en «Åpne/Hent»-stripe øverst i Safari på iPhone.

Fra datoen:

- Fra datoen vises App Store-merket (`img/app-store-<språk>.svg`, Apples offisielle merke) og introduksjonsprisen.
- Introprisen er 129 kr (norsk), 129 kr (svensk), $9.99 (engelsk) og 9,99 € (tysk). Sju dager etter datoen bytter alle sidene til ordinær pris: 149 kr, 149 kr, $11.99 og 12,99 €.

Merket vises både øverst og i bunnteksten, og knappen «App Store» i menyen går til appen fra datoen (før det til toppen). Lenken går til `https://apps.apple.com/app/id6758005408`.

## Delebilder

Når lenken deles (Facebook, Messenger, iMessage), vises `img/og-image-<språk>.png` (1200 × 630). Manualsidene bruker samme bilder (satt i `verktoy/lag-manual.py`).

## Om Trax

Seksjonen «Laget av en hundefører» (`#om`, engelsk `#about`) viser foreløpig et bilde av Quatro (`img/quatro-hode.jpg`, 480 × 480, vist i 160 × 160 (120 på mobil), uten metadata). Når et bilde av Silje og Quatro finnes, bytt `src` og `alt` på alle tre sidene; stilen fyller ruten.

Seksjonen om delebildet (`#deling`, svensk `#delning`, engelsk `#sharing`) viser `img/delebilde.webp` (680 × 1209, laget fra `appstore-bilder/kilde/egne/delebilde-nb.jpg`). Bildet har norske tekster på alle tre språkene; bytt til egne svenske og engelske versjoner når de finnes.

Seksjonen om å sende spor til en annen Trax-bruker (`#send-spor`, svensk `#skicka-spar`, engelsk `#send-track`, tysk `#fahrte-senden` med det engelske bildet) står rett etter delebildet og viser infobildet `img/send-spor-<språk>.webp` (800 × 1000). Det er Instagram-innlegget fra `markedsforing/del-spor/` i prosjektmappen, skalert ned; lag det på nytt der (`kilde/page.html`) og konverter hvis appen endres.

## Bevegelse og sporlinja

`forside.js` (felles for alle språk) gir forsiden bevegelse: delene i hver seksjon glir inn når de kommer til syne, telefonen i toppen synker litt når du scroller, og sporlinja fortsetter fra toppen og nedover siden. Skjermbildegalleriet glir ikke inn, fordi bevegelse inni den vannrette rullelista hakket på iPhone. Hver seksjon er en gjenstand (1–5) som får en grønn hake når sporet når den; siste gjenstand er App Store-knappen nederst. På skjermer fra 1240 px går linja i margen til høyre, på smalere skjermer vises gjenstandene som prikker foran overskriftene. Gjenstandene settes i `MAAL` øverst i skriptet. Med «Reduser bevegelse» står alt stille, linja er tegnet ferdig og alle gjenstandene er funnet.

## Versjon 2.0

Seksjonen «Nytt i versjon 2.0» (`#versjon-2`, svensk, tysk og engelsk `#version-2`) står mellom funksjonene og delebildet. Den sier at 2.0 er ute som gratis oppdatering, og lister det nye som ikke står i funksjonslisten over. «Kommer snart»-tekstene for 2.0 ble fjernet da 2.0 kom ut (17. oktober 2026). Den tyske siden har i tillegg et avsnitt om at tysk kommer i 2.1.
