def safe_division(x, y):
    try:
        return x / y

    except ZeroDivisionError:
        return "Error: Division by zero!"

    except ValueError:
        return "Error: Invalid input!"


if __name__ == '__main__':
    print(safe_division(2, 1))
    print(safe_division(5, 0))
    print(safe_division(5, int('a')))
    print(safe_division(int('b'), 10))
