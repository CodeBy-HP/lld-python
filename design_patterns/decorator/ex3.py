from abc import ABC, abstractmethod

# Abstract Base Pizza Class
class Pizza(ABC):
    @abstractmethod
    def cost(self):
        pass

# Concrete Pizza Classes
class Farmhouse(Pizza):
    def cost(self):
        return 100

class Margherita(Pizza):
    def cost(self):
        return 120

class VegDelight(Pizza):
    def cost(self):
        return 140

# Base Decorator
class ToppingDecorator(Pizza,ABC):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza

    @abstractmethod
    def cost(self):
        pass

# Concrete Toppings
class ExtraCheese(ToppingDecorator):
    def cost(self):
        return self.pizza.cost() + 30

class Olives(ToppingDecorator):
    def cost(self):
        return self.pizza.cost() + 20

class Pepperoni(ToppingDecorator):
    def cost(self):
        return self.pizza.cost() + 50

# Ordering a Margherita pizza with Extra Cheese and Olives
pizza = Margherita()
pizza = ExtraCheese(pizza)  # Wrapping Margherita with Extra Cheese
pizza = Olives(pizza)  # Wrapping previous result with Olives

print(pizza.cost())  # Output: 120 + 30 + 20 = 170
