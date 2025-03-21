cars = [
    {"brand": "Toyota", "model": "Camry", "year": 2020, "mileage": 15000},
    {"brand": "Honda", "model": "Civic", "year": 2019, "mileage": 22000},
    {"brand": "Ford", "model": "Mustang", "year": 2021, "mileage": 5000},
    {"brand": "Chevrolet", "model": "Malibu", "year": 2018, "mileage": 30000},
    {"brand": "Tesla", "model": "Model 3", "year": 2022, "mileage": 2000}
]

def drive(car, km):
    car['mileage'] += km

if __name__ == "__main__":
    drive(cars[0], 100)
    drive(cars[1], 250)
    drive(cars[2], 50)

    for car in cars:
        print(f"{car['brand']} {car['model']} ({car['year']}): {car['mileage']} km")