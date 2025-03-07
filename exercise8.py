numbers = list(range(1, 51))

even_numbers = [num for num in numbers if num % 2 == 0]
odd_squares = [num ** 2 for num in numbers if num % 2 != 0]
divisible_by_5 = [num for num in numbers if num % 5 == 0]

print(f"Even Numbers: {even_numbers}")
print(f"Squares of Odd Numbers: {odd_squares}")
print(f"Numbers Divisible by 5: {divisible_by_5}")
