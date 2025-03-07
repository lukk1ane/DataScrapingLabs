# exercise 1
def process_file():
    filename = "data.txt"
    try:
        with open(filename, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            line_count = len(lines)
            word_count = len(content.split())
            char_count = len(content)

            print(f"File: {filename}")
            print(f"Lines: {line_count}")
            print(f"Words: {word_count}")
            print(f"Characters: {char_count}")

            return {
                'lines': lines,
                'line_count': line_count,
                'word_count': word_count,
                'char_count': char_count,
                'content': content
            }
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None


# exercise 2
def student_scores_system(extracted_data=None):
    students = {"Gio": 97}

    if extracted_data and 'lines' in extracted_data:
        for line in extracted_data['lines']:
            words = line.split()
            if words and len(words[0]) > 3:
                import random
                name = words[0].capitalize()
                if name not in students:  # avoid duplicates
                    students[name] = random.randint(60, 100)

    def find_highest_scoring_student():
        return max(students.items(), key=lambda x: x[1])

    def compute_average_score():
        return sum(students.values()) / len(students) if students else 0

    def get_above_average_students():
        avg = compute_average_score()
        return [name for name, score in students.items() if score > avg]

    highest_student, highest_score = find_highest_scoring_student()
    average = compute_average_score()
    above_avg = get_above_average_students()

    print("\nStudent Scores System:")
    print(f"Students: {students}")
    print(f"Highest scoring student: {highest_student} with {highest_score}")
    print(f"Average score: {average:.2f}")
    print(f"Students above average: {above_avg}")

    return students


# exercise 3
def car_management_system():
    # Create a list of cars
    cars = [
        {"brand": "Toyota", "model": "Corolla", "year": 2020, "mileage": 15000},
        {"brand": "Honda", "model": "Civic", "year": 2019, "mileage": 20000},
        {"brand": "Ford", "model": "Mustang", "year": 2021, "mileage": 8000},
        {"brand": "BMW", "model": "X5", "year": 2018, "mileage": 35000},
        {"brand": "Tesla", "model": "Model 3", "year": 2022, "mileage": 10000}
    ]

    def drive(car, km):
        car["mileage"] += km
        return car
    print("\nCar Management System:")
    print("Original car data:")
    for car in cars:
        print(f"{car['brand']} {car['model']}: {car['mileage']} km")

    # Drive some cars
    drive(cars[0], 1500)
    drive(cars[2], 2000)
    drive(cars[4], 800)

    print("\nUpdated car data after driving:")
    for car in cars:
        print(f"{car['brand']} {car['model']}: {car['mileage']} km")

    return cars


# exercise 4
def numpy_operations(cars):
    import numpy as np

    mileage_array = np.array([car["mileage"] for car in cars])

    total_mileage = np.sum(mileage_array)
    max_mileage = np.max(mileage_array)
    min_mileage = np.min(mileage_array)
    mean_mileage = np.mean(mileage_array)

    print("\nNumPy Array Operations:")
    print(f"Mileage array: {mileage_array}")
    print(f"Total mileage: {total_mileage}")
    print(f"Maximum mileage: {max_mileage}")
    print(f"Minimum mileage: {min_mileage}")
    print(f"Mean mileage: {mean_mileage:.2f}")

    return mileage_array


# exercise 5
def set_operations(cars):
    car_brands = {car["brand"] for car in cars}

    print("\nSet Operations:")
    print(f"Original car brands set: {car_brands}")

    car_brands.add("Mercedes")
    car_brands.add("Audi")
    print(f"After adding new brands: {car_brands}")

    def remove_brand(brand):
        if brand in car_brands:
            car_brands.remove(brand)
    remove_brand("Honda")

    print(f"After removing 'Honda': {car_brands}")

    is_tesla_present = "Tesla" in car_brands
    print(f"Is 'Tesla' in the set? {is_tesla_present}")

    return car_brands


# exercise 6
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print(f"{self.name} makes a generic animal sound")


class Dog(Animal):
    def make_sound(self):
        print(f"{self.name} barks: Woof!")


class Cat(Animal):
    def make_sound(self):
        print(f"{self.name} meows: Meow!")


def animal_sounds_demo():
    animals = [
        Dog("Buddy"),
        Cat("Whiskers"),
        Dog("Max"),
        Cat("Mittens"),
        Animal("Mystery")
    ]

    print("\nAnimal Sounds Demo:")

    for animal in animals:
        animal.make_sound()

    return animals


# exercise 7
def fibonacci(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def fibonacci_demo():
    print("\nFibonacci Sequence:")
    # Generate and print the first 10 Fibonacci numbers
    fib_numbers = list(fibonacci(10))
    print(f"First 10 Fibonacci numbers: {fib_numbers}")
    return fib_numbers


# exercise 8
def list_comprehensions():
    numbers = list(range(1, 51))

    even_numbers = [n for n in numbers if n % 2 == 0]

    odd_squares = [n ** 2 for n in numbers if n % 2 != 0]

    divisible_by_5 = [n for n in numbers if n % 5 == 0]

    print("\nList Comprehensions:")
    print(f"Even numbers: {even_numbers}")
    print(f"Squares of odd numbers: {odd_squares}")
    print(f"Numbers divisible by 5: {divisible_by_5}")

    return {
        'even_numbers': even_numbers,
        'odd_squares': odd_squares,
        'divisible_by_5': divisible_by_5
    }


# exercise 9
def safe_divide(a, b):
    try:
        a, b = float(a), float(b)

        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        result = a / b
        return result
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return None
    except ValueError as e:
        print(f"Error: Invalid input - {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def safe_divide_demo():
    print("\nSafe Division Demo:")
    test_cases = [
        (10, 2),
        (5, 0),
        ("20", "5"),
        ("abc", 5),
        (15, "0"),
        (8, "abc")
    ]

    for a, b in test_cases:
        print(f"Dividing {a} by {b}: ", end="")
        result = safe_divide(a, b)
        if result is not None:
            print(f"Result = {result}")
        else:
            print("Failed")

    return test_cases


# exercise 10
def random_numbers_stats():
    import random
    from collections import Counter

    random_numbers = [random.randint(1, 100) for _ in range(20)]

    max_value = max(random_numbers)
    min_value = min(random_numbers)
    sum_value = sum(random_numbers)
    avg_value = sum_value / len(random_numbers)

    counter = Counter(random_numbers)
    most_common = counter.most_common(1)[0]

    print("\nRandom Numbers Statistics:")
    print(f"Random numbers: {random_numbers}")
    print(f"Maximum value: {max_value}")
    print(f"Minimum value: {min_value}")
    print(f"Sum: {sum_value}")
    print(f"Average: {avg_value:.2f}")
    print(f"Most frequent number: {most_common[0]} (appears {most_common[1]} times)")

    return {
        'numbers': random_numbers,
        'max': max_value,
        'min': min_value,
        'sum': sum_value,
        'avg': avg_value,
        'most_frequent': most_common
    }


# 1
extracted_data = process_file()

# 2
students = student_scores_system(extracted_data)

# 3
cars = car_management_system()

# 4
mileage_array = numpy_operations(cars)

# 5
car_brands = set_operations(cars)

# 6
animals = animal_sounds_demo()

# 7
fib_numbers = fibonacci_demo()

# 8
list_comp_results = list_comprehensions()

# 9
test_cases = safe_divide_demo()

# 10
random_stats = random_numbers_stats()
