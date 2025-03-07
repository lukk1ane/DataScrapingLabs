import numpy as np


class CarManager:
    def __init__(self):
        self.cars = []
        self.unique_brands = set()

    def add_car(self, brand, model, year, mileage):
        self.cars.append({"brand": brand, "model": model, "year": year, "mileage": mileage})
        self.unique_brands.add(brand)

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

    def manage_brands(self, add_brands=None, remove_brand=None):
        if add_brands:
            self.unique_brands.update(add_brands)
        if remove_brand and remove_brand in self.unique_brands:
            self.unique_brands.remove(remove_brand)
        return self.unique_brands


if __name__ == '__main__': # car management simulation

    car_manager = CarManager()

    car_manager.add_car("Toyota", "Corolla", 2015, 50000)
    car_manager.add_car("Honda", "Civic", 2018, 30000)
    car_manager.add_car("Ford", "Focus", 2020, 20000)

    # driving
    car_manager.drive(car_manager.cars[0], 150)
    car_manager.drive(car_manager.cars[1], 200)

    print("\nUpdated Car Data:", car_manager.get_all_cars())

    # mileage statistics
    mileage_stats = car_manager.compute_mileage_stats()
    print("\nMileage Stats:", mileage_stats)

    # manipulations on brands
    print("\nInitial Brands:", car_manager.unique_brands)
    car_manager.manage_brands(add_brands={"BMW", "Mercedes"})
    print("Brands after addition:", car_manager.unique_brands)
    car_manager.manage_brands(remove_brand="Honda")
    print("Brands after removal:", car_manager.unique_brands)
    print("\nIs Tesla in the set?", "\nAnswer:", "Tesla" in car_manager.unique_brands)



