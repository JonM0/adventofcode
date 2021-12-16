from sys import argv
from collections import Counter, defaultdict
from colorama import Style

data = open(argv[1]).readlines()


class Polymer:
    def __init__(self, template: str, rules):
        self.rules = rules
        self.counts = Counter(template)
        self.couples = Counter(zip(template, template[1:]))
        self.steps = 0

    def step(self, n: int = 1):
        for _ in range(n):
            new_couples = defaultdict(lambda: 0)
            for (a, b), count in self.couples.items():
                new = self.rules[a, b]
                self.counts[new] += count
                new_couples[a, new] += count
                new_couples[new, b] += count
            self.couples = new_couples
            self.steps += 1

    @property
    def quantity_delta(self) -> int:
        return max(self.counts.values()) - min(self.counts.values())


polymer = Polymer(data[0].strip(), {(l[0], l[1]): l[6] for l in data[2:]})

polymer.step(10)
print(f'difference after {polymer.steps} steps: {Style.BRIGHT}{polymer.quantity_delta}{Style.RESET_ALL}')

polymer.step(30)
print(f'difference after {polymer.steps} steps: {Style.BRIGHT}{polymer.quantity_delta}{Style.RESET_ALL}')
