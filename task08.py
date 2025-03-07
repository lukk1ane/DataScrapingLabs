numbers = list(range(1, 51))

even_numbers = [num for num in numbers if num % 2 == 0]
squares_of_odd_numbers = [num ** 2 for num in numbers if num % 2 != 0]
numbers_divisible_by_5 = [num for num in numbers if num % 5 == 0]

print("Even Numbers:", even_numbers)
print("Squares of Odd Numbers:", squares_of_odd_numbers)
print("Numbers Divisible by 5:", numbers_divisible_by_5)