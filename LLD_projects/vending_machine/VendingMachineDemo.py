from VendingMachine import VendingMachine
from Coin import Coin
from Note import Note
from Product import Product


def run():
    vm = VendingMachine.get_instance()

    p1 = Product("COKE",0.25)
    p2 = Product("CHIPS",0.5)
    p3 = Product("5STAR",1)

    vm.inventory.add_product(p1,2)
    vm.inventory.add_product(p2,1)
    vm.inventory.add_product(p3,5)

    vm.display_product()

    vm.select_product(p1)
    vm.insert_coin(Coin.PENNY)
    vm.insert_note(Note.TEN)
    vm.return_change()
    vm.dispense_product()
    vm.return_change()
    vm.display_product()



    p1 = Product("COKE",0.25)
    p2 = Product("CHIPS",0.5)
    p3 = Product("5STAR",1)

    vm.inventory.add_product(p1,2)
    vm.inventory.add_product(p2,1)
    vm.inventory.add_product(p3,5)

    

    vm.select_product(p1)
    vm.insert_coin(Coin.PENNY)
    vm.insert_note(Note.TEN)
    vm.return_change()
    vm.dispense_product()
    vm.return_change()


if  __name__ == "__main__":
    run()