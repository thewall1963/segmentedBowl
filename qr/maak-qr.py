#!/usr/bin/env python3
"""
Maakt de QR-code voor de zaaglijst: een kale SVG, een PNG en een 16:9 dia.

    pip install segno
    python qr/maak-qr.py                      # gebruikt de GitHub Pages-link
    python qr/maak-qr.py https://elders.nl/   # of een adres naar keuze

Verhuist de site, bijvoorbeeld naar Vercel, draai dit dan opnieuw met het
nieuwe adres. De oude code blijft anders naar de oude plek wijzen.
"""

import sys
import segno

STANDAARD_URL = "https://thewall1963.github.io/segmentedBowl/"

INK = "#171A12"      # bijna-zwart, dezelfde inkt als de pagina
PAPIER = "#FFFFFF"
GROND = "#E7E8E1"
AMBER = "#A06B15"
NOOT = "#5A4030"


def maak(url, map_="qr"):
    # Foutcorrectie Q (25%) kost bij dit adres geen extra blokjes ten opzichte
    # van M, dus die marge is gratis: de code scant nog als er iets voor staat.
    qr = segno.make(url, error="Q")

    qr.save(f"{map_}/zaaglijst-qr.svg", scale=10, border=4, dark=INK, light=PAPIER)
    qr.save(f"{map_}/zaaglijst-qr.png", scale=48, border=4, dark=INK, light=PAPIER)

    mods = qr.symbol_size(1, 0)[0]
    breed, hoog = 1920, 1080
    zijde = 620
    stap = zijde / mods
    qx, qy = (breed - zijde) / 2, 270
    rand = stap * 4          # stille zone; zonder deze rand vindt geen telefoon de code

    # Aaneengesloten blokjes worden per rij tot één rechthoek samengevoegd.
    vlakken = []
    for r, rij in enumerate(qr.matrix):
        c = 0
        while c < mods:
            if rij[c]:
                n = 1
                while c + n < mods and rij[c + n]:
                    n += 1
                vlakken.append(
                    '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>'
                    % (qx + c * stap, qy + r * stap, n * stap + 0.2, stap + 0.2)
                )
                c += n
            else:
                c += 1

    kort = url.split("//")[-1].rstrip("/")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breed} {hoog}" width="{breed}" height="{hoog}">
  <rect width="{breed}" height="{hoog}" fill="{GROND}"/>
  <rect x="{qx - rand:.0f}" y="{qy - rand:.0f}" width="{zijde + 2 * rand:.0f}" height="{zijde + 2 * rand:.0f}" fill="{PAPIER}" rx="6"/>
  <g fill="{INK}" shape-rendering="crispEdges">
    {chr(10).join("    " + v for v in vlakken).strip()}
  </g>
  <text x="{breed // 2}" y="168" text-anchor="middle" fill="{INK}"
        font-family="Georgia, 'Times New Roman', serif" font-size="66" font-weight="600">Zaaglijst voor segmentschalen</text>
  <text x="{breed // 2}" y="216" text-anchor="middle" fill="{AMBER}"
        font-family="Menlo, Consolas, monospace" font-size="25" letter-spacing="3.4">SCAN VOOR DE REKENHULP</text>
  <text x="{breed // 2}" y="1010" text-anchor="middle" fill="{NOOT}"
        font-family="Menlo, Consolas, monospace" font-size="30">{kort}</text>
</svg>
'''
    with open(f"{map_}/zaaglijst-dia.svg", "w") as f:
        f.write(svg)

    print(f"{mods} x {mods} blokjes, versie {qr.version}, foutcorrectie Q")
    print(f"wijst naar {url}")


if __name__ == "__main__":
    maak(sys.argv[1] if len(sys.argv) > 1 else STANDAARD_URL)
