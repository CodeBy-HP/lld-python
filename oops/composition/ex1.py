class Address:
    def __init__(self,street,city):
        self.street = street
        self.city = city


class Person:
    def __init__(self,name,street,city):
        self.name = name
        self.address = Address(street,city)

    def get_person_detail(self):
        return f"{self.name} lives at {self.address.street} , {self.address.city}"
    

person = Person("harsh", "ayodhya nagar", "bhopal")

print(person.get_person_detail())
        

        