import os
import random
import statistics
from typing import Dict, List, Tuple, Generator, Set, Optional, Union, Any
from collections import Counter
import numpy as np


#################################################
# Exercise 1: File Handling
#################################################

class FileAnalyzer:
    """Analyzes text files and extracts statistics."""
    
    def __init__(self, filepath: str):
        """
        Initialize the file analyzer.
        
        Args:
            filepath: Path to the file to analyze
        """
        self.filepath = filepath
        self.content = ""
        self.line_count = 0
        self.word_count = 0
        self.char_count = 0
        self.exists = os.path.exists(filepath)
    
    def analyze(self) -> Dict[str, int]:
        """
        Analyze the file and extract statistics.
        
        Returns:
            Dictionary containing line, word, and character counts
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        if not self.exists:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
                
                # Reset file pointer and count lines
                f.seek(0)
                self.line_count = sum(1 for _ in f)
            
            # Count words and characters
            self.word_count = len(self.content.split())
            self.char_count = len(self.content)
            
            return {
                'lines': self.line_count,
                'words': self.word_count,
                'characters': self.char_count
            }
            
        except Exception as e:
            print(f"Error analyzing file: {e}")
            raise
    
    def get_content(self) -> str:
        """Get the content of the analyzed file."""
        return self.content
    
    def get_stats(self) -> Dict[str, int]:
        """Get file statistics as a dictionary."""
        return {
            'lines': self.line_count,
            'words': self.word_count,
            'characters': self.char_count
        }


def exercise1() -> Dict[str, int]:
    """
    Exercise 1: File Analysis
    
    - Read a file data.txt
    - Count and return the number of lines, words, and characters
    - Handle exceptions if the file is missing
    - Store the extracted data for later use
    
    Returns:
        Dictionary with file statistics
    """
    filepath = "data.txt"
    
    try:
        # Create a sample file if it doesn't exist
        if not os.path.exists(filepath):
            print(f"Creating sample file '{filepath}'...")
            sample_text = (
                "This is a sample text file.\n"
                "It contains multiple lines of text.\n"
                "We can use this for our exercises.\n"
                "Python is a powerful programming language.\n"
                "File handling is an essential skill."
            )
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(sample_text)
        
        # Analyze the file
        analyzer = FileAnalyzer(filepath)
        stats = analyzer.analyze()
        
        print(f"File Analysis Results:")
        print(f"  - Lines: {stats['lines']}")
        print(f"  - Words: {stats['words']}")
        print(f"  - Characters: {stats['characters']}")
        
        return stats
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return {'lines': 0, 'words': 0, 'characters': 0}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {'lines': 0, 'words': 0, 'characters': 0}


#################################################
# Exercise 2: Dictionary Usage
#################################################

class StudentManager:
    """Manages student records and provides analytics."""
    
    def __init__(self):
        """Initialize the student manager."""
        self.students: Dict[str, float] = {}
    
    def add_student(self, name: str, score: float) -> None:
        """
        Add a student with their score.
        
        Args:
            name: Student name
            score: Student score
        """
        self.students[name] = score
    
    def add_students(self, students: Dict[str, float]) -> None:
        """
        Add multiple students.
        
        Args:
            students: Dictionary mapping student names to scores
        """
        self.students.update(students)
    
    def get_highest_scorer(self) -> Tuple[str, float]:
        """
        Find the student with the highest score.
        
        Returns:
            Tuple of (student_name, score)
            
        Raises:
            ValueError: If no students are registered
        """
        if not self.students:
            raise ValueError("No students registered")
        
        highest_scorer = max(self.students.items(), key=lambda x: x[1])
        return highest_scorer
    
    def get_average_score(self) -> float:
        """
        Calculate the average score of all students.
        
        Returns:
            Average score
            
        Raises:
            ValueError: If no students are registered
        """
        if not self.students:
            raise ValueError("No students registered")
        
        return sum(self.students.values()) / len(self.students)
    
    def get_above_average(self) -> Dict[str, float]:
        """
        Get students with scores above the average.
        
        Returns:
            Dictionary of students with above-average scores
        """
        if not self.students:
            return {}
        
        avg = self.get_average_score()
        return {name: score for name, score in self.students.items() if score > avg}


def create_student_names_from_file(file_content: str) -> List[str]:
    """
    Extract potential student names from file content.
    
    Args:
        file_content: Content of a text file
        
    Returns:
        List of potential student names (words starting with uppercase)
    """
    words = file_content.split()
    # Filter words that might be names (starting with uppercase, length > 2)
    names = [word.strip('.,!?()[]{}:;"\'-') for word in words 
             if word and word[0].isupper() and len(word) > 2]
    
    # Remove duplicates while preserving order
    unique_names = []
    for name in names:
        if name not in unique_names:
            unique_names.append(name)
    
    return unique_names[:10]  # Return at most 10 names


def exercise2(file_content: str = "") -> Dict[str, Any]:
    """
    Exercise 2: Student Score Management
    
    - Use a dictionary to store student names and scores
    - Implement functions to:
      - Find the highest scoring student
      - Compute the average score
      - Get a list of students above average
    - Use the extracted data from Exercise 1 to create sample student names
    
    Args:
        file_content: Text content to extract student names from
        
    Returns:
        Dictionary with exercise results
    """
    # Create a student manager
    manager = StudentManager()
    
    # Get potential student names from file or use defaults
    student_names = create_student_names_from_file(file_content)
    if not student_names:
        student_names = ["Alice", "Bob", "Charlie", "David", "Emma", 
                         "Frank", "Grace", "Hannah", "Ian", "Julia"]
    
    # Generate random scores and add students
    for name in student_names:
        score = round(random.uniform(60, 100), 1)
        manager.add_student(name, score)
    
    # Compute statistics
    try:
        highest_scorer = manager.get_highest_scorer()
        average_score = manager.get_average_score()
        above_average = manager.get_above_average()
        
        print("\nStudent Score Analysis:")
        print(f"  - Total students: {len(manager.students)}")
        print(f"  - Highest scorer: {highest_scorer[0]} ({highest_scorer[1]})")
        print(f"  - Average score: {average_score:.2f}")
        print(f"  - Students above average:")
        for name, score in above_average.items():
            print(f"    * {name}: {score}")
        
        return {
            'students': manager.students,
            'highest_scorer': highest_scorer,
            'average_score': average_score,
            'above_average': above_average
        }
        
    except ValueError as e:
        print(f"Error: {e}")
        return {
            'students': {},
            'highest_scorer': None,
            'average_score': 0,
            'above_average': {}
        }


#################################################
# Exercise 3: Lists and Dictionaries
#################################################

def create_car(brand: str, model: str, year: int, mileage: float) -> Dict[str, Any]:
    """
    Create a car dictionary with specified attributes.
    
    Args:
        brand: Car brand
        model: Car model
        year: Manufacturing year
        mileage: Current mileage in kilometers
        
    Returns:
        Dictionary representing a car
    """
    return {
        'brand': brand,
        'model': model,
        'year': year,
        'mileage': mileage
    }


def drive(car: Dict[str, Any], km: float) -> Dict[str, Any]:
    """
    Update a car's mileage after driving a specified distance.
    
    Args:
        car: Car dictionary
        km: Distance driven in kilometers
        
    Returns:
        Updated car dictionary
        
    Raises:
        ValueError: If km is negative
    """
    if km < 0:
        raise ValueError("Distance cannot be negative")
    
    car['mileage'] += km
    return car


def exercise3() -> List[Dict[str, Any]]:
    """
    Exercise 3: Car Fleet Management
    
    - Create a list of cars where each car is a dictionary with brand, model, year, and mileage
    - Implement a function drive(car, km) that updates the mileage
    - Simulate driving some cars and store updated data
    
    Returns:
        List of car dictionaries after simulation
    """
    # Create a list of cars
    cars = [
        create_car("Toyota", "Corolla", 2019, 15000),
        create_car("Honda", "Civic", 2020, 8000),
        create_car("Ford", "Mustang", 2018, 20000),
        create_car("Tesla", "Model 3", 2021, 5000),
        create_car("BMW", "X5", 2017, 35000),
        create_car("Audi", "A4", 2020, 12000),
        create_car("Mercedes", "C-Class", 2019, 18000),
        create_car("Volkswagen", "Golf", 2018, 22000)
    ]
    
    # Simulate driving some cars
    print("\nCar Fleet Simulation:")
    
    # Select random cars and drive them random distances
    for _ in range(5):
        car_index = random.randint(0, len(cars) - 1)
        distance = random.randint(100, 500)
        
        car = cars[car_index]
        old_mileage = car['mileage']
        
        try:
            drive(car, distance)
            print(f"  - Drove {car['brand']} {car['model']} for {distance} km "
                  f"(Mileage: {old_mileage} → {car['mileage']})")
        except ValueError as e:
            print(f"  - Error: {e}")
    
    return cars


#################################################
# Exercise 4: NumPy Arrays
#################################################

def exercise4(cars: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Exercise 4: Mileage Analysis with NumPy
    
    - Convert mileage values from Exercise 3 into a NumPy array
    - Compute and print:
      - Total mileage
      - Maximum & minimum mileage
      - Mean mileage of all cars
    
    Args:
        cars: List of car dictionaries
        
    Returns:
        Dictionary with mileage statistics
    """
    # Extract mileage values
    mileage_values = np.array([car['mileage'] for car in cars])
    
    # Compute statistics
    total_mileage = np.sum(mileage_values)
    max_mileage = np.max(mileage_values)
    min_mileage = np.min(mileage_values)
    mean_mileage = np.mean(mileage_values)
    
    print("\nMileage Analysis (using NumPy):")
    print(f"  - Total fleet mileage: {total_mileage} km")
    print(f"  - Maximum mileage: {max_mileage} km")
    print(f"  - Minimum mileage: {min_mileage} km")
    print(f"  - Mean mileage: {mean_mileage:.2f} km")
    
    return {
        'mileage_array': mileage_values,
        'total_mileage': total_mileage,
        'max_mileage': max_mileage,
        'min_mileage': min_mileage,
        'mean_mileage': mean_mileage
    }


