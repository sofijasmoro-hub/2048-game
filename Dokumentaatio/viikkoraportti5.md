# Viikkoraportti 5

**Mitä olen tehnyt tällä viikolla?**  
Tein ensimmäisen vertaisarvioinnin toisen opiskelijan 2048-tekoälystä. Korjasin oman työni vertaisarvioinnissa löytyneen bugin: hakusyvyys 0 kaatoi ohjelman. Nyt käyttöliittymä kysyy syvyyttä uudelleen, jos se on alle 1. Korvasin hitaan koko pelin testin testillä, joka alkaa valmiista voittotilanteesta, ja lisäsin testit käyttöliittymän syötteen käsittelylle. Ohjaajan palautteen perusteella lisäsin testin, jossa expectimaxin arvo syvyydellä 2 on laskettu käsin koko hakupuusta. Päivitin toteutus- ja testausdokumentin.

**Miten ohjelma on edistynyt?**  
Ohjelman ydintoiminta on mielestäni valmis. Testejä on 49, ne menevät läpi alle sekunnissa, testikattavuus on 99 % ja pylint antaa 10/10.

**Mitä opin tällä viikolla?**  
Korjasin ja toivottavasti ymmärsin oikein, miten korjata

**Mikä jäi epäselväksi tai tuottanut vaikeuksia?**  
Oli aluksi vähän vaikeaa tulkita, missä on ongelma vertaisarvioinnin perusteella, koska olen työstänyt samaa asiaa aika pitkään, mutta jotakuinkin nyt ymmärrän, missä oli vika.

**Mitä teen seuraavaksi?**  
Teen toisen vertaisarvioinnin ja viimeistelen dokumentaation. Jos aikaa jää, yritän nopeuttaa hakua, jotta syvyyttä 2 voisi käyttää nopeammin.

**Käytetyt tunnit:** 9 h

**Tekoälyn käyttö:**  
Käytin tekoälyä (Claude) vertaisarvioinnin tulkitsemiseen, koska en aluksi ihan ymmärtänyt, mikä vikana. Sen jälkeen, kun ymmärsin, mistä on kyse, niin korjasin vian itse.
