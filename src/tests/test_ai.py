"""Yksikkötestit tekoälylle (expectimax ja heuristiikka)."""

import random
import unittest

from src.ai import best_move, evaluate, expectimax, monotonicity
from src.main import play


def empty():
    return [[0] * 4 for _ in range(4)]


class TestHeuristic(unittest.TestCase):
    def test_enemman_tyhjia_on_parempi(self):
        few = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [0, 0, 0, 0]]
        many = empty()
        many[0][0] = 2
        self.assertGreater(evaluate(many), evaluate(few))

    def test_iso_laatta_kulmassa_on_parempi(self):
        corner = empty()
        corner[0][0] = 64
        middle = empty()
        middle[1][1] = 64
        self.assertGreater(evaluate(corner), evaluate(middle))

    def test_jarjestyksessa_oleva_rivi_on_monotoninen(self):
        board = empty()
        board[0] = [16, 8, 4, 2]
        self.assertEqual(monotonicity(board), 0)

    def test_sekalainen_rivi_saa_miinusta(self):
        board = empty()
        board[0] = [2, 16, 2, 16]
        self.assertLess(monotonicity(board), 0)


class TestExpectimax(unittest.TestCase):
    def test_syvyys_nolla_palauttaa_heuristiikan(self):
        board = empty()
        board[0][0] = 2
        self.assertEqual(expectimax(board, 0, True), evaluate(board))

    def test_chance_solmu_on_painotettu_keskiarvo(self):
        board = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 0]]
        with_2 = [row[:] for row in board]
        with_2[3][3] = 2
        with_4 = [row[:] for row in board]
        with_4[3][3] = 4
        expected = 0.9 * evaluate(with_2) + 0.1 * evaluate(with_4)
        self.assertAlmostEqual(expectimax(board, 1, False), expected)

    def test_chance_solmu_ei_muuta_lautaa(self):
        board = empty()
        board[0][0] = 2
        copy = [row[:] for row in board]
        expectimax(board, 2, False)
        self.assertEqual(board, copy)


class TestBestMove(unittest.TestCase):
    def test_ei_siirtoa_kun_peli_on_ohi(self):
        stuck = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
        self.assertIsNone(best_move(stuck))

    def test_palauttaa_ainoan_mahdollisen_siirron(self):
        board = [[2, 4, 8, 16], [2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64]]
        self.assertIn(best_move(board, 1), ("up", "down"))


class TestKokoPeli(unittest.TestCase):
    def test_tekoaly_pelaa_pelin_loppuun(self):
        random.seed(42)
        tile, score, moves = play(depth=1, show=False)
        self.assertGreater(moves, 0)
        self.assertGreater(score, 0)
        self.assertGreaterEqual(tile, 256)


if __name__ == "__main__":
    unittest.main()
