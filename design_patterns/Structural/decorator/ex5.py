from abc import ABC, abstractmethod


class SmartHomeSystem(ABC):
    @abstractmethod
    def getFeatures(self):
        pass

    @abstractmethod
    def cost(self):
        pass


class Home(SmartHomeSystem):
    def getFeatures(self):
        return "Base Home"
    
    def cost(self):
        return 100


class HomeDecorator(SmartHomeSystem):  
    def __init__(self, home: SmartHomeSystem):
        self.home = home

    def getFeatures(self):
        return self.home.getFeatures() 

    def cost(self):
        return self.home.cost() 


class SmartLighting(HomeDecorator):  
    def getFeatures(self):
        return super().getFeatures() + ", Smart Lighting"
    
    def cost(self):
        return super().cost() + 50
    

class SecurityCamera(HomeDecorator):
    def getFeatures(self):
        return super().getFeatures()  + ", Security Camera"
    
    def cost(self):
        return super().cost() + 80
    

home = Home()
home = SmartLighting(home)
home = SecurityCamera(home)

print(home.getFeatures())  # Output: "Base Home, Smart Lighting, Security Camera"
print(home.cost())         # Output: 230
