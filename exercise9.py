def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except ValueError:
        return "Error: Invalid input values."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    else:
        return result


print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide('10', 2))
print(safe_divide(10, 'a'))
