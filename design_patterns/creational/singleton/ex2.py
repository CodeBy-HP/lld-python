
class Singleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance
    

ob1 = Singleton().get_instance()
ob2 = Singleton().get_instance()

print(ob1.__hash__(), ob2.__hash__())