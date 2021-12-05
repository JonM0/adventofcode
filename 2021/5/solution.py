import re
import numpy as np

input_matcher = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')


def inclusive_range(start, stop, step=None):
    if step == None:
        step = 1 if start <= stop else -1
    return range(start, stop + step, step)


class Line:
    def __init__(self, str_repr: str) -> None:
        m = input_matcher.match(str_repr)
        self.a = int(m[1]), int(m[2])
        self.b = int(m[3]), int(m[4])

    def __repr__(self) -> str:
        (ax, ay), (bx, by) = self.a, self.b
        return f"Line('{ax},{ay} -> {bx},{by}')"

    @property
    def diagonal(self):
        (ax, ay), (bx, by) = self.a, self.b
        return ay != by and ax != bx

    @property
    def all_points(self):
        (ax, ay), (bx, by) = self.a, self.b
        return (np.array(inclusive_range(ax, bx)),
                np.array(inclusive_range(ay, by)))


ocean_map = np.zeros(shape=(1000, 1000))
lines = list(map(Line, open('input.txt')))

# first star
for l in lines:
    if not l.diagonal:
        ocean_map[l.all_points] += 1

print('- with only horizontal or vertical lines')
print(f'danger points: {np.count_nonzero(ocean_map > 1)}')

# second star
for l in lines:
    if l.diagonal:
        ocean_map[l.all_points] += 1

print('- using all lines')
print(f'danger points: {np.count_nonzero(ocean_map > 1)}')
