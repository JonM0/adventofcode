from colorama import Style
from collections import deque
from typing import Iterable, Tuple
import numpy as np
from sys import argv


def neighbors(p: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    y, x = p
    return ((y-1, x), (y+1, x), (y, x-1), (y, x+1))


class CaveFloor:
    def __init__(self, repr: Iterable[str]):
        self.heigth_map = np.array([[int(n) for n in l.strip()] for l in repr])

        self.h, self.w = self.heigth_map.shape

        self.low_points = []
        for p in np.ndindex(self.heigth_map.shape):
            h = self.heigth_map[p]
            if all(not self.within_bounds(n) or h < self.heigth_map[n] for n in neighbors(p)):
                self.low_points.append(p)

        self.basins = [Basin(self, p) for p in self.low_points]

    @property
    def low_point_risk_levels(self) -> int:
        return np.sum(self.heigth_map[tuple(zip(*self.low_points))]) + len(self.low_points)

    @property
    def largest_3_basins_size_prod(self) -> int:
        from heapq import nlargest
        return np.product(nlargest(3, (b.size for b in cave_floor.basins)))

    def within_bounds(self, point: Tuple[int, int]) -> bool:
        y, x = point
        return 0 <= y < self.h and 0 <= x < self.w


class Basin:
    def __init__(self, cave_floor: CaveFloor, low_point: Tuple[int, int]):
        self.cave_floor = cave_floor
        self.low_point = low_point
        self.points = set()

        # # cleaner but much slower
        # from skimage.morphology import flood
        # self.points = flood(cave_floor.heigth_map < 9, low_point, connectivity=1)

        q = deque([low_point])
        while q:
            p = q.popleft()
            if cave_floor.within_bounds(p) and p not in self.points and cave_floor.heigth_map[p] != 9:
                self.points.add(p)
                q += neighbors(p)

    @property
    def size(self) -> int:
        return len(self.points)


cave_floor = CaveFloor(open(argv[1]))


print(f'sum of risk levels for low points: {Style.BRIGHT}{cave_floor.low_point_risk_levels}{Style.RESET_ALL}')

print(f'product of 3 biggest basin sizes: {Style.BRIGHT}{cave_floor.largest_3_basins_size_prod}{Style.RESET_ALL}')
