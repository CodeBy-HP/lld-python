# has - a relationship one object can contain another, but both can exist independelty

class Student:
    def __init__(self,name):
        self.name = name
        self.courses = []
    
    def get_name(self):
        return self.name
    
    def get_courses(self):
        print(f"{self.name} has {', '.join(self.courses)}")


class Course:
    def __init__(self,name):
        self.name = name
        self.students = []

    def add_student(self,student):
        self.students.append(student)
        print(f"Student {student.get_name()} has a been added to the course {self.name}")

    def get_students(self):
        return [student.get_name() for student in self.students]
    

student1  = Student("harsh")
student2 = Student("ankit")

course = Course("Math")

course.add_student(student1)
course.add_student(student2)

student_in_course = course.get_students()
print(f"Students in {course.name} course: {', '.join(student_in_course)}")