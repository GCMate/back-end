# Course Class
class Course:

    def __init__(self, crse, id, subj, title):
        self.crse = crse
        self.id = id
        self.subj = subj
        self.title = title

    def toJson(self):
        return {'crse': self.crse, 'id': self.id, 'subj': self.subj, 'title': self.title}
    


