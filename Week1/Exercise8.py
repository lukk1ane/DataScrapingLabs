nums = list(range(1, 51))

# A list of even numbers
even_nums = [num for num in nums if num % 2 == 0]
# print(even_nums)

# A list of squares of odd numbers
square_of_odds = [num ** 2 for num in nums if num % 2 == 1]
# print(square_of_odds)

# A list of numbers divisible by 5.
divisible_by_five = [num for num in nums if num % 5 == 0]
# print(divisible_by_five)