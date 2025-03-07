import numpy as np
import random
from collections import Counter

# Exercise 1: File Reading and Statistics
def count_file_stats(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_chars = sum(len(line) for line in lines)
            return num_lines, num_words, num_chars
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

# Exercise 2: Student Scores
def highest_scoring_student(students):
    return max(students.items(), key=lambda x: x[1])

def average_score(students):
    return sum(students.values()) / len(students)

def above_average_students(students):
    avg = average_score(students)
    return {name: score for name, score in students.items() if score > avg}

# Exercise 3: Cars and Mileage
def drive(car, km):
    car['mileage'] += km

# Exercise 6: Animal Sounds
class Animal:
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        print("Woof!")

class Cat(Animal):
    def make_sound(self):
        print("Meow!")

# Exercise 7: Fibonacci Generator
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Exercise 9: Safe Division
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Division by zero.")
    except (ValueError, TypeError):
        print("Error: Invalid value or unsupported operand type.")

# Main Program
if __name__ == "__main__":
    # Exercise 1
    print("=== Exercise 1 ===")
    file_stats = count_file_stats('data.txt')
    if file_stats:
        print(f"Lines: {file_stats[0]}, Words: {file_stats[1]}, Characters: {file_stats[2]}")
        # Store the extracted data for later use
        stored_stats = {"lines": file_stats[0], "words": file_stats[1], "chars": file_stats[2]}
    else:
        stored_stats = {"lines": 0, "words": 0, "chars": 0}  # Default if file is missing

    # Exercise 2
    print("\n=== Exercise 2 ===")
    # Use the extracted data from Exercise 1 to create sample student names
    student_names = [f"Student_{i}" for i in range(1, stored_stats["lines"] + 1)]
    student_scores = [random.randint(50, 100) for _ in student_names]
    students = dict(zip(student_names, student_scores))  # Use a dictionary

    print("Students and scores:", students)
    print("Highest scoring student:", highest_scoring_student(students))
    print("Average score:", average_score(students))
    print("Students above average:", above_average_students(students))

    # Exercise 3
    print("\n=== Exercise 3 ===")
    cars = [
        {"brand": "Toyota", "model": "Corolla", "year": 2015, "mileage": 50000},
        {"brand": "Honda", "model": "Civic", "year": 2018, "mileage": 30000},
    ]
    drive(cars[0], 1000)
    print("Updated car mileage:", cars[0])

    # Exercise 4
    print("\n=== Exercise 4 ===")
    mileages = np.array([car['mileage'] for car in cars])
    print("Total mileage:", np.sum(mileages))
    print("Maximum mileage:", np.max(mileages))
    print("Minimum mileage:", np.min(mileages))
    print("Mean mileage:", np.mean(mileages))

    # Exercise 5
    print("\n=== Exercise 5 ===")
    unique_brands = set(car['brand'] for car in cars)
    unique_brands.add("Tesla")
    unique_brands.remove("Honda")
    print("Unique car brands:", unique_brands)
    print("Is Tesla in the set?", "Tesla" in unique_brands)

    # Exercise 6
    print("\n=== Exercise 6 ===")
    animals = [Dog(), Cat()]
    for animal in animals:
        animal.make_sound()

    # Exercise 7
    print("\n=== Exercise 7 ===")
    print("First 10 Fibonacci numbers:", list(fibonacci(10)))

    # Exercise 8
    print("\n=== Exercise 8 ===")
    numbers = list(range(1, 51))
    even_numbers = [x for x in numbers if x % 2 == 0]
    squares_of_odds = [x**2 for x in numbers if x % 2 != 0]
    divisible_by_5 = [x for x in numbers if x % 5 == 0]
    print("Even numbers:", even_numbers)
    print("Squares of odd numbers:", squares_of_odds)
    print("Numbers divisible by 5:", divisible_by_5)

    # Exercise 9
    print("\n=== Exercise 9 ===")
    print("Safe divide 10 / 2:", safe_divide(10, 2))
    print("Safe divide 10 / 0:", safe_divide(10, 0))
    print("Safe divide 10 / 'a':", safe_divide(10, 'a'))

    # Exercise 10
    print("\n=== Exercise 10 ===")
    random_numbers = [random.randint(1, 100) for _ in range(20)]
    print("Random numbers:", random_numbers)
    print("Maximum value:", max(random_numbers))
    print("Minimum value:", min(random_numbers))
    print("Sum:", sum(random_numbers))
    print("Average:", sum(random_numbers) / len(random_numbers))
    print("Most frequent number:", Counter(random_numbers).most_common(1)[0][0])