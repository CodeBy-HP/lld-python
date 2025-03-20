
class Inventory:
    def __init__(self):
        self.product_dict = {}
    
    def add_product(self, product, quantity):
        self.product_dict[product] = quantity
    
    def remove(self, product):
        if product in self.product_dict:
            del self.product_dict[product]
        else:
            print("Product not found")

    def update_quantity(self,quantity,product):
        self.product_dict[product] = quantity
    
    def get_quantity(self,product):
        return self.product_dict[product]
    
    def is_available(self,product):
        return product in self.product_dict and self.product_dict[product] > 0

    def get_products(self):
        return self.product_dict