# "Software entities (classes, modules, functions) should be open for extension but closed for modification."

from abc import ABC, abstractmethod

class DiscountStrategy(ABC):  
    @abstractmethod
    def get_discount(self, amount):
        pass

class GoldDiscountStrategy(DiscountStrategy):
    def get_discount(self, amount):
        return amount * 0.13 

class SilverDiscountStrategy(DiscountStrategy):
    def get_discount(self, amount):
        return amount * 0.15  

class CalculateDiscount:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy
    
    def calculate(self, amount):
        return self.strategy.get_discount(amount)

gold_customer = CalculateDiscount(GoldDiscountStrategy())
silver_customer = CalculateDiscount(SilverDiscountStrategy())

print(gold_customer.calculate(1000))  
print(silver_customer.calculate(1000)) 

