import os
import random
import numpy as np
from collections import Counter

# Exercise 1: 
def process_file(filename):
    """
    Read a file, count lines, words, and characters.
    Returns a tuple of (lines, words, characters, content)
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
            lines = content.split('\n')
            words = content.split()
            characters = len(content)
            
            print(f"File Statistics for {filename}:")
            print(f"Lines: {len(lines)}")
            print(f"Words: {len(words)}")
            print(f"Characters: {characters}")
            
            return len(lines), len(words), characters, content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return 0, 0, 0, ""

# Exercise 2: Student Dictionary
def create_student_dict(content):
    """Create a dictionary of students and scores from file content"""
    student_dict = {}
    lines = content.strip().split('\n')
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            name = parts[0]
            try:
                score = float(parts[1])
                student_dict[name] = score
            except ValueError:
                continue  # Skip invalid scores
    
    return student_dict

def student_stats(student_dict):
    """Process student scores and return statistics"""
    if not student_dict:
        print("No valid student data found.")
        return None, 0, []
    
    # Find highest scoring student
    highest_student = max(student_dict.items(), key=lambda x: x[1])
    
    # Compute average score
    average_score = sum(student_dict.values()) / len(student_dict)
    
    # Get list of students above average
    above_average = [name for name, score in student_dict.items() if score > average_score]
    
    print(f"\nStudent Statistics:")
    print(f"Highest scoring student: {highest_student[0]} with {highest_student[1]} points")
    print(f"Average score: {average_score:.2f}")
    print(f"Students above average: {', '.join(above_average)}")
    
    return highest_student, average_score, above_average

# Exercise 3: Car Dictionary and Function
def create_cars(names):
    """Create cars using names from data.txt"""
    cars = []
    # Use some names from data file for car brands if possible
    for i, name in enumerate(names[:5]):
        models = ["Sedan", "SUV", "Hatchback", "Coupe", "Truck"]
        cars.append({
            'brand': name,
            'model': models[i % len(models)],
            'year': random.randint(2018, 2024),
            'mileage': random.randint(10000, 50000)
        })
    
    # Add some standard cars if we don't have enough names
    if len(cars) < 5:
        standard_cars = [
            {'brand': 'Toyota', 'model': 'Corolla', 'year': 2019, 'mileage': 35000},
            {'brand': 'Honda', 'model': 'Civic', 'year': 2020, 'mileage': 28000},
            {'brand': 'Ford', 'model': 'Mustang', 'year': 2018, 'mileage': 45000},
            {'brand': 'BMW', 'model': 'X5', 'year': 2021, 'mileage': 15000},
            {'brand': 'Tesla', 'model': 'Model 3', 'year': 2022, 'mileage': 10000}
        ]
        cars.extend(standard_cars[:(5-len(cars))])
    
    return cars

def drive(car, km):
    """Update car mileage after driving km kilometers"""
    car['mileage'] += km
    return car

def car_simulator(cars):
    """Simulate driving cars"""
    print("\nCar Simulation:")
    for car in cars:
        km_to_drive = random.randint(1000, 5000)
        print(f"Driving {car['brand']} {car['model']} for {km_to_drive} km")
        drive(car, km_to_drive)
    
    print("\nUpdated car mileages:")
    for car in cars:
        print(f"{car['brand']} {car['model']}: {car['mileage']} km")
    
    return cars

# Exercise 4: NumPy Array Operations
def mileage_analysis(cars):
    """Analyze car mileage using NumPy"""
    mileages = np.array([car['mileage'] for car in cars])
    
    print("\nMileage Analysis (NumPy):")
    print(f"Total mileage: {np.sum(mileages)} km")
    print(f"Maximum mileage: {np.max(mileages)} km")
    print(f"Minimum mileage: {np.min(mileages)} km")
    print(f"Mean mileage: {np.mean(mileages):.2f} km")
    
    return mileages

# Exercise 5: Set Operations
def brand_operations(cars):
    """Perform set operations on car brands"""
    # Extract unique brands
    brands = {car['brand'] for car in cars}
    
    print("\nSet Operations on Car Brands:")
    print(f"Initial brands: {brands}")
    
    # Add new brands
    new_brands = ['Audi', 'Mercedes', 'Volvo']
    for brand in new_brands:
        brands.add(brand)
    print(f"After adding {', '.join(new_brands)}: {brands}")
    
    # Remove a brand (remove the first one if possible)
    if brands:
        brand_to_remove = next(iter(brands))
        brands.remove(brand_to_remove)
        print(f"After removing {brand_to_remove}: {brands}")
    
    # Check if "Tesla" is in the set
    tesla_check = 'Tesla' in brands
    print(f"Is Tesla in the set? {tesla_check}")
    
    return brands

# Exercise 6: Class Inheritance
class Animal:
    def __init__(self, name):
        self.name = name
    
    def make_sound(self):
        return "Some generic animal sound"

class Dog(Animal):
    def make_sound(self):
        return "Woof!"

class Cat(Animal):
    def make_sound(self):
        return "Meow!"

def animal_sounds(names):
    """Create animals using names from data.txt"""
    animals = []
    
    # Use names from file for animals if available
    for i, name in enumerate(names[:4]):
        if i % 2 == 0:
            animals.append(Dog(name))
        else:
            animals.append(Cat(name))
    
    # Add default animals if we don't have enough names
    if len(animals) < 4:
        default_animals = [
            Dog("Buddy"),
            Cat("Whiskers"),
            Dog("Max"),
            Cat("Luna")
        ]
        animals.extend(default_animals[:(4-len(animals))])
    
    print("\nAnimal Sounds:")
    for animal in animals:
        print(f"{animal.name} says: {animal.make_sound()}")
    
    return animals

# Exercise 7: Generator Function
def fibonacci(n):
    """Generate the first n Fibonacci numbers"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

