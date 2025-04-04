def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)

numbers = list(range(1, 51))

even_numbers = [num for num in numbers if num % 2 == 0]

odd_squares = [num**2 for num in numbers if num % 2 != 0]

divisible_by_5 = [num for num in numbers if num % 5 == 0]

print("Even Numbers:", even_numbers)
print("Squares of Odd Numbers:", odd_squares)
print("Numbers Divisible by 5:", divisible_by_5)

def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except ValueError:
        return "Error: Invalid input"

# Test cases
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("10", 2))