# 2048-tekoäly

Tekoäly, joka pelaa 2048-peliä expectimax-algoritmilla ja käärmeheuristiikalla.

## Dokumentaatio

- [Määrittelydokumentti](Dokumentaatio/maarittelydokumentti.md)
- [Toteutusdokumentti](Dokumentaatio/toteutusdokumentti.md)
- [Testausdokumentti](Dokumentaatio/testausdokumentti.md)
- [Viikkoraportti 1](Dokumentaatio/viikkoraportti1.md)
- [Viikkoraportti 2](Dokumentaatio/viikkoraportti2.md)
- [Viikkoraportti 3](Dokumentaatio/viikkoraportti3.md)
- [Viikkoraportti 4](Dokumentaatio/viikkoraportti4.md)

## Käyttö

Asenna riippuvuudet:

    python3 -m pip install -r requirements.txt

Käynnistä ohjelma:

    python3 -m src.main

Aja testit:

    python3 -m pytest

Testikattavuus:

    python3 -m coverage run -m pytest
    python3 -m coverage report -m

Koodin laatu:

    python3 -m pylint src
