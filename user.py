# User Class
class User:

    def __init__(self, rin, phone, courses, chats):
        self.rin = rin
        self.phone = phone
        self.courses = courses
        self.chats = chats

    def get_courses(self):
        """Returns the user's list of registered courses"""
        return self.courses

    def in_course(self, course_id):
        """Returns whether the user is registered to the given course"""
        return course_id in self.courses

    def get_rin(self):
        """Returns the user's RIN"""
        return self.rin

    def get_phone(self):
        """Returns the user's phone number"""
        return self.phone

    def get_chats(self):
        """Returns the user's list of registered group chats"""
        return self.chats

    def add_course(self, course_id):
        """Registers a user to the given course if they are not registered to it"""
        if course_id not in self.courses:
            self.courses.append(course_id)
            return True
        return False

    def remove_course(self, course_id):
        """Removes a course from a user's list of registered courses"""
        if course_id not in self.courses:
            return False
        self.courses.remove(course_id)
        return True
