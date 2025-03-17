
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Worker(Workable):
    def work(self):
        print("Worker is working")

class Robot(Worker):  
    def work(self):
        print("🤖 Robot is working!")

class Human(Worker, Eatable): 
    def work(self):
        print("👨 Human is working!")

    def eat(self):
        print("🍽️ Human is eating!")

robo = Robot()
robo.work()

hum = Human()
hum.work()
hum.eat()

