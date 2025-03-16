
class Engine:
    def __init__(self,horsepower):
        self.horsepower = horsepower


class Car:
    def __init__(self,brand,engine):
        self.brand = brand
        self.engine = engine # car has a engine


engine = Engine(150)
car1 = Car("fortuner",engine)

print(f"{car1.brand} has a {car1.engine.horsepower} horsepower engine")