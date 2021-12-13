from sys import argv
from typing import Iterable, List, Tuple
import numpy as np
from colorama import Style

data = open(argv[1]).readlines()


def mirror(x, f):
    return f - abs(f - x)


class Page:
    def __init__(self, marks: List[Tuple[int, int]]):
        marks = tuple(map(np.array, zip(*marks)))
        self.marks = list(reversed(marks))

    def fold(self, axis, at):
        self.marks[axis] = at - abs(self.marks[axis] - at)

    @property
    def as_image(self):
        size = tuple(max(axis) + 1 for axis in self.marks)
        image = np.zeros(size, dtype=np.int8)
        image[tuple(self.marks)] = 1
        return image

    @property
    def dots_visible(self):
        return np.count_nonzero(self.as_image)


splitter = data.index('\n')
page = Page([tuple(map(int, l.strip().split(',')))
             for l in data[:splitter]])

folds = [(0 if a[-1] == 'y' else 1, int(n))
         for a, n in
         (l.split('=') for l in data[splitter+1:])]

for a, c in folds[0:1]:
    page.fold(a, c)


print(f'dots visible after 1 fold: {Style.BRIGHT}{page.dots_visible}{Style.RESET_ALL}')


for a, c in folds[1:]:
    page.fold(a, c)

printchars = {1: '#', 0: ' '}
print('pattern after all folds:')
print('\n'.join(''.join(map(printchars.get, l)) for l in page.as_image))
