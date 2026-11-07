"""Yksikkötestit pelin säännöille."""

import random
import unittest

from src.game import (add_random_tile, empty_cells, is_game_over, max_tile,
                      merge_row_left, move, new_board, possible_moves)

# Täysi lauta, jossa ei voi tehdä yhtään siirtoa.
STUCK = [
    [2, 4, 2, 4],
    [4, 2, 4, 2],
    [2, 4, 2, 4],
    [4, 2, 4, 2],
]


class TestMergeRow(unittest.TestCase):
    def test_tyhja_rivi_pysyy_tyhjana(self):
        self.assertEqual(merge_row_left([0, 0, 0, 0]), ([0, 0, 0, 0], 0))

    def test_laatat_siirtyvat_vasemmalle(self):
        self.assertEqual(merge_row_left([0, 2, 0, 4]), ([2, 4, 0, 0], 0))

    def test_kaksi_samaa_yhdistyy(self):
        self.assertEqual(merge_row_left([2, 0, 2, 0]), ([4, 0, 0, 0], 4))

    def test_nelja_samaa_yhdistyy_kahdeksi(self):
        self.assertEqual(merge_row_left([2, 2, 2, 2]), ([4, 4, 0, 0], 8))

    def test_laatta_yhdistyy_vain_kerran(self):
        # 4 + 4 -> 8, mutta syntynyt 8 ei saa yhdistyä toisen 8:n kanssa.
        self.assertEqual(merge_row_left([4, 4, 8, 0]), ([8, 8, 0, 0], 8))

    def test_kolme_samaa(self):
        self.assertEqual(merge_row_left([2, 2, 2, 0]), ([4, 2, 0, 0], 4))

    def test_erisuuret_eivat_yhdisty(self):
        self.assertEqual(merge_row_left([2, 4, 8, 16]), ([2, 4, 8, 16], 0))


class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = [
            [2, 0, 0, 2],
            [0, 4, 0, 4],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
        ]

    def test_vasemmalle(self):
        new, score, changed = move(self.board, "left")
        self.assertEqual(new[0], [4, 0, 0, 0])
        self.assertEqual(new[1], [8, 0, 0, 0])
        self.assertEqual(score, 12)
        self.assertTrue(changed)

    def test_oikealle(self):
        new, _, _ = move(self.board, "right")
        self.assertEqual(new[0], [0, 0, 0, 4])
        self.assertEqual(new[3], [0, 0, 0, 2])

    def test_ylos(self):
        new, score, _ = move(self.board, "up")
        self.assertEqual([row[0] for row in new], [4, 0, 0, 0])
        self.assertEqual([row[3] for row in new], [2, 4, 0, 0])
        self.assertEqual(score, 4)

    def test_alas(self):
        new, _, _ = move(self.board, "down")
        self.assertEqual([row[0] for row in new], [0, 0, 0, 4])
        self.assertEqual([row[1] for row in new], [0, 0, 0, 4])

    def test_alkuperainen_lauta_ei_muutu(self):
        copy = [row[:] for row in self.board]
        move(self.board, "left")
        self.assertEqual(self.board, copy)

    def test_siirto_joka_ei_muuta_lautaa(self):
        board = [[2, 4, 0, 0]] + [[0] * 4 for _ in range(3)]
        _, _, changed = move(board, "left")
        self.assertFalse(changed)

    def test_tuntematon_suunta(self):
        with self.assertRaises(ValueError):
            move(self.board, "diagonal")


class TestBoard(unittest.TestCase):
    def test_uudessa_laudassa_kaksi_laattaa(self):
        board = new_board()
        self.assertEqual(len(empty_cells(board)), 14)

    def test_uusi_laatta_on_2_tai_4(self):
        random.seed(1)
        for _ in range(100):
            board = [[0] * 4 for _ in range(4)]
            add_random_tile(board)
            values = [x for row in board for x in row if x]
            self.assertEqual(len(values), 1)
            self.assertIn(values[0], (2, 4))

    def test_laatan_lisays_tayteen_lautaan_ei_tee_mitaan(self):
        board = [row[:] for row in STUCK]
        add_random_tile(board)
        self.assertEqual(board, STUCK)

    def test_peli_paattyy_kun_siirtoja_ei_ole(self):
        self.assertTrue(is_game_over(STUCK))
        self.assertEqual(possible_moves(STUCK), [])

    def test_taysi_lauta_jossa_voi_yhdistaa(self):
        board = [row[:] for row in STUCK]
        board[0][1] = 2  # 2 ja 2 vierekkäin
        self.assertFalse(is_game_over(board))

    def test_suurin_laatta(self):
        self.assertEqual(max_tile(STUCK), 4)


if __name__ == "__main__":
    unittest.main()
