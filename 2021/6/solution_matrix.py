from collections import Counter
import numpy as np
from sys import argv

data = Counter(int(n) for n in open(argv[1]).readline().split(','))

transition = np.matrix([[0, 1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [1, 0, 0, 0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0]])

start_gen = np.vstack([data[i] for i in range(9)])

# first star
print(f'after 80 generations: {sum(transition ** 80 * start_gen)}')

# second star
print(f'after 256 generations: {sum(transition ** 256 * start_gen)}')
