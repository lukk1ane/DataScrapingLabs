car_brands = {"Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Audi"}

car_brands.add("Tesla")
car_brands.add("Mercedes")

car_brands.remove("Ford")

is_tesla_present = "Tesla" in car_brands

print(f"Car Brands: {car_brands}")
print(f"Is Tesla in the set? {is_tesla_present}")
