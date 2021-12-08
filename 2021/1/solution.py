from sys import argv

input = [int(l) for l in open(argv[1])]
inc_count = sum(x < y for (x, y) in zip(input, input[1:]))
print(f'Increases: {inc_count}')

sliding3 = list(map(sum, zip(input, input[1:], input[2:])))
inc_count_s3 = sum(x < y for (x, y) in zip(sliding3, sliding3[1:]))
print(f'Increases in sliding3: {inc_count_s3}')
