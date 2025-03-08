import random

cars = [
    {"brand": "Toyota", "model": "Corolla", "year": 2018, "mileage": 35000},
    {"brand": "Honda", "model": "Civic", "year": 2020, "mileage": 25000},
    {"brand": "Ford", "model": "Mustang", "year": 2019, "mileage": 18000},
    {"brand": "Chevrolet", "model": "Camaro", "year": 2021, "mileage": 5000},
    {"brand": "BMW", "model": "X5", "year": 2017, "mileage": 45000}
]

def drive(car, km):
    miles = km * 0.621371
    old_mil = car['mileage']
    car['mileage'] += miles
    print(f'driving {km} kms ({miles} miles) with {car['brand']} {car['model']}. mileage: {old_mil} -> {car['mileage']}')

if __name__ == "__main__":
    for car in cars:
        drive(car, random.randint(150,4000))

    print()
    print(cars)