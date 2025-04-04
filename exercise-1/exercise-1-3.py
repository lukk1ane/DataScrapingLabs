import random
from collections import Counter

random_numbers = [random.randint(1, 100) for _ in range(20)]

max_value = max(random_numbers)
min_value = min(random_numbers)

sum_values = sum(random_numbers)
average_value = sum_values / len(random_numbers)

frequent_number = Counter(random_numbers).most_common(1)[0]

print("Random Numbers:", random_numbers)
print("Max Value:", max_value)
print("Min Value:", min_value)
print("Sum:", sum_values)
print("Average:", average_value)
print("Most Frequent Number:", frequent_number)
