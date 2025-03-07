import numpy as np
import random
from collections import Counter

# Exercise 1
def read_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
        lines = data.split('\n')
        words = data.split(" ")
        chars = len(words) * len(lines)
        return len(lines), len(words), chars

# Exercise 2
students = {"student1": 85, "student2": 90, "student3": 78, "student4": 92}

def highest_scorer(students):
    return max(students, key=students.get)

def average_score(students):
    return sum(students.values()) / len(students)

def above_average_students(students):
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]

# Exercise 3
cars = [{'brand': 'toyota', 'model': 'idk', 'year': 2001, 'mileage': 101010},
        {'brand': 'toyota2', 'model': 'idk2', 'year': 2002, 'mileage': 202020},
        {'brand': 'toyota3', 'model': 'idk3', 'year': 2003, 'mileage': 303030}]

def drive(car, km):
    car["mileage"] += km

# Exercise 4
mileages = np.array([car["mileage"] for car in cars])

def mileage_stats(mileages):
    return np.sum(mileages), np.max(mileages), np.min(mileages), np.mean(mileages)

# Exercise 5
car_brands = {car["brand"] for car in cars}
car_brands.add("Honda")
car_brands.discard("Ford")

# Exercise 6
class Animal:
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

animals = [Dog(), Cat()]
sounds = [animal.make_sound() for animal in animals]

# Exercise 7: Fibonacci Generator
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Exercise 8
numbers = list(range(1, 51))
even_numbers = [n for n in numbers if n % 2 == 0]
squares_of_odds = [n**2 for n in numbers if n % 2 != 0]
numbers_divisible_by_5 = [n for n in numbers if n % 5 == 0]

# Exercise 9
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero!"
    except ValueError:
        return "Invalid input!"

# Exercise 10
random_numbers = [random.randint(1, 100) for _ in range(20)]
max_value = max(random_numbers)
min_value = min(random_numbers)
sum_values = sum(random_numbers)
average_value = sum_values / len(random_numbers)
most_frequent = Counter(random_numbers).most_common(1)[0][0]


print("Exercise 1:", read_file("data.txt"))
print("Exercise 2:", highest_scorer(students), average_score(students), above_average_students(students))
drive(cars[0], 10000)
print("Exercise 3:", cars)
print("Exercise 4:", mileage_stats(mileages))
print("Exercise 5:", car_brands)
print("Exercise 6:", sounds)
print("Exercise 7:", list(fibonacci(10)))
print("Exercise 8:", even_numbers, squares_of_odds, numbers_divisible_by_5)
print("Exercise 9:", safe_divide(10, 2), safe_divide(10, 0))
print("Exercise 10:", max_value, min_value, sum_values, average_value, most_frequent)
