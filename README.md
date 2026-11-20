# Trax

Nettsiden for appen Trax (iPhone og Android): https://trax-dogtracking.no. Vanlige HTML-filer på GitHub Pages, uten rammeverk og uten byggesteg på serveren.

## Sidene

| Side | Norsk | Svensk | Engelsk | Tysk |
|---|---|---|---|---|
| Forside | `/` | `/sv/` | `/en/` | `/de/` |
| Funksjoner | `/funksjoner/` | `/sv/funktioner/` | `/en/features/` | `/de/funktionen/` |
| Nytt | `/nytt/` | `/sv/nyheter/` | `/en/whats-new/` | `/de/neu/` |
| Hjelp og support | `/hjelp/` | `/sv/hjalp/` | `/en/help/` | `/de/hilfe/` |
| Personvern | `/personvern/` | `/sv/integritet/` | `/en/privacy/` | `/de/datenschutz/` |
| Brukermanual | `/manual/` | `/sv/manual/` | `/en/manual/` | `/de/manual/` |

Personvern- og manualadressene er de samme som før (App Store og Google Play lenker dit).

**Gamle adresser:** App Store-oppføringen lenker til `/#support`. Forsiden har en liste over gamle ankre i `data-gamle` på `<body>`, og `side.js` sender dem videre: `/#support` → `/hjelp/`, `/#personvern` → `/personvern/`, `/#arrangorer` → `/hjelp/#arrangorer`, `/#versjon-2-5` → `/nytt/#versjon-2-5`, `/#deling` → `/funksjoner/#deling` osv., med de tilsvarende ankrene på de andre språkene. Uten JavaScript ligger `id="support"` på Hjelp-kolonnen i bunnteksten, så lenken havner der.

## Slik endrer du siden

Forsiden, Funksjoner, Nytt og Hjelp **lages av et skript**. Ikke rediger HTML-filene for hånd; endre tekstene og kjør skriptet:

```
python3 verktoy/lag-sider.py
```

- `verktoy/tekster.py`: alle tekster på de fire sidene, på alle fire språk. Her endrer du tekst.
- `verktoy/felles.py`: meny, bunntekst, `<head>` (beskrivelse, `hreflang`, delebilde), adressene til sidene og butikklenkene. Brukes av både `lag-sider.py` og `lag-manual.py`, så menyen er lik overalt.
- `verktoy/galleri-<språk>.html`: skjermbildegalleriet (iPhone/Android) på Funksjoner.
- `stil.css`: utseendet på alle sider. Øk `VERSJON` i `felles.py` når `stil.css` eller `side.js` endres, og kjør skriptene, så henter nettleserne de nye filene.
- `side.js`: gamle ankre, «Last ned» som går rett til riktig butikk på iPhone/Android, fanene i «Slik fungerer det», myk inngang (av med «Reduser bevegelse») og lukking av menyene. Siden virker uten skriptet.
- `galleri.js`: piler og prikker i skjermbildegalleriet.

Skriptet lager også `sitemap.xml` og `robots.txt`. Det kan kjøres så mange ganger du vil og gir samme resultat.

**Personvernsidene** skrives fortsatt for hånd: endre teksten mellom `<main …>` og `</main>` i `personvern/index.html` (og de tre andre språkene), og kjør `lag-sider.py`, så får siden riktig meny og bunntekst.

**Manualen** lages fra manualen i appen, se under.

## Skrifter og bilder

- Skriftene Inter og Inter Tight ligger i `fonter/` (latinske tegn, woff2). De lastes fra vår egen side, ikke fra Google Fonts, så besøkende ikke sendes til Google. Lisens: SIL Open Font License 1.1, © The Inter Project Authors.
- `img/app/<språk>/<navn>.webp` (600 × 1304): skjermbildene på forsiden og Nytt. De er laget fra manualbildene i app-repoet (`Trax/Assets.xcassets/manual-<navn>[-sv|-en|-de]`), så de viser appen slik den er nå. Når appen endres, lag dem på nytt fra de samme bildene.
- `img/quatro.webp` (720 × 720): bildet i «Om»-delen, uten metadata.
- `img/delebilde.webp`: delebildet på Funksjoner (ekte bilde laget av Trax).
- `img/galleri/`: galleriet på Funksjoner (iPhone sju bilder, Android åtte bilder per språk).
- `img/og-image-<språk>.png`: delebildet når lenken deles. Tysk bruker det engelske til et tysk finnes (`og="en"` i `felles.py`).
- Ubrukte bilder fra den gamle forsiden ligger igjen (`img/quatro-hode.jpg`, `img/send-spor-*.webp`, `img/video/` og `film.js`) i tilfelle de skal brukes igjen.

## Regler for tekstene

- Skriv «jeg/meg», ikke «vi». Trax er et enkeltpersonprosjekt.
- Norsk: «spor», ikke «gange/gå» om å spore med hunden.
- Ikke nevn hundens navn eller rase, politiet, tjenesten eller at Silje er hundefører.
- Funksjoner som bare finnes på iPhone (nå Sporplaner i 2.6) merkes med `<span class="ios">iPhone</span>`.
- Prisen står én gang for begge butikkene: 149 kr (norsk og svensk), $11.99 (engelsk), 12,99 € (tysk).

## Ny versjon av appen

Legg en ny versjon øverst i `versjoner` under `nytt` i `tekster.py` (med `id="versjon-x-y"` og to skjermbilder), og oppdater «Nytt»-pillen øverst på forsiden (`nyhet`). Det viktigste fra eldre versjoner flyttes inn i funksjonslisten (`funksjoner` → `grupper`).

## Brukermanual

Brukermanualen lages automatisk fra manualen i appen (`ManualContent` i `Trax/UserManualView.swift` og `manual-*`-bildene i app-repoet), så nettmanualen og appen sier det samme. Ikke rediger manualsidene for hånd.

Når manualen i appen er endret, kjør fra roten av dette repoet (med app-repoet klonet ved siden av):

```
python3 verktoy/lag-manual.py ../Trax
# eller bare noen språk, f.eks.:
python3 verktoy/lag-manual.py ../Trax de
```

Kjør skriptet mot den app-versjonen som er i App Store (eller er sendt inn), ikke uten videre mot `main`: `main` i app-repoet kan ha endringer som ikke er ute ennå. For en bestemt versjon: `git -C ../Trax worktree add ../Trax-x.y <commit>` og `python3 verktoy/lag-manual.py ../Trax-x.y`. Nettmanualen er nå laget fra versjon 2.6 (app-main `e58966d`, Trax PR #315).

Manualen bruker `stil.css` og menyen/bunnteksten fra `felles.py`; de egne reglene (innholdsliste, nummererte steg, tips, skjermbilder) står i `MANUAL_CSS` i skriptet. Nytt språk: legg til en linje i `LANGS` i skriptet og i `SPRAK`/`SIDER` i `felles.py`.

## Nytt språk på nettsiden

Legg språket til i `SPRAK` og `SIDER` i `felles.py`, legg tekstene inn i `tekster.py`, lag `verktoy/galleri-<språk>.html` og bildene i `img/app/<språk>/`, App Store- og Google Play-merkene i `img/`, og kjør begge skriptene.

## Statistikk

Sidene teller besøk med GoatCounter (uten informasjonskapsler), lagt inn i bunnteksten i `felles.py`.
