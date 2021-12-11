from colorama import Style
from typing import Iterable, List, Tuple
import numpy as np
from sys import argv


class CaveFloor:
    def __init__(self, starting_energy: List[List[int]]):
        starting_energy = np.array(starting_energy)
        self.octopus_matrix = np.vectorize(Octopus)(starting_energy)

        h, w = self.octopus_matrix.shape

        def neighbours(p: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
            y, x = p
            return (y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)

        def in_bounds(p):
            y, x = p
            return 0 <= y < h and 0 <= x < w

        for p in np.ndindex(self.octopus_matrix.shape):
            o = self.octopus_matrix[p]
            for n in filter(in_bounds, neighbours(p)):
                o.neighbours.append(self.octopus_matrix[n])

        self.octopuses: List[Octopus] = list(self.octopus_matrix.reshape(100))
        self.steps = 0

    def step(self, n: int = 1):
        for _ in range(n):
            for o in self.octopuses:
                o.increment()
            for o in self.octopuses:
                o.finalize()
            self.steps += 1

    def step_until_syncronized(self):
        while any(o.energy != 0 for o in self.octopuses):
            self.step()

    @property
    def flash_count(self) -> int:
        return sum(o.flash_count for o in self.octopuses)


class Octopus:
    def __init__(self, starting_energy: int):
        self.energy = starting_energy
        self.neighbours = []
        self.just_flashed = False
        self.flash_count = 0

    def __repr__(self) -> str:
        return f'Octopus({self.energy}, {len(self.neighbours)})'

    def finalize(self):
        self.just_flashed = False

    def increment(self):
        if not self.just_flashed:
            self.energy += 1
            if self.energy > 9:
                self.just_flashed = True
                self.flash_count += 1
                self.energy = 0
                for n in self.neighbours:
                    n.increment()


f = CaveFloor([[int(n) for n in l.strip()] for l in open(argv[1])])

f.step(100)
print(f'total flashes in 100 steps: {Style.BRIGHT}{f.flash_count}{Style.RESET_ALL}')

f.step_until_syncronized()
print(f'first syncronized step: {Style.BRIGHT}{f.steps}{Style.RESET_ALL}')
