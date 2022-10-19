import sqlite3
from user import User
from chat import Chat
from course import Course

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
conn = sqlite3.connect('GCmate.db')
c = conn.cursor()


# Create user table if none in database
try:
    c.execute("""CREATE TABLE users (
                first text,
                last text,
                rin integer,
                phone integer
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
                numb int,
                chatID text
                )""")
except:
    pass

# Create user-course table if none in database
try:
    c.execute("""CREATE TABLE ucoTable (
                courseID text, 
                rin int
                )""")
except:
    pass

# Create user-chat table if none in database
try:
    c.execute("""CREATE TABLE uchTable (
                chatID text, 
                rin int
                )""")
except:
    pass                

# Create course-chat table if none in database
try:
    c.execute("""CREATE TABLE cctable (
                courseID text, 
                chatID int
                )""")
except:
    pass

# print user table
def get_Users():
    c.execute("SELECT * FROM Users")
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


# create a new user object and insert it
def create_and_insert_user(first, last, rin, phone):
    new_user = User(first, last, rin, phone)
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
        c.execute("INSERT INTO users VALUES (:first, :last, :rin, :phone)", {'first': new_user.first, 'last': new_user.last, 'rin': new_user.rin, 'phone': new_user.phone})

# create a new course object and insert it
def create_and_insert_course(course_id):
    new_course = Course(course_id)
    insert_course(new_course)

# Add course
def insert_course(new_course):
    with conn:
        c.execute("INSERT INTO courses VALUES (:id)", {'id': new_course.id})

# create a new chat object and insert it
def create_and_insert_chat(course_id, num):
    new_chat = Chat(course_id, num)
    insert_chat(new_chat)

# Add chat
def insert_chat(new_chat):
    with conn:
        c.execute("INSERT INTO chats VALUES (:course, :num, chatID)", {'course': new_chat.course, 'num': new_chat.num, 'chatID': new_chat.chatID()})

# Get user by RIN
def get_user_by_rin(RIN):
    c.execute("SELECT * FROM users WHERE rin=:rin", {'rin': RIN})
    return c.fetchone()




usr1 = User('Will', 'Bacon', 661889750, 8587400565)
usr2 = User('Someone', 'Else', 661889999, 4208675309)
usr3 = User('Third', 'Person', 661889999, 4208675309)

insert_user(usr1)
get_Users()
insert_user(usr2)
get_Users()
insert_user(usr3)
get_Users()

usrbyrin = get_user_by_rin(661889750)
print(type(usrbyrin))

