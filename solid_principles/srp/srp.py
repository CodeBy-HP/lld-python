# Single Responsiblity to Change
# Each class should have only one reason to change.
# A class should have only one responsibility.

class Marker:
    def __init__(self, price, color):
        self.price = price
        self.color = color


class Invoice:
    def __init__(self, marker, quantity):
        self.marker = marker
        self.quantity = quantity

    def get_total(self):
        return self.marker.price * self.quantity  


class PrintInv:
    def __init__(self, invoice):
        self.invoice = invoice

    def print_invoice(self):
        print(f"Printing the invoice... Total: {self.invoice.get_total()}")  


class SaveInvToDB:
    def __init__(self, invoice):
        self.invoice = invoice

    def save_to_db(self):
        print("Saving the invoice to DB...")  


marker = Marker(23, "red")
invoice = Invoice(marker, 4)

print(invoice.get_total())

printer = PrintInv(invoice)
printer.print_invoice()  

db_saver = SaveInvToDB(invoice)
db_saver.save_to_db()  

