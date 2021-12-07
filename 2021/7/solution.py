import statistics as st

data = [int(n) for n in open('input.txt').readline().split(',')]


def dist(a: int, b: int) -> int:
    return abs(a - b)


def half_square(d: int) -> int:
    return int(d * (d + 1) / 2)


def abs_error(pos: int) -> int:
    return sum(dist(pos, x) for x in data)


def hsq_error(pos: int) -> int:
    return sum(half_square(dist(pos, x)) for x in data)


# first star
median = int(st.median(data))
print(abs_error(median))  # median optimizes sum abs error

# second star
mean = int(st.mean(data))
print(hsq_error(mean))  # mean optimizes sum square error
