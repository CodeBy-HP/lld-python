from abc import ABC, abstractmethod

# Abstract Strategy Class
class DriveStrategy(ABC):
    @abstractmethod
    def drive(self):
        pass

# Concrete Strategy Classes
class NormalDriveStrategy(DriveStrategy):
    def drive(self):
        print("Normal Drive Strategy")

class SpecialDriveStrategy(DriveStrategy):
    def drive(self):
        print("Special Drive Strategy")

# Context Class
class Vehicle:
    def __init__(self, strategy: DriveStrategy):
        self.strategy = strategy
    
    def drive(self):
        self.strategy.drive()

# Concrete Context Classes
class OffroadVehicle(Vehicle):
    pass 

class PassengerVehicle(Vehicle):
    pass

# Usage
vh1 = OffroadVehicle(SpecialDriveStrategy())
vh1.drive()
vh2 = OffroadVehicle(NormalDriveStrategy())
vh2.drive()