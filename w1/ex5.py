from ex3 import cars

unique_brands = {car['brand'] for car in cars}

unique_brands.add('Mercedes')
unique_brands.add('Ferrari')
unique_brands.remove('BMW')

print(unique_brands)
brand = 'Tesla'

print(f'brands {'' if brand in unique_brands else 'does not'} contain {brand}')