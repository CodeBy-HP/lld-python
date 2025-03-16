# the classmethod only depends upon the variables of class and not instance
class Example:
    counter = 0

    @classmethod
    def increment(cls):
        cls.counter += 1


Example.increment()
print(Example.counter)