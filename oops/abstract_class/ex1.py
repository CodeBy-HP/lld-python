from abc import ABC, abstractmethod


class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        pass

    @abstractmethod
    def stop_engine(self):
        pass


class Car(Vehicle):
    def start_engine(self):
        print("car engine started")

    def stop_engine(self):
        print("car engine stopeed")

    def __del__(self):
        print("car object is deleted")


car1 = Car()

car1.start_engine()
car1.stop_engine()

del car1

# car1.start_engine()      it will give error