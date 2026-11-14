# Testausdokumentti

## Testien ajaminen

Testit on tehty unittestillä ja ne ajetaan pytestillä:

    python3 -m pytest

Testikattavuus:

    python3 -m coverage run -m pytest
    python3 -m coverage report -m

Kattavuudesta on jätetty pois testitiedostot ja käyttöliittymä (`main.py`).

## Mitä testataan?

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

- **Heuristiikka:** lauta, jossa on enemmän tyhjiä ruutuja tai iso laatta kulmassa, saa paremmat pisteet.
- **Expectimax:** syvyydellä 0 palautetaan heuristiikan arvo. Chance-solmun arvo tarkistetaan
  käsin laskettua painotettua keskiarvoa vasten (0,9 · arvo laatalla 2 + 0,1 · arvo laatalla 4).
  Lisäksi tarkistetaan, ettei haku muuta lautaa.
- **Hajautustaulu:** haku antaa saman tuloksen välimuistin kanssa ja ilman sitä, välimuisti täyttyy,
  ja jo tallennettu arvo palautetaan laskematta uudelleen.
- **Paras siirto:** kun peli on ohi, siirtoa ei palauteta. Kun vain osa siirroista on mahdollisia,
  valitaan niistä jokin.
- **Koko peli:** tekoäly pelaa pelin loppuun kiinteällä satunnaissiemenellä ja pääsee vähintään 256-laattaan.

## Empiirinen testaus

Tekoälyn suorituskykyä testataan ajamalla useita pelejä (käyttöliittymän valinta 3)
ja kirjaamalla, kuinka suuren laatan tekoäly saavuttaa ja kuinka kauan peli kestää.
Tuloksia verrataan eri hakusyvyyksillä ja heuristiikoilla. Tulokset lisätään tähän
taulukkona ja kuvaajana, kun heuristiikkaa on paranneltu.

## Testikattavuus

```
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
src/__init__.py       0      0      0      0   100%
src/ai.py            72      1     34      1    98%   112
src/game.py          63      0     22      0   100%
-------------------------------------------------------------
TOTAL               135      1     56      1    99%
```
