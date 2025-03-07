class Animal:

    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Woof!"


class Cat(Animal):
    def make_sound(self):
        return "Meow!"

if __name__ == "__main__":
    animals = [Dog(), Cat(), Dog(), Cat()]
    for animal in animals:
        print(animal.make_sound())