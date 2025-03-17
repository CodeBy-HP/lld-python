# class should depend on interfaces reather than concrete classes


from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        print(f"💳 Paid {amount} using Credit Card")

class PayPalPayment(PaymentMethod):
    def pay(self, amount):
        print(f"💰 Paid {amount} using PayPal")

class ShoppingCart:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def checkout(self, amount):
        self.payment_method.pay(amount)

cart1 = ShoppingCart(CreditCardPayment())
cart1.checkout(1000)

cart2 = ShoppingCart(PayPalPayment())
cart2.checkout(500)
