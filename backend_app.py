import sqlite3
from user import User
from chat import Chat
from course import Course
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin

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
                id text
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

# print user table
def get_Users():
    c.execute("SELECT * FROM Users")
    print(c.fetchall())

# print course table
def get_Courses():
    c.execute("SELECT * FROM Courses")
    print(c.fetchall())

# print chat table
def get_Chats():
    c.execute("SELECT * FROM Chats")
    print(c.fetchall())

# print ucoTable table
def get_ucoTable():
    c.execute("SELECT * FROM ucoTable")
    print(c.fetchall())

# print uchTable table
def get_uchTable():
    c.execute("SELECT * FROM uchTable")
    print(c.fetchall())

# print ccTable table
def get_ccTable():
    c.execute("SELECT * FROM ccTable")
    print(c.fetchall())

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

# check if RIN is taken, returns string
def available_rin(RIN):
    c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': RIN})
    if c.fetchone() is None:
        return {"valid": "true"}
    else:
        return {"valid": "false"}

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
    if taken_phone(new_user.phone):
        print("phone number {} is already taken".format(new_user.phone))
        return
    with conn:
        c.execute("INSERT INTO users VALUES (:rin, :phone)", {'rin': new_user.rin, 'phone': new_user.phone})

# delete user
def delete_user(usr):
    with conn:
        c.execute("DELETE FROM users where rin ={}".format(usr.rin))
        c.execute("DELETE FROM ucoTable where rin ={}".format(usr.rin))
        c.execute("DELETE FROM uchTable where rin ={}".format(usr.rin))

# create a new course object and insert it
def create_and_insert_course(course_id):
    new_course = Course(course_id)
    insert_course(new_course)

# Add course
def insert_course(new_course):
    with conn:
        c.execute("INSERT INTO courses VALUES (:id)", {'id': new_course.id})

# delete course
def delete_course(my_course):
    with conn:
        c.execute("DELETE FROM courses where id ={}".format(my_course.id))
        c.execute("DELETE FROM ucoTable where courseID ={}".format(my_course.id))
        c.execute("DELETE FROM uchTable where  courseID ={}".format(my_course.id))
        c.execute("DELETE FROM ccTable where courseID ={}".format(my_course.id))

# create a new chat object and insert it
def create_and_insert_chat(course_id, num):
    new_chat = Chat(course_id, num)
    insert_chat(new_chat)

# Add chat
def insert_chat(new_chat):
    with conn:
        c.execute("INSERT INTO chats VALUES (:course, :num, chatID)", {'course': new_chat.course, 'num': new_chat.num, 'chatID': new_chat.chatID()})

# delete chat
def delete_chat(my_chat):
    with conn:
        c.execute("DELETE FROM chats where chatID ={}".format(my_chat.chatID))
        c.execute("DELETE FROM uchTable where chatID ={}".format(my_chat.chatID))
        c.execute("DELETE FROM ccTable where chatID={}".format(my_chat.chatID))

# Get user by RIN
def get_user_by_rin(RIN):
    c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': RIN})
    return c.fetchone()




usr1 = User("661889750", "8587400565")
usr2 = User("661889999", "4208675309")
usr3 = User("661889999", "4208675309")

insert_user(usr1)
get_Users()
insert_user(usr2)
get_Users()
insert_user(usr3)
get_Users()
delete_user(usr2)
get_Users()

usrbyrin = get_user_by_rin("661889750")


create_and_insert_course("math101")
get_Courses()
print(type(usrbyrin))

# Sending data from front -> back
@app.route('/api/rin', methods=['POST'])
def valid_rin():
    data = request.get_json() 
    print("{}, {}".format(data['RIN'], available_rin(data['RIN'])))
    return {"valid": available_rin(data['RIN'])}

if __name__ == "__main__": 
    app.run(debug=True)