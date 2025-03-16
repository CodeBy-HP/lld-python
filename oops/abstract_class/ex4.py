
from abc import ABC, abstractmethod


class LibraryItem(ABC):
    @abstractmethod
    def check_out(self):
        pass
    
    @abstractmethod
    def return_item(self):
        pass

class DigitalItem(ABC):
    @abstractmethod
    def download(self):
        pass


class Book(LibraryItem):
    def check_out(self):
        print("checked out")

    def return_item(self):
        print("book returned")

    def __del__(self):
        print("book object is destroyed")


class Ebook(LibraryItem,DigitalItem):
    def download(self):
        print("book downloaded")

    def check_out(self):
        print("checked out")

    def return_item(self):
        print("book returned")

    def read(self):
        print("reading the book")

    def __del__(self):
        print("the ebook object is destroyed")


book1 = Book()
book1.check_out()

ebook1 = Ebook()
ebook1.read()

del book1
del ebook1
    


