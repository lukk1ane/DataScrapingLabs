import json
from typing import override
from collections import Counter
import numpy as np
import random


def task1():
    try:
        with open('data.txt', 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            num_words = sum(len(line.split()) for line in lines)
            num_chars = sum(len(line) for line in lines)
            print(num_lines, num_words, num_chars)
            return num_lines, num_words, num_chars
    except FileNotFoundError:
        print('File not found')

def task2():
    students = {"student a": 67, "student b": 25, "student c": 52}
    highest_scoring_student = max(students, key=students.get)
    avg_score = sum(students.values()) // len(students)
    above_avg = {name: score for name, score in students.items() if score > avg_score}
    print(f'{highest_scoring_student}, {avg_score}, {above_avg}')

def task3():
    def create_cars():
        return [
            {"brand": "Toyota", "model": "Corolla", "year": 2018, "mileage": 50000},
            {"brand": "Honda", "model": "Civic", "year": 2020, "mileage": 30000},
            {"brand": "Ford", "model": "Focus", "year": 2019, "mileage": 40000}
        ]

    def drive(car, km):
        car["mileage"] += km

    def simulate_driving(cars):
        for car in cars:
            drive(car, 5000)
        with open("car_data.json", "w", encoding='utf-8') as json_file:
            json.dump(cars, json_file, indent=4)

    cars = create_cars()
    simulate_driving(cars)
    print("Updated Car Data:", cars)

def task4():
    with open('car_data.json', 'r') as cars:
        cars = json.load(cars)
        mileage_array = np.array([car["mileage"] for car in cars])
        print("Total Mileage:", np.sum(mileage_array))
        print("Maximum Mileage:", np.max(mileage_array))
        print("Minimum Mileage:", np.min(mileage_array))
        print("Mean Mileage:", np.mean(mileage_array))

def task5():
    with open('car_data.json', 'r') as cars:
        cars = json.load(cars)
        car_brands = set([car['brand'] for car in cars])
        if 'Ford' in car_brands:
            car_brands.remove('Ford')
            print(f'Brands after removing Ford: ', car_brands)
        if 'Tesla' in car_brands:
            print("Tesla is in card brands")
        else:
            print("Tesla is not in card brands")

def task6():
    class Animal:
        def make_sound(self):
            print("Animal is making sound")

    class Dog(Animal):
        def make_sound(self):
            print("Dog is making sound")

    class Cat(Animal):
        def make_sound(self):
            print("Cat is making sound")

    animals = [Dog(), Cat()]
    for animal in animals:
        animal.make_sound()

def task7():
    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    for num in fibonacci(10):
        print(num)

def task8():
    lst = [i for i in range(50)]
    lst_even = [i for i in lst if i % 2 == 0]
    lst_odd = [i**2 for i in lst if i % 2 == 1]
    lst_div5 = [i for i in lst if i % 5 == 0]
    print(lst_even, lst_odd, lst_div5)

def task9():
    def safe_divide(a, b):
        try:
            result = int(a) / int(b)
            return result
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."
        except ValueError:
            return "Error: Invalid input. Please enter numbers only."

    print(safe_divide(1, 2))
    print(safe_divide(5, 0))
    print(safe_divide(5, "b"))

def task10():
    random_numbers = [random.randint(1, 100) for _ in range(20)]
    max_value = max(random_numbers)
    min_value = min(random_numbers)
    sum_values = sum(random_numbers)
    average = sum_values / len(random_numbers)
    most_frequent = Counter(random_numbers).most_common(1)[0][0]
    print(max_value, min_value, sum_values, average, most_frequent)


if __name__ == '__main__':
    # task1()
    # task2()
    # task3()
    # task4()
    # task5()
    # task6()
    # task7()
    # task8()
    # task9()
    task10()