#################################################
# Exercise 5: Sets
#################################################

def exercise5(cars: List[Dict[str, Any]]) -> Set[str]:
    """
    Exercise 5: Brand Management with Sets
    
    - Extract unique car brands from Exercise 3 into a set
    - Add new brands to the set
    - Remove a brand
    - Check if "Tesla" is in the set
    
    Args:
        cars: List of car dictionaries
        
    Returns:
        Final set of car brands
    """
    # Extract unique brands
    brands = {car['brand'] for car in cars}
    
    print("\nCar Brand Management (using Sets):")
    print(f"  - Initial unique brands: {brands}")
    
    # Add new brands
    new_brands = {"Lexus", "Hyundai", "Kia"}
    brands.update(new_brands)
    print(f"  - After adding {new_brands}: {brands}")
    
    # Remove a brand (Audi if it exists, otherwise first brand)
    brand_to_remove = "Audi" if "Audi" in brands else next(iter(brands))
    brands.remove(brand_to_remove)
    print(f"  - After removing '{brand_to_remove}': {brands}")
    
    # Check if Tesla is in the set
    print(f"  - Is 'Tesla' in the set? {'Yes' if 'Tesla' in brands else 'No'}")
    
    return brands


#################################################
# Exercise 6: OOP and Inheritance
#################################################

