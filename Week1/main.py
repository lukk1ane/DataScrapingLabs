#Ex1
import random

import numpy as np
from collections import Counter


def analyze_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            num_lines = len(lines)
            words = [word for line in lines for word in line.split()]
            num_words = len(words)
            num_chars = sum(len(line) for line in lines)

            data = {
                "lines": num_lines,
                "words": num_words,
                "characters": num_chars,
                "sample_words": words[:5]
            }

            with open("analysis_result.txt", "w") as result_file:
                result_file.write(str(data))

            return data
    except FileNotFoundError:
        print("Error: The file does not exist.")
        return None


file_data = analyze_file("data.txt")
if file_data:
    print("File Analysis:")
    print(f"Lines: {file_data['lines']}")
    print(f"Words: {file_data['words']}")
    print(f"Characters: {file_data['characters']}")


#Ex2
def create_student_data(sample_names):
    scores = [97, 92, 78, 90, 88]
    return {name: score for name, score in zip(sample_names, scores)}


def highest_scoring_student(students):
    return max(students, key=students.get)


def average_score(students):
    return sum(students.values()) / len(students)


def students_above_average(students):
    avg = average_score(students)
    return [name for name, score in students.items() if score > avg]


sample_names = file_data.get("sample_words", ["Lorem", "Ipsum", "is", "simply", "dummy"])
students = create_student_data(sample_names)

highest = highest_scoring_student(students)
avg = average_score(students)
above_avg_students = students_above_average(students)

print(f"Highest Scoring Student: {highest}")
print(f"Average Score: {avg:.2f}")
print(f"Students Above Average: {', '.join(above_avg_students)}")


def create_car_list():
    return [
        {"brand": "Audi", "model": "RS7", "year": 2023, "mileage": 17000},
        {"brand": "Mercedes", "model": "E63", "year": 2020, "mileage": 30000},
        {"brand": "BMW", "model": "M5", "year": 2017, "mileage": 60000}
    ]


def drive(car, km):
    car["mileage"] += km
    return car


cars = create_car_list()
drive(cars[0], 150)
drive(cars[1], 200)
drive(cars[2], 100)

with open("car_data.txt", "w") as car_file:
    car_file.write(str(cars))

print("Updated Car Data:")
for car in cars:
    print(car)

#Ex4
mileages = np.array(([car["mileage"] for car in cars]))
print(f"Total Mileage: {np.sum(mileages)}")
print(f"Maximum Mileage: {np.max(mileages)}")
print(f"Minimum Mileage: {np.min(mileages)}")
print(f"Mean Mileage: {np.mean(mileages):}")

#Ex5
car_brands = {car["brand"] for car in cars}
car_brands.update(["Ferrari", "Alfa Romeo"])
car_brands.discard("BMW")
print(f"Car Brands: {car_brands}")
print(f"Is Tesla in the set? {'Tesla' in car_brands}")


#Ex6

class Animal:
    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Bark"


class Cat(Animal):
    def make_sound(self):
        return "Meow"


animals = [Dog(), Cat(), Dog()]
for animal in animals:
    print(animal.make_sound())


def fibonacci(n):
    a, b = 0, 1
    count = 0

    while count < n:
        yield a
        a, b = b, a + b
        count += 1


for num in fibonacci(10):
    print(num)

#Ex8
numbers = list(range(1, 51))
even_numbers = [n for n in numbers if n % 2 == 0]
squares_of_odds = [n ** 2 for n in numbers if n % 2 != 0]
numbers_divisible_by_5 = [n for n in numbers if n % 5 == 0]
print(f"Even Numbers: {even_numbers}")
print(f"Squares of Odd Numbers: {squares_of_odds}")
print(f"Numbers Divisible by 5: {numbers_divisible_by_5}")


#Ex9
def safe_divide(a, b):
    try:
        a_float = float(a)
        b_float = float(b)

        result = a_float / b_float
        return result

    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None

    except ValueError:
        print("Error: Inputs must be valid numbers")
        return None


safe_divide(10, 2)
safe_divide(10, 0)
safe_divide('a', 2)

#Ex10
random_numbers = [random.randint(1, 100) for _ in range(20)]
max_value = max(random_numbers)
min_value = min(random_numbers)
sum_values = sum(random_numbers)
average_value = sum_values / len(random_numbers)
most_frequent = Counter(random_numbers).most_common(1)[0][0]
print(f"Random Numbers: {random_numbers}")
print(f"Maximum: {max_value}")
print(f"Minimum: {min_value}")
print(f"Sum: {sum_values}")
print(f"Average: {average_value:.2f}")
print(f"Most Frequent Number: {most_frequent}")
