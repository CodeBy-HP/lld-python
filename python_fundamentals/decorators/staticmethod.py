# The @staticmethod decorator in Python defines a method inside a class that does not depend on the instance (self) or the class (cls).
# It behaves like a regular function but is placed inside a class for better organization.

class Example:
    @staticmethod
    def static_method():
        print("i am a static method")

    def normal_mehod(self):
        print("i am a normal mehthod")


ex1 = Example()
ex1.normal_mehod()
Example.static_method()