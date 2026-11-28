"""Yksikkötestit tekoälylle (expectimax ja käärmeheuristiikka)."""

import random
import unittest

from src.ai import (TILE_PROBABILITIES, best_move, board_key, chance_node,
                    evaluate, max_node, search_depth)
from src.game import DIRECTIONS, add_random_tile, empty_cells, move

STUCK = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]


def empty():
    return [[0] * 4 for _ in range(4)]


def reference_expectimax(board, depth):
    """Yksinkertainen vertailutoteutus ilman välimuistia ja optimointeja.

    Laskee saman asian kuin chance_node, mutta suoraan määritelmän mukaan:
    jokaisesta tyhjästä ruudusta ja laatasta tehdään oma kopio laudasta.
    """
    if depth == 0:
        return evaluate(board)
    cells = empty_cells(board)
    if not cells:
        return evaluate(board)
    total = 0
    for r, c in cells:
        for tile, probability in TILE_PROBABILITIES:
            copy = [row[:] for row in board]
            copy[r][c] = tile
            values = [reference_expectimax(move(copy, d)[0], depth - 1)
                      for d in DIRECTIONS if move(copy, d)[2]]
            total += probability * (max(values) if values else 0)
    return total / len(cells)


def random_board(seed, tiles):
    """Luo satunnaisen laudan, jossa on annettu määrä laattoja."""
    random.seed(seed)
    board = empty()
    for _ in range(tiles):
        add_random_tile(board)
    return board


class TestHeuristic(unittest.TestCase):
    def test_tyhja_lauta_on_nolla(self):
        self.assertEqual(evaluate(empty()), 0)

    def test_iso_laatta_kulmassa_on_parempi(self):
        corner = empty()
        corner[0][0] = 64
        middle = empty()
        middle[1][1] = 64
        self.assertGreater(evaluate(corner), evaluate(middle))

    def test_kaarmeen_jarjestys_on_parempi_kuin_kaanteinen(self):
        snake = empty()
        snake[0] = [64, 32, 16, 8]
        reverse = empty()
        reverse[0] = [8, 16, 32, 64]
        self.assertGreater(evaluate(snake), evaluate(reverse))

    def test_kaarme_jatkuu_toiselle_riville_oikealta(self):
        # Ensimmäisen rivin jälkeen käärme kääntyy: rivin 2 oikea reuna
        # on arvokkaampi kuin vasen reuna.
        right = empty()
        right[1][3] = 8
        left = empty()
        left[1][0] = 8
        self.assertGreater(evaluate(right), evaluate(left))


class TestSearchDepth(unittest.TestCase):
    def test_tyhja_lauta_kayttaa_perussyvyytta(self):
        self.assertEqual(search_depth(empty(), 2), 2)

    def test_melkein_taysi_lauta_kasvattaa_syvyytta(self):
        board = [row[:] for row in STUCK]
        board[0][0] = board[0][1] = board[0][2] = board[0][3] = 0
        self.assertEqual(search_depth(board, 2), 3)

    def test_taysi_lauta_kasvattaa_eniten(self):
        board = [row[:] for row in STUCK]
        board[3][3] = 0
        self.assertEqual(search_depth(board, 2), 4)


class TestExpectimax(unittest.TestCase):
    def test_haku_paattyy_siirtoon(self):
        # Syvyydellä 0 lauta arvioidaan heti siirron jälkeen,
        # ilman satunnaista laattaa.
        board = empty()
        board[0][0] = 2
        self.assertEqual(chance_node(board, 0, {}), evaluate(board))

    def test_max_node_havitty_peli_on_nolla(self):
        self.assertEqual(max_node(STUCK, 1, {}), 0)

    def test_max_node_valitsee_parhaan_siirron(self):
        board = empty()
        board[0][1] = 2048
        expected = max(evaluate(move(board, d)[0])
                       for d in DIRECTIONS if move(board, d)[2])
        self.assertEqual(max_node(board, 1, {}), expected)

    def test_kasin_laskettu_odotusarvo(self):
        # Lauta, jossa on vain yksi tyhjä ruutu (3, 3).
        board = [row[:] for row in STUCK]
        board[3][3] = 0
        with_2 = [row[:] for row in board]
        with_2[3][3] = 2
        with_4 = [row[:] for row in board]
        with_4[3][3] = 4
        expected = (0.9 * max_node(with_2, 1, {})
                    + 0.1 * max_node(with_4, 1, {}))
        self.assertAlmostEqual(chance_node(board, 1, {}), expected)

    def test_keskiarvo_kahdesta_tyhjasta_ruudusta(self):
        # Kahden tyhjän ruudun tulokset lasketaan yhteen ja jaetaan kahdella.
        board = [row[:] for row in STUCK]
        board[3][2] = board[3][3] = 0
        total = 0
        for col in (2, 3):
            for tile, probability in ((2, 0.9), (4, 0.1)):
                copy = [row[:] for row in board]
                copy[3][col] = tile
                total += probability * max_node(copy, 1, {})
        self.assertAlmostEqual(chance_node(board, 1, {}), total / 2)

    def test_sama_tulos_kuin_vertailutoteutuksella(self):
        # Verrataan optimoitua hakua yksinkertaiseen toteutukseen
        # usealla satunnaisella laudalla.
        for seed in range(10):
            board = random_board(seed, 10)
            for depth in (1, 2):
                self.assertAlmostEqual(
                    chance_node(board, depth, {}),
                    reference_expectimax(board, depth))

    def test_haku_ei_muuta_lautaa(self):
        board = random_board(3, 6)
        copy = [row[:] for row in board]
        chance_node(board, 2, {})
        self.assertEqual(board, copy)


