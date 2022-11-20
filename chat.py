# Chat Class
class Chat:

    def __init__(self, courseID, name):
        self.courseID = courseID
        self.name = name
        self.members = []


    
    def getCourseID(self):
        return self.courseID

    def getCourseName(self):
        return self.name

    def getMembers(self):
        return self.members

    def addMember(self, rin):
        if rin not in self.members:
            self.members.append(rin)
            return True
        else:
            return False
        # return self.members
    
    def removeMember(self, rin):
        if rin in self.members:
            self.members.remove(rin)
        