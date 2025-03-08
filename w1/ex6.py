import random
from typing import override


class Animal:
    def make_sound(self):
        pass


class Dog(Animal):
    @override
    def make_sound(self):
        print('woof woof')


class Cat(Animal):
    @override
    def make_sound(self):
        print('meow meow')


animals = [Cat() if random.randint(1, 100) % 2 == 0 else Dog() for _ in range(8)]

for animal in animals:
    animal.make_sound()
