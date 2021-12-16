from sys import argv
from typing import Iterable, Tuple
import networkx as nx
import numpy as np
from colorama import Style


def neighbours(p: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
    y, x = p
    return (y-1, x), (y, x-1), (y, x+1), (y+1, x)


def generate_graph(base_risk: np.ndarray) -> nx.DiGraph:
    h, w = base_risk.shape

    def in_bounds(p: Tuple[int, int]):
        y, x = p
        return 0 <= y < h and 0 <= x < w

    g = nx.DiGraph(shape=(h, w))
    for p in np.ndindex(base_risk.shape):
        for n in filter(in_bounds, neighbours(p)):
            g.add_edge(p, n, weight=base_risk[n])

    return g


def generate_big_graph(base_risk: np.ndarray, scale: int) -> nx.DiGraph:
    h, w = base_risk.shape
    big_h, big_w = h * scale, w * scale

    def in_bounds(p: Tuple[int, int]):
        y, x = p
        return 0 <= y < big_h and 0 <= x < big_w

    g = nx.DiGraph(shape=(big_h, big_w))
    for ty, tx in np.ndindex(scale, scale):
        risks = (base_risk + (ty+tx-1)) % 9 + 1

        for p in np.ndindex(base_risk.shape):
            big_p = p[0] + ty * h, p[1] + tx * w
            for n in filter(in_bounds, neighbours(big_p)):
                g.add_edge(n, big_p, weight=risks[p])

    return g


base_risk = np.array([[int(c) for c in l.strip()] for l in open(argv[1])])

# first star

g = generate_graph(base_risk)
h, w = g.graph['shape']
min_length = nx.shortest_path_length(g, (0, 0), (h-1, w-1), weight='weight')
print(f'min risk on {h}x{w}: {Style.BRIGHT}{min_length}{Style.RESET_ALL}')

# second star

big_g = generate_big_graph(base_risk, 5)
h, w = big_g.graph['shape']
min_length = nx.shortest_path_length(big_g, (0, 0), (h-1, w-1), weight='weight')
print(f'min risk on {h}x{w}: {Style.BRIGHT}{min_length}{Style.RESET_ALL}')
