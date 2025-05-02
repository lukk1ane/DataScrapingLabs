# exercise 1
import numpy as np
import random
from collections import Counter

def read_file_data():
    linecounter = 0
    wordcounter = 0
    charactercounter = 0
    file_content = ""

    try:
        with open('data.txt', 'r') as file:
            file_content = file.read()
            file.seek(0)
            for line in file:
                linecounter += 1
                words = line.split()
                wordcounter += len(words)
                charactercounter += sum(len(word) for word in words)

        extracted_data = {
            "Lines": linecounter,
            "Words": wordcounter,
            "Characters (excluding spaces/newlines)": charactercounter
        }

        with open('output.txt', 'w') as output_file:
            output_file.write("Extracted Data:\n")
            output_file.write(f"Lines: {linecounter}\n")
            output_file.write(f"Words: {wordcounter}\n")
            output_file.write(f"Characters : {charactercounter}\n\n")
            output_file.write("File Content:\n")
            output_file.write(file_content)

        print(f"Lines: {linecounter}")
        print(f"Words: {wordcounter}")
        print(f"Characters : {charactercounter}")

        return extracted_data

    except FileNotFoundError:
        print("Error: The file 'data.txt' is missing!")
        return None
# exercise 2
def students():
    studentdata = {"John": [10, 9, 8, 10], "Ana": [10, 7, 8, 9], "Terry": [9, 8, 10, 4]}
    
    def find_highest_scorer():
        highestscorer = ""
        highestscore = 0
        for k, v in studentdata.items():
            if sum(v) > highestscore:
                highestscorer = k
                highestscore = sum(v)
        return highestscorer

    def average_score():
        totalscore = sum(sum(v) for v in studentdata.values())
        return totalscore / len(studentdata)

    def above_average():
        avg_score = average_score()
        students_above = [k for k, v in studentdata.items() if sum(v) > avg_score]
        return students_above

    return find_highest_scorer(), average_score(), above_average()

data = read_file_data()
students_result = students()
print("Highest Scorer:", students_result[0])
print("Average Score:", students_result[1])
print("Students Above Average:", students_result[2])


# exercise 3
def cars_simulation():
    cars = [
        {"brand": "Toyota", "model": "Corolla", "year": 2015, "mileage": 60000},
        {"brand": "Honda", "model": "Civic", "year": 2018, "mileage": 30000},
        {"brand": "Ford", "model": "Focus", "year": 2020, "mileage": 15000}
    ]
    
    def drive(car, km):
        car["mileage"] += km
        print(f"{car['brand']} {car['model']} driven for {km} km. New mileage: {car['mileage']}")
    
    # Simulate driving
    drive(cars[0], 500)
    drive(cars[1], 1200)
    drive(cars[2], 800)
    
    return cars
cars_simulation()

# execise 4

def analyze_mileage(cars):
    mileage_array = np.array([car["mileage"] for car in cars])
    
    total_mileage = np.sum(mileage_array)
    max_mileage = np.max(mileage_array)
    min_mileage = np.min(mileage_array)
    mean_mileage = np.mean(mileage_array)
    
    print(f"Total Mileage: {total_mileage}")
    print(f"Maximum Mileage: {max_mileage}")
    print(f"Minimum Mileage: {min_mileage}")
    print(f"Mean Mileage: {mean_mileage:.2f}")

analyze_mileage(cars_simulation())

# exercise 5
def manage_car_brands(cars):
    car_brands = {car["brand"] for car in cars}

    is_tesla_present = "Tesla" in car_brands
    
    print("Car Brands:", car_brands)
    print("Is Tesla in the set?:", is_tesla_present)
    
    return car_brands

manage_car_brands(cars_simulation())


# exercise 6
class Animal:
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

def animal_sounds():
    animals = [Dog(), Cat(), Dog(), Cat()]
    for animal in animals:
        print(animal.make_sound())
animal_sounds()

# exercise 7
def fibonacci():
    a = 0
    first = 0
    second = 1
    lst = [0, 1]
    while (a < 8):
        lst.append(lst[a] + lst[a + 1])
        a += 1
    return  lst
print(fibonacci())

# exercise 8
numbers = list(range(1, 51))
even_numbers = [n for n in numbers if n % 2 == 0]
squares_of_odd_numbers = [n**2 for n in numbers if n % 2 != 0]
numbers_divisible_by_5 = [n for n in numbers if n % 5 == 0]
print(even_numbers)
print(squares_of_odd_numbers)
print(numbers_divisible_by_5)

# exercise 9
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."
    except ValueError:
        return "Error: Invalid input. Please provide numbers."
print(safe_divide(10, 2)) 
print(safe_divide(10, 0))


# exercise 10
random_numbers = [random.randint(1, 100) for _ in range(20)]
max_value = max(random_numbers)
min_value = min(random_numbers)
sum_values = sum(random_numbers)
avg_value = sum_values / len(random_numbers)

# Finding most frequent number using for loop
frequency = {}
for num in random_numbers:
    frequency[num] = frequency.get(num, 0) + 1
most_frequent = max(frequency, key=frequency.get)

print("Random Numbers:", random_numbers)
print("Max Value:", max_value)
print("Min Value:", min_value)
print("Sum:", sum_values)
print("Average:", avg_value)
print("Most Frequent Number:", most_frequent)