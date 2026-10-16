import json
import xml.etree.ElementTree as ET


class User:

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    def login(self) -> None:
        print(f"{self.name} logged in.")

    def logout(self) -> None:
        print(f"{self.name} logged out.")




class PlatformError(Exception):
    pass


class UserNotFoundError(PlatformError):
    pass


class CourseNotFoundError(PlatformError):
    pass

class Student(User):

    def __init__(self, user_id: int, name: str, email: str) -> None:
        super().__init__(user_id, name, email)

    def submit_assignment(self, assignment: "Assignment") -> None:
        assignment.status = "submitted"
        print(f"Student {self.name} submitted the assignment.")

    def view_grades(self, assignment: "Assignment") -> None:
        print(f"Grade: {assignment.grade}")


class Teacher(User):

    def __init__(self, user_id: int, name: str, email: str) -> None:
        super().__init__(user_id, name, email)

    def create_course(self, course: "Course") -> None:
        print(f"Teacher {self.name} created course: {course.title}")

    def create_assignment(self, lesson: "Lesson",
                          assignment: "Assignment") -> None:
        lesson.assignments.append(assignment)

    def grade_assignment(self, assignment: "Assignment",
                         grade: float) -> None:
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100.")

        assignment.grade = grade
        print(f"Teacher {self.name} assigned grade {grade}.")


class Administrator(User):
    def remove_user(
            self, platform: "LearningPlatform", user_id: int
    ) -> None:
        platform.delete_user(user_id)
        print(f"Administrator {self.name} removed user {user_id}.")



class Course:

    def __init__(
        self, course_id: int, title: str, description: str
    ) -> None:
        self.id = course_id
        self.title = title
        self.description = description
        self.modules: list[Module] = []

    def add_module(self, module: "Module") -> None:
        self.modules.append(module)

    def remove_module(self, module: "Module") -> None:
        self.modules.remove(module)


class Module:

    def __init__(
        self, module_id: int, title: str, order: int
    ) -> None:
        self.id = module_id
        self.title = title
        self.order = order
        self.lessons: list[Lesson] = []

    def add_lesson(self, lesson: "Lesson") -> None:
        self.lessons.append(lesson)

    def remove_lesson(self, lesson: "Lesson") -> None:
        self.lessons.remove(lesson)


class Lesson:

    def __init__(
        self, lesson_id: int, title: str, content: str
    ) -> None:
        self.id = lesson_id
        self.title = title
        self.content = content
        self.assignments: list[Assignment] = []

    def edit_content(self, new_content: str) -> None:
        self.content = new_content

    def view(self) -> None:
        print(f"{self.title}: {self.content}")


class Assignment:

    def __init__(
        self,
        assignment_id: int,
        title: str,
        description: str,
        deadline: str,
    ) -> None:
        self.id = assignment_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = "not submitted"
        self.grade: float | None = None

    def edit(self, title: str, description: str,
             deadline: str) -> None:
        self.title = title
        self.description = description
        self.deadline = deadline


class Enrollment:

    def __init__(
        self, enrollment_id: int, date: str, status: str,
        student: Student, course: Course
    ) -> None:
        self.id = enrollment_id
        self.date = date
        self.status = status
        self.student = student
        self.course = course

    def enroll(self) -> None:
        self.status = "active"

    def cancel(self) -> None:
        self.status = "cancelled"


class Certificate:

    def __init__(
        self, certificate_id: int, issue_date: str, title: str
    ) -> None:
        self.id = certificate_id
        self.issue_date = issue_date
        self.title = title

    def generate(self) -> None:
        print(f"Certificate generated: {self.title}")

    def view(self) -> None:
        print(f"{self.title}, issued on {self.issue_date}")


class Notification:

    def __init__(
        self, notification_id: int, message: str, user: User
    ) -> None:
        self.id = notification_id
        self.message = message
        self.user = user
        self.is_read = False

    def mark_as_read(self) -> None:
        self.is_read = True



