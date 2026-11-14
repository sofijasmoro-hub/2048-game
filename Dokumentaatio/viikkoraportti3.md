# Viikkoraportti 3

**Mitä olen tehnyt tällä viikolla?**  
Lisäsin expectimax-hakuun hajautustaulun, johon tallennetaan jo laskettujen tilanteiden arvot. Tein käyttöliittymän, jossa voi katsoa tekoälyn peliä, pelata itse tai ajaa useita pelejä ja nähdä tilastot. Otin käyttöön pylintin (tulos 10/10), lisäsin testit hajautustaululle ja aloitin testausdokumentin.

**Miten ohjelma on edistynyt?**  
Hajautustaulu nopeutti hakua: syvyydellä 2 yksi peli kesti ennen noin 6 sekuntia ja nyt noin 2,5 sekuntia. Syvyydellä 3 tekoäly pääsi testipelissä 2048-laattaan, mutta peli kesti noin 2,5 minuuttia. Testejä on 35, ja testikattavuus on 99%.

**Mitä opin tällä viikolla?**  
Opin käyttämään pylintiä koodin laadun tarkistamiseen ja lukemaan coveragen kattavuusraporttia. Opin myös, miten hajautustaulu nopeuttaa hakua

**Mikä jäi epäselväksi tai tuottanut vaikeuksia?**  
Syvyys 3 on vielä ehkä liian hidas. Heuristiikan painot on yhä valittu kokeilemalla.

**Mitä teen seuraavaksi?**  
Sain ohjaajalta palautetta, että tavoitteena on mahdollisimman suuri laatta eikä pelkkä 2048. Toteutan seuraavaksi käärmeheuristiikan ja nopeutan hakua, jotta tekoäly pääsisi 4096- tai 8192-laattaan. Ajan useita pelejä ja vertaan tuloksia eri heuristiikoilla.

**Käytetyt tunnit:** 5h

**Tekoälyn käyttö:**  
Käytin tekoälyä tehtävien tarkistukseen, jotta kaikki on varmasti oikein.
