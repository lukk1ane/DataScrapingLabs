import numpy as np


# Excercise 1

try:
    with open("data.txt","r") as file:
        lines = file.readlines()
        linesLength = len(lines)
        words = []
        for i in lines:
            words += i.split()
        lenWords = len(words)
        countChars = 0
        for i in words:
            countChars += len(i)
        print("Exercise 1")
        print("NumberOfLines: ",linesLength)
        print("Number of Words: ",lenWords)
        print("Number of Characters: ", countChars)
        print("____________")
        # Exercise 2
        def findHighestScore(dict):
            return max(dict.values())

        def findAverageScore(dict):
            sum = 0
            for k, v in dict.items():
                sum += v
            return sum / len(dict)


        def getAverageStudents(dict):
            avg = findAverageScore(dict)
            students = []
            for k, v in dict.items():
                if v >= avg:
                    students.append(k)
            return students


        d2 = {}
        j = 0.3

        for i in words:
            d2[i] = 2+j
            j+=0.2
        print(getAverageStudents(d2)," Exercise 2")
        print("____________")

except FileNotFoundError:
        print("file not found")
# Exercise 3
cars = [{"brand" : "Tesla","model": "b", "year" : "2002", "milage" : 20},
        {"brand" : "BMW","model": "b", "year" : "2002", "milage" : 15},
        {"brand" : "Tesla","model": "b", "year" : "2002", "milage" : 0}]

def drive(car,km):
    car["milage"] += km

for i in cars:
    drive(i,5)
print(cars, " Exercise 3")
print("____________")
# Exercise 4
milages = []
for i in cars:
    milages.append(i["milage"])


npArrayOfCars = np.array(milages)
print(npArrayOfCars)
sumMilage = sum(npArrayOfCars)
maxMilage = np.max(npArrayOfCars)
minMilage = np.min(npArrayOfCars)
meanMilage = np.mean(npArrayOfCars)

print(sumMilage,maxMilage,minMilage,meanMilage, " Exercise 4")
print("____________")
# Exercise 5
brands = []
for i in cars:
    brands.append(i["brand"])
carsSet = set(brands)
carsSet.add("Mercedes")
carsSet.remove("BMW")
print("Tesla" in carsSet , "   Exercise 5")
print("____________")


# Exercise 6

class Animal:
    def __init__(self,name):
        self.name = name
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Woof"

class Cat(Animal):
    def make_sound(self):
        return "Meow"
print("Exercise 6")
animals = [ Cat("Fury"),Dog("Ziggy"),Dog("Brian"),Cat("Morgana")]
for i in animals:
    print(i.make_sound())
print("____________")


# with only generator function
def fibonacci(n):
    a, b = 0, 1
    yield b
    for i in range(n - 1):
        yield (a + b)
        a, b = b, a + b

# generator plus iterative
def fib(n):
    if n == 1:
        return 1
    else:
        return n + fib(n - 1)

def fibonacci(n):
    for i in range(1,n+1):
        yield fib(i)

fibs = fibonacci(10)
print("Exercise 7")
for i in fibs:
    print(i)
print("____________")
print("Exercise 8")
listOfNums = [i for i in range(1,51)]
evenNums = [i for i in listOfNums if i%2 == 0]
squaresOfOddNumbesr = [i**2 for i in listOfNums if i%2 == 1]
DivisibleByFive = [i for i in listOfNums if i % 5 == 0]

print(listOfNums, " List of numbers from 1 to 50")
print(evenNums, " List of Even Numbers")
print(squaresOfOddNumbesr, " List of squares of odd numbers")
print(DivisibleByFive , " List of Numbers divisible by 5")
print("____________")
# Exercise 9

def safe_divide(a,b):
    try:
        return a/b
    except ZeroDivisionError:
        return "Zero division error"


print("Exercise 9")
print( "5 divided by 2 = ", safe_divide(5,2))
print("9 divided by 3 = ",safe_divide(9,3))
print("5 divided by 0 is ",safe_divide(5,0))
print("____________")


print("Exercise 10")
import random
randomInts = [random.randint(1,100) for i in range(20)]
maximum = max(randomInts)
minimum = min(randomInts)
sum = sum(randomInts)
avg = sum/len(randomInts)

# calculate most frequent:
dictionary = {}
for i in randomInts:
    if i in dictionary:
        dictionary[i] += 1
    else:
        dictionary[i] = 0

frequency = max(dictionary.values())
mostFrequent = 0
for k,v in dictionary.items():
    if v == frequency:
        mostFrequent = k

print(randomInts, " 20 random integers")
print("Max :", maximum, " ", "Min: ", minimum)
print("Sum :", sum, " ", "Avg: ", avg)
print("Most frequent number is:", mostFrequent)