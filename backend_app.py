import sqlite3
from threading import Lock
from user import User
from chat import Chat
from course import Course
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app, supports_credentials = True)
app.config['CORS_HEADERS'] = 'Content-Type'

# =========================================================
#                          TODO 
# =========================================================  
# ☑ Implement logic to create new User object
# ☑ Implement logic to add new User object
# ☑ Implement logic to create new Course object
# ☑ Implement logic to add new Course object
# ☑ Implement logic to create new Chat object
# ☑ Implement logic to add new Chat object
# ☑ Implement logic to get User object from RIN
# ☐ Implement logic to get User object’s name from RIN
# ☐ Implement logic to get User object’s phone number from RIN
# ☐ Implement logic to send and receive User object’s course list
# ☐ Implement logic to send and receive User object’s chat list
# ☐ Implement logic to send and receive Course object’s name
# ☐ Implement logic to send and receive Course object’s list of chat IDs
# ☐ Implement logic to send and receive Chat object’s ID
# ☐ Implement logic to send and receive Chat object’s list of users




# Connect to database and get control
conn = sqlite3.connect('GCmate.db', check_same_thread=False)
c = conn.cursor()
lock= Lock()

# Create user table if none in database
try:
    c.execute("""CREATE TABLE users (
                rin text,
                phone text
                )""")
except:
    pass

# Create course table if none in database
try:
    c.execute("""CREATE TABLE courses (
                crse text,
                id text,
                subj text,
                title text
                )""")
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
                chatID text,
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



# get user table
def get_Users():
    c.execute("SELECT * FROM Users")
    return c.fetchall()

# get course table
def get_Courses():
    c.execute("SELECT * FROM Courses")
    return c.fetchall()

# get course table
def get_Courses_by_subj(subj):
    c.execute("SELECT * FROM Courses WHERE subj=:subj", {'subj': subj})
    return c.fetchall()

# get course table
def get_Course_subj():
    c.execute("SELECT DISTINCT subj FROM Courses")
    return c.fetchall()

# get chat table
def get_Chats():
    c.execute("SELECT * FROM Chats")
    return c.fetchall()

# get ucoTable table
def get_ucoTable():
    c.execute("SELECT * FROM ucoTable")
    return c.fetchall()

# get uchTable table
def get_uchTable():
    c.execute("SELECT * FROM uchTable")
    return c.fetchall()

# get ccTable table
def get_ccTable():
    c.execute("SELECT * FROM ccTable")
    return c.fetchall()

# check if RIN is taken
def taken_rin(RIN):
    c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': RIN})
    if c.fetchone() is None:
        return False
    else:
        return True


# check if phone number is taken
def taken_phone(phone):
    c.execute("SELECT * FROM users WHERE phone=:phone", {'phone': phone})
    if c.fetchone() is None:
        return False
    else:
        return True

# check if course is already in the database 
# if in db: return true 
# else: return false
def course_in_db(id):
    c.execute("SELECT * FROM courses WHERE id=:id", {'id': id})
    if c.fetchone() is None:
        return False
    else:
        return True


# check if RIN is taken, returns string
def available_rin(RIN):
    c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': RIN})
    if c.fetchone() is None:
        return "true"
    else:
        return "false"

# check if phone number is taken, returns string
def available_phone(phone):
    c.execute("SELECT * FROM users WHERE phone=:phone", {'phone': phone})
    if c.fetchone() is None:
        return "true"
    else:
        return "false"
        
# create a new user object and insert it
def create_and_insert_user(rin, phone):
    new_user = User(rin, phone)
    insert_user(new_user)

# Add user
def insert_user(new_user):
    if taken_rin(new_user.rin):
        print("rin {} is already taken".format(new_user.rin))
        return
    elif taken_phone(new_user.phone):
        print("phone number {} is already taken".format(new_user.phone))
        return
    else:
        with conn:
            c.execute("INSERT INTO users VALUES (:rin, :phone)", {'rin': new_user.rin, 'phone': new_user.phone})
            conn.commit()

# delete user
def delete_user(usr):
    with conn:
        c.execute("DELETE FROM users where rin ={}".format(usr.rin))
        c.execute("DELETE FROM ucoTable where rin ={}".format(usr.rin))
        c.execute("DELETE FROM uchTable where rin ={}".format(usr.rin))
        conn.commit()

# create a new course object and insert it
def create_and_insert_course(crse, course_id, subj, title):
    new_course = Course(crse, course_id, subj, title)
    insert_course(new_course)

# Add course
def insert_course(new_course):
    with conn:
        c.execute("INSERT INTO courses VALUES (:crse, :id, :subj, :title)", {'crse': new_course.crse ,'id': new_course.id, 'subj': new_course.subj, 'title': new_course.title})
        conn.commit()

# delete course
def delete_course(my_course):
    with conn:
        c.execute("DELETE FROM courses where id ={}".format(my_course.id))
        c.execute("DELETE FROM ucoTable where courseID ={}".format(my_course.id))
        c.execute("DELETE FROM uchTable where  courseID ={}".format(my_course.id))
        c.execute("DELETE FROM ccTable where courseID ={}".format(my_course.id))
        conn.commit()

# create a new chat object and insert it
def create_and_insert_chat(course_id, num):
    new_chat = Chat(course_id, num)
    insert_chat(new_chat)

# Add chat
def insert_chat(new_chat):
    with conn:
        c.execute("INSERT INTO chats VALUES (:course, :num, chatID)", {'course': new_chat.course, 'num': new_chat.num, 'chatID': new_chat.chatID()})
        conn.commit()

