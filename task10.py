import random
from collections import Counter

random_numbers = [random.randint(1, 100) for _ in range(20)]

max_value = max(random_numbers)
min_value = min(random_numbers)
total_sum = sum(random_numbers)
average = total_sum / len(random_numbers)

frequency = Counter(random_numbers)
most_frequent_number = frequency.most_common(1)[0]

print("Random Numbers:", random_numbers)
print("Maximum Value:", max_value)
print("Minimum Value:", min_value)
print("Sum:", total_sum)
print("Average:", average)
print("Most Frequent Number:", most_frequent_number[0], "with frequency:", most_frequent_number[1])