from collections import Counter
import numpy as np
import random

# _____Week 1_____
# Exercise 1
def file_statistics(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_chars = sum(len(line) for line in lines)

        stats = {"lines": num_lines, "words": num_words, "characters": num_chars}
        return stats
    except FileNotFoundError:
        return f"Error: {filename} not found."



# Exercise 2
students = {
    "Alice": 85, "Bob": 92, "Charlie": 78, "David": 88, "Eve": 95
}

def highest_scorer(students):
    return max(students, key=students.get)

def average_score(students):
    return sum(students.values()) / len(students)

def above_average_students(students):
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]



# Exercise 3
cars = [
    {"brand": "Toyota", "model": "Corolla", "year": 2018, "mileage": 40000},
    {"brand": "Honda", "model": "Civic", "year": 2020, "mileage": 25000},
    {"brand": "Ford", "model": "Focus", "year": 2017, "mileage": 60000}
]

def drive(car, km):
    car["mileage"] += km



# Exercise 4
mileage_list = np.array([car["mileage"] for car in cars])
# print("Total Mileage:", np.sum(mileage_list))
# print("Max Mileage:", np.max(mileage_list))
# print("Min Mileage:", np.min(mileage_list))
# print("Mean Mileage:", np.mean(mileage_list))



# Exercise 5
car_brands = {car["brand"] for car in cars}

car_brands.update({"BMW", "Mercedes", "Toyota"})
car_brands.discard("Ford")

is_tesla_present = "Tesla" in car_brands



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

animals = [Dog(), Cat(), Dog(), Cat()]



# Exercise 7
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
# print(list(fibonacci(10)))



# Exercise 8
numbers = list(range(1, 51))

evens = [n for n in numbers if n % 2 == 0]
squares_of_odds = [n**2 for n in numbers if n % 2 != 0]
divisible_by_5 = [n for n in numbers if n % 5 == 0]



# Exercise 9
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except ValueError:
        return "Error: Invalid input, please enter numbers."

# print(safe_divide(10, 2))
# print(safe_divide(10, 0))
# print(safe_divide("a", 5))



# Exercise 10
random_numbers = [random.randint(1, 100) for _ in range(20)]
# print("Numbers:", random_numbers)
# print("Max:", max(random_numbers))
# print("Min:", min(random_numbers))
# print("Sum:", sum(random_numbers))
# print("Average:", sum(random_numbers) / len(random_numbers))

most_common = Counter(random_numbers).most_common(1)
# print("Most Frequent Number:", most_common[0][0] if most_common else None)

