
from abc import ABC, abstractmethod


class Appliance(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class WashingMachine(Appliance):
    def turn_on(self):
        print("washing machine is turning on")

    def turn_off(self):
        print("washing machine is turning off")

    def __del__(self):
        print("washing machine object is deleted")


machine1 = WashingMachine()
machine1.turn_on()
machine1.turn_off()

del machine1
        
    
