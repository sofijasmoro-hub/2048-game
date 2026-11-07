

## **Viikkoraportti 2**

**Mitä olen tehnyt tällä viikolla?**  
Lisäsin projektiin pelin säännöt (laattojen siirto, yhdistäminen, uusi laatta ja pelin päättyminen) sekä tekoälyn ensimmäisen version, joka käyttää expectimax-algoritmia ja heuristiikkaa. Lisäsin yksikkötestit pelin säännöille ja tekoälylle sekä testikattavuuden seurannan coveragella. Siirsin koodin GitHubiin terminaalin ja gitin avulla.

**Miten ohjelma on edistynyt?**  
Tekoäly pystyy pelaamaan kokonaisen pelin. Hakusyvyydellä 1 se pääsee noin 256-laattaan ja syvyydellä 2 noin 512-laattaan, joten tavoitteeseen 2048 ei vielä päästä. Testejä on 30, ja kaikki menevät läpi terminaalin kautta.

**Mitä opin tällä viikolla?**  
Opin käyttämään gitiä terminaalissa: tiedostojen lisäämistä, committeja ja pushia. Opin myös, mitä tehdä, kun push ei onnistu. Ensin push epäonnistui, koska koneeni oli kirjautunut eri GitHub-tilillä kuin se, jolle repo kuului, ja korjasin asian lisäämällä tilin repon collaboratoriksi. Sen jälkeen push hylättiin, koska GitHubissa oli muutoksia, joita koneellani ei ollut, ja opin hakemaan ne komennolla `git pull --rebase`. Opin myös ajamaan testit pytestillä ja tulkitsemaan coveragen kattavuusraportin. Lisäksi huomasin, että Macilla Python käynnistetään komennolla `python3`.

**Mikä jäi epäselväksi tai tuottanut vaikeuksia?**  
2048-pelin koodi oli minulle aluksi vieras, ja minun pitää vielä perehtyä tarkemmin siihen, miten expectimax-funktio ja heuristiikka toimivat. GitHubin käyttöoikeuksien kanssa oli ongelmia, mutta sain ne ratkaistua. Heuristiikan painojen valinta on vielä epäselvää.

**Mitä teen seuraavaksi?**  
Käyn tekoälyn koodin läpi niin, että ymmärrän sen kunnolla. Sen jälkeen parannan heuristiikkaa ja lisään hajautustaulun, jotta haku nopeutuu ja tekoäly pääsee 2048-laattaan.

**Käytetyt tunnit:** 6 h

**Lähteet:**

- Wikipedia: 2048 (video game) [https\://en.wikipedia.org/wiki/2048\_(video\_game)](https://en.wikipedia.org/wiki/2048_\(video_game\))  
- Wikipedia: Expectiminimax [https\://en.wikipedia.org/wiki/Expectiminimax](https://en.wikipedia.org/wiki/Expectiminimax) 

**Tekoälyn käyttö:**

Käytin silloin, kun koodi oli jumittunut. Esimerkiksi silloin kun en huomannut, että Macbookin terminaalissa ja Githubissa on eri käyttäjät ja siksi en voinut lähettää koodia Githubiin.