class Animal:
    """Base class for animals."""
    
    def __init__(self, name: str):
        """
        Initialize an animal.
        
        Args:
            name: Name of the animal
        """
        self.name = name
    
    def make_sound(self) -> str:
        """
        Make an animal sound.
        
        Returns:
            String representing the animal sound
        """
        return "..."


class Dog(Animal):
    """Class representing a dog."""
    
    def make_sound(self) -> str:
        """
        Make a dog sound.
        
        Returns:
            String representing the dog sound
        """
        return "Woof!"


class Cat(Animal):
    """Class representing a cat."""
    
    def make_sound(self) -> str:
        """
        Make a cat sound.
        
        Returns:
            String representing the cat sound
        """
        return "Meow!"


def exercise6() -> List[Animal]:
    """
    Exercise 6: Animal Sound Simulator
    
    - Create a base class Animal with a method make_sound()
    - Create subclasses Dog and Cat, overriding make_sound()
    - Store different animals in a list and call make_sound() on each
    
    Returns:
        List of Animal objects
    """
    # Create a list of animals
    animals = [
        Dog("Rex"),
        Cat("Whiskers"),
        Dog("Buddy"),
        Cat("Fluffy"),
        Animal("Generic Animal")
    ]
    
    print("\nAnimal Sound Simulator:")
    for animal in animals:
        print(f"  - {animal.name} says: {animal.make_sound()}")
    
    return animals