class TestCache(unittest.TestCase):
    def setUp(self):
        self.board = [[2, 4, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]]

    def test_avain_on_sama_samalle_laudalle(self):
        copy = [row[:] for row in self.board]
        self.assertEqual(board_key(self.board), board_key(copy))

    def test_valimuisti_tayttyy(self):
        cache = {}
        chance_node(self.board, 2, cache)
        self.assertGreater(len(cache), 0)

    def test_tallennettu_arvo_palautetaan(self):
        cache = {(board_key(self.board), 2): 12345}
        self.assertEqual(chance_node(self.board, 2, cache), 12345)


class TestBestMove(unittest.TestCase):
    def test_ei_siirtoa_kun_peli_on_ohi(self):
        self.assertIsNone(best_move(STUCK))

    def test_siirtaa_ison_laatan_kulmaan(self):
        board = empty()
        board[0][1] = 2048
        self.assertEqual(best_move(board, 1, adaptive=False), "left")

    def test_palauttaa_ainoan_mahdollisen_siirron(self):
        board = [[2, 4, 8, 16], [2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64]]
        self.assertIn(best_move(board, 1), ("up", "down"))


class TestTarkkaArvo(unittest.TestCase):
    """Expectimaxin arvo syvyydellä 2 laskettuna käsin koko hakupuusta.

    Lähtölaudalla on yksi tyhjä ruutu (3, 2). Hakupuu:

    Laatta 2 (todennäköisyys 0,9):
        left  -> tyhjä ruutu (2, 3)
            laatta 2: ei siirtoja -> 0
            laatta 4: paras siirroista up ja down -> LEAF_2
            arvo 0,9 * 0 + 0,1 * LEAF_2
        right -> tyhjä ruutu (2, 0)
            laatta 2 ja laatta 4: ei siirtoja -> arvo 0
        max(left, right) = 0,1 * LEAF_2
    Laatta 4 (todennäköisyys 0,1):
        sama rakenne, paras arvo 0,1 * LEAF_4

    Odotusarvo = 0,9 * 0,1 * LEAF_2 + 0,1 * 0,1 * LEAF_4
    """

    START = [[32, 4, 2, 16], [8, 32, 16, 4], [64, 64, 8, 64], [8, 16, 0, 8]]

    # Lehtisolmut eli laudat kahden siirron jälkeen.
    UP_2 = [[32, 4, 2, 16], [8, 32, 16, 8], [128, 8, 64, 8], [8, 16, 2, 0]]
    DOWN_2 = [[32, 4, 2, 0], [8, 32, 16, 16], [128, 8, 64, 8], [8, 16, 2, 8]]
    UP_4 = [[32, 4, 2, 16], [8, 32, 16, 8], [128, 8, 64, 8], [8, 16, 4, 0]]
    DOWN_4 = [[32, 4, 2, 0], [8, 32, 16, 16], [128, 8, 64, 8], [8, 16, 4, 8]]

    def test_lehtisolmut_ovat_oikeat(self):
        # Tarkistetaan polku: laatta 2, left, laatta 4, up.
        board = [row[:] for row in self.START]
        board[3][2] = 2
        board, _, _ = move(board, "left")
        board[2][3] = 4
        self.assertEqual(move(board, "up")[0], self.UP_2)
        self.assertEqual(move(board, "down")[0], self.DOWN_2)

    def test_odotusarvo_syvyydella_2(self):
        leaf_2 = max(evaluate(self.UP_2), evaluate(self.DOWN_2))
        leaf_4 = max(evaluate(self.UP_4), evaluate(self.DOWN_4))
        expected = 0.9 * 0.1 * leaf_2 + 0.1 * 0.1 * leaf_4
        board = [row[:] for row in self.START]
        self.assertAlmostEqual(chance_node(board, 2, {}), expected)

    def test_valitsee_siirron_joka_ei_havia_varmasti(self):
        # Siirto right johtaa varmasti häviöön, joten paras on left.
        board = [row[:] for row in self.START]
        board[3][2] = 2
        self.assertEqual(best_move(board, 2, adaptive=False), "left")


class TestVoittotilanne(unittest.TestCase):
    def test_yhdistaa_2048_laatan_kulmaan(self):
        board = empty()
        board[0][0] = 1024
        board[0][1] = 1024
        self.assertEqual(best_move(board, 2, adaptive=False), "left")
        self.assertEqual(move(board, "left")[0][0][0], 2048)

    def test_syvyys_nolla_ei_kelpaa(self):
        with self.assertRaises(ValueError):
            best_move(empty(), 0)


if __name__ == "__main__":
    unittest.main()
