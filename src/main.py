"""Tekstikäyttöliittymä: katso tekoälyn peliä, pelaa itse tai aja tilastot."""

import time

from src.ai import best_move
from src.game import (add_random_tile, is_game_over, max_tile, move,
                      new_board)

KEYS = {"w": "up", "a": "left", "s": "down", "d": "right"}


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


def play_yourself():
    """Pelaaja pelaa itse näppäimillä w, a, s ja d."""
    board = new_board()
    score = 0
    while not is_game_over(board):
        print(f"Pisteet: {score}")
        print_board(board)
        key = input("Siirto (w/a/s/d, q = lopeta): ").strip().lower()
        if key == "q":
            break
        if key not in KEYS:
            print("Käytä näppäimiä w, a, s, d tai q.\n")
            continue
        new, gained, changed = move(board, KEYS[key])
        if not changed:
            print("Siirto ei muuttanut lautaa, kokeile toista suuntaa.\n")
            continue
        board = new
        score += gained
        add_random_tile(board)
    print_board(board)
    print(f"Peli päättyi. Suurin laatta: {max_tile(board)}, pisteet: {score}")


def statistics(games, depth):
    """Pelaa useita pelejä tekoälyllä ja tulostaa yhteenvedon."""
    results = {}
    start = time.time()
    for i in range(games):
        tile, score, moves = play(depth, show=False)
        results[tile] = results.get(tile, 0) + 1
        print(f"Peli {i + 1}: suurin laatta {tile}, pisteet {score}, siirrot {moves}")
    print(f"\nAikaa kului {time.time() - start:.1f} s")
    for tile in sorted(results):
        print(f"{tile:5}: {results[tile]} peliä")


def ask_number(text, default):
    """Kysyy käyttäjältä kokonaisluvun. Tyhjä tai virheellinen syöte -> oletus."""
    answer = input(f"{text} [{default}]: ").strip()
    return int(answer) if answer.isdigit() else default


def main():
    """Näyttää valikon ja käynnistää valitun toiminnon."""
    while True:
        print("2048-tekoäly")
        print("1 = katso, kun tekoäly pelaa")
        print("2 = pelaa itse")
        print("3 = aja useita pelejä ja näytä tilastot")
        print("q = lopeta")
        choice = input("Valinta: ").strip().lower()
        if choice == "1":
            depth = ask_number("Hakusyvyys", 2)
            tile, score, moves = play(depth)
            print(f"Peli päättyi. Suurin laatta: {tile}, pisteet: {score}, "
                  f"siirrot: {moves}\n")
        elif choice == "2":
            play_yourself()
        elif choice == "3":
            games = ask_number("Pelien määrä", 5)
            depth = ask_number("Hakusyvyys", 2)
            statistics(games, depth)
        elif choice == "q":
            break
        else:
            print("Tuntematon valinta.\n")


if __name__ == "__main__":
    main()
