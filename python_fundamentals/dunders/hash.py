class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def __eq__(self, other):
        return isinstance(other, Car) and self.brand == other.brand and self.model == other.model

    def __hash__(self):
        return hash((self.brand, self.model))

# Usage
car1 = Car("Toyota", "Camry")
car2 = Car("Toyota", "Camry")
car3 = Car("Honda", "Civic")

car_set = {car1, car2, car3}
print(len(car_set))  # 2 (car1 and car2 are treated as the same object)

print(car_set)
