# segmentedBowl

Hulpmiddelen voor het maken van een gesegmenteerde houten schaal: je geeft de
vorm van de schaal en het aantal segmenten op, en krijgt terug hoe je de
trapeziumvormige segmenten moet zagen.

## web/

`web/index.html` — de webversie, bedoeld om binnen de club te delen. Eén
bestand zonder afhankelijkheden: openen in een browser is genoeg.

Wat erin zit:

- **Invoer** — segmenten per ring, aantal ringen, bodemdiameter, en de bovenmaat
  als randdiameter *of* als wandhelling. Verder wandprofiel (gebogen, recht,
  bol), ringhoogte, wanddikte en zaagsnede. Alle maten in mm.
- **Tekeningen** — bovenaanzicht van de gekozen ring, en het segment met
  maatvoering en de verstekhoek.
- **Zaaglijst** — per ring de buiten- en binnendiameter, lange zijde, korte
  zijde, strookbreedte en strooklengte.
- **Verstekmal** — maten voor een rechthoekige driehoek van karton of multiplex
  waarmee je de verstekhoek uitzet: zijde `x` langs een rechte kant, daar haaks
  `y` op. Alleen hele en halve centimeters tussen 15 en 30 cm, en alleen paren
  die binnen 0,07° van de verstekhoek blijven.
- **Werkwijze** — zeven stappen van verstek instellen tot draaien, plus
  aandachtspunten over nerf, houtsoorten en wanddikte.

## Python/

`Python/bowl_calculator.py` — de oorspronkelijke opzet: één ring per keer,
via de terminal, met een tekening in matplotlib.

```sh
pip install -r requirements.txt
python Python/bowl_calculator.py
```

## De meetkunde

Voor een ring met `N` segmenten, buitendiameter `Do` en binnendiameter
`Di = Do − 2 × wanddikte`, met `α = 180/N`:

| maat | formule |
|---|---|
| verstekhoek, per uiteinde | `α` |
| lange zijde | `Do × tan(α)` |
| korte zijde | `Di × sin(α)` |
| strookbreedte | `Do/2 − (Di/2) × cos(α)` |

De veelhoek ligt zo dat de **platte kanten** de gewenste buitendiameter halen en
de **binnenhoeken** op de gewenste binnendiameter liggen. De blank is daarmee
overal ruim genoeg; het overschot draai je weg.

Bij een schuine wand heeft een ring hoogte: de buitenkant loopt over die hoogte
al naar buiten. Elke ring wordt daarom gemaakt op zijn wijdste maat (bovenkant
van de ring) en zijn nauwste (onderkant). Over een ringhoogte `h` bij een
wandhelling `β` ten opzichte van het horizontale vlak is dat `h / tan(β)` per
kant.

Rekenvoorbeeld — Ø 140 onderaan de ring, wanddikte 20, 8 segmenten, helling 55°,
ringhoogte 18: Ø buiten wordt 165,2 en Ø binnen 100,0, dus lange zijde 68,4,
korte zijde 38,3 en strookbreedte 36,4 mm.
