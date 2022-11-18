# User Class
class User:

    def __init__(self, rin, phone, courses, chats):
        self.rin = rin
        self.phone = phone
        self.courses = courses
        self.chats = chats

    # def __init__(self, rin, phone):
    #     self.rin = rin
    #     self.phone = phone
    #     self.courses = []
    #     self.chats = []

    def get_courses(self):
        return self.courses

    def in_course(self, courseID):
        return courseID in self.courses

    def get_rin(self):
        return self.rin

    def get_phone(self):
        return self.phone

    def get_chats(self):
        return self.chats

    def add_course(self, courseID):
        if courseID not in self.courses:
           self.courses.append(courseID)
           return True
        return False

    def remove_course(self, courseID):
        if courseID not in self.courses:
            return False
        self.courses.remove(courseID)
        return True
    

    
    


   