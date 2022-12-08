import json
from user import User
from course import Course
from chat import Chat
from dbCommunicator import DbCommunicator

class FeCommunicator:
    def __init__(self, database):
        self.database = database
        self.dbComm = DbCommunicator(self.database, 'courses.json')
        self.courses = []
        self.users = []
        self.chats = []

    def new_user(self, rin, phone):
        """Create and add a new user to database"""
        add_user = True
        for usr in self.users:
            if (usr.get_rin() == rin) or (usr.get_phone() == phone):
                add_user = False
                break
        if add_user:
            self.users.append(User(rin, phone, [], []))
            self.dbComm.add_user(rin, phone)
        return add_user

    def available_rin(self, rin):
        """Check if a RIN is available (not in database)"""
        for usr in self.users:
            if usr.get_rin() == rin:
                return False
        return True

    def get_subjects(self):
        """Get all subjects"""
        return self.dbComm.get_subjects()

    def get_courses_by_subject(self, subject):
        """Get list of courses for a specific subject"""
        cbs = []
        cbs_dict = {}
        for c in self.courses:
            if c.get_subj() == subject:
                cbs.append(c.to_json())
        cbs_dict['COURSES'] = cbs
        return cbs

    def get_user(self, rin):
        """Return user object given a RIN"""
        for usr in self.users:
            if usr.get_rin() == rin:
                return usr
        return None

    def get_chat(self, course_id):
        """Return chat object given a course id"""
        for chat in self.chats:
            if chat.get_course_id() == course_id:
                return chat
        return None

    def set_user(self, usr):
        """Set user object in list"""
        for i in range(len(self.users)):
            if self.users[i].rin == usr.get_rin():
                self.users[i] = usr
                break

    def set_chat(self, chat):
        """Set chat object in list"""
        for i in range(len(self.chats)):
            if self.chats[i].course_id == chat.get_course_id():
                self.chats[i] = chat
                break

    def have_course(self, course_id):
        """Check whether a course id exists in the database"""
        for c in self.courses:
            if c.get_id() == course_id:
                return True
        return False

    def update_user_course(self, rin, course_id):
        """Update user's course list with a course"""
        usr = self.get_user(rin)
        if usr == None:
            return False
        if not self.have_course(course_id):
            return False
        if usr.add_course(course_id):
            self.set_user(usr)
            self.dbComm.update_user_course(rin, course_id)
            return True
        return False

    def update_user_chat(self, rin, course_id):
        """Add user to a group chat"""
        chat = self.get_chat(course_id)
        usr = self.get_user(rin)
        if usr == None:
            return False
        if chat == None:
            return False
        if not self.have_course(course_id):
            return False
        if chat.add_member(rin):
            self.set_chat(chat)
            self.dbComm.update_user_chat(rin, course_id)
            return True
        return False

    def remove_user_chat(self, rin, course_id):
        """Remove user from a group chat"""
        chat = self.get_chat(course_id)
        usr = self.get_user(rin)
        chat.remove_member(usr.get_rin())
        self.dbComm.remove_user_chat(rin, course_id)
        return True

    def remove_user_course(self, rin, course_id):
        """Remove user from a course"""
        usr = self.get_user(rin)
        # if we don't have that user --> return false
        if usr == None:
            return False
        # if we don't have that course --> return false
        if not self.have_course(course_id):
            return False
        # if the user object validates the removal --> update the database
        if usr.remove_course(course_id):
            chat = self.get_chat(course_id)
            chat.remove_member(usr.get_rin())
            self.set_chat(chat)
            self.set_user(usr)
            self.dbComm.remove_user_course(rin, course_id)
            self.dbComm.remove_user_chat(rin, course_id)
            return True
        return False

    def get_user_courses(self, rin):
        """Get courses that a user is in"""
        usr = self.get_user(rin)
        if usr == None:
            return []
        usr_courses = usr.get_courses()
        course_list = []
        for c in usr_courses:
            for cour in self.courses:
                if c == cour.get_id():
                    course_list.append(cour.to_usr())
                    break
        return course_list

    def get_chat_members(self, course_id):
        """Get members of a group chat"""
        ch = self.get_chat(course_id)
        if ch == None:
            return False
        chatMem = ch.get_members()
        return chatMem

    def remove_user(self, rin):
        """Delete a user"""
        usr = self.get_user(rin)
        if usr == None:
            return False
        usr_courses = usr.get_courses()
        for c in usr_courses:
            # print(c)
            self.remove_user_course(rin, c)
        for ch in self.chats:
            ch.remove_member(usr.get_rin())
        self.users.remove(usr)
        self.dbComm.remove_user(rin)
        return True

    def populate(self):
        """Creates user and class objects from the database when the 
           app is booted up"""
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

    def get_all_uco(self):
        """Get all user-course relations"""
        return self.dbComm.get_all_uco()

    def get_all_uch(self):
        """Get all user-chat relations"""
        return self.dbComm.get_all_uch()
