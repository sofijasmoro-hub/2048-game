"""Yksikkötestit käyttöliittymän syötteen käsittelylle."""

import unittest
from unittest.mock import patch

from src.main import ask_number


class TestAskNumber(unittest.TestCase):
    @patch("builtins.input", return_value="3")
    def test_kelvollinen_luku(self, _):
        self.assertEqual(ask_number("Syvyys", 2), 3)

    @patch("builtins.input", return_value="")
    def test_tyhja_syote_palauttaa_oletuksen(self, _):
        self.assertEqual(ask_number("Syvyys", 2), 2)

    @patch("builtins.input", side_effect=["0", "3"])
    def test_nolla_kysytaan_uudelleen(self, mock_input):
        self.assertEqual(ask_number("Syvyys", 2), 3)
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", side_effect=["abc", "-1", "4"])
    def test_virheellinen_syote_kysytaan_uudelleen(self, mock_input):
        self.assertEqual(ask_number("Syvyys", 2), 4)
        self.assertEqual(mock_input.call_count, 3)


if __name__ == "__main__":
    unittest.main()
