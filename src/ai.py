"""2048-pelin tekoäly: expectimax-haku ja käärmeheuristiikka.

Tämä on harjoitustyön ydin.
"""

from src.game import DIRECTIONS, SIZE, empty_cells, move

# Käärmeheuristiikan järjestys: suurin paino vasemmassa yläkulmassa,
# ja painot pienenevät mutkitellen rivi riviltä kuin käärme.
SNAKE_ORDER = [
    [15, 14, 13, 12],
    [8, 9, 10, 11],
    [7, 6, 5, 4],
    [0, 1, 2, 3],
]

# Jokaisen ruudun paino on 4^järjestysnumero. Painot ovat jyrkkiä, jotta
# yksi iso laatta oikeassa paikassa on arvokkaampi kuin monta pientä.
SNAKE_WEIGHTS = [[4 ** n for n in row] for row in SNAKE_ORDER]

# Uuden laatan arvot ja niiden todennäköisyydet.
TILE_PROBABILITIES = ((2, 0.9), (4, 0.1))


def evaluate(board):
    """Käärmeheuristiikka: mitä suurempi arvo, sitä parempi lauta.

    Jokainen laatta kerrotaan oman ruutunsa painolla ja tulot lasketaan
    yhteen. Tekoäly pyrkii siis pitämään suurimman laatan kulmassa ja
    muut laatat suuruusjärjestyksessä käärmeen muotoisella reitillä.
    """
    return sum(board[r][c] * SNAKE_WEIGHTS[r][c]
               for r in range(SIZE) for c in range(SIZE))


def board_key(board):
    """Muuttaa laudan muotoon, jota voi käyttää hajautustaulun avaimena.

    Lista ei kelpaa dictin avaimeksi, mutta tuple kelpaa.
    """
    return tuple(tuple(row) for row in board)


def search_depth(board, base_depth):
    """Valitsee hakusyvyyden sen mukaan, kuinka täynnä lauta on.

    Kun tyhjiä ruutuja on vähän, satunnaisia vaihtoehtoja on vähän ja
    haku on nopea, joten voidaan laskea syvemmälle.

    Args:
        board: pelilauta.
        base_depth: käyttäjän antama syvyys, jota käytetään pelin alussa.
    """
    empty = len(empty_cells(board))
    if empty >= 6:
        return base_depth
    if empty >= 3:
        return base_depth + 1
    return base_depth + 2


def max_node(board, depth, cache):
    """Tekoälyn vuoro: paras arvo kaikista mahdollisista siirroista.

    Args:
        board: pelilauta.
        depth: montako tekoälyn siirtoa vielä lasketaan (vähintään 1).
        cache: hajautustaulu jo lasketuille tilanteille.

    Returns:
        Parhaan siirron arvo, tai 0 jos siirtoja ei ole (peli hävitty).
    """
    best = None
    for direction in DIRECTIONS:
        new_board, _, changed = move(board, direction)
        if not changed:
            continue
        value = chance_node(new_board, depth - 1, cache)
        if best is None or value > best:
            best = value
    return best if best is not None else 0


def chance_node(board, depth, cache):
    """Satunnaisen laatan vuoro: odotusarvo kaikista mahdollisista laatoista.

    Haku päättyy aina tekoälyn siirtoon: jos syvyys on 0, lauta arvioidaan
    heti siirron jälkeen ennen uuden laatan lisäämistä.

    Args:
        board: pelilauta tekoälyn siirron jälkeen.
        depth: montako tekoälyn siirtoa vielä lasketaan.
        cache: hajautustaulu jo lasketuille tilanteille.

    Returns:
        Laudan odotusarvo.
    """
    if depth == 0:
        return evaluate(board)

    key = (board_key(board), depth)
    if key in cache:
        return cache[key]

    cells = empty_cells(board)
    if not cells:
        return evaluate(board)

    total = 0
    for r, c in cells:
        for tile, probability in TILE_PROBABILITIES:
            board[r][c] = tile
            total += probability * max_node(board, depth, cache)
            board[r][c] = 0
    value = total / len(cells)

    cache[key] = value
    return value


def best_move(board, depth=2, adaptive=True):
    """Palauttaa parhaan siirtosuunnan, tai None jos siirtoja ei ole.

    Args:
        board: pelilauta.
        depth: montako tekoälyn siirtoa eteenpäin lasketaan pelin alussa.
        adaptive: jos True, syvyyttä kasvatetaan laudan täyttyessä.

    Raises:
        ValueError: jos syvyys on pienempi kuin 1.
    """
    if depth < 1:
        raise ValueError("Hakusyvyyden pitää olla vähintään 1")
    if adaptive:
        depth = search_depth(board, depth)
    cache = {}
    best_direction = None
    best_value = None
    for direction in DIRECTIONS:
        new_board, _, changed = move(board, direction)
        if not changed:
            continue
        value = chance_node(new_board, depth - 1, cache)
        if best_value is None or value > best_value:
            best_value = value
            best_direction = direction
    return best_direction
