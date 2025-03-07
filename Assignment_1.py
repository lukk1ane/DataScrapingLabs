from functools import reduce

import numpy as np
import random


# --- Exercise 1: File Analysis ---
def exercise_1(filename="data.txt"):
    print('--- Exercise 1: File Analysis ---')
    try:
        with open(filename, "r") as file:
            line_count = 0
            word_count = 0
            char_count = 0
            for line in file:
                line_count += 1
                char_count += len(line)
                words = line.split()
                word_count += len(words)
            return line_count, word_count, char_count
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None


result = exercise_1('data')
if result:
    lines, words, chars = result
    print(f"Lines: {lines}, Words: {words}, Characters: {chars}\n")
exercise_1("non_existent_file.txt")
print()


# --- Exercise 2: Student Scores Analysis ---
def exercise_2():
    print('--- Exercise 2: Student Scores Analysis ---')
    student_data = {
        "Alice": 90,
        "Bob": 85,
        "Charlie": 92,
        "David": 78,
        "Eve": 95,
    }
    best_student = sorted(student_data.items(), key=lambda x: x[1], reverse=True)[0]
    average_score = reduce(lambda x, y: x + y, student_data.values()) / len(student_data)
    better_than_average = list(filter(lambda x: x[1] >= average_score, student_data.items()))
    print(f"Best student: {best_student}")
    print(f"Average score: {average_score:.2f}")
    print(f"Students above average: {better_than_average}\n")


exercise_2()

# --- Exercise 3: Car Mileage Update ---
cars = {
    'car1': {"brand": "Toyota", "model": "Camry", "year": 2020, "mileage": 35000},
    'car2': {"brand": "Honda", "model": "Civic", "year": 2019, "mileage": 42000},
    'car3': {"brand": "Ford", "model": "Mustang", "year": 2022, "mileage": 15000},
    'car4': {"brand": "Chevrolet", "model": "Silverado", "year": 2021, "mileage": 28000},
    'car5': {"brand": "Tesla", "model": "Model 3", "year": 2023, "mileage": 8000}
}


def exercise_3():
    print('--- Exercise 3: Car Mileage Update ---')

    def drive(car, km):
        mileage = car['mileage']
        print('before')
        print(f'{car}')
        car['mileage'] += km
        print('after')
        print(f'{car}')
        return car

    for car_id in cars.keys():
        cars[car_id] = drive(cars[car_id], 1000)

    return cars


exercise_3()


# --- Exercise 4: Car Mileage Statistics ---
def exercise_4():
    print('--- Exercise 4: Car Mileage Statistics ---')
    mileage = np.array(list(map(lambda item: item[1]['mileage'], cars.items())))
    print(f"Sum: {np.sum(mileage)}, Min: {np.min(mileage)}, Max: {np.max(mileage)}, Mean: {np.mean(mileage):.2f}\n")


exercise_4()


# --- Exercise 5: Car Brand Set Operations ---
def exercise_5():
    print('--- Exercise 5: Car Brand Set Operations ---')
    _set = set(list(map(lambda x: x[1]['brand'], cars.items())))
    print(f"Initial set: {_set}")
    _set.add('Tesla')
    print(f"Added 'Tesla': {_set}")
    _set.remove('Toyota')
    print(f"Removed 'Toyota': {_set}")
    print(f"Contains 'Tesla': {_set.__contains__('Tesla')}\n")


exercise_5()


def exercise_6():
    print('--- Exercise 6: Inheritance ---')

    class Animal:
        def __init__(self, name, sound):
            self.name = name
            self.sound = sound

        def make_sound(self):
            print(f'{self.name} says {self.sound}')

    class Dog(Animal):
        def __init__(self, name, breed, sound):
            super().__init__(name, sound)
            self.breed = breed
            self.sound = sound

        def make_sound(self):
            super().make_sound()

    class Cat(Animal):
        def __init__(self, name, sound):
            super().__init__(name, sound)
            self.sound = sound

        def make_sound(self):
            super().make_sound()

    animal_list = [Animal('test_1', "Generic Sound"), Dog('pako', 'wupaka', 'woof!'), Cat('garfield', 'meow!')]
    for animal in animal_list:
        animal.make_sound()


exercise_6()


def exercise_7(n=10):
    print('--- Exercise 7: fibonacci ---')

    def fibonacci(n):
        if n <= 0:
            print(0)
        if n == 1:
            print(1)
        a, b, c = 0, 1, 1
        for _ in range(2, n + 1):
            c = b + a
            a = b
            b = c
        print(b)

    return fibonacci(n)


exercise_7()


def exercise_8():
    print('--- Exercise 8: list comprehensions ---')

    list_1 = [i for i in range(1, 51)]
    print(list_1)
    list_2 = [i for i in range(1, 51) if not i % 2]
    print(list_2)
    list_3 = [i ** 2 for i in range(1, 51) if i % 2]
    print(list_3)
    list_4 = [i for i in range(1, 51) if not i % 5]
    print(list_4)


exercise_8()


def exercise_9():
    print('--- Exercise 9: safe_division ---')

    def safe_divide(a, b):
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."
        except TypeError:
            return "Error: Invalid input types. Please provide numbers."

    print(safe_divide(10, 2))  # Valid division
    print(safe_divide(10, 0))  # ZeroDivisionError
    print(safe_divide("10", 2))  # TypeError
    print(safe_divide(10, "2"))  # TypeError
    print(safe_divide(10.5, 2))  # valid float


exercise_9()


def exercise_10():
    print('--- Exercise 10 ---')
    random_numbers = [random.randint(1, 100) for _ in range(20)]
    random_numbers.sort()
    print(f'random numbers: {random_numbers}')
    print(f'min: {random_numbers[0]}')
    print(f'max:{random_numbers[-1]}')
    print(f'sum: {sum(random_numbers)}')
    print(f'average:{sum(random_numbers) / len(random_numbers)}')
    dict = {}
    for i in random_numbers:
        if i not in dict:
            dict[i] = 1
        else:
            dict[i] += 1
    print(sorted(dict.items(), key=lambda item: item[1], reverse=True)[0])


exercise_10()
