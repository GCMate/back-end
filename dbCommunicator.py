import sqlite3
import json
from user import User
from course import Course
from chat import Chat

class DbCommunicator:
    def __init__(self, database, json_file):
        self.database = database
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE users (
                        rin text,
                        phone text
                        )""")
        except:
            pass

        # Create course table if none in database
        try:
            # print("course")
            c.execute("""CREATE TABLE courses (
                        crse text,
                        id text,
                        subj text,
                        title text
                        )""")
            # print("after course")
        except:
            pass

        # Create chat table if none in database
        try:
            c.execute("""CREATE TABLE chats (
                        course text, 
                        numb text,
                        chatID text
                        )""")
        except:
            pass

        # Create user-course table if none in database
        try:
            c.execute("""CREATE TABLE ucoTable (
                        courseID text, 
                        rin text
                        )""")
        except:
            pass

        # Create user-chat table if none in database
        try:
            c.execute("""CREATE TABLE uchTable (
                        courseID text,  
                        rin text
                        )""")
        except:
            pass                

        # Create course-chat table if none in database
        try:
            c.execute("""CREATE TABLE cctTable (
                        courseID text, 
                        chatID text
                        )""")
        except:
            pass
        f = open(json_file)
        values = json.load(f)
        with conn:
            for data in values:
                for x, i in enumerate(data['courses']):
                    # print("here")
                    c.execute("SELECT * FROM courses WHERE id=:id", {'id': i['id']})
                    # print(i['id'])
                    retval = c.fetchall()
                    # print(retval)
                    if retval == []:
                        # continue

                        c.execute("INSERT INTO courses VALUES (:crse, :id, :subj, :title)", {'crse':i['crse'] , 'id': i['id'], 'subj': i['subj'], 'title': i['title']})
            conn.commit()
        conn.close()

    def add_user(self, rin, phone):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (:rin, :phone)", {'rin': rin, 'phone': phone})
        conn.commit()
        conn.close()

    # check if course is already in the database 
    # if in db: return true 
    # else: return false
    def course_in_db(self, id):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        retval = c.execute("SELECT * FROM courses WHERE id=:id", {'id': id})
        conn.close()
        if retval is None:
            return False
        else:
            return True

    def get_subjects(self):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT DISTINCT subj FROM courses")
        subjs = c.fetchall()
        conn.close()
        subject_dict = {}
        subject_list = []
        for i in subjs:
            subject_list.append(i[0])
        subject_dict['SUBJECTS'] = subject_list 
        return subject_dict

    # check if RIN is taken
    def taken_rin(self, rin):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': rin})
        retval = c.fetchone()
        conn.close()
        if retval is None:
            return False
        else:
            return True

    # get all rins
    def get_rins(self):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT rin FROM users")
        ret_lst = [] 
        for val in c.fetchall():
            ret_lst.append(val[0])
        conn.close()
        return ret_lst

    # Adds a course to a user's list of registered courses 
    # def add_user_in_course(self,rin, courseID):
    #     # if we don'† have the course --> return false
    #     # if not self.course_in_db(courseID):
    #     #     return "false"
    #     # # if we don'† have the user --> return false
    #     # if not self.taken_rin(rin):
    #     #     return "false"
        
    #     # if user-course is already linked in db --> return false (don't want duplicates)
    #     # c.execute("SELECT * FROM ucoTable WHERE courseID=:courseID AND rin=:rin", {'courseID': courseID, 'rin': rin})
    #     # result = c.fetchone()

    #     # if result is None:
    #     conn = sqlite3.connect(self.database, check_same_thread=False)
    #     c = conn.cursor()
    #     with conn:
    #         c.execute("INSERT INTO ucoTable VALUES (:courseID, :rin)", {'courseID': courseID, 'rin': rin})
    #         conn.commit()
    #     conn.close()
    #     return "true"    
    #     # else: 
    #     #     conn.close()
    #     #     return "false" 

    # return user object 
    def get_user(self, rin):
        if not self.taken_rin(rin):
            return None
        else:
            # get student's courses
            courses = []
            chats = []
            conn = sqlite3.connect(self.database, check_same_thread=False)
            c = conn.cursor()
            c.execute("SELECT * FROM ucoTable WHERE rin=:rin", {'rin': rin})
            r_courses = c.fetchall()
            if r_courses is not None:
                for i in r_courses:
                    courses.append(i[0])
            c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': rin})
            phone = c.fetchone()[1]
            conn.close()
            return User(rin, phone, courses, chats)


    def get_chat(self, courseID):
        if not self.course_in_db(courseID):
            return None
        
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT title FROM courses WHERE id=:id", {'id': courseID})
        name = c.fetchone()
        c.execute("SELECT rin FROM uchTable WHERE courseID=:courseID", {'courseID': courseID})
        rins = c.fetchall()
        conn.close()
        my_chat = Chat(courseID, name)
        if rins is not None:
            for r in rins:
                my_chat.addMember(r[0])
        return my_chat
        


    # get list of course objects
    def get_courses(self):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM courses")
        c_vals = c.fetchall()
        c_objs = []
        # print(len(c_vals))
        for i in c_vals:
            c_objs.append(Course(i[0], i[1], i[2], i[3]))
        conn.close()
        return c_objs

    # add course to user's list
    def update_user_course(self, rin, courseID):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        with conn:
            # c.execute("SELECT * FROM ucoTable WHERE courseID=:courseID AND rin=:rin", {'courseID': courseID, 'rin': rin})
            # classes = c.fetchall()
            # if classes is None:
            c.execute("INSERT INTO ucoTable VALUES (:courseID, :rin)", {'courseID': courseID, 'rin': rin})
            conn.commit()
        conn.close()

    def update_user_chat(self, rin, courseID):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        with conn:
            # c.execute("SELECT * FROM uchTable WHERE courseID=:courseID AND rin=:rin", {'courseID': courseID, 'rin': rin})
            # chats = c.fetchall()
            # if chats == None:
            c.execute("INSERT INTO uchTable VALUES (:courseID, :rin)", {'courseID': courseID, 'rin': rin})
            conn.commit()
        conn.close()


    # remove user from course
    def remove_user_course(self, rin, courseID):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        with conn:
            c.execute("DELETE FROM ucoTable WHERE courseID=:courseID AND rin=:rin", {'courseID': courseID, 'rin': rin})
            conn.commit()
        conn.close()

    def remove_user_chat(self, rin, courseID):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        with conn:
            c.execute("DELETE FROM uchTable WHERE courseID=:courseID AND rin=:rin", {'courseID': courseID, 'rin': rin})
            conn.commit()
        conn.close()
    
    # delete user
    def remove_user(self, rin):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        with conn:
            c.execute("DELETE FROM users where rin ={}".format(rin))
            c.execute("DELETE FROM ucoTable where rin ={}".format(rin))
            c.execute("DELETE FROM uchTable where rin ={}".format(rin))
            conn.commit()
        conn.close()

    # get all user-course relations (for debugging purposes)
    def get_all_uco(self):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM ucoTable")
        ret_lst = [] 
        for val in list(c.fetchall()):
            ret_lst.append(val)
        conn.close()
        return ret_lst

    def get_all_uch(self):
        conn = sqlite3.connect(self.database, check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM uchTable")
        ret_lst = [] 
        for val in list(c.fetchall()):
            ret_lst.append(val)
        conn.close()
        return ret_lst
            
            

        