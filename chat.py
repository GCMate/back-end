# Chat Class
class Chat:

    def __init__(self, course, num):
        self.course = course
        self.num = num


    
    def chatID(self):
        return '{}{}'.format(self.course, self.num)