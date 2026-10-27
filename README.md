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

Appen er på tysk fra versjon 2.1 (ute 19. oktober 2026), og 2.1-beskjedene på den tyske siden og i manualen er fjernet. Den tyske siden har egne tyske skjermbilder i galleriet og Apples tyske App Store-merke (`img/app-store-de.svg`). Delebildet er fortsatt det engelske (`og="en"` i `LANGS` i `verktoy/lag-manual.py` og `og:image` i `de/index.html`); lag `img/og-image-de.png` og bytt begge stedene når det finnes. Lanseringsvideoen for 2.0 er også den engelske.

Språksidene har samme stil. Endrer du tekst eller utseende på én av dem, gjør det samme på de andre. Forsiden har `<body class="forside">` med bred layout og flater; reglene for den står samlet nederst i stilen. Personvernsidene og manualen bruker samme stil uten klassen, som lesesider. Ankeret `#personvern`/`#integritet`/`#privacy` finnes fortsatt på forsiden (kort sammendrag med lenke) i tilfelle skript er slått av.

Språkvelgeren i menyen (`<details class="lang">`) har én linje per språk. Nytt språk: lag `xx/index.html`, legg til en linje i språkvelgeren, bunnteksten og `hreflang`/`og:locale:alternate` på alle sidene.

## Skjermbildegalleri

Forsiden har et sveipbart galleri med sju skjermbilder: hjemskjerm, detaljkort, valg av øvelse (sportypene), feltsøk, blodspor, kryss-spor og nattmodus (`img/galleri/galleri-<språk>-<nr>-<navn>.webp`, 640 × 999). Bildene er laget fra skjermbildene i det nye designet (`appstore-bilder/kilde/nytt-design/<språk>/`, fra skjermbilde-workflowen i app-repoet), satt i en telefon på samme bakgrunn som App Store-bildene, uten piler og merkelapper. Teksten under hvert bilde står i HTML-en. Toppbildet på forsiden er bilde 2 (detaljkortet). Bildene er fra versjon 2.0. De tyske bildene (`galleri-de-*`) er laget ved å bytte skjermen i de engelske bildene med de tyske skjermbildene fra `appstore-bilder/kilde/nytt-design/de/` (samme skjermbilder som de andre språkene, skalert til 418 px bredde og plassert 111 px fra venstre og 59 px fra toppen). `galleri.js` legger til piler og prikker og er felles for alle språk. Nytt språk: lag sju nye bilder og kopier `<div class="galleri">` med oversatt tekst.

Over galleriet er en bryter «iPhone | Android» (`<fieldset class="g-os">` med to radioknapper). Galleriet har to lister, `<ul class="g-liste" data-os="ios">` og `data-os="android"`, og bryteren viser den ene. iPhone er valgt fra start, men på Android-telefoner velger `galleri.js` Android. Uten JS bytter CSS-en (`:has()`) listene. Android-bildene (`img/galleri/galleri-android-<språk>-<nr>-<navn>.webp`, 640 × 999, åtte per språk) er laget fra Silje sine norske Android-skjermbilder (`markedsforing/android-play/kilde/shots/` i prosjektmappen). For engelsk, svensk og tysk er teksten i skjermbildene byttet ut med appens egne oversettelser (skriptene ligger i `nettside/android-galleri/oversett/` i prosjektmappen); bytt dem gjerne ut med ekte skjermbilder på de språkene når det finnes. Galleribildene er laget med `nettside/android-galleri/lag-android.py` i prosjektmappen: den legger en Android-telefon over iPhonen i `galleri-nb-1-hjem.webp`, så bakgrunnen blir lik.

## Lanseringsvideo

Lanseringsvideoen for 2.0 (`img/video/trax-2-<nb|sv|en>.mp4` med plakatbilde, og `film.js`) ble tatt av forsiden 25. oktober 2026 sammen med «Nytt i versjon 2.0». Filene ligger igjen i repoet hvis de skal brukes igjen. `film.js` spiller av alt med klassen `.v2-film`.

## Brukermanual

Brukermanualen ligger på `/manual/`, `/sv/manual/`, `/en/manual/` og `/de/manual/`, med bilder i `img/manual/`. Den lages automatisk fra manualen i appen (`ManualContent` i `Trax/UserManualView.swift` og `manual-*`-bildene i app-repoet), så nettmanualen og appen sier det samme. Ikke rediger manualsidene for hånd.

Når manualen i appen er endret, kjør fra roten av dette repoet (med app-repoet klonet ved siden av):

```
python3 verktoy/lag-manual.py ../Trax
# eller bare noen språk, f.eks.:
python3 verktoy/lag-manual.py ../Trax de
```

Kjør skriptet mot den app-versjonen som er i App Store (eller er sendt inn), ikke uten videre mot `main`: `main` i app-repoet kan ha endringer som ikke er ute ennå, og da beskriver nettmanualen ting brukerne ikke har. Derfor ble «Kommer i v. 2.1»-merkene fjernet for hånd i manualsidene da 2.1 kom ut, i stedet for å kjøre skriptet på nytt.

Nettmanualen er nå laget fra versjon 2.5.1 (bygg 45), fra app-main `7c8195f` etter Trax PR #307 (runde 8 i #108: manualtekst og nye skjermbilder for alt nytt i 2.4 og 2.5). Main har ingen appendringer etter bygg 45 (`c8ce604`) utover personvernteksten om stedsnavn (PR #306) og manualen, så teksten passer appen som er ute. Slik gjør du det for en bestemt versjon: `git -C ../Trax worktree add ../Trax-2.5.1 44518bf`, og kjør `python3 verktoy/lag-manual.py ../Trax-2.5.1`. Neste gang brukes commiten neste bygg ble arkivert fra.

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

## Versjonsseksjoner

Forsiden har én seksjon for siste versjon (`class="v2"`, nå «Nytt i versjon 2.5», `#versjon-2-5`, svensk, engelsk og tysk `#version-2-5`), rett etter funksjonene. Når en ny versjon kommer, flyttes det viktigste fra forrige versjonsseksjon inn i funksjonslisten (`#funksjoner`), og den gamle seksjonen fjernes. Det ble gjort for 2.2 (23. oktober 2026), 2.0 (25. oktober 2026) og 2.3 (27. oktober 2026). Feltsøk og arealsøk, vind og vær, vurdering, redigering, flere spor i én PDF, sikkerhetskopi, IGP-nivå og mal, markering og treningsmomenter står nå i funksjonslisten. 2.4 og 2.5 kom aldri ut i App Store; 2.5.1 (bygg 45) har alt, og siden kaller den «2.5».
