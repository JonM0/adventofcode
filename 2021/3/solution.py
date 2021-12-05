from typing import List, Tuple

input = [tuple(map(int, l.strip('\n'))) for l in open('input.txt')]

def columnwise_mode(l: List[Tuple[int]]) -> Tuple[int]:
    l_unzipped = list(zip(*l)) # unzip list
    return tuple(
        int(s >= len(l)/2) 
        for s in map(sum, l_unzipped)) # find most common for each column

def bittuple_to_int(t: Tuple[int]) -> int:
    return int(str.join('', map(str, t)), base=2)

# first star
col_mode = columnwise_mode(input)
gamma = bittuple_to_int(col_mode)
epsilon = gamma ^ (2**len(col_mode)-1)

print('- first star')
print(f'gamma: {gamma}, epsilon: {epsilon}')
print(f'power cons: {gamma*epsilon}')

# second star
oxy_cand = list(input)
i = 0
while len(oxy_cand) > 1:
    mode = columnwise_mode(oxy_cand)[i]
    oxy_cand = list(filter(lambda c: c[i] == mode, oxy_cand))
    i += 1
oxygen = bittuple_to_int(oxy_cand[0])

co2_cand = list(input)
i = 0
while len(co2_cand) > 1:
    mode = 1 - columnwise_mode(co2_cand)[i]
    co2_cand = list(filter(lambda c: c[i] == mode, co2_cand))
    i += 1
co2 = bittuple_to_int(co2_cand[0])

print('- second star')
print(f'oxygen: {oxygen}, co2: {co2}')
print(f'power cons: {oxygen*co2}')