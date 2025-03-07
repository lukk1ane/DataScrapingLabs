import random

# Exercise 1
words = []
log = {"lines": 0, "words": 0, "characters": 0}
try:
    file = open("data.txt")
    for line in file:
        log["lines"] += 1
        for word in line.split():
            words.append(word)
            log["words"] += 1
            for char in word:
                log["characters"] += 1
    print(f"Lines: {log['lines']}, Words: {log['words']}, Chars: {log['characters']}")
except FileNotFoundError:
    print("The data file is missing. Please make sure it is present in the directory.")

# Exercise 2
students = dict.fromkeys(words, 0)
for student in students:
    students[student] = random.randint(1, 100)

print(students)


def highest_score(students):
    return max(students, key=students.get)


print(highest_score(students))

# Exercise 3
cars = [{"brand": "BMW", "model": 1, "year": 2000, "mileage": 12045},
        {"brand": "Tesla", "model": 3, "year": 2012, "mileage": 2351},
        {"brand": "Toyota", "model": 2, "year": 1998, "mileage": 100434},
        {"brand": "BMW", "model": 1, "year": 1989, "mileage": 120212},
        {"brand": "Tesla", "model": 3, "year": 2016, "mileage": 23332},
        {"brand": "Toyota", "model": 2, "year": 1998, "mileage": 87854}
        ]


def drive(car, km):
    car["mileage"] += km


for car in cars:
    drive(car, random.randint(200, 2000))

print(cars)

# Exercise 4
import numpy as np

np_mileage = np.array([car["mileage"] for car in cars])

print(np_mileage.sum())
print(np_mileage.max())
print(np_mileage.min())
print(np_mileage.mean())

# Exercise 5
brands = set([car["brand"] for car in cars])
print(brands)
brands.remove("Tesla")
print("Tesla" in brands)


# Exercise 6
class Animal:
    def make_sound(self):
        print("Animal sound!")


class Dog(Animal):
    def make_sound(self):
        print("Woof!")


class Cat(Animal):
    def make_sound(self):
        print("Meow!")


animals = [Dog(), Cat(), Animal(), Dog(), Cat()]

for animal in animals:
    animal.make_sound()


# Exercise 7
def fibonacci(n):
    count = 0
    a = 0
    b = 1
    s = None
    while count < n:
        yield a
        s = a + b
        a = b
        b = s
        count += 1


for num in fibonacci(10):
    print(num)

# Exercise 8
nums = list(range(1, 51))
evens = [num for num in nums if not num % 2]
odd_squares = [num ** 2 for num in nums if num % 2]
div_five = [num for num in nums if not num % 5]
print(nums)
print(evens)
print(odd_squares)
print(div_five)


# Exercise 9
def safe_divide(a, b):
    try:
        if type(a) is not int or type(b) is not int:
            raise ValueError
        return a / b
    except ZeroDivisionError:
        print("Division by zero")
    except ValueError:
        print("Value error")


val = safe_divide(10, 2)
print(val)
safe_divide(10, 0)
safe_divide(10, "0")

# Exercise 10
rand_nums = [random.randint(1, 100) for _ in range(20)]
num_log = dict.fromkeys(rand_nums, 0)
print(rand_nums)
print(f"max: {max(rand_nums)}, min:{min(rand_nums)}")
print(f"sum: {sum(rand_nums)}, avg: {sum(rand_nums) / len(rand_nums)}")
for num in rand_nums:
    num_log[num] += 1
print(f"most frequent: {max(num_log, key=num_log.get)}")