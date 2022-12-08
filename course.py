# Course Class
class Course:

    def __init__(self, crse, ID, subj, title):
        self.crse = crse
        self.id = ID
        self.subj = subj
        self.title = title

    def to_json(self):
        """Returns course's data in a json format"""
        return {'crse': self.crse, 'id': self.id, 'subj': self.subj, 'title': self.title}

    def to_usr(self):
        """Returns course data"""
        return (self.crse, self.id, self.subj, self.title)

    def get_crse(self):
        """Returns course number"""
        return self.crse

    def get_id(self):
        """Returns course id"""
        return self.id

    def get_subj(self):
        """Returns course's subject"""
        return self.subj

    def get_title(self):
        """Returns course's title"""
        return self.title
