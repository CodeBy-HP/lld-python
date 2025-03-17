# "Objects of a derived class should be replaceable with objects of the base class without altering the correctness of the program."

# In simple terms, a subclass should extend the behavior of the parent class without changing its expected behavior.


from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def no_of_tyres(self) -> int:
        pass

class EngineVehicle(Vehicle):
    @abstractmethod
    def has_engine(self) -> bool:
        pass

class Bicycle(Vehicle):  
    def no_of_tyres(self) -> int:
        return 2

class Car(EngineVehicle):  
    def no_of_tyres(self) -> int:
        return 4

    def has_engine(self) -> bool:
        return True

class Bike(EngineVehicle):
    def no_of_tyres(self) -> int:
        return 2

    def has_engine(self) -> bool:
        return True


v1 = Bike()
print(v1.no_of_tyres())

v2 = Bicycle()
print(v2.no_of_tyres())
