import numpy as np

#task3
cars = [
    {"brand": "Toyota", "model": "Corolla", "year": 2020, "mileage": 250},
    {"brand": "Ford", "model": "Focus", "year": 2018, "mileage": 400},
    {"brand": "Honda", "model": "Civic", "year": 2022, "mileage": 100}
]

def drive(car, km):
    car["mileage"] += km

drive(cars[0], 15)  
drive(cars[1], 19) 
drive(cars[2], 5)  

for car in cars:
    print(car)

#task4
mileage_values = [car["mileage"] for car in cars]

mileage_array = np.array(mileage_values)
total_mileage = np.sum(mileage_array)
max_mileage = np.max(mileage_array)
min_mileage = np.min(mileage_array)
mean_mileage = np.mean(mileage_array)

print(f"Total mileage: {total_mileage}")
print(f"Maximum mileage: {max_mileage}")
print(f"Minimum mileage: {min_mileage}")
print(f"Mean mileage: {mean_mileage}")


#task5
car_brands = {car["brand"] for car in cars}
car_brands.add("Tesla")
car_brands.add("BMW")
car_brands.remove("Ford")
is_tesla_in_set = "Tesla" in car_brands

print(f"Car brands set: {car_brands}")
print(f"Is Tesla in the set? {is_tesla_in_set}")
