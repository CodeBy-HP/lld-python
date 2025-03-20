from VendingMachineState import VendingMachineState

class DispenseState(VendingMachineState):
    def select_product(self):
        print("The product already selected")

    def insert_coin(self):
        print("Already have money")

    def insert_note(self):
        print("Already have money")

    def dispense_product(self):
        quantity = self.vending_machine.inventory.get_quantity(self.vending_machine.selected_product)
        self.vending_machine.inventory.update_quantity(quantity-1,self.vending_machine.selected_product)
        print(f"{self.vending_machine.selected_product.name} Dispensed Sucessfully")
        self.vending_machine.set_state(self.vending_machine.return_state)

    def return_change(self):
        print("First Dispense the product")


