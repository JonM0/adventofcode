from __future__ import annotations
from typing import Iterable, List
from sys import argv

standard_signals = {0: set('abcefg'), 1: set('cf'),     2: set('acdeg'), 3: set('acdfg'),   4: set('bcdf'),
                    5: set('abdfg'),  6: set('abdefg'), 7: set('acf'),   8: set('abcdefg'), 9: set('abcdfg')}

digit_len = {d: len(s) for d, s in standard_signals.items()}

digits_long = {i: {d for d, l in digit_len.items() if l == i}
               for i in range(2, 8)}

digit_contains = {d: {x for x, p in standard_signals.items() if p < standard_signals[d]}
                  for d in range(10)}
digit_contained_in = {d: {x for x, p in standard_signals.items() if p > standard_signals[d]}
                      for d in range(10)}


def sorted_str(s: Iterable[str]) -> str:
    return str.join('', sorted(s))


class DigitPattern:
    def __init__(self, signals: Iterable[str]):
        self.signals = set(signals)
        self.candidates = set(digits_long[len(self.signals)])
        self.true_digit = None

        self.solve([])

    def solve(self, solved: Iterable[DigitPattern]) -> None:
        for d in solved:
            self.candidates -= {d.true_digit}
            if self.signals > d.signals:
                self.candidates &= digit_contained_in[d.true_digit]
            if self.signals < d.signals:
                self.candidates &= digit_contains[d.true_digit]

        if len(self.candidates) == 1:
            (self.true_digit,) = self.candidates

    @property
    def is_solved(self) -> bool:
        return self.true_digit != None


class SignalPattern:
    def __init__(self, digit_patterns):
        self.patterns = [DigitPattern(x) for x in digit_patterns.split()]

        unsolved = set(self.patterns)
        solved = set()

        while(unsolved):
            solved |= {d for d in unsolved if d.is_solved}
            unsolved -= solved

            for d in unsolved:
                d.solve(solved)

        self.pattern_map = {sorted_str(p.signals): p.true_digit
                            for p in self.patterns}

    def decode_digit(self, pattern: str) -> int:
        return self.pattern_map[pattern]

    def decode_number(self, pattern: List[str]) -> int:
        return int(str.join('', map(str, map(self.decode_digit, pattern))))


def process_input(line: str):
    pattern, output = line.split('|')
    return (SignalPattern(pattern),
            tuple(sorted_str(x) for x in output.split()))


data = list(map(process_input, open(argv[1])))

# first star
easy_digits = {next(iter(ds)) for ds in digits_long.values() if len(ds) == 1}

tot_easy_digits = sum(
    sum(d in easy_digits for d in map(p.decode_digit, o))
    for p, o in data)
print(f'instances of easy digits: {tot_easy_digits}')

# second star
sum_numbers = sum(p.decode_number(o) for p, o in data)
print(f'sum of all numbers: {sum_numbers}')
