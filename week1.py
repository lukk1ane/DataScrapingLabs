# exercise 1
import os
import random
import numpy as np
from collections import Counter

def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_chars = sum(len(line) for line in lines)

            result = {
                "lines": num_lines,
                "words": num_words,
                "characters": num_chars
            }

            store_data(result)
            return result

    except FileNotFoundError:
        print(f"Error: The file '{filename}' is missing.")
        return None


def store_data(data, storage_file="processed_data.txt"):
    with open(storage_file, "w", encoding="utf-8") as file:
        file.write(str(data))


if __name__ == "__main__":
    filename = "data.txt"
    result = process_file(filename)
    if result:
        print(f"Lines: {result['lines']}, Words: {result['words']}, Characters: {result['characters']}")


def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_chars = sum(len(line) for line in lines)

            result = {
                "lines": num_lines,
                "words": num_words,
                "characters": num_chars
            }

            store_data(result)
            return result

    except FileNotFoundError:
        print(f"Error: The file '{filename}' is missing.")
        return None

# exercise 2
def store_data(data, storage_file="processed_data.txt"):
    with open(storage_file, "w", encoding="utf-8") as file:
        file.write(str(data))


def generate_student_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            words = file.read().split()
            students = {word.capitalize(): random.randint(50, 100) for word in words[:10]}  # Generate 10 students
            return students
    except FileNotFoundError:
        print(f"Error: The file '{filename}' is missing.")
        return {}


def highest_scoring_student(students):
    return max(students, key=students.get)


def average_score(students):
    return sum(students.values()) / len(students) if students else 0


def students_above_average(students):
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]


if __name__ == "__main__":
    students = generate_student_data(filename)
    if students:
        print("Student Scores:", students)
        print("Highest Scoring Student:", highest_scoring_student(students))
        print("Average Score:", average_score(students))
        print("Students Above Average:", students_above_average(students))
# exercise 3
def drive(car, km):
    car["mileage"] += km


def create_car_list():
    return [
        {"brand": "Toyota", "model": "Corolla", "year": 2015, "mileage": 80000},
        {"brand": "Ford", "model": "Focus", "year": 2018, "mileage": 60000},
        {"brand": "Honda", "model": "Civic", "year": 2020, "mileage": 30000},
    ]


def simulate_driving(cars):
    for car in cars:
        drive(car, random.randint(100, 500))
    store_data(cars, "updated_cars.txt")
    return cars


if __name__ == "__main__":

    cars = create_car_list()
    print("Initial Cars:", cars)
    updated_cars = simulate_driving(cars)
    print("Updated Cars:", updated_cars)
# exercise 4
def analyze_mileage(cars):
    mileages = np.array([car["mileage"] for car in cars])
    print(f"Total Mileage: {np.sum(mileages)}")
    print(f"Max Mileage: {np.max(mileages)}")
    print(f"Min Mileage: {np.min(mileages)}")
    print(f"Mean Mileage: {np.mean(mileages)}")


if __name__ == "__main__":
    analyze_mileage(updated_cars)
#  exercise 5
def process_car_brands(cars):
    brands = {car["brand"] for car in cars}
    print("Unique Car Brands:", brands)

    brands.update(["Tesla", "BMW"])
    print("Updated Brands:", brands)

    brands.discard("Ford")
    print("After Removal:", brands)

    print("Is Tesla in the set?", "Tesla" in brands)


if __name__ == "__main__":

    analyze_mileage(updated_cars)
    process_car_brands(updated_cars)
# exercise 6

class Animal:
    def make_sound(self):
        raise NotImplementedError("Subclass must implement abstract method")


class Dog(Animal):
    def make_sound(self):
        return "Woof!"


class Cat(Animal):
    def make_sound(self):
        return "Meow!"


animals = [Dog(), Cat()]


for animal in animals:
    print(animal.make_sound())
# exercise 7
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
# exercise 8
numbers = list(range(1, 51))
even_numbers = [num for num in numbers if num % 2 == 0]
squares_of_odd_numbers = [num**2 for num in numbers if num % 2 != 0]
divisible_by_5 = [num for num in numbers if num % 5 == 0]

print("Even numbers:", even_numbers)
print("Squares of odd numbers:", squares_of_odd_numbers)
print("Numbers divisible by 5:", divisible_by_5)

# exercise 9
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
    except ValueError:
        return "Error: Invalid value. Please enter numeric values."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    else:
        return result

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide(10, "a"))
print(safe_divide("10", 2))

# exercise 10
random_integers = [random.randint(1, 100) for _ in range(20)]
max_value = max(random_integers)
min_value = min(random_integers)
total_sum = sum(random_integers)
average = total_sum / len(random_integers)
counter = Counter(random_integers)
most_frequent_number = counter.most_common(1)[0][0]

print("Random integers:", random_integers)
print("Maximum value:", max_value)
print("Minimum value:", min_value)
print("Sum:", total_sum)
print("Average:", average)
print("Most frequent number:", most_frequent_number)