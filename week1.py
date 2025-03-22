# import numpy as np
import random

# exercise 1

def read_file(path):
    try: 
        with open(path, "r") as file: 
            return file.read()
    except FileNotFoundError:
        return "file not found"


def count(path): 
    res = {"lines": 0, "words": 0, "characters": 0}
    data = read_file(path)
    res["lines"] = len(data.split("\n"))
    res["words"] = len([1 for str in data.split() if not str.strip(",.").isnumeric()])
    res["characters"] = len(data)
    return res

file_count = count("data.txt")


# exercise 2
scores = {"elene": 94, "keso": 97, "eva": 100, "frank": 81, "sponge": 91}

def highest(scores):
    return max(scores, key=scores.get)

def average(scores): 
    return sum(scores.values()) / len(scores)

def above_avg(scores): 
    avg = average(scores)
    return [s for s in scores.keys() if scores[s] > avg]




# exercise 3
cars = [
    {"brand": "Toyota", "model": "Corolla", "year": 2015, "mileage": 75000},
    {"brand": "Ford", "model": "Focus", "year": 2018, "mileage": 54000},
    {"brand": "BMW", "model": "X5", "year": 2020, "mileage": 30000}, 
    {"brand": "Mercedes", "model": "C-Class", "year": 2017, "mileage": 62000}, 
    {"brand": "Mercedes", "model": "benz", "year": 2017, "mileage": 61000},
]

def drive(car,km): 
    car["mileage"] += km

for i in range(len(cars)): 
    drive(cars[i], i*400)
# print(cars)


# exercise 4
# mileages = np.array([car["mileage"] for car in cars])
# total = np.sum(mileages)
# max, min = np.max(mileages), np.min(mileages)
# avg = np.average(mileages)

# uncomment, could not run last task with max and min because of numpy import


# exercise 5 
brands = set(car["brand"] for car in cars)
brands.add("niva")
brands.remove("Mercedes")

# print("Tesla" in brands)


#exercise 6
class Animal: 
    def make_sound(self): 
        print("animal sound")

class Dog(Animal):
    def make_sound(self):
        print("dog sound")


class Cat(Animal):
    def make_sound(self):
        print("cat sound")
animals = [Cat(), Animal(), Dog(), Cat(), Animal()]
# for animal in animals: 
#     animal.make_sound()


# exercise 7
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# for f in fib(7): print(f)
# exercise 8
lst = list(range(1,51))
for i in range(1, 51): lst.append(i)
evens = [n for n in lst if n % 2==0]
odds = [n**2 for n in lst if n%2==1]
div_5 = [n for n in lst if n%5==0]

# exercise 9
def safe_divide(a,b): 
    try: 
        if type(a) is not int or type(b) is not int: raise ValueError
        return a/b
    except ZeroDivisionError: 
        return "can not divide by zero"
    except ValueError: 
        return "enter valid numbers"
    
# print(safe_divide(15, 5))
# print(safe_divide(0, 5))
# print(safe_divide(0, 0))
# print(safe_divide(15, 0))
# print(safe_divide("15", 1))

# exercise 10
numbers = [random.randint(1,101) for _ in range(20)]
print("max:", max(numbers), "min:",min(numbers))
print("sum:", sum(numbers), "average:", sum(numbers) / len(numbers))

freq = dict.fromkeys(numbers, 0)
for i in numbers: freq[i] +=1
print(max(freq, key=freq.get)) 




