import numpy as np

from ex3 import cars

mil_vals = np.array([car['mileage'] for car in cars])

print(f'total mileage: {mil_vals.sum()}')
print(f'minimal mileage: {mil_vals.min()}')
print(f'maximal mileage: {mil_vals.max()}')
print(f'mean mileage: {mil_vals.mean()}')