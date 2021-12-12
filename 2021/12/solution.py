from colorama import Style
from sys import argv
from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple
from functools import lru_cache


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.adj: List[Cave] = []
        self.is_big = self.name.isupper()

    def __repr__(self) -> str:
        return f"Cave('{self.name}')"


class CaveMap:
    def __init__(self, edges: Iterable[Tuple[str, str]]):
        cave_named: Dict[str, Cave] = keydefaultdict(Cave)
        for a, b in edges:
            cave_named[a].adj.append(cave_named[b])
            cave_named[b].adj.append(cave_named[a])
        assert 'start' in cave_named and 'end' in cave_named
        self.caves = list(cave_named.values())
        self.start = cave_named['start']
        self.end = cave_named['end']

    @lru_cache(maxsize=None)
    def paths_count(self, start: Cave, end: Cave, excluding: Set[Cave] = frozenset(), can_visit_one_twice: bool = False) -> int:
        if start == end:
            return 1
        if start in excluding:
            if not can_visit_one_twice or start in (self.start, self.end):
                return 0
            else:
                can_visit_one_twice = False
        if not start.is_big:
            excluding = excluding | {start}
        return sum(self.paths_count(a, end, excluding, can_visit_one_twice) for a in start.adj)


cm = CaveMap(l.strip().split('-') for l in open(argv[1]))

print(f'first star: {Style.BRIGHT}{cm.paths_count(cm.start, cm.end)}{Style.RESET_ALL}')
print(f'second star: {Style.BRIGHT}{cm.paths_count(cm.start, cm.end, can_visit_one_twice=True)}{Style.RESET_ALL}')

print(cm.paths_count.cache_info())
