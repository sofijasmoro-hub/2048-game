"""2048-pelin tekoäly: expectimax-haku ja heuristinen arviointifunktio.

Tämä on harjoitustyön ydin.
"""

from src.game import DIRECTIONS, SIZE, empty_cells, move

# Heuristiikan painot. Näitä säädetään myöhemmin testaamalla.
EMPTY_WEIGHT = 270
CORNER_WEIGHT = 1.0
MONOTONICITY_WEIGHT = 1.0


def monotonicity(board):
    """Laskee, kuinka hyvin laatat ovat suuruusjärjestyksessä.

    Jokaiselle riville ja sarakkeelle lasketaan, kuinka paljon arvot
    rikkovat kasvavaa tai laskevaa järjestystä. Parempi suunta otetaan
    mukaan. Tulos on 0 tai negatiivinen: mitä lähempänä nollaa, sitä
    paremmassa järjestyksessä laatat ovat.
    """
    total = 0
    lines = [row for row in board] + [list(col) for col in zip(*board)]
    for line in lines:
        increasing = 0
        decreasing = 0
        for i in range(SIZE - 1):
            if line[i] > line[i + 1]:
                decreasing += line[i] - line[i + 1]
            else:
                increasing += line[i + 1] - line[i]
        total -= min(increasing, decreasing)
    return total


def evaluate(board):
    """Heuristinen arviointifunktio: mitä suurempi arvo, sitä parempi lauta.

    Huomioi tyhjien ruutujen määrän, suurimman laatan kulmassa olemisen
    ja laattojen järjestyksen (monotonisuuden).
    """
    empty = len(empty_cells(board))
    biggest = max(max(row) for row in board)
    corners = [board[0][0], board[0][SIZE - 1],
               board[SIZE - 1][0], board[SIZE - 1][SIZE - 1]]
    corner_bonus = biggest if biggest in corners else 0

    return (EMPTY_WEIGHT * empty
            + CORNER_WEIGHT * corner_bonus
            + MONOTONICITY_WEIGHT * monotonicity(board))


def expectimax(board, depth, is_max_turn):
    """Laskee laudan arvon expectimax-algoritmilla.

    Args:
        board: pelilauta.
        depth: montako tasoa vielä lasketaan eteenpäin.
        is_max_turn: True, jos on tekoälyn vuoro (max-solmu),
            False, jos on satunnaisen laatan vuoro (chance-solmu).

    Returns:
        Laudan arvo lukuna.
    """
    if depth == 0:
        return evaluate(board)

    if is_max_turn:
        best = None
        for direction in DIRECTIONS:
            new_board, _, changed = move(board, direction)
            if not changed:
                continue
            value = expectimax(new_board, depth - 1, False)
            if best is None or value > best:
                best = value
        # Jos siirtoja ei ole, peli on hävitty.
        return best if best is not None else evaluate(board)

    cells = empty_cells(board)
    if not cells:
        return evaluate(board)

    # Chance-solmu: painotettu keskiarvo kaikista mahdollisista laatoista.
    total = 0
    for r, c in cells:
        for tile, probability in ((2, 0.9), (4, 0.1)):
            board[r][c] = tile
            total += probability * expectimax(board, depth - 1, True)
            board[r][c] = 0
    return total / len(cells)


def best_move(board, depth=2):
    """Palauttaa parhaan siirtosuunnan, tai None jos siirtoja ei ole.

    Args:
        board: pelilauta.
        depth: montako tekoälyn siirtoa eteenpäin lasketaan.
    """
    best_direction = None
    best_value = None
    for direction in DIRECTIONS:
        new_board, _, changed = move(board, direction)
        if not changed:
            continue
        # Syvyys kerrotaan kahdella, koska yksi kierros on
        # tekoälyn siirto + satunnainen laatta.
        value = expectimax(new_board, depth * 2 - 1, False)
        if best_value is None or value > best_value:
            best_value = value
            best_direction = direction
    return best_direction
