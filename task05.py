cars = [
    {"brand": "Toyota", "model": "Camry", "year": 2020, "mileage": 15100},
    {"brand": "Honda", "model": "Civic", "year": 2019, "mileage": 22250},
    {"brand": "Ford", "model": "Mustang", "year": 2021, "mileage": 5050},
    {"brand": "Chevrolet", "model": "Malibu", "year": 2018, "mileage": 30000},
    {"brand": "Tesla", "model": "Model 3", "year": 2022, "mileage": 2000}
]

unique_brands = set(car['brand'] for car in cars)

unique_brands.add("Nissan")
unique_brands.add("BMW")
unique_brands.remove("Chevrolet")

is_tesla_present = "Tesla" in unique_brands

print("Unique Car Brands:", unique_brands)
print("Is 'Tesla' in the set?", is_tesla_present)