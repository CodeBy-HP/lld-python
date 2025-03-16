# The Factory Pattern is a creational design pattern that provides a way to instantiate objects without exposing the instantiation logic.

from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass
    

class Circle(Shape):
    def draw(self):
        return "Circle"
    
class Rectangle(Shape):
    def draw(self):
        return "Rectangle"



class ShapeFactory:
    @staticmethod
    def getShape(shape_type : str) -> Shape:
        shape_type = shape_type.upper()

        if shape_type == "CIRCLE":
            return Circle()
        
        elif shape_type == "RECTANGLE":
            return Rectangle()
        
        else:
            raise ValueError("Invalid shape type")
        

if __name__ == '__main__':

    factory = ShapeFactory()

    shape1 = factory.getShape("CIRCLE")

    shape2 = factory.getShape("RECTANGLE")

    print(shape1.draw())
    print(shape2.draw())


