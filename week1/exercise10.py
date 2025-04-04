import random
from collections import Counter

random_integers = [random.randint(1, 100) for _ in range(20)]

max_value = max(random_integers)
min_value = min(random_integers)
sum_values = sum(random_integers)
average_value = sum_values / len(random_integers)

frequency = Counter(random_integers)
most_frequent = frequency.most_common(1)[0][0]

print(f"Maximum Value: {max_value}")
print(f"Minimum Value: {min_value}")
print(f"Sum: {sum_values}")
print(f"Average: {average_value:.2f}")
print(f"Most Frequent Number: {most_frequent}")
