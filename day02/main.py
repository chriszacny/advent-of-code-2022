"""
Advent of code 2022 Day 2. 

TODO: This is HACKY code. These functions need to be split and a lot of error conditions checked for.

"""

import unittest
import os
from enum import Enum


class YourMove(Enum):
    X = 1 # Rock
    Y = 2 # Paper
    Z = 3 # Scissors


class OpponentMove(Enum):
    A = 1 # Rock
    B = 2 # Paper
    C = 3 # Scissors


class Outcome(Enum):
    LOST = 0
    DRAW = 3
    WIN = 6


shape_score_table = {
    YourMove.X: 1,
    OpponentMove.A: 1,
    YourMove.Y: 2,
    OpponentMove.B: 2,
    YourMove.Z: 3,
    OpponentMove.C: 3
}


outcome_table = {
    (YourMove.X, OpponentMove.A): Outcome.DRAW, # Same shape
    (YourMove.X, OpponentMove.B): Outcome.LOST, # Their Paper defeats your Rock
    (YourMove.X, OpponentMove.C): Outcome.WIN, # Your Rock defeats their Scissors

    (YourMove.Y, OpponentMove.B): Outcome.DRAW, # Same shape
    (YourMove.Y, OpponentMove.A): Outcome.WIN, # Your Paper defeats their Rock
    (YourMove.Y, OpponentMove.C): Outcome.LOST, # Their Scissors defeats your Paper

    (YourMove.Z, OpponentMove.C): Outcome.DRAW, # Same shape
    (YourMove.Z, OpponentMove.A): Outcome.LOST, # Their Rock defeats your Scissors
    (YourMove.Z, OpponentMove.B): Outcome.WIN, # Your Scissors defeats thir Paper
}


win_score_table = {
    Outcome.DRAW: 3,
    Outcome.WIN: 6,
    Outcome.LOST: 0
}


def score_single_round(your_move: YourMove, their_move: OpponentMove) -> tuple[int, int]:
    """
    Calculated a single round score. Returns (your_score, their_score) as ints.
    """
    your_score = 0
    their_score = 0

    # Calculate their shape score
    your_score += shape_score_table[your_move]
    their_score += shape_score_table[their_move]

    outcome = outcome_table[(your_move, their_move)]
    if outcome == Outcome.DRAW:
        your_score += win_score_table[Outcome.DRAW]
        their_score += win_score_table[Outcome.DRAW]
    elif outcome == Outcome.WIN:
        your_score += win_score_table[Outcome.WIN]
        their_score += win_score_table[Outcome.LOST]
    else:
        your_score += win_score_table[Outcome.LOST]
        their_score += win_score_table[Outcome.WIN]

    return (your_score, their_score)


def calculate_total_score(moves: str) -> tuple[int, int]:
    """
    Calculated a collection of RPS games. Returns (your_total_score, their_total_score) as ints.
    """
    your_total_score = 0
    their_total_score = 0

    games = moves.split(os.linesep)
    for game in games:
        sanitized_game = game.strip()
        move = sanitized_game.split(" ")
        if (len(move) < 2):
            continue
        their_move = OpponentMove[move[0]]
        your_move = YourMove[move[1]]
        game_result = score_single_round(your_move, their_move)
        your_total_score += game_result[0]
        their_total_score += game_result[1]
    return (your_total_score, their_total_score)


class TestHarness(unittest.TestCase):

    def test_score_single_round(self):
        result = score_single_round(YourMove.Y, OpponentMove.A)
        self.assertEqual(result[0], 8)
        self.assertEqual(result[1], 1)


    def test_calculate_total_score(self):
        data = """A Y
        B X
        C Z
        """
        self.assertEqual(calculate_total_score(data), (15, 15))


def main():
    with open("input.dat", "r") as f_hdl:
        str_data = f_hdl.read()
        print(calculate_total_score(str_data))
        

if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#    unittest.main()
