from collections import Counter
from sys import argv

first_star_gens = 80
second_star_gens = 256
data = Counter(int(n) for n in open(argv[1]).readline().split(','))

def next_gen(g):
    return (g[1], g[2], g[3], g[4], g[5], g[6], g[0]+g[7], g[8], g[0])

# first star
gen = data
for _ in range(first_star_gens):
    gen = next_gen(gen)

print(f'after {first_star_gens} generations: {sum(gen)}')

# second star
for _ in range(first_star_gens, second_star_gens):
    gen = next_gen(gen)

print(f'after {second_star_gens} generations: {sum(gen)}')