import numpy as np
import random
import re


def read_and_count(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            lines = content.splitlines()
            words = content.split()
            characters = len(content)

            print(f"File '{filename}' contains:")
            print(f"- {len(lines)} lines")
            print(f"- {len(words)} words")
            print(f"- {characters} characters")

            return content, lines, words, characters
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, [], [], 0


def extract_car_info(content):
    car_brands = []

    common_car_brands = ["Toyota", "Honda", "Ford", "BMW", "Tesla", "Audi", "Mercedes",
                         "Volkswagen", "Chevrolet", "Nissan", "Hyundai", "Kia", "Lexus"]

    for line in content.splitlines():
        for brand in common_car_brands:
            if brand in line:
                car_brands.append(brand)

    if not car_brands:
        potential_brands = set()
        for word in content.split():
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word and clean_word[0].isupper() and len(clean_word) > 2:
                potential_brands.add(clean_word)

        car_brands = list(potential_brands)[:5]
    if not car_brands:
        print("Warning: Could not extract car brands from the file. Using placeholder brands.")
        car_brands = ["Brand" + str(i) for i in range(1, 6)]

    cars = []
    for i, brand in enumerate(car_brands[:5]):
        model = f"Model{i + 1}"
        year = 2020 - i
        mileage = random.randint(5000, 50000)
        cars.append({"brand": brand, "model": model, "year": year, "mileage": mileage})

    return cars


def extract_student_data(content, words):
    student_names = []

    student_pattern = re.compile(r'\b(?:student|name)[s]?\b', re.IGNORECASE)

    lines_with_students = [line for line in content.splitlines() if student_pattern.search(line)]

    if lines_with_students:
        for line in lines_with_students:
            words_in_line = line.split()
            for i, word in enumerate(words_in_line):
                if student_pattern.search(word) and i + 1 < len(words_in_line):
                    potential_name = words_in_line[i + 1]
                    clean_name = re.sub(r'[^\w\s]', '', potential_name)
                    if clean_name and len(clean_name) > 2:
                        student_names.append(clean_name)

    if not student_names:
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word and (clean_word[0].isupper() or (3 <= len(clean_word) <= 10)):
                student_names.append(clean_word)
                if len(student_names) >= 5:  # Limit to 5 students
                    break

    if not student_names:
        student_names = ["Student" + str(i) for i in range(1, 6)]

    scores = [random.randint(50, 100) for _ in range(len(student_names))]

    return dict(zip(student_names[:5], scores[:5]))

def find_highest_scorer(students):
    return max(students.items(), key=lambda x: x[1])


def compute_average_score(students):
    return sum(students.values()) / len(students) if students else 0


def students_above_average(students):
    avg = compute_average_score(students)
    return [name for name, score in students.items() if score > avg]


def drive(car, km):
    car["mileage"] += km
    return car


def simulate_driving(cars):
    updated_cars = []
    for car in cars:
        distance = random.randint(100, 1000)
        updated_car = drive(car.copy(), distance)
        updated_cars.append(updated_car)
    return updated_cars


def analyze_mileage(cars):
    mileages = np.array([car["mileage"] for car in cars])

    total_mileage = np.sum(mileages)
    max_mileage = np.max(mileages)
    min_mileage = np.min(mileages)
    mean_mileage = np.mean(mileages)

    print(f"Total mileage: {total_mileage}")
    print(f"Maximum mileage: {max_mileage}")
    print(f"Minimum mileage: {min_mileage}")
    print(f"Mean mileage: {mean_mileage:.2f}")

    return mileages


def process_car_brands(cars):
    brand_set = {car["brand"] for car in cars}
    print("Original brand set:", brand_set)

    content, _, words, _ = read_and_count("data.txt")
    existing_brands = brand_set.copy()
    new_brands = []

    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word)
        if (clean_word and clean_word[0].isupper() and
                clean_word not in existing_brands and
                len(clean_word) > 2):
            new_brands.append(clean_word)
            if len(new_brands) >= 3:
                break

    if not new_brands:
        new_brands = ["NewBrand1", "NewBrand2", "NewBrand3"]

    for brand in new_brands:
        brand_set.add(brand)
    print("After adding brands:", brand_set)

    if brand_set:
        brand_to_remove = next(iter(brand_set))
        brand_set.remove(brand_to_remove)
        print(f"After removing {brand_to_remove}:", brand_set)

    e_brand = next((brand for brand in brand_set if "e" in brand.lower()), None)
    if e_brand:
        print(f"Is '{e_brand}' in the set? {e_brand in brand_set}")
    else:
        print("No brand with 'e' found in the set.")

    return brand_set


if __name__ == "__main__":
    filename = "data.txt"

    content, lines, words, char_count = read_and_count(filename)

    if content is not None:
        print("\n--- Student Information ---")
        students = extract_student_data(content, words)
        print("Students:", students)

        if students:
            highest_scorer, highest_score = find_highest_scorer(students)
            print(f"Highest scoring student: {highest_scorer} with {highest_score} points")
            average = compute_average_score(students)
            print(f"Average score: {average:.2f}")
            above_avg = students_above_average(students)
            print(f"Students above average: {above_avg}")

        print("\n--- Car Information ---")
        cars = extract_car_info(content)
        print("Original cars:")
        for car in cars:
            print(f"  {car['brand']} {car['model']} ({car['year']}): {car['mileage']} km")

        driven_cars = simulate_driving(cars)
        print("\nAfter driving:")
        for car in driven_cars:
            print(f"  {car['brand']} {car['model']} ({car['year']}): {car['mileage']} km")

        print("\n--- Mileage Analysis ---")
        mileages = analyze_mileage(driven_cars)

        print("\n--- Car Brand Set Operations ---")
        final_brand_set = process_car_brands(driven_cars)