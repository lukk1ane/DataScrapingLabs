def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "cannot divide by zero."
    except ValueError:
        return "valueerror"

print(safe_divide(10, 0))
print(safe_divide(3, 2))
