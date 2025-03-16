class Car:
    brand = "Unoknown"
    model = "Unoknown"
    year = 0

    def display_info(self):
        print(f"{self.brand} {self.model} {self.year}")


car1 = Car()

car1.brand = "TATA"
car1.model = "NEXON"
car1.year = 2021

car1.display_info()