import os
import random
import numpy as np
from collections import Counter

# ----------------------------
# Exercise 1: File Reading and Data Extraction
# ----------------------------
def exercise1_read_file(filename="data.txt"):
    """
    Reads a file and counts the number of lines, words, and characters.
    Returns a dictionary with the counts and a list of lines for later use.
    Handles FileNotFoundError if the file is missing.
    """
    try:
        with open(filename, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None

    lines = data.splitlines()
    words = data.split()
    characters = len(data)
    counts = {
        'line_count': len(lines),
        'word_count': len(words),
        'character_count': characters
    }
    return counts, lines

# ----------------------------
# Exercise 2: Student Scores Dictionary
# ----------------------------
def create_student_scores(sample_names):
    """
    Create a dictionary of student names and assign random scores (0-100).
    """
    students = {}
    for name in sample_names:
        students[name] = random.randint(0, 100)
    return students

def highest_scoring_student(students):
    """
    Finds the student with the highest score.
    Returns a tuple (student_name, score).
    """
    return max(students.items(), key=lambda item: item[1])

def average_score(students):
    """
    Computes the average score of all students.
    """
    return sum(students.values()) / len(students)

def students_above_average(students):
    """
    Returns a list of student names whose scores are above the average.
    """
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]

# ----------------------------
# Exercise 3: Car Data and Driving Simulation
# ----------------------------
def drive(car, km):
    """
    Simulates driving a car by updating its mileage.
    """
    if 'mileage' in car:
        car['mileage'] += km
    else:
        print("Error: Car does not have mileage information!")

# ----------------------------
# Exercise 4: Mileage Statistics using NumPy
# ----------------------------
def mileage_statistics(cars):
    """
    Extracts mileage values from the list of cars, converts them into a NumPy array,
    and computes total, maximum, minimum, and mean mileage.
    """
    mileage_values = np.array([car['mileage'] for car in cars])
    total_mileage = np.sum(mileage_values)
    max_mileage = np.max(mileage_values)
    min_mileage = np.min(mileage_values)
    mean_mileage = np.mean(mileage_values)
    return total_mileage, max_mileage, min_mileage, mean_mileage

# ----------------------------
# Exercise 5: Unique Car Brands Set
# ----------------------------
def car_brands_set(cars):
    """
    Extracts unique car brands from the list of cars into a set.
    Then adds new brands, removes one, and checks for 'Tesla'.
    """
    brands = {car['brand'] for car in cars}
    # Add new brands
    brands.add("BMW")
    brands.add("Audi")
    # Remove a brand (example: remove "Ford" if it exists)
    brands.discard("Ford")
    # Check if "Tesla" is in the set
    tesla_check = "Tesla" in brands
    return brands, tesla_check

# ----------------------------
# Exercise 6: Animal Classes with Inheritance
# ----------------------------
class Animal:
    def make_sound(self):
        """
        Base method for making a sound.
        """
        pass

class Dog(Animal):
    def make_sound(self):
        print("Woof!")

class Cat(Animal):
    def make_sound(self):
        print("Meow!")

def animal_sounds():
    """
    Creates a list of animals and calls make_sound() on each.
    """
    animals = [Dog(), Cat(), Dog()]
    for animal in animals:
        animal.make_sound()

