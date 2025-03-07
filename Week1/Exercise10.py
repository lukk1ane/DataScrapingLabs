from random import randint
from collections import Counter


nums = [randint(1, 100) for _ in range(20)]
print(nums)

print("Max value:", max(nums))
print("Min value:", min(nums))
print("Sum:", sum(nums))
print("Average:", sum(nums) / len(nums))
print("Most frequent number:", Counter(nums).most_common(1)[0][0])