#################################################
# Exercise 7: Generators
#################################################

def fibonacci(n: int) -> Generator[int, None, None]:
    """
    Generate the first n Fibonacci numbers.
    
    Args:
        n: Number of Fibonacci numbers to generate
        
    Yields:
        Fibonacci numbers one by one
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    a, b = 0, 1
    count = 0
    
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


def exercise7(n: int = 10) -> List[int]:
    """
    Exercise 7: Fibonacci Generator
    
    - Write a generator function fibonacci(n) that yields the first n Fibonacci numbers
    - Use it to print the first 10 Fibonacci numbers
    
    Args:
        n: Number of Fibonacci numbers to generate
        
    Returns:
        List of generated Fibonacci numbers
    """
    print(f"\nFirst {n} Fibonacci numbers:")
    
    try:
        fib_numbers = list(fibonacci(n))
        
        # Print in a nice format
        print("  ", end="")
        for i, num in enumerate(fib_numbers):
            print(f"{num}", end="")
            if i < len(fib_numbers) - 1:
                print(", ", end="")
        print()
        
        return fib_numbers
        
    except ValueError as e:
        print(f"  Error: {e}")
        return []


#################################################
# Exercise 8: List Comprehensions
#################################################

def exercise8() -> Dict[str, List[int]]:
    """
    Exercise 8: List Comprehension Examples
    
    - Create a list of numbers from 1 to 50
    - Use list comprehensions to generate:
      - A list of even numbers
      - A list of squares of odd numbers
      - A list of numbers divisible by 5
    
    Returns:
        Dictionary containing all generated lists
    """
    # Create a list of numbers from 1 to 50
    numbers = list(range(1, 51))
    
    # Generate lists using comprehensions
    even_numbers = [num for num in numbers if num % 2 == 0]
    odd_squares = [num**2 for num in numbers if num % 2 == 1]
    div_by_five = [num for num in numbers if num % 5 == 0]
    
    print("\nList Comprehension Results:")
    print(f"  - Even numbers: {even_numbers}")
    print(f"  - Squares of odd numbers: {odd_squares}")
    print(f"  - Numbers divisible by 5: {div_by_five}")
    
    return {
        'numbers': numbers,
        'even_numbers': even_numbers,
        'odd_squares': odd_squares,
        'divisible_by_five': div_by_five
    }


#################################################
# Exercise 9: Exception Handling
#################################################

def safe_divide(a: Union[int, float], b: Union[int, float]) -> Optional[float]:
    """
    Safely divide two numbers, handling potential exceptions.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division or None if an error occurs
    """
    try:
        return a / b
    except ZeroDivisionError:
        print("  Error: Division by zero is not allowed")
        return None
    except (TypeError, ValueError) as e:
        print(f"  Error: {e}")
        return None
    except Exception as e:
        print(f"  Unexpected error: {e}")
        return None


def exercise9() -> Dict[Tuple[Any, Any], Optional[float]]:
    """
    Exercise 9: Safe Division with Exception Handling
    
    - Write a function safe_divide(a, b) that divides two numbers
    - Handle ZeroDivisionError and ValueError exceptions
    - Test with different values, including invalid cases
    
    Returns:
        Dictionary mapping test cases to results
    """
    # Test cases
    test_cases = [
        (10, 2),        # Regular division
        (5, 0),         # Division by zero
        (7, 2),         # Division resulting in a float
        ("10", 2),      # String numerator
        (10, "2"),      # String denominator
        (None, 5)       # Invalid input
    ]
    
    results = {}
    
    print("\nSafe Division Test Cases:")
    for a, b in test_cases:
        print(f"  - Dividing {a} by {b}:")
        result = safe_divide(a, b)
        if result is not None:
            print(f"    Result: {result}")
        results[(a, b)] = result
    
    return results


#################################################
# Exercise 10: Random Numbers and Statistics
#################################################

def exercise10() -> Dict[str, Any]:
    """
    Exercise 10: Random Number Statistics
    
    - Create a list of 20 random integers (1-100)
    - Compute and print:
      - Maximum & minimum values
      - Sum & average
      - Most frequent number
    
    Returns:
        Dictionary with all computed statistics
    """
    # Generate random numbers
    random_numbers = [random.randint(1, 100) for _ in range(20)]
    
    # Compute statistics
    max_value = max(random_numbers)
    min_value = min(random_numbers)
    sum_value = sum(random_numbers)
    avg_value = sum_value / len(random_numbers)
    counter = Counter(random_numbers)
    most_common = counter.most_common(1)[0]
    
    print("\nRandom Number Statistics:")
    print(f"  - Generated numbers: {random_numbers}")
    print(f"  - Maximum value: {max_value}")
    print(f"  - Minimum value: {min_value}")
    print(f"  - Sum: {sum_value}")
    print(f"  - Average: {avg_value:.2f}")
    print(f"  - Most frequent number: {most_common[0]} (appears {most_common[1]} times)")
    
    return {
        'random_numbers': random_numbers,
        'max': max_value,
        'min': min_value,
        'sum': sum_value,
        'average': avg_value,
        'most_frequent': most_common
    }


#################################################
# Main Function
#################################################

def main():
    """Main function to run all exercises."""
    print("=" * 50)
    print("Python Programming Exercises")
    print("=" * 50)
    
    # Exercise 1
    print("\nExercise 1: File Analysis")
    file_stats = exercise1()
    
    # Get file content for Exercise 2
    file_content = ""
    filepath = "data.txt"
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
    
    # Exercise 2
    print("\nExercise 2: Student Score Management")
    exercise2(file_content)
    
    # Exercise 3
    print("\nExercise 3: Car Fleet Management")
    cars = exercise3()
    
    # Exercise 4
    print("\nExercise 4: Mileage Analysis with NumPy")
    exercise4(cars)
    
    # Exercise 5
    print("\nExercise 5: Brand Management with Sets")
    exercise5(cars)
    
    # Exercise 6
    print("\nExercise 6: Animal Sound Simulator")
    exercise6()
    
    # Exercise 7
    print("\nExercise 7: Fibonacci Generator")
    exercise7()
    
    # Exercise 8
    print("\nExercise 8: List Comprehension Examples")
    exercise8()
    
    # Exercise 9
    print("\nExercise 9: Safe Division with Exception Handling")
    exercise9()
    
    # Exercise 10
    print("\nExercise 10: Random Number Statistics")
    exercise10()


if __name__ == "__main__":
    main()