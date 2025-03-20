from tabulate import tabulate

class VendingMachineInterface:
    def display_product(self, inventory):
        product_dict = inventory.get_products()
        table = []
        for product, quantity in product_dict.items():
            table.append([product.name, f"${product.cost:.2f}", quantity])
        
        headers = ["Product Name", "Cost", "Quantity"]
        print(tabulate(table, headers, tablefmt="grid"))
