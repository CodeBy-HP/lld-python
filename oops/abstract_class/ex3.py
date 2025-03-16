
from abc import ABC, abstractmethod


class Appliance(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

class SmartMachine(ABC):
    @abstractmethod
    def connect_to_wifi(self,network):
        pass


class WashingMachine(Appliance,SmartMachine):
    def connect_to_wifi(self,network):
        print(f"machine is connected to wifi {network}")

    def turn_on(self):
        print("machine is turned on")

    def turn_off(self):
        print("machine is turned off")

    def __del__(self):
        print("machine is destroyed")


machine1 = WashingMachine()
machine1.connect_to_wifi("Home network")
machine1.turn_on()
machine1.turn_off()

del machine1

