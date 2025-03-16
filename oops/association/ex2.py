class Driver:
    def __init__(self,name):
        self.name = name

class Car:
    def __init__(self,brand):
        self.brand = brand


driver = Driver("harsh")
car1 = Car("lambo")

driver.car = car1

print(driver.car.brand)
        