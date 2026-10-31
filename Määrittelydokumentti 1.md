**Määrittelydokumentti 1**

Opinto-ohjelma: Tietojenkäsittelytieteen kandidaatti (TKT)  
Dokumentaation kieli: suomi

**Ohjelmointikieli**

Teen projektin Pythonilla. Osaan vain Pythonia, joten pystyn vertaisarvioimaan vain Pythonilla tehtyjä projekteja.

**Minkä ongelman ratkaisen?**

2048:ssa pitää joka vuorolla valita yksi neljästä suunnasta. Siirron jälkeen satunnaiseen paikkaan tulee uusi laatta, joten on vaikea tietää, mikä siirto on paras. Teen tekoälyn, joka valitsee joka vuorolla parhaan siirron niin, että se pääsee vähintään 2048-laattaan.

**Mitä algoritmeja ja tietorakenteita toteutan?**

Algoritmit:

* Expectimax: kokeilee kaikki siirrot muutaman siirron eteenpäin ja laskee satunnaisista laatoista keskiarvon.  
* Heuristiikka: arvioi laudan, esimerkiksi tyhjien ruutujen määrän ja sen, onko isoin laatta kulmassa.

Tietorakenteet:

* 4x4-taulukko pelilaudalle.  
* Hajautustaulu (dict), johon tallennetaan jo laskettujen lautojen arvot, jotta samaa lautaa ei lasketa uudelleen.

**Syötteet**

Ohjelma saa pelilaudan ja palauttaa suunnan, johon kannattaa siirtää. Käyttäjä voi valita, kuinka monta siirtoa eteenpäin tekoäly laskee, ja katsoa, miten tekoäly pelaa.

**Aika- ja tilavaativuus**

Jos tekoäly laskee d siirtoa eteenpäin, aikavaativuus on eksponentiaalinen, noin O(b^d), missä b on vaihtoehtojen määrä yhdellä vuorolla. Siksi syvyys pitää pitää pienenä, esimerkiksi 2–3.

Tilavaativuus on O(d), koska haku tehdään rekursiolla.

**Harjoitustyön ydin**

Työn ydin on expectimax-algoritmi ja sen käyttämä heuristinen arviointifunktio, eli se, miten tekoäly päättää seuraavan siirron. Pelin säännöt ja käyttöliittymä ovat vain välineitä, joilla tekoälyä voi ajaa ja testata. Siksi ne toteutetaan mahdollisimman yksinkertaisesti, ja suurin osa ajasta käytetään hakualgoritmin, heuristiikan ja niiden optimoinnin kehittämiseen ja testaamiseen.

**Lähteet**

* Kurssimateriaali  
* Wikipedia: Expectiminimax, https\://en.wikipedia.org/wiki/Expectiminimax  
* Wikipedia: 2048 (video game), [https\://en.wikipedia.org/wiki/2048\_(video\_game)](https://en.wikipedia.org/wiki/2048_\(video_game\))

Tekoälyn käyttö:  
En käyttänyt