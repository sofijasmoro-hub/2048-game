"""Käynnistää pelin, jossa tekoäly pelaa 2048:aa ja näyttää laudan."""

import sys

from src.ai import best_move
from src.game import add_random_tile, max_tile, move, new_board


def print_board(board):
    """Tulostaa pelilaudan konsoliin."""
    for row in board:
        print(" ".join(f"{x:5}" if x else "    ." for x in row))
    print()


def play(depth=2, show=True):
    """Pelaa yhden pelin tekoälyllä.

    Palauttaa kolmikon (suurin laatta, pisteet, siirtojen määrä).
    """
    board = new_board()
    score = 0
    moves = 0
    while True:
        direction = best_move(board, depth)
        if direction is None:
            break
        board, gained, _ = move(board, direction)
        score += gained
        moves += 1
        add_random_tile(board)
        if show:
            print(f"Siirto {moves}: {direction}, pisteet {score}")
            print_board(board)
    return max_tile(board), score, moves


if __name__ == "__main__":
    search_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    tile, points, count = play(search_depth)
    print(f"Peli päättyi. Suurin laatta: {tile}, pisteet: {points}, siirrot: {count}")
