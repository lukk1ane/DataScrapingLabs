import os
import numpy as np
import random
from collections import Counter

"""Task 1"""
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            data = file.readlines()
            return len(data), sum(len(line.split()) for line in data), sum(len(line) for line in data)
    except FileNotFoundError:
        print("File not found.")
        return 0, 0, 0

"""Task 2"""


def process_students():
    result = read_file("data.txt")
    if len(result) < 4:
        _, _, _, words = 0, 0, 0, []
    else:
        _, _, _, words = result

    student_names = words[:5] if len(words) >= 5 else ["Alice", "Bob", "Charlie", "David", "Eve"]
    students = {name: random.randint(50, 100) for name in student_names}

    highest_scorer = max(students, key=students.get)
    avg_score = sum(students.values()) / len(students)
    above_avg = [name for name, score in students.items() if score > avg_score]

    return students, highest_scorer, avg_score, above_avg

"""Task 3"""


cars = [
    {"brand": "Toyota", "model": "Corolla", "year": 2015, "mileage": 50000},
    {"brand": "Ford", "model": "Focus", "year": 2018, "mileage": 30000},
    {"brand": "Honda", "model": "Civic", "year": 2020, "mileage": 15000},
]

def drive(car, km):
    car["mileage"] += km

def simulate_driving():
    for car in cars:
        distance = random.randint(100, 500)  # Simulate driving random distances
        drive(car, distance)

"""Task 4"""
def analyze_mileage():
    mileage_values = np.array([car["mileage"] for car in cars])
    return (mileage_values.sum().item(),
            mileage_values.max().item(),
            mileage_values.min().item(),
            mileage_values.mean().item())

"""Task 5"""

def car_brand_operations():
    car_brands = {car["brand"] for car in cars}
    car_brands.add("Tesla")
    car_brands.discard("Ford")
    return "Tesla" in car_brands

"""Task 6"""

class Animal:
    def make_sound(self):
        return "Grrrrr"


class Dog(Animal):
    def make_sound(self):
        return "Woof!"


class Cat(Animal):
    def make_sound(self):
        return "Meow!"


animals = [Dog(), Cat(), Dog()]


"""Task 7"""

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

"""Task 8"""

numbers = list(range(1, 51))
even_numbers = [num for num in numbers if num % 2 == 0]
square_odds = [num ** 2 for num in numbers if num % 2 != 0]
div_by_five = [num for num in numbers if num % 5 == 0]

"""Task 9"""

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero."
    except ValueError:
        return "Invalid input."

"""Task 10"""

random_numbers = [random.randint(1, 100) for _ in range(20)]
max_num = max(random_numbers)
min_num = min(random_numbers)
sum_num = sum(random_numbers)
avg_num = sum_num / len(random_numbers)
most_frequent = Counter(random_numbers).most_common(1)[0][0]

if __name__ == "__main__":
    print("Exercise 1:", read_file("data.txt"))
    print("Exercise 2:", process_students())
    drive(cars[0], 100)
    print("Exercise 3:", cars)
    print("Exercise 4:", analyze_mileage())
    print("Exercise 5:", car_brand_operations())
    for animal in animals:
        print("Exercise 6:", animal.make_sound())
    print("Exercise 7:", list(fibonacci(10)))
    print("Exercise 8:", even_numbers, square_odds, div_by_five)
    print("Exercise 9:", safe_divide(10, 2), safe_divide(10, 0))
    print("Exercise 10:", max_num, min_num, sum_num, avg_num, most_frequent)
