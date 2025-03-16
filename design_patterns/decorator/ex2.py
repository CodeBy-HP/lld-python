# ✅ Why is this the Best Approach?
# ✔ Flexible & Scalable – You can add, remove, or reorder toppings easily.
# ✔ Follows Open/Closed Principle (OCP) – New toppings can be added without modifying the base Pizza class.
# ✔ No Class Explosion – Unlike inheritance, we don’t need separate subclasses for each combination.
# ✔ Preserves Encapsulation – Each topping (decorator) manages only its behavior without modifying the Pizza class.

class Pizza:
    def cost(self):
        return 100  # Base price

# Base Decorator
class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self.pizza = pizza  # Store the wrapped pizza object

    def cost(self):
        return self.pizza.cost()

# Concrete Decorators (Toppings)
class Cheese(PizzaDecorator):
    def cost(self):
        return self.pizza.cost() + 30

class Pepperoni(PizzaDecorator):
    def cost(self):
        return self.pizza.cost() + 50

class Olives(PizzaDecorator):
    def cost(self):
        return self.pizza.cost() + 20

# Ordering a Pizza with Cheese + Pepperoni + Olives
pizza = Pizza()
pizza = Cheese(pizza)  # Wrap base pizza with Cheese
pizza = Pepperoni(pizza)  # Wrap previous pizza with Pepperoni
pizza = Olives(pizza)  # Wrap previous pizza with Olives

print(pizza.cost())  # ✅ Output: 200
