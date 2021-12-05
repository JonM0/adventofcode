import re

move_matcher = re.compile(r'([duf])\w+ (\d+)')

input = [(m[1], int(m[2])) for m in map(move_matcher.match, open('input.txt'))]

# first star
x, y = 0, 0
for dir, n in input:
    if dir == 'd':
        y += n
    elif dir == 'u':
        y -= n
    else:
        x += n

print('- first star')
print(f'final position: ({x}, {y})')
print(f'product: {x*y}')

# second star
x, y = 0, 0
aim = 0
for dir, n in input:
    if dir == 'd':
        aim += n
    elif dir == 'u':
        aim -= n
    else:
        x += n
        y += aim*n

print('- second star')
print(f'final position: ({x}, {y})')
print(f'product: {x*y}')

