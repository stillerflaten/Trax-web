# Trax

Nettside for iOS-appen Trax: support og personvernerklæring.

Norsk (`index.html`):
- Support: `/#support`
- Personvern: `/#personvern`

Svensk (`sv/index.html`):
- Support: `/sv/#support`
- Integritet: `/sv/#integritet`

Engelsk (`en/index.html`):
- Support: `/en/#support`
- Privacy: `/en/#privacy`

De tre sidene har samme stil. Endrer du tekst eller utseende på én av dem, gjør det samme på de andre.

Språkvelgeren i menyen (`<details class="lang">`) har én linje per språk. Nytt språk: lag `xx/index.html`, legg til en linje i språkvelgeren, bunnteksten og `hreflang`/`og:locale:alternate` på alle sidene.

## Skjermbildegalleri

Forsiden har et sveipbart galleri med fem skjermbilder (`img/galleri/galleri-<språk>-<nr>-<navn>.webp`, 640 × 999). Bildene er App Store-bildene uten overskrift, laget fra `appstore-bilder/kilde/shot.html` i prosjektmappa, og teksten under hvert bilde står i HTML-en. `galleri.js` legger til piler og prikker og er felles for alle språk. Nytt språk: lag fem nye bilder og kopier `<div class="galleri">` med oversatt tekst.

## Brukermanual

Brukermanualen ligger på `/manual/`, `/sv/manual/` og `/en/manual/`, med bilder i `img/manual/`. Den lages automatisk fra manualen i appen (`ManualContent` i `Trax/UserManualView.swift` og `manual-*`-bildene i app-repoet), så nettmanualen og appen sier det samme. Ikke rediger manualsidene for hånd.

Når manualen i appen er endret, kjør fra roten av dette repoet (med app-repoet klonet ved siden av):

```
python3 verktoy/lag-manual.py ../Trax
```

Skriptet henter stilen fra `index.html`, så endringer i utseendet på forsiden følger med neste gang det kjøres. Nytt språk: legg til en linje i `LANGS` øverst i skriptet.
