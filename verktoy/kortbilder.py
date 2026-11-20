"""Utsnittene på funksjonskortene («Treningsformer og høydepunkter» på forsiden).

Hvert kort viser en bit av et ekte skjermbilde fra manualen i appen
(Trax/Assets.xcassets/manual-<kilde>[-sv|-en|-de], 840 × 1826 piksler).
Her står hvilken bit (fra y0 til y1, hele bredden). Bitene er valgt så de
viser det kortet handler om, og så de ikke viser ekte hundenavn.

Lag bildene på nytt med (app-repoet klonet ved siden av):

    python3 verktoy/kortbilder.py ../Trax

De havner i img/app/<språk>/kort-<navn>.webp, 600 piksler brede.
lag-sider.py leser høyden herfra, så kjør også lag-sider.py etter en endring.
"""

import pathlib
import sys

BREDDE = 600  # bredden på bildefilene
KILDE_BREDDE = 840  # bredden på manualbildene i appen

# navn: (manualbilde, y0, y1)
KORT = {
    "kort-plan": ("plan-draw", 250, 1290),
    "kort-detalj": ("detail", 190, 1430),
    "kort-igp": ("igp-lay", 125, 1365),
    "kort-blod": ("blood", 560, 1800),
    "kort-felt": ("search-find", 110, 1350),
    "kort-hund": ("dogpage", 680, 1640),
    "kort-natt": ("night", 150, 1110),
}

SPRAK = {"nb": "", "sv": "-sv", "en": "-en", "de": "-de"}


def hoyde(navn):
    _, y0, y1 = KORT[navn]
    return round(BREDDE * (y1 - y0) / KILDE_BREDDE)


def lag(app_repo):
    from PIL import Image

    rot = pathlib.Path(__file__).resolve().parent.parent
    xc = pathlib.Path(app_repo) / "Trax" / "Assets.xcassets"
    for lang, suffiks in SPRAK.items():
        for navn, (kilde, y0, y1) in KORT.items():
            mappe = xc / f"manual-{kilde}{suffiks}.imageset"
            fil = next(p for p in sorted(mappe.iterdir()) if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
            im = Image.open(fil).convert("RGB")
            if im.width != KILDE_BREDDE:
                im = im.resize((KILDE_BREDDE, round(im.height * KILDE_BREDDE / im.width)), Image.LANCZOS)
            ut = im.crop((0, y0, KILDE_BREDDE, y1)).resize((BREDDE, hoyde(navn)), Image.LANCZOS)
            mal = rot / "img" / "app" / lang / f"{navn}.webp"
            ut.save(mal, "WEBP", quality=82, method=6)
            print(mal.relative_to(rot))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Bruk: python3 verktoy/kortbilder.py ../Trax")
    lag(sys.argv[1])
