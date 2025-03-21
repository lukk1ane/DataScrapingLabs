def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except ValueError:
        return "Error: Invalid value provided."

if __name__ == "__main__":
    test_cases = [
        (10, 2),
        (10, 0),
        (10, 'a'),
        (10, 5)
    ]

    for a, b in test_cases:
        # testing on invalid values (string, zero division)
        print(f"Dividing {a} by {b}: {safe_divide(a, b)}")