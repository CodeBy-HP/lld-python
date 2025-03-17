# abstract design pattern does not have has_a relationship between classes

from abc import ABC, abstractmethod


# Abstract Product Interfaces
class Button(ABC):
    @abstractmethod
    def click(self):
        pass


class CheckBox(ABC):
    @abstractmethod
    def check(self):
        pass


# Concrete Products
class WindowButton(Button):
    def click(self):
        print("Window button clicked")


class MacButton(Button):
    def click(self):
        print("Mac button clicked")


class WindowCheckBox(CheckBox):
    def check(self):
        print("Window checkbox checked")


class MacCheckBox(CheckBox):
    def check(self):
        print("Mac checkbox checked")


# Abstract Factory
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> CheckBox:
        pass


# Concrete Factories
class WindowFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowButton()  

    def create_checkbox(self) -> CheckBox:
        return WindowCheckBox()  


class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()  

    def create_checkbox(self) -> CheckBox:
        return MacCheckBox()  


# Application Class
class Application:
    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def run(self):
        self.button.click()
        self.checkbox.check()


# Usage
if __name__ == "__main__":
    print("App: Launched with the WindowsFactory.")
    app = Application(WindowFactory())
    app.run()

    print("\nApp: Launched with the MacFactory.")
    app = Application(MacFactory())
    app.run()
