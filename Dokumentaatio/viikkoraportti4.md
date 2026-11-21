# Viikkoraportti 4

**Mitä olen tehnyt tällä viikolla?**  
Tein ohjaajan palautteen perusteella kolme muutosta tekoälyyn. Vanha heuristiikka korvattiin käärmeheuristiikalla. Hakusyvyys kasvaa nyt laudan täyttyessä: käyttäjä antaa syvyyden pelin alkuun, ja sitä kasvatetaan, kun tyhjiä ruutuja on vähän. Lisäksi haku päättyy aina tekoälyn siirtoon eikä satunnaiseen laattaan. Expectimaxin testaamista varten tein vertailutoteutuksen, johon optimoidun haun tulosta verrataan. Aloitin toteutusdokumentin ja päivitin testausdokumentin.

**Miten ohjelma on edistynyt?**  
Tekoäly pääsee nyt parhaimmillaan 8192-laattaan. Syvyydellä 1 kymmenestä pelistä seitsemän pääsi vähintään 2048-laattaan. Syvyydellä 2 tulokset ovat parempia, mutta yksi peli kestää 1–2 minuuttia. Testejä on 40, testikattavuus on 99 % ja pylint antaa 10/10.

**Mitä opin tällä viikolla?**  
Opin paremmin ymmärtämään käärmeheuristiikkaa.

**Mikä jäi epäselväksi tai tuottanut vaikeuksia?**  
Syvyydellä 2 peli on vielä hidas. Käärmeen painot on valittu kokeilemalla.

**Mitä teen seuraavaksi?**  
Teen vertaisarvioinnin ja korjaan saamani palautteen perusteella. Yritän nopeuttaa hakua ja täydennän toteutus- ja testausdokumenttia.

**Käytetyt tunnit:** 8 h

**Tekoälyn käyttö:**  
Käytin Claudea koodin tarkistukseen. Esimerkiksi siihen, että koodi on oikeassa paikassa eikä ole mitään toistoja eikä huolimattomuusvirheitä.
