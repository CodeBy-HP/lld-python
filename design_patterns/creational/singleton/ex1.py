class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name="default", age=24):
        if not hasattr(self, 'initialized'):
            self.name = name
            self.age = age
            self.initialized = True

s1 = Singleton("harsh", 23)
s2 = Singleton()

print(s1.__hash__(), s1.name, s1.age)
print(s2.__hash__(), s2.name, s2.age)