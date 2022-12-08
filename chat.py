# Chat Class
class Chat:

    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name
        self.members = []

    def get_course_id(self):
        """Returns course id"""
        return self.course_id

    def get_course_name(self):
        """Returns course name"""
        return self.name

    def get_members(self):
        """Returns list of members"""
        return self.members

    def add_member(self, rin):
        """Adds a RIN to the list of members"""
        if rin not in self.members:
            self.members.append(rin)
            return True
        return False

    def remove_member(self, rin):
        """Removes a RIN from the list of members"""
        if rin in self.members:
            self.members.remove(rin)
