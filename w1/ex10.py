import random

ints = [random.randint(1,15) for _ in range(20)]

print(ints)
print(f'max val: {max(ints)}')
print(f'min val: {min(ints)}')
print(f'sum: {sum(ints)}')
print(f'average: {sum(ints)/len(ints)}')
print(f'most frequent:{max(set(ints), key=ints.count)}')