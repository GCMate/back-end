# Course Class
class Course:

    def __init__(self, crse, ID, subj, title):
        self.crse = crse
        self.id = ID
        self.subj = subj
        self.title = title

    def toJson(self):
        return {'crse': self.crse, 'id': self.id, 'subj': self.subj, 'title': self.title}

    def toUsr(self):
        return (self.crse, self.id, self.subj, self.title)

    def get_crse(self):
        return self.crse

    def get_id(self):
        return self.id

    def get_subj(self):
        return self.subj
    
    def get_title(self):
        return self.title
    


    
    