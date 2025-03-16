class Car:
    def __init__(self,brand,year,model):
        self.brand = brand
        self.year = year
        self.model = model

    def display_info(self):
        print(f"{self.brand} {self.year} {self.model}")


car = Car("Tata", "nexon", 2021)
car.display_info()