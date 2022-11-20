import json
from user import User
from course import Course
from chat import Chat
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


    # check if rin is available
    def available_rin(self, rin):
        for usr in self.users:
            if (usr.get_rin() == rin):
                return False
        return True

    # get all subjects
    def get_subjects(self):
        return self.dbComm.get_subjects()

    # get list of courses for a specific subject
    def get_courses_by_subject(self, subject):
        cbs = []
        cbs_dict = {}
        for c in self.courses:
            if (c.get_subj() == subject):
                cbs.append(c.toJson())
        cbs_dict['COURSES'] = cbs
        return cbs

    # return user object
    def get_user(self, rin):
        for usr in self.users:
            if usr.get_rin() == rin:
                return usr
        return None

    def get_chat(self, courseID):
        for chat in self.chats:
            if chat.getCourseID() == courseID:
                return chat
        return None

    # set user object in list
    def set_user(self, usr):
        for i in range(len(self.users)):
            if self.users[i].rin == usr.get_rin():
                self.users[i] = usr
                break

    def set_chat(self, chat):
        for i in range(len(self.chats)):
            if self.chats[i].courseID == chat.getCourseID():
                self.chats[i] = chat
                break

    # check whether we have a course or not
    def have_course(self, courseID):
        for c in self.courses:
            if c.get_id() == courseID:
                return True
        return False

    # update user's course list with a course
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

    # add user to chat
    def update_user_chat(self, rin, courseID):
        chat = self.get_chat(courseID)
        usr = self.get_user(rin)
        if usr == None:
            return False
        if chat == None:
            return False
        if not self.have_course(courseID):
            return False
        if chat.addMember(rin):
            self.set_chat(chat)
            self.dbComm.update_user_chat(rin, courseID)
            return True
        return False   

    # Remove user from a chat 
    def remove_user_chat(self, rin, courseID): 
        chat = self.get_chat(courseID)
        usr = self.get_user(rin)
        chat.removeMember(usr.get_rin())
        self.dbComm.remove_user_chat(rin, courseID)
        return True     

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
            chat = self.get_chat(courseID)
            chat.removeMember(usr.get_rin())
            self.set_chat(chat)
            self.set_user(usr)
            self.dbComm.remove_user_course(rin, courseID)
            self.dbComm.remove_user_chat(rin, courseID)
            return True
        return False

    # get courses that a user is in
    def get_user_courses(self, rin):
        usr = self.get_user(rin)
        if usr == None:
            return []
        usr_courses = usr.get_courses()
        course_list = []
        for c in usr_courses:
            for cour in self.courses:
                if c == cour.get_id():
                    course_list.append(cour.toUsr())
                    break
        return course_list

    # get members of a chat
    def get_chat_members(self, courseID):
        ch = self.get_chat(courseID)
        if ch == None:
            return False
        chatMem = ch.getMembers()
        return chatMem

    # delete user
    def remove_user(self, rin):
        usr = self.get_user(rin)
        if usr == None:
            return False
        usr_courses = usr.get_courses()
        for c in usr_courses:
            # print(c)
            self.remove_user_course(rin, c)
        for ch in self.chats:
            ch.removeMember(usr.get_rin())
        self.users.remove(usr)
        self.dbComm.remove_user(rin)
        return True
        
        
    # function that creates user and class objects from the db when app is booted up
    def populate(self):
        rl = self.dbComm.get_rins()
        ul = []
        cl = []
        self.courses = self.dbComm.get_courses()
        for i in rl:
            ul.append(self.dbComm.get_user(i))
        for j in self.courses:
            cl.append(self.dbComm.get_chat(j.get_id()))
        
        self.users = ul
        self.chats = cl

    # get all user-course relations
    def get_all_uco(self):
        return self.dbComm.get_all_uco()

    def get_all_uch(self):
        return self.dbComm.get_all_uch()



    # ignore this... should delete
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
            


    
        
        

                
            
