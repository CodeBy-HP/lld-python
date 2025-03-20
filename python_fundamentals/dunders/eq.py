class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def __eq__(self, other):
        if isinstance(other, Car):
            return vars(self) == vars(other)  # compares the objects that is stored in dictionary __dict__ of the instance
        return False

    

# Usage
c1 = Car("Toyota", "Camry")
c2 = Car("Toyota", "Camry")
c3 = Car("Honda", "Civic")

print(c1 == c2)  # True  (Since brand and model are the same)
print(c1 == c3)  # False

