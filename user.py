# User Class
class User:

    def __init__(self, first, last, rin, phone):
        self.first = first
        self.last = last
        self.rin = rin
        self.phone = phone
        
    
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

   