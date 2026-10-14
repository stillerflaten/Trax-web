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

De tre sidene har samme stil. Endrer du tekst eller utseende på én av dem, gjør det samme på de andre. Forsiden har `<body class="forside">` med bred layout og flater; reglene for den står samlet nederst i stilen. Personvernsidene og manualen bruker samme stil uten klassen, som lesesider. Ankeret `#personvern`/`#integritet`/`#privacy` finnes fortsatt på forsiden (kort sammendrag med lenke) i tilfelle skript er slått av.

Språkvelgeren i menyen (`<details class="lang">`) har én linje per språk. Nytt språk: lag `xx/index.html`, legg til en linje i språkvelgeren, bunnteksten og `hreflang`/`og:locale:alternate` på alle sidene.

## Skjermbildegalleri

Forsiden har et sveipbart galleri med fem skjermbilder (`img/galleri/galleri-<språk>-<nr>-<navn>.webp`, 640 × 999). Bildene er laget fra skjermbildene i det nye designet (`appstore-bilder/kilde/nytt-design/<språk>/`, fra skjermbilde-workflowen i app-repoet), satt i en telefon på samme bakgrunn som App Store-bildene, uten piler og merkelapper. Teksten under hvert bilde står i HTML-en. Toppbildet på forsiden er bilde 5. Før lansering står det «Ny versjon, kommer snart» på toppbildet og en setning over galleriet; begge skjules automatisk fra lanseringsdatoen. `galleri.js` legger til piler og prikker og er felles for alle språk. Nytt språk: lag fem nye bilder og kopier `<div class="galleri">` med oversatt tekst.

## Brukermanual

Brukermanualen ligger på `/manual/`, `/sv/manual/` og `/en/manual/`, med bilder i `img/manual/`. Den lages automatisk fra manualen i appen (`ManualContent` i `Trax/UserManualView.swift` og `manual-*`-bildene i app-repoet), så nettmanualen og appen sier det samme. Ikke rediger manualsidene for hånd.

Når manualen i appen er endret, kjør fra roten av dette repoet (med app-repoet klonet ved siden av):

```
python3 verktoy/lag-manual.py ../Trax
```

Skriptet henter stilen fra `index.html`, så endringer i utseendet på forsiden følger med neste gang det kjøres. Nytt språk: legg til en linje i `LANGS` øverst i skriptet.

## App Store-knapp og pris

Toppen viser «Snart i App Store» til lanseringsdatoen er satt. Sett datoen i `data-lansering` på `<body>` i alle tre sidene (format `ÅÅÅÅ-MM-DD`):

- Fra datoen vises App Store-merket (`img/app-store-<språk>.svg`, Apples offisielle merke) og introduksjonsprisen.
- Introprisen er 129 kr (norsk), 129 kr (svensk) og $9.99 (engelsk). Sju dager etter datoen bytter alle tre sidene til ordinær pris: 149 kr, 149 kr og $11.99.

Merket vises både øverst og i bunnteksten, og knappen «App Store» i menyen går til appen fra datoen (før det til toppen). Lenken går til `https://apps.apple.com/app/id6758005408`.

## Delebilder

Når lenken deles (Facebook, Messenger, iMessage), vises `img/og-image-<språk>.png` (1200 × 630). Manualsidene bruker samme bilder (satt i `verktoy/lag-manual.py`).

## Om Trax

Seksjonen «Laget av en hundefører» (`#om`, engelsk `#about`) viser foreløpig et bilde av Quatro (`img/quatro-hode.jpg`, 480 × 480, vist i 160 × 160 (120 på mobil), uten metadata). Når et bilde av Silje og Quatro finnes, bytt `src` og `alt` på alle tre sidene; stilen fyller ruten.

Seksjonen om delebildet (`#deling`, svensk `#delning`, engelsk `#sharing`) viser `img/delebilde.webp` (680 × 1209, laget fra `appstore-bilder/kilde/egne/delebilde-nb.jpg`). Merket «Kommer i neste versjon» har klassen `ny-tekst` og skjules automatisk når `data-lansering` er satt. Bildet har norske tekster på alle tre språkene; bytt til egne svenske og engelske versjoner når de finnes.

## Bevegelse og sporlinja

`forside.js` (felles for alle språk) gir forsiden bevegelse: delene i hver seksjon glir inn når de kommer til syne, telefonen i toppen synker litt når du scroller, og sporlinja fortsetter fra toppen og nedover siden. Hver seksjon er en gjenstand (1–4) som får en grønn hake når sporet når den; siste gjenstand er App Store-knappen nederst. På skjermer fra 1240 px går linja i margen til høyre, på smalere skjermer vises gjenstandene som prikker foran overskriftene. Gjenstandene settes i `MAAL` øverst i skriptet. Med «Reduser bevegelse» står alt stille, linja er tegnet ferdig og alle gjenstandene er funnet.
