# association losely coupled relationship ( one object can exist without another)

class Teacher:
    def __init__(self,name):
        self.name = name

    def assign_homework(self,student,homework):
        print(f"{self.name} assigns homework {homework} to {student.name}")
        student.receive_homework(homework)


class Student:
    def __init__(self,name):
        self.name = name
        self.homework_list = []

    def receive_homework(self,homework):
        self.homework_list.append(homework)
        print(f"{self.name} received homework {homework}")

    def show_homework(self):
        print(f"{self.name}'s homework: {', '.join(self.homework_list)}")


teacher = Teacher("Mr. verma")
student = Student("harsh")

teacher.assign_homework(student, "math homework")

student.show_homework()
