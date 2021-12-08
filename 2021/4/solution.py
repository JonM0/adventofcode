from typing import List, Callable
import numpy as np
from sys import argv

input = open(argv[1]).readlines()

extraction_order = list(map(int, input[0].split(',')))
extraction_time_map = {n: i for i, n in enumerate(extraction_order)}
vect_extraction_time_map: Callable[[int],int] = np.vectorize(extraction_time_map.get)

class Board:
    def __init__(self, string_repr: List[str]):
        self.values = np.array([list(map(int, l.split()))
                               for l in string_repr])
        assert self.values.shape == (5, 5)

        self.extraction_time: np.ndarray = vect_extraction_time_map(self.values)

        self.column_completion = self.extraction_time.max(axis=0)
        self.row_completion = self.extraction_time.max(axis=1)

        self.bingo_time: int = min(min(self.column_completion),
                                   min(self.row_completion))

    @property
    def score(self) -> int:
        sum_unmarked = sum(self.values[self.extraction_time > self.bingo_time])
        bingo_num = extraction_order[self.bingo_time]
        return sum_unmarked * bingo_num


boards = [Board(input[i:i+5]) for i in range(2, len(input), 6)]

# first star
winning_board = min(boards, key=lambda b: b.bingo_time)
print(f'winning score: {winning_board.score}')

# second star
losing_board = max(boards, key=lambda b: b.bingo_time)
print(f'losing score: {losing_board.score}')
