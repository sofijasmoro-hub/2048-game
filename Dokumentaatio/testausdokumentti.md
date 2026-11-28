# Testausdokumentti

## Testien ajaminen

Testit on tehty unittestillä ja ne ajetaan pytestillä:

    python3 -m pytest

Testikattavuus:

    python3 -m coverage run -m pytest
    python3 -m coverage report -m

Kaikki testit vievät alle sekunnin.

## Yksikkötestit

### Pelin säännöt (`test_game.py`)

Rivin yhdistämistä testataan syötteillä, joissa tyypillisesti tulee virheitä:

- tyhjä rivi
- laatat, joiden välissä on tyhjiä ruutuja: `[0, 2, 0, 4]`
- neljä samaa laattaa: `[2, 2, 2, 2]` -> `[4, 4, 0, 0]`
- kolme samaa laattaa: `[2, 2,

cat > Dokumentaatio/testausdokumentti.md << 'EOF'
# Testausdokumentti

## Testien ajaminen

Testit on tehty unittestillä ja ne ajetaan pytestillä:

    python3 -m pytest

Testikattavuus:

    python3 -m coverage run -m pytest
    python3 -m coverage report -m

Kaikki testit vievät alle sekunnin.

## Yksikkötestit

### Pelin säännöt (`test_game.py`)

Rivin yhdistämistä testataan syötteillä, joissa tyypillisesti tulee virheitä:

- tyhjä rivi
- laatat, joiden välissä on tyhjiä ruutuja: `[0, 2, 0, 4]`
- neljä samaa laattaa: `[2, 2, 2, 2]` -> `[4, 4, 0, 0]`
- kolme samaa laattaa: `[2, 2, 2, 0]` -> `[4, 2, 0, 0]`
- laatta yhdistyy vain kerran: `[4, 4, 8, 0]` -> `[8, 8, 0, 0]` eikä `[16, 0, 0, 0]`
- erisuuret laatat eivät yhdisty

Lisäksi testataan siirrot kaikkiin neljään suuntaan, että alkuperäinen lauta ei muutu,
että siirto ilman muutosta tunnistetaan ja että peli päättyy vain, kun mitään ei voi yhdistää.

### Tekoäly (`test_ai.py`)

- **Käärmeheuristiikka:** tyhjä lauta on 0, iso laatta kulmassa on parempi kuin keskellä,
  käärmeen järjestys on parempi kuin käänteinen, ja käärme kääntyy toisella rivillä oikealta.
- **Hakusyvyys:** tyhjällä laudalla käytetään perussyvyyttä, ja syvyys kasvaa laudan täyttyessä.
  Syvyys 0 aiheuttaa selkeän virheen (`ValueError`).
- **Expectimax, syvyys 1:**
  - Haku päättyy siirtoon: syvyydellä 0 lauta arvioidaan ilman satunnaista laattaa.
  - Hävitty peli saa arvon 0.
  - Odotusarvo tarkistetaan laudalla, jossa on yksi tyhjä ruutu (painotus 0,9 ja 0,1).
  - Kahden tyhjän ruudun tulokset lasketaan yhteen ja jaetaan kahdella.
- **Expectimax, tarkka arvo syvyydellä 2 (`TestTarkkaArvo`):**
  Testiä varten valittiin lauta, jonka koko hakupuu on niin pieni, että sen voi laskea käsin.
  Puussa on kuitenkin kaikki olennainen: kaksi siirtovaihtoehtoa, satunnaiset laatat 2 ja 4,
  haarat, joissa peli häviää (arvo 0), ja valinta parhaasta siirrosta. Hakupuu on kirjoitettu
  testin kommenttiin, ja odotusarvo on 0,9 · 0,1 · LEAF_2 + 0,1 · 0,1 · LEAF_4, missä LEAF_2 ja
  LEAF_4 ovat parhaiden lehtisolmujen arvot. Lisäksi testataan, että lehtisolmujen laudat ovat
  oikeat ja että tekoäly valitsee siirron, joka ei johda varmaan häviöön.
- **Vertailutoteutus:** optimoidun haun tulosta verrataan yksinkertaiseen toteutukseen, joka
  laskee saman asian suoraan määritelmän mukaan ilman välimuistia. Vertailu tehdään kymmenellä
  satunnaisella laudalla syvyyksillä 1 ja 2.
- **Hajautustaulu:** taulu täyttyy haun aikana, ja jo tallennettu arvo palautetaan laskematta uudelleen.
- **Paras siirto:** kun peli on ohi, siirtoa ei palauteta, ja iso laatta siirretään kulmaan.
- **Voittotilanne:** kun laudalla on kaksi 1024-laattaa, tekoäly yhdistää ne 2048-laataksi kulmaan.
  Tämä korvasi aiemman testin, joka pelasi kokonaisen pelin ja oli hidas.

### Testien luotettavuuden tarkistus

Testien toimivuus tarkistettiin muuttamalla koodia tarkoituksella väärin. Testit epäonnistuivat,
kun todennäköisyydet 0,9 ja 0,1 vaihdettiin keskenään, kun hävitylle pelille annettiin
heuristiikan arvo nollan sijaan ja kun keskiarvon jakolasku poistettiin.

### Käyttöliittymä (`test_main.py`)

Käyttöliittymästä testataan syötteen käsittely: kelvollinen luku hyväksytään, tyhjä syöte
palauttaa oletusarvon, ja virheellistä syötettä (0, negatiivinen luku, teksti) kysytään uudelleen.
Syöte annetaan testeissä `unittest.mock`-kirjaston avulla.

Muuten käyttöliittymä (`main.py`) on testattu käsin, eikä sitä lasketa mukaan testikattavuuteen.

## Empiirinen testaus

Tekoälyn suorituskykyä testattiin ajamalla useita pelejä käyttöliittymän valinnalla 3.
Testit voi toistaa käynnistämällä ohjelman komennolla `python3 -m src.main` ja valitsemalla 3.

| Syvyys alussa | Pelejä | Suurin laatta | Aika / peli |
|---|---|---|---|
| 1 | 10 | 8192: 1, 4096: 3, 2048: 3, 512: 2, 128: 1 | 0,1–9 s |
| 2 | 2 | 8192: 1, 4096: 1 | 80–115 s |

Ennen käärmeheuristiikkaa tekoäly pääsi syvyydellä 1 noin 256-laattaan ja syvyydellä 2 noin 512-laattaan.

## Testikattavuus

```
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
src/__init__.py       0      0      0      0   100%
src/ai.py            60      1     30      1    98%   107
src/game.py          63      0     22      0   100%
-------------------------------------------------------------
TOTAL               123      1     52      1    99%
```
