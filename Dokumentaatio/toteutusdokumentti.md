# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelma koostuu kolmesta moduulista:

- `src/game.py`: pelin säännöt eli laattojen siirto ja yhdistäminen, uuden laatan lisääminen ja pelin päättymisen tunnistaminen. Pelilauta on 4x4-lista listoja, jossa tyhjä ruutu on 0.
- `src/ai.py`: tekoäly, joka on työn ydin. Sisältää expectimax-haun, käärmeheuristiikan ja hajautustaulun.
- `src/main.py`: tekstikäyttöliittymä, jossa voi katsoa tekoälyn peliä, pelata itse tai ajaa useita pelejä ja nähdä tilastot.

## Tekoäly

### Expectimax

Haku on jaettu kahteen funktioon:

- `max_node`: tekoälyn vuoro. Kokeillaan kaikki siirrot, jotka muuttavat lautaa, ja valitaan suurin arvo. Jos siirtoja ei ole, peli on hävitty ja arvo on 0.
- `chance_node`: satunnaisen laatan vuoro. Jokaiseen tyhjään ruutuun kokeillaan laattaa 2 (todennäköisyys 0,9) ja 4 (todennäköisyys 0,1). Tulokset painotetaan todennäköisyyksillä ja niistä lasketaan keskiarvo.

Haku päättyy aina tekoälyn siirtoon: kun syvyys on käytetty, lauta arvioidaan heti siirron jälkeen ennen satunnaista laattaa.

### Käärmeheuristiikka

Laudan jokaiselle ruudulle on annettu paino 4^n, missä n kulkee käärmeen muotoista reittiä vasemmasta yläkulmasta (n = 15) mutkitellen alas (n = 0). Laudan arvo on laattojen ja painojen tulojen summa. Heuristiikka ohjaa tekoälyn pitämään suurimman laatan kulmassa ja muut laatat järjestyksessä sen perässä, jolloin ne voi yhdistää ketjuna.

### Kasvava hakusyvyys

Käyttäjä antaa hakusyvyyden, jota käytetään pelin alussa. Kun tyhjiä ruutuja on 3–5, syvyyttä kasvatetaan yhdellä, ja kun niitä on alle 3, kahdella. Kun tyhjiä ruutuja on vähän, satunnaisia vaihtoehtoja on vähän ja haku on nopea. Samalla tilanne on vaarallisin, joten syvempi haku auttaa eniten.

### Hajautustaulu

Sama lauta voi tulla hakupuussa vastaan useaa eri reittiä. Siksi `chance_node` tallentaa lasketut arvot Pythonin dictiin avaimella (lauta tuplena, syvyys). Taulu luodaan uudelleen jokaiselle siirrolle.

## Aika- ja tilavaativuus

Olkoon d hakusyvyys (tekoälyn siirtojen määrä) ja e tyhjien ruutujen määrä. Max-solmulla on enintään 4 lasta ja chance-solmulla enintään 2e lasta. Pahimmassa tapauksessa aikavaativuus on siis O((8e)^d). Laudan koko on vakio, joten yksittäinen siirto ja heuristiikan laskeminen ovat O(1).

Hajautustaulu ei muuta pahimman tapauksen vaativuutta, mutta käytännössä se vähentää laskettavien solmujen määrää. Tilavaativuus on O(d) rekursion vuoksi, ja lisäksi hajautustaulu vie tilaa tallennettujen tilanteiden verran.

Kasvava syvyys perustuu siihen, että haarautumiskerroin 8e pienenee laudan täyttyessä. Pienellä e:llä suurempi d on yhtä nopea kuin pieni d tyhjällä laudalla.

## Suorituskyky

| Syvyys alussa | Pelejä | Suurin laatta | Aika / peli |
|---|---|---|---|
| 1 | 10 | 8192: 1, 4096: 3, 2048: 3, 512: 2, 128: 1 | 0,1–9 s |
| 2 | 2 | 8192: 1, 4096: 1 | 80–115 s |

## Puutteet ja parannusehdotukset

- Syvyydellä 2 peli on hidas. Hakua voisi nopeuttaa esimerkiksi jättämällä hyvin epätodennäköiset haarat laskematta tai esittämällä laudan bittiesityksenä.
- Käärmeen painot on valittu kokeilemalla. Eri painoja voisi verrata järjestelmällisesti.
- Syvyydellä 1 tulokset vaihtelevat paljon pelistä toiseen.

## Palautteen perusteella tehdyt muutokset

- **Hakusyvyyden tarkistus:** vertaisarvioinnissa huomattiin, että syvyys 0 kaatoi ohjelman `RecursionError`-virheeseen. Nyt käyttöliittymä kysyy syvyyttä uudelleen, jos se on alle 1, ja `best_move` antaa selkeän `ValueError`-virheen, jos sitä kutsutaan syvyydellä 0.
- **Nopeammat testit:** kokonaisen pelin pelaava testi korvattiin testillä, joka alkaa valmiista voittotilanteesta. Testien ajo nopeutui noin 3 sekunnista alle sekuntiin.
- **Expectimaxin tarkka testi:** ohjaajan palautteen perusteella lisättiin testi, jossa expectimaxin arvo syvyydellä 2 on laskettu käsin koko hakupuusta.

## Laajojen kielimallien käyttö

Käytin tekoälyä (Claude) koodin tarkistamiseen, että kaikki on oikein kirjoitettu eikä mitään ylimääräistä löydy.

## Lähteet

- Wikipedia: Expectiminimax, https://en.wikipedia.org/wiki/Expectiminimax
- Wikipedia: 2048 (video game), https://en.wikipedia.org/wiki/2048_(video_game)
- Ohjaajan (Hannun) palaute liittyen käärmeheuristiikka ja kasvava hakusyvyys
