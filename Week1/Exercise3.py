import numpy as np


class CarManager:
    def __init__(self):
        self.cars = []

    def add_car(self, brand, model, year, mileage):
        self.cars.append({"brand": brand, "model": model, "year": year, "mileage": mileage})

    def drive(self, car, km):
        car["mileage"] += km

    def get_all_cars(self):
        return self.cars

    def get_mileage_array(self):
        return np.array([car["mileage"] for car in self.cars], dtype=float)

    def compute_mileage_stats(self):
        mileage_array = self.get_mileage_array()
        return {
            "Total mileage": float(np.sum(mileage_array)),
            "Max mileage": float(np.max(mileage_array)),
            "Min mileage": float(np.min(mileage_array)),
            "Mean mileage": float(np.mean(mileage_array)),
        }


if __name__ == '__main__': # Car management simulation

    car_manager = CarManager()

    car_manager.add_car("Toyota", "Corolla", 2015, 50000)
    car_manager.add_car("Honda", "Civic", 2018, 30000)
    car_manager.add_car("Ford", "Focus", 2020, 20000)

    # Simulate driving
    car_manager.drive(car_manager.cars[0], 150)
    car_manager.drive(car_manager.cars[1], 200)

    print("Updated Car Data:", car_manager.get_all_cars())

    # Compute mileage statistics
    mileage_stats = car_manager.compute_mileage_stats()
    print("Mileage Stats:", mileage_stats)


