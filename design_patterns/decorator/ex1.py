# why we use decorator pattern
# if we use simple inheritance then following problems occurs
#  Class Explosion – If we want different combinations (e.g., only Olives, Cheese + Olives, Cheese + Pepperoni), we would need many subclasses.
#  Tightly Coupled Code – If we want to change the cost of CheesePizza, we have to modify multiple classes.
#  Not Flexible – What if we want to add Mushrooms later? We'd have to create even more subclasses.

# Base Pizza class
class Pizza:
    def cost(self):
        return 100  # Base price

# Subclasses for different types of pizzas
class CheesePizza(Pizza):
    def cost(self):
        return super().cost() + 30

class PepperoniCheesePizza(CheesePizza):
    def cost(self):
        return super().cost() + 50

class OlivePepperoniCheesePizza(PepperoniCheesePizza):
    def cost(self):
        return super().cost() + 20

# Ordering Cheese + Pepperoni + Olives Pizza
pizza = OlivePepperoniCheesePizza()
print(f"Total Cost: {pizza.cost()}")  # Output: 200


# Bad Approach
