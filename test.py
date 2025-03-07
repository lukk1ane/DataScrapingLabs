import os
import numpy as np
import random
from collections import Counter

# Exercise 1:
def file_statistics(filename):
    try:
        with open(filename, 'r') as file:
            data = file.readlines()
            num_lines = len(data)
            num_words = sum(len(line.split()) for line in data)
            num_chars = sum(len(line) for line in data)
            
            # Store extracted data
            extracted_data = {
                "lines": num_lines,
                "words": num_words,
                "characters": num_chars
            }
            return extracted_data
    except FileNotFoundError:
        return "File not found"

# Exercise 2:
def highest_scorer(students):
    return max(students, key=students.get)

def average_score(students):
    return sum(students.values()) / len(students)

def above_average_students(students):
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]

# Exercise 3:
cars = [
    {"brand": "Toyota", "model": "Corolla", "year": 2015, "mileage": 60000},
    {"brand": "Honda", "model": "Civic", "year": 2018, "mileage": 40000},
    {"brand": "Ford", "model": "Focus", "year": 2016, "mileage": 50000}
]

def drive(car, km):
    car["mileage"] += km

# Exercise 4:
mileages = np.array([car["mileage"] for car in cars])
print("Total mileage:", np.sum(mileages))
print("Max mileage:", np.max(mileages))
print("Min mileage:", np.min(mileages))
print("Mean mileage:", np.mean(mileages))

# Exercise 5:
brands = {car["brand"] for car in cars}
brands.add("Tesla")
brands.remove("Ford")
is_tesla_present = "Tesla" in brands

# Exercise 6:
class Animal:
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Bark"

class Cat(Animal):
    def make_sound(self):
        return "Meow"

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.make_sound())

# Exercise 7:
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(list(fibonacci(10)))

# Exercise 8:
even_numbers = [x for x in range(1, 51) if x % 2 == 0]
squares_of_odds = [x**2 for x in range(1, 51) if x % 2 != 0]
numbers_divisible_by_5 = [x for x in range(1, 51) if x % 5 == 0]

# Exercise 9:
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except ValueError:
        return "Invalid input"

# Exercise 10:
random_numbers = [random.randint(1, 100) for _ in range(20)]
print("Max:", max(random_numbers))
print("Min:", min(random_numbers))
print("Sum:", sum(random_numbers))
print("Average:", sum(random_numbers) / len(random_numbers))
most_frequent = Counter(random_numbers).most_common(1)[0][0]
print("Most Frequent Number:", most_frequent)