from abc import ABC, abstractmethod


class Pizza(ABC):
    @abstractmethod
    def cost(self):
        pass


class Margherita(Pizza):
    def cost(self):
        return 120
    

class PizzaDecorator(Pizza):  # aleready a abstract class as Pizza is inherited from ABC
    def __init__(self, pizza: Pizza):
        self.pizza = pizza
    
    @abstractmethod
    def cost(self):
        pass


class ExtraCheese(PizzaDecorator):
    def cost(self):
        return self.pizza.cost() + 20
    

class Pepperoni(PizzaDecorator):
    def cost(self):
        return self.pizza.cost() + 20
    

pizza = Margherita()
pizza = ExtraCheese(pizza)  # 120 + 20 = 140
pizza = Pepperoni(pizza)    # 140 + 20 = 160

print(pizza.cost())  #  Output: 160
