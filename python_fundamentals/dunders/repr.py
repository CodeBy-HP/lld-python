#  The __repr__ method is used to return a developer-friendly string representation of an object.
# It helps in debugging and logging.

class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def __repr__(self):
        return f"Car(brand='{self.brand}', model='{self.model}')"

# Usage
c = Car("Toyota", "Camry")
print(c)  # Car(brand='Toyota', model='Camry')  <- Instead of <__main__.Car object at 0x...>
