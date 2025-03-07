import numpy as np

mileages = [12000, 15000, 18000, 22000, 14000,
             10000, 25000, 30000, 35000, 19000]

mileages_array = np.array(mileages)

total_mileage = np.sum(mileages_array)
max_mileage = np.max(mileages_array)
min_mileage = np.min(mileages_array)
mean_mileage = np.mean(mileages_array)

print(f"Total Mileage: {total_mileage}")
print(f"Maximum Mileage: {max_mileage}")
print(f"Minimum Mileage: {min_mileage}")
print(f"Mean Mileage: {mean_mileage}")
