"""2048-pelin säännöt.

Pelilauta on 4x4-lista listoja. Jokaisessa ruudussa on laatan arvo
(2, 4, 8, ...) tai 0, jos ruutu on tyhjä.
"""

import random

SIZE = 4
DIRECTIONS = ["up", "down", "left", "right"]


def new_board():
    """Luo tyhjän pelilaudan ja lisää siihen kaksi aloituslaattaa."""
    board = [[0] * SIZE for _ in range(SIZE)]
    add_random_tile(board)
    add_random_tile(board)
    return board


def empty_cells(board):
    """Palauttaa listan tyhjien ruutujen koordinaateista (rivi, sarake)."""
    return [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]


def add_random_tile(board):
    """Lisää satunnaiseen tyhjään ruutuun laatan 2 (90 %) tai 4 (10 %).

    Muokkaa lautaa paikallaan. Jos tyhjiä ruutuja ei ole, ei tee mitään.
    """
    cells = empty_cells(board)
    if not cells:
        return
    r, c = random.choice(cells)
    board[r][c] = 2 if random.random() < 0.9 else 4


def merge_row_left(row):
    """Siirtää yhden rivin laatat vasemmalle ja yhdistää samat laatat.

    Jokainen laatta voi yhdistyä vain kerran yhden siirron aikana.
    Esimerkki: [2, 2, 2, 2] -> [4, 4, 0, 0].

    Palauttaa uuden rivin ja yhdistämisestä saadut pisteet.
    """
    tiles = [x for x in row if x != 0]
    result = []
    score = 0
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            result.append(tiles[i] * 2)
            score += tiles[i] * 2
            i += 2
        else:
            result.append(tiles[i])
            i += 1
    result += [0] * (len(row) - len(result))
    return result, score


def _transpose(board):
    """Vaihtaa rivit ja sarakkeet keskenään."""
    return [list(col) for col in zip(*board)]


def _reverse(board):
    """Kääntää jokaisen rivin toisin päin."""
    return [row[::-1] for row in board]


def move(board, direction):
    """Tekee siirron annettuun suuntaan.

    Ei muokkaa alkuperäistä lautaa, vaan palauttaa uuden laudan.

    Palauttaa kolmikon (uusi_lauta, pisteet, muuttuiko_lauta).
    """
    if direction not in DIRECTIONS:
        raise ValueError(f"Tuntematon suunta: {direction}")

    # Kaikki suunnat muutetaan vasemmalle siirroksi kääntämällä lautaa.
    if direction == "left":
        grid = [row[:] for row in board]
    elif direction == "right":
        grid = _reverse(board)
    elif direction == "up":
        grid = _transpose(board)
    else:  # down
        grid = _reverse(_transpose(board))

    new_grid = []
    score = 0
    for row in grid:
        new_row, row_score = merge_row_left(row)
        new_grid.append(new_row)
        score += row_score

    # Käännetään lauta takaisin alkuperäiseen asentoon.
    if direction == "right":
        new_grid = _reverse(new_grid)
    elif direction == "up":
        new_grid = _transpose(new_grid)
    elif direction == "down":
        new_grid = _transpose(_reverse(new_grid))

    return new_grid, score, new_grid != board


def possible_moves(board):
    """Palauttaa listan suunnista, joihin siirto muuttaa lautaa."""
    return [d for d in DIRECTIONS if move(board, d)[2]]


def is_game_over(board):
    """Palauttaa True, jos yhtään siirtoa ei voi enää tehdä."""
    return not possible_moves(board)


def max_tile(board):
    """Palauttaa laudan suurimman laatan arvon."""
    return max(max(row) for row in board)