# delete chat
def delete_chat(my_chat):
    with conn:
        c.execute("DELETE FROM chats where chatID ={}".format(my_chat.chatID))
        c.execute("DELETE FROM uchTable where chatID ={}".format(my_chat.chatID))
        c.execute("DELETE FROM ccTable where chatID={}".format(my_chat.chatID))
        conn.commit()

# Get user by RIN
def get_user_by_rin(RIN):
    c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': RIN})
    return c.fetchone()

# Adds a course to a user's list of registered courses 
def add_user_in_course(rin, courseID):
    # if we don'† have the course --> return false
    if not course_in_db(courseID):
        return "false"
    # if we don'† have the user --> return false
    if not taken_rin(rin):
        return "false"
    # if user-course is already linked in db --> return false (don't want duplicates)
    c.execute("SELECT * FROM ucoTable WHERE courseID=:courseID AND rin=:rin", {'courseID': courseID, 'rin': rin})
    result = c.fetchone()
    if result is not None:
        return "false"
    else: 
        with conn:
            c.execute("INSERT INTO ucoTable VALUES (:courseID, :rin)", {'courseID': courseID, 'rin': rin})
            conn.commit()
        return "true"
    
# Returns all courses registered to a user     
def get_users_courses(userRin):
    lock.acquire(True)
    c.execute("SELECT * FROM ucoTable WHERE rin=:user_rin", {'user_rin': userRin})
    user_courses = c.fetchall()    
    course_list = []
    for course in user_courses: 
        c.execute("SELECT * FROM courses WHERE id=:id", {'id': course[0]})
        course_data = c.fetchone()
        course_list.append(course_data)  
    lock.release()    
    return course_list

# load courses into database
def load_courses(json_file):
    f = open(json_file)
    values = json.load(f)
    with conn:
        for data in values:
            for x, i in enumerate(data['courses']):
                if course_in_db(i['id']):
                    continue
                c.execute("INSERT INTO courses VALUES (:crse, :id, :subj, :title)", {'crse':i['crse'] , 'id': i['id'], 'subj': i['subj'], 'title': i['title']})
        conn.commit()


def subjects_to_json():
    subjs = get_Course_subj()
    subject_dict = {}
    subject_list = []
    for i in subjs:
        subject_list.append(i[0])
    subject_dict['SUBJECTS'] = subject_list 
    return subject_dict

def course_by_sub_to_json(subj):
    course_vals = get_Courses_by_subj(subj)
    course_dict = {}
    course_list = []
    for i in course_vals:
        curr_course = Course(i[0], i[1], i[2], i[3])
        course_list.append(curr_course.toJson())
        # print(curr_course.toJson())
    course_dict['COURSES'] = course_list 
    return course_list

# ====== Run at Start ======
load_courses('courses.json')

usr1 = User("661889750", "8587400565")
# === Brian's Testing Code ===
usr2 = User("661878609", "16465915259")
if (taken_rin(661878609)): delete_user(usr2)
# ============================
print("\n== Test User Inserted ==")
insert_user(usr1)
print("\n== Test: Get All Users ==")
print(get_Users())
#print("\n== Test: Add a Course to Existing User ==")
#print(add_user_in_course("661889750", "ADMN-1030"))
#print("\n== Test: Add second Course to Existing User ==")
#print(add_user_in_course("661889750", "ADMN-1111"))
print("\n== Test: Get Existing User's Course ==")
print(get_users_courses(usr1.rin))

# === Course Removal Test === 
usrRC = User("661231234", "15555555555")
#delete_user(usrRC)
insert_user(usrRC)
print("\n== New User Inserted ==")
print(get_Users())
print(get_users_courses(usrRC.rin))
#print(add_user_in_course("661231234", "ADMN-1030"))
# ===========================

# Sending data from front -> back
@app.route('/api/rin', methods=['POST'])
def valid_rin():
    data = request.get_json() 
    print("{}, {}".format(data['RIN'], available_rin(data['RIN'])))
    return {"valid": available_rin(data['RIN'])}

# Storing RIN and Phone number in database as a new user  
@app.route('/api/phoneRIN', methods=['POST'])
def create_new_user():
    data = request.get_json() 
    print("{}, {}".format(data['RIN'], data['PHONE']))
    create_and_insert_user(data['RIN'], data['PHONE'])
    return {"valid": available_phone(data['PHONE'])}

# get list of course subjects
@app.route('/api/subj', methods=['GET'])
def get_subjects():
   return jsonify(subjects_to_json())

# get list of course from subject
@app.route('/api/coursebysubj', methods=['POST'])
def get_cour_by_subject():
   data = request.get_json()  
   return jsonify(course_by_sub_to_json(data['SUBJECT']))

# Update a user's course list with one course 
@app.route('/api/ucupdate', methods=['POST'])
@app.errorhandler(500)
def update_user_course():
   data = request.get_json()  
   result = add_user_in_course(data['RIN'],data['COURSEID'])
   # Duplicate course chosen 
   if (result == "false"): 
    return 500
   else: 
    user_courses = get_users_courses(data['RIN'])

    return {"courses": user_courses}

# Returns a user's registered courses 
@app.route('/api/userCourses', methods=['POST'])
def send_user_courses(): 
    data = request.get_json() 
    user_courses = get_users_courses(data['RIN'])
    
    return {"courses": user_courses}
    
if __name__ == "__main__": 
    app.run(debug=True)