def print_fibonacci(n=10):
    """Print the first n Fibonacci numbers"""
    print(f"\nFirst {n} Fibonacci numbers:")
    fib_numbers = list(fibonacci(n))
    print(fib_numbers)
    return fib_numbers

# Exercise 8: List Comprehensions
def list_comprehensions():
    """Demonstrate list comprehensions"""
    numbers = list(range(1, 51))
    
   
    even_numbers = [num for num in numbers if num % 2 == 0]
    
    
    odd_squares = [num**2 for num in numbers if num % 2 != 0]
    
   
    divisible_by_5 = [num for num in numbers if num % 5 == 0]
    
    print("\nList Comprehensions:")
    print(f"Even numbers: {even_numbers}")
    print(f"Squares of odd numbers: {odd_squares}")
    print(f"Numbers divisible by 5: {divisible_by_5}")
    
    return even_numbers, odd_squares, divisible_by_5

# Exercise 9: Exception Handling
def safe_divide(a, b):
    """Safely divide two numbers with exception handling"""
    try:
        a = float(a)
        b = float(b)
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"
    except ValueError:
        return "Error: Please enter valid numbers"
    except Exception as e:
        return f"Error: {str(e)}"

def test_division():
    """Test the safe_divide function with various inputs"""
    test_cases = [
        (10, 2),
        (5, 0),
        ('20', '5'),
        ('abc', 5),
        (7, 'xyz')
    ]
    
    print("\nSafe Division Results:")
    for a, b in test_cases:
        result = safe_divide(a, b)
        print(f"{a} / {b} = {result}")
    
    return test_cases

# Exercise 10: Random Numbers Analysis
def random_numbers_analysis():
    """Generate and analyze random numbers"""
    random_nums = [random.randint(1, 100) for _ in range(20)]
    
    # Calculate statistics
    maximum = max(random_nums)
    minimum = min(random_nums)
    total_sum = sum(random_nums)
    average = total_sum / len(random_nums)
    
    # Find most frequent number
    counter = Counter(random_nums)
    most_common = counter.most_common(1)[0]
    
    print("\nRandom Numbers Analysis:")
    print(f"Numbers: {random_nums}")
    print(f"Maximum: {maximum}")
    print(f"Minimum: {minimum}")
    print(f"Sum: {total_sum}")
    print(f"Average: {average:.2f}")
    print(f"Most frequent: {most_common[0]} (appears {most_common[1]} times)")
    
    return random_nums, maximum, minimum, total_sum, average, most_common


def main():
    filename = "data.txt"
    
    # Exercise 1: Process file
    lines, words, chars, content = process_file(filename)
    
    if chars == 0:
        print("Cannot continue without valid data.txt file.")
        return
    
    # Extract names from file content for use in other exercises
    student_dict = create_student_dict(content)
    names = list(student_dict.keys())
    
    # Exercise 2: Student statistics
    highest, avg, above_avg = student_stats(student_dict)
    
    # Exercise 3: Car simulator using names from file
    cars = create_cars(names)
    updated_cars = car_simulator(cars)
    
    # Exercise 4: NumPy mileage analysis
    mileages = mileage_analysis(updated_cars)
    
    # Exercise 5: Set operations on car brands
    brands = brand_operations(updated_cars)
    
    # Exercise 6: Animal classes using names from file
    animals = animal_sounds(names)
    
    # Exercise 7: Fibonacci generator
    fib_nums = print_fibonacci()
    
    # Exercise 8: List comprehensions
    even, odd_sqr, div5 = list_comprehensions()
    
    # Exercise 9: Safe division with exception handling
    test_division()
    
    # Exercise 10: Random numbers analysis
    rand_analysis = random_numbers_analysis()
    
    print("\nAll exercises completed successfully!")

if __name__ == "__main__":
    main()