class LearningPlatform:

    def __init__(self) -> None:
        self.users: dict[int, User] = {}
        self.courses: dict[int, Course] = {}


    def add_user(self, user: User) -> None:
        if user.id in self.users:
            raise ValueError("A user with this ID already exists.")
        self.users[user.id] = user


    def get_user(self, user_id: int) -> User:
        if user_id not in self.users:
            raise UserNotFoundError(
                f"User with ID {user_id} was not found."
            )
        return self.users[user_id]

    def update_user(self, user_id: int, name: str, email: str) -> None:
        user = self.get_user(user_id)
        user.name = name
        user.email = email


    def delete_user(self, user_id: int) -> None:
        self.get_user(user_id)
        del self.users[user_id]


    def add_course(self, course: Course) -> None:
        if course.id in self.courses:
            raise ValueError("A course with this ID already exists.")
        self.courses[course.id] = course


    def get_course(self, course_id: int) -> Course:
        if course_id not in self.courses:
            raise CourseNotFoundError(
                f"Course with ID {course_id} was not found."
            )
        return self.courses[course_id]


    def update_course(
        self, course_id: int, title: str, description: str
    ) -> None:
        course = self.get_course(course_id)
        course.title = title
        course.description = description


    def delete_course(self, course_id: int) -> None:
        self.get_course(course_id)
        del self.courses[course_id]


    def save_users_json(self, filename: str) -> None:
        users_data = []

        for user in self.users.values():
            users_data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(users_data, file, ensure_ascii=False, indent=4)


    def load_users_json(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as file:
            users_data = json.load(file)

        for data in users_data:
            user = User(
                data["id"],
                data["name"],
                data["email"]
            )
            self.add_user(user)


    def save_users_xml(self, filename: str) -> None:
        root = ET.Element("users")

        for user in self.users.values():
            user_element = ET.SubElement(root, "user")

            ET.SubElement(user_element, "id").text = str(user.id)
            ET.SubElement(user_element, "name").text = user.name
            ET.SubElement(user_element, "email").text = user.email

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)



    def load_users_xml(self, filename: str) -> None:
        tree = ET.parse(filename)
        root = tree.getroot()

        for user_element in root.findall("user"):
            user = User(
                int(user_element.find("id").text),
                user_element.find("name").text,
                user_element.find("email").text
            )
            self.add_user(user)



    def save_courses_json(self, filename: str) -> None:
        courses_data = []

        for course in self.courses.values():
            courses_data.append({
                "id": course.id,
                "title": course.title,
                "description": course.description
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(courses_data, file, ensure_ascii=False, indent=4)

    def load_courses_json(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as file:
            courses_data = json.load(file)

        for data in courses_data:
            course = Course(
                data["id"],
                data["title"],
                data["description"]
            )
            self.add_course(course)





student = Student(1, "Anna", "anna@example.com")
teacher = Teacher(2, "Ivan", "ivan@example.com")

course = Course(1, "Python Basics", "Introduction to Python")
module = Module(1, "OOP", 1)
lesson = Lesson(1, "Classes", "Introduction to classes")


assignment = Assignment(
    1,
    "Create a class",
    "Write a simple Python class",
    "2026-10-20"
)


course.add_module(module)
module.add_lesson(lesson)
teacher.create_assignment(lesson, assignment)


student.submit_assignment(assignment)


teacher.grade_assignment(assignment, 95)


student.view_grades(assignment)


print("\n CRUD test")

platform = LearningPlatform()

platform.add_user(student)
print(platform.get_user(1).name)

platform.update_user(1, "Anna Smith", "anna.smith@example.com")
print(platform.get_user(1).name)

platform.delete_user(1)
print("User deleted.")


#проверка поведения программы при совпадающих id юзеров

print("\n Exception handling test")

platform = LearningPlatform()

try:
    platform.add_user(student)
    platform.add_user(student)
except ValueError as error:
    print(f"Could not add user: {error}")

try:
    platform.get_user(999)
except UserNotFoundError as error:
    print(f"Could not find user: {error}")




print("\n JSON test")

platform = LearningPlatform()
student = Student(1, "Anna", "anna@example.com")
platform.add_user(student)

platform.save_users_json("users.json")
print("Users saved to users.json")



print("\nJSON loading test")

new_platform = LearningPlatform()
new_platform.load_users_json("users.json")

print(new_platform.get_user(1).name)



print("\n XML test")

xml_platform = LearningPlatform()
xml_platform.add_user(
    Student(2, "Maria", "maria@example.com")
)

xml_platform.save_users_xml("users.xml")
print("Users saved to users.xml")

loaded_platform = LearningPlatform()
loaded_platform.load_users_xml("users.xml")
print(loaded_platform.get_user(2).name)




print("\n Courses JSON test")

course_platform = LearningPlatform()
course_platform.add_course(
    Course(10, "Python OOP", "Object-oriented programming")
)

course_platform.save_courses_json("courses.json")
print("Courses saved to courses.json")

restored_platform = LearningPlatform()
restored_platform.load_courses_json("courses.json")
print(restored_platform.get_course(10).title)
