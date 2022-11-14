import json
from user_v2 import User
from course_v2 import Course
from dbCommunicator import DbCommunicator


class FeCommunicator:
    def __init__(self, database):
        self.database = database
        self.dbComm= DbCommunicator(self.database, 'courses.json')
        self.courses = []
        self.users = []
        self.chats = []
        
    def database(self):
        return self.database

    # create new_user
    def new_user(self, rin, phone):
        add_user = True
        for usr in self.users:
            if (usr.get_rin() == rin) or (usr.get_phone() == phone):
                add_user = False
                break
        if add_user:
            self.users.append(User(rin,phone, [],[]))
            self.dbComm.add_user(rin, phone)
        return add_user



    def available_rin(self, rin):
        for usr in self.users:
            if (usr.get_rin() == rin):
                return False
        return True

    def get_subjects(self):
        return self.dbComm.get_subjects()

    def get_courses_by_subject(self, subject):
        cbs = []
        cbs_dict = {}
        for c in self.courses:
            if (c.get_subj() == subject):
                cbs.append(c.toJson())
        cbs_dict['COURSES'] = cbs
        return cbs_dict

    def get_user(self, rin):
        for usr in self.users:
            if usr.get_rin() == rin:
                return usr
        return None

    def set_user(self, usr):
        for i in range(len(self.users)):
            if self.users[i].rin == usr.get_rin():
                self.users[i] = usr
                break

    def have_course(self, courseID):
        for c in self.courses:
            if c.get_id() == courseID:
                return True
        return False

    def update_user_course(self, rin, courseID):
        usr = self.get_user(rin)
        if usr == None:
            return False
        if not self.have_course(courseID):
            return False
        if usr.add_course(courseID):
            self.set_user(usr)
            self.dbComm.update_user_course(rin, courseID)
            return True
        return False   

    # remove user from a course
    def remove_user_course(self, rin, courseID):
        usr = self.get_user(rin)
        # if we don't have that user --> return false
        if usr == None:
            return False
        # if we don't have that course --> return false
        if not self.have_course(courseID):
            return False
        # if the user object validates the removal --> update the database
        if usr.remove_course(courseID):
            self.set_user(usr)
            self.dbComm.remove_user_course(rin, courseID)
            return True
        return False


    def get_user_courses(self, rin):
        usr = self.get_user(rin)
        if usr == None:
            return False
        usr_courses = usr.get_courses()
        course_list = []
        for c in usr_courses:
            for cour in self.courses:
                if c == cour.get_id():
                    course_list.append(cour.toJson())
                    break
        return course_list

    def remove_user(self, rin):
        usr = self.get_user(rin)
        if usr == None:
            return False
        usr_courses = usr.get_courses()
        for c in usr_courses:
            # print(c)
            self.remove_user_course(rin, c)
        self.users.remove(usr)
        self.dbComm.remove_user(rin)
        return True
        
        

    def populate(self):
        rl = self.dbComm.get_rins()
        ul = []
        self.courses = self.dbComm.get_courses()
        for i in rl:
            ul.append(self.dbComm.get_user(i))
        self.users = ul

    def get_all_uco(self):
        return self.dbComm.get_all_uco()

    
    def test_cour(self, rin):
        usr = self.get_user(rin)
        if usr == None:
            return False
        usr_courses = usr.get_courses()
        u_l = []
        for c in usr_courses:
            # print(c)
            u_l.append(c)
            # self.remove_user_course(rin, c)
        # self.users.remove(usr)
        # self.dbComm.remove_user(rin)
        return u_l
            


    
        
        

                
            