# ----------------------------
# Exercise 7: Fibonacci Generator
# ----------------------------
def fibonacci(n):
    """
    Generator function that yields the first n Fibonacci numbers.
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def print_fibonacci(n=10):
    """
    Prints the first n Fibonacci numbers.
    """
    for num in fibonacci(n):
        print(num, end=' ')
    print()  # for newline

# ----------------------------
# Exercise 8: List Comprehensions on Numbers 1 to 50
# ----------------------------
def list_comprehensions():
    numbers = list(range(1, 51))
    evens = [num for num in numbers if num % 2 == 0]
    squares_odd = [num ** 2 for num in numbers if num % 2 != 0]
    divisible_by_5 = [num for num in numbers if num % 5 == 0]
    return numbers, evens, squares_odd, divisible_by_5

# ----------------------------
# Exercise 9: Safe Division with Exception Handling
# ----------------------------
def safe_divide(a, b):
    """
    Divides two numbers while safely handling division by zero and type errors.
    """
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Division by zero!")
        return None
    except TypeError:
        print("Error: Invalid input type for division!")
        return None
    return result

# ----------------------------
# Exercise 10: Random Integers Statistics
# ----------------------------
def random_integers_statistics():
    """
    Creates a list of 20 random integers (range 1-100) and computes:
      - Maximum and minimum values.
      - Sum and average.
      - The most frequent number.
    """
    random_integers = [random.randint(1, 100) for _ in range(20)]
    max_val = max(random_integers)
    min_val = min(random_integers)
    total = sum(random_integers)
    average = total / len(random_integers)
    counter = Counter(random_integers)
    most_common_num = counter.most_common(1)[0][0]
    return random_integers, max_val, min_val, total, average, most_common_num

# ----------------------------
# Main Function to Run Exercises
# ----------------------------
def main():
    print("=== Exercise 1: File Reading ===")
    counts, lines = exercise1_read_file()
    if counts:
        print("File Data:", counts)
    else:
        # If file not found, create some sample data for later use.
        sample_text = "Alice\nBob\nCharlie\nDavid\nEve"
        lines = sample_text.splitlines()
        counts = {
            'line_count': len(lines),
            'word_count': len(sample_text.split()),
            'character_count': len(sample_text)
        }
        print("Using sample data:", counts)

    print("\n=== Exercise 2: Student Scores ===")
    # Use the lines extracted (or sample names) from Exercise 1 as student names.
    sample_names = [line.strip() for line in lines if line.strip()]
    students = create_student_scores(sample_names)
    print("Student Scores:", students)
    top_student = highest_scoring_student(students)
    print("Highest Scoring Student:", top_student)
    avg = average_score(students)
    print("Average Score:", avg)
    above_avg = students_above_average(students)
    print("Students above average:", above_avg)

    print("\n=== Exercise 3: Car Data and Driving Simulation ===")
    cars = [
        {"brand": "Toyota", "model": "Corolla", "year": 2015, "mileage": 50000},
        {"brand": "Ford", "model": "Fiesta", "year": 2012, "mileage": 75000},
        {"brand": "Honda", "model": "Civic", "year": 2018, "mileage": 30000}
    ]
    # Simulate driving
    drive(cars[0], 100)
    drive(cars[1], 50)
    drive(cars[2], 200)
    print("Updated Cars Data:")
    for car in cars:
        print(car)

    print("\n=== Exercise 4: Mileage Statistics ===")
    total_mileage, max_mileage, min_mileage, mean_mileage = mileage_statistics(cars)
    print(f"Total Mileage: {total_mileage}")
    print(f"Max Mileage: {max_mileage}")
    print(f"Min Mileage: {min_mileage}")
    print(f"Mean Mileage: {mean_mileage}")

    print("\n=== Exercise 5: Car Brands Set ===")
    brands, tesla_exists = car_brands_set(cars)
    print("Car Brands Set:", brands)
    print("Is Tesla in the set?", tesla_exists)

    print("\n=== Exercise 6: Animal Sounds ===")
    animal_sounds()

    print("\n=== Exercise 7: Fibonacci Generator ===")
    print("First 10 Fibonacci Numbers:")
    print_fibonacci(10)

    print("\n=== Exercise 8: List Comprehensions ===")
    numbers, evens, squares_odd, divisible_by_5 = list_comprehensions()
    print("Numbers 1 to 50:", numbers)
    print("Even Numbers:", evens)
    print("Squares of Odd Numbers:", squares_odd)
    print("Numbers Divisible by 5:", divisible_by_5)

    print("\n=== Exercise 9: Safe Division ===")
    # Test safe_divide with various cases
    print("10 / 2 =", safe_divide(10, 2))
    print("10 / 0 =", safe_divide(10, 0))
    print("10 / 'a' =", safe_divide(10, 'a'))

    print("\n=== Exercise 10: Random Integers Statistics ===")
    random_ints, max_val, min_val, total, average, most_common_num = random_integers_statistics()
    print("Random Integers:", random_ints)
    print(f"Max: {max_val}, Min: {min_val}")
    print(f"Sum: {total}, Average: {average}")
    print("Most Frequent Number:", most_common_num)

if __name__ == "__main__":
    main()
