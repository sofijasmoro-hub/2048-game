# Testausdokumentti

## Testien ajaminen

Testit on tehty unittestillä ja ne ajetaan pytestillä:

    python3 -m pytest

Testikattavuus:

    python3 -m coverage run -m pytest
    python3 -m coverage report -m

Kattavuudesta on jätetty pois testitiedostot ja käyttöliittymä (`main.py`).

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
- **Expectimax:**
  - Haku päättyy siirtoon: syvyydellä 0 lauta arvioidaan ilman satunnaista laattaa.
  - Hävitty peli saa arvon 0.
  - Odotusarvo tarkistetaan käsin laskettua arvoa vasten laudalla, jossa on yksi tyhjä ruutu.
  - **Vertailutoteutus:** expectimaxin testaaminen on hankalaa, koska oikeaa arvoa on vaikea laskea käsin.
    Siksi testeissä on yksinkertainen vertailutoteutus, joka laskee saman asian suoraan määritelmän
    mukaan ilman välimuistia. Optimoidun haun tulosta verrataan siihen kymmenellä satunnaisella
    laudalla syvyyksillä 1 ja 2.
  - Haku ei muuta alkuperäistä lautaa.
- **Hajautustaulu:** taulu täyttyy haun aikana, ja jo tallennettu arvo palautetaan laskematta uudelleen.
- **Paras siirto:** kun peli on ohi, siirtoa ei palauteta, ja iso laatta siirretään kulmaan.
- **Koko peli:** tekoäly pelaa pelin loppuun kiinteällä satunnaissiemenellä ja pääsee vähintään 2048-laattaan.

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
src/ai.py            58      1     28      1    98%   107
src/game.py          63      0     22      0   100%
-------------------------------------------------------------
TOTAL               121      1     50      1    99%
```
