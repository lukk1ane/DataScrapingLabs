import numpy as np

cars = [
    {"brand": "Toyota", "model": "Camry", "year": 2020, "mileage": 15100},
    {"brand": "Honda", "model": "Civic", "year": 2019, "mileage": 22250},
    {"brand": "Ford", "model": "Mustang", "year": 2021, "mileage": 5050},
    {"brand": "Chevrolet", "model": "Malibu", "year": 2018, "mileage": 30000},
    {"brand": "Tesla", "model": "Model 3", "year": 2022, "mileage": 2000}
]

mileage_values = np.array([car['mileage'] for car in cars])

total_mileage = np.sum(mileage_values)
max_mileage = np.max(mileage_values)
min_mileage = np.min(mileage_values)
mean_mileage = np.mean(mileage_values)

print(f"Total Mileage: {total_mileage} km")
print(f"Maximum Mileage: {max_mileage} km")
print(f"Minimum Mileage: {min_mileage} km")
print(f"Mean Mileage: {mean_mileage:.2f} km")