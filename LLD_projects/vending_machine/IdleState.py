from VendingMachineState import VendingMachineState

class IdleState(VendingMachineState):
    def select_product(self,product):
        if self.vending_machine.inventory.is_available(product):
            self.vending_machine.selected_product = product
            print(f"{product.name} selected sucessfully !!!")
            self.vending_machine.set_state(self.vending_machine.ready_state)
        else:
            print(f"{product.name} not available !!!")

    def insert_coin(self):
        print("Select the product first")

    def insert_note(self):
        print("Select the product first")

    def dispense_product(self):
        print("Select the product first")

    def return_change(self):
        print("No change to return")
