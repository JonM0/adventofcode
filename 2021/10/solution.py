from colorama import Style
from sys import argv
from collections import deque
from cached_property import cached_property
from statistics import median

chunk_start = set('([{<')
corresponding = {'(': ')', '[': ']', '{': '}', '<': '>'}

score_err = {')': 3, ']': 57, '}': 1197, '>': 25137}
score_compl = {'(': 1, '[': 2, '{': 3, '<': 4}


class CodeLine:
    def __init__(self, line: str):
        self.line = line.strip()

        s = deque()
        self.first_error = None
        for c in self.line:
            if c in chunk_start:
                s.appendleft(c)
            elif len(s) == 0 or corresponding[s.popleft()] != c:
                self.first_error = c
                break

        self.missing_closing = list(s)

    def __repr__(self) -> str:
        return f"CodeLine('{self.line}')"

    @property
    def corrupted(self):
        return self.first_error is not None

    @property
    def score_corruption(self):
        return score_err[self.first_error] if self.corrupted else 0

    @cached_property
    def score_completion(self):
        score = 0
        if not self.corrupted:
            for c in self.missing_closing:
                score = score * 5 + score_compl[c]
        return score


data = [CodeLine(l) for l in open(argv[1])]

print(f'total syntax error score: {Style.BRIGHT}{sum(l.score_corruption for l in data)}{Style.RESET_ALL}')

print(f'middle completion score:  {Style.BRIGHT}{median(l.score_completion for l in data if not l.corrupted)}{Style.RESET_ALL}')
