import os
import numpy as np
import random
from collections import Counter

# Exercise 1: File Processing
def read_file_data(filename):
    try:
        with open(filename, "r") as file:
            content = file.readlines()
            num_lines = len(content)
            num_words = sum(len(line.split()) for line in content)
            num_chars = sum(len(line) for line in content)
            extracted_data = {"lines": num_lines, "words": num_words, "chars": num_chars}
            print("File Data:", extracted_data)
            return extracted_data
    except FileNotFoundError:
        print("Error: File not found.")
        return None

file_data = read_file_data("data.txt")

# Exercise 2: Student Scores
students = {"Alice": 85, "Bob": 78, "Charlie": 92, "David": 88}

def highest_scoring_student(students):
    return max(students, key=students.get)

def average_score(students):
    return sum(students.values()) / len(students)

def students_above_average(students):
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]

print("Highest scoring student:", highest_scoring_student(students))
print("Average score:", average_score(students))
print("Students above average:", students_above_average(students))

# Exercise 3: Car Management
cars = [
    {"brand": "Toyota", "model": "Corolla", "year": 2018, "mileage": 50000},
    {"brand": "Ford", "model": "Focus", "year": 2020, "mileage": 30000},
    {"brand": "BMW", "model": "X5", "year": 2019, "mileage": 60000},
]

def drive(car, km):
    car["mileage"] += km

drive(cars[0], 100)
drive(cars[1], 200)

# Exercise 4: NumPy Mileage
mileages = np.array([car["mileage"] for car in cars])
print("Total mileage:", np.sum(mileages))
print("Max mileage:", np.max(mileages))
print("Min mileage:", np.min(mileages))
print("Mean mileage:", np.mean(mileages))

# Exercise 5: Car Brands Set
car_brands = {car["brand"] for car in cars}
car_brands.update(["Tesla", "Honda"])
car_brands.discard("Ford")
print("Is Tesla in the set?", "Tesla" in car_brands)

# Exercise 6: Inheritance
class Animal:
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        print("Woof!")

class Cat(Animal):
    def make_sound(self):
        print("Meow!")

animals = [Dog(), Cat()]
for animal in animals:
    animal.make_sound()

# Exercise 7: Fibonacci Generator
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print("First 10 Fibonacci numbers:", list(fibonacci(10)))

# Exercise 8: List Comprehensions
numbers = list(range(1, 51))
even_numbers = [n for n in numbers if n % 2 == 0]
squares_of_odds = [n**2 for n in numbers if n % 2 != 0]
divisible_by_5 = [n for n in numbers if n % 5 == 0]

print("Even numbers:", even_numbers)
print("Squares of odd numbers:", squares_of_odds)
print("Numbers divisible by 5:", divisible_by_5)

# Exercise 9: Safe Division
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
    except ValueError:
        return "Error: Invalid input."

print("Safe division (10 / 2):", safe_divide(10, 2))
print("Safe division (10 / 0):", safe_divide(10, 0))

# Exercise 10: Random Integers
random_numbers = [random.randint(1, 100) for _ in range(20)]
print("Random numbers:", random_numbers)
print("Max:", max(random_numbers))
print("Min:", min(random_numbers))
print("Sum:", sum(random_numbers))
print("Average:", sum(random_numbers) / len(random_numbers))
most_frequent = Counter(random_numbers).most_common(1)[0][0]
print("Most frequent number:", most_frequent)
