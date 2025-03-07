
def Exercise_1 (filename):
    with open(filename, 'r' ) as file:
        date = file.read()
        lines = date.split('\n')
        words = data.split(' ')
        chars = data.split()
        return len(lines), len(words), len(chars)

def Exercise_2 (dictionary):
    def HighestScore(dictionary):
        return max(dictionary, key=dictionary.get)

    def AverageScore(dictionary):
        return sum(dictionary.values()) / len(dictionary)

    def AboveAverage(dictionary):
        average = sum(dictionary.values()) / len(dictionary)
        return [name for name, score in dictionary.items() if score > average]

def Exercise_3():
    cars = [
        {"brand": "toyota", "model": "idk", "year": 2001, "mileage": 101010},
        {"brand": "toyota2", "model": "idk2", "year": 2002, "mileage": 202020},
        {"brand": "toyota3", "model": "idk3", "year": 2003, "mileage": 303030}
    ]

    def drive(car, km):
        car["mileage"] += km

    def Simulate(cars):
        for car in cars:
            drive(car, 10000)
        return cars

    return Simulate(cars)

updated_cars = Exercise_3()
for car in updated_cars:
    print(car)


Exercise_3()

Exercise_3()

