from dbCommunicator import DbCommunicator
from user import User
from course import Course
from feCommunicator import FeCommunicator


# my_comm = DbCommunicator("tester.db", 'courses.json')

my_fe = FeCommunicator("GCMate.db")
my_fe.populate()

# Add new user 
# print("Add user tests (Assuming Fresh DB)")
# print("==============")
# print("Add user rin: {}, phone: {}, expected: {}, actual: {}".format(661889750,8587400565, True,  my_fe.new_user("661889750", "8587400565")))
# print("Add user rin: {}, phone: {}, expected: {}, actual: {}".format(661889740,8587400565, False,  my_fe.new_user("661889740", "8587400565")))
# print("Add user rin: {}, phone: {}, expected: {}, actual: {}".format(661878609, 16465915259, True,  my_fe.new_user("661878609", "16465915259")))


my_fe.new_user("661889750", "8587400565")
my_fe.new_user("661878609", "16465915259")
print(my_fe.get_all_uco())
# my_fe.new_user("661889750", "8587400565")
# my_fe.new_user("661889750", "8587400565")
# print(len(my_fe.users))
print("\nUser rins:")
print("---------")
for i in my_fe.users:
    print("rin: {}".format(i.rin))
print(my_fe.get_subjects())
print(my_fe.get_courses_by_subject("ISCI"))

print("\nAdding courses:")
print(my_fe.update_user_course("661889750", "ADMN-4400"))
print(my_fe.update_user_course("661889750", "ISCI-6510"))
print(my_fe.update_user_course("661889750", "ISCI-1600"))
# print(my_fe.remove_user("661889750"))


print("\nAdding chats:")
print(my_fe.update_user_chat("661889750", "ADMN-4400"))
print(my_fe.update_user_chat("661889750", "ISCI-6510"))
print(my_fe.update_user_chat("661889750", "ISCI-1600"))
print(my_fe.update_user_chat("661889750", "ISCI-1600"))
print(my_fe.update_user_chat("661889751", "ISCI-1600"))

# for c in my_fe.chats:
    # if c.getCourseID() == "ISCI-1600":
    # print(c.getMembers())

print("\nChat Members")
print("------------")
print(my_fe.get_chat_members('ISCI-4510'))
print("\n")

print(my_fe.get_all_uch())

print("\n\ncourseID for courses taken by rin: {}".format("661889750"))
print("---------")
for i in my_fe.get_user_courses("661889750"):
    print(i)

# print(my_fe.remove_user("661889750"))
# print("\nUsers:")
# print("---------")
# for i in my_fe.users:
#     print("rin: {}, courses: {}".format(i.rin, i.courses))

# print(my_fe.remove_user_course("661889750", "ADMN-4400"))
print(my_fe.remove_user_course("661889750", 'ISCI-6510'))
print(my_fe.test_cour("661889750"))
print(my_fe.get_all_uco())

# print(my_fe.remove_user("661889750"))
# print(my_fe.get_all_uco())

# test_usr = User("661889750", "8587400565", [], [])
# print(test_usr.add_course("blah"))
# print(test_usr.add_course("blah"))
# print(test_usr.get_courses())

# print(my_fe.remove_user_course("661889750", "ADMN-4400"))
# print(my_fe.update_user_course("661889750", "ISCI-6510"))
# print(my_fe.get_user_courses("661889750"))

# print(my_fe.remove_user_course("661889750", "ADMN-4400"))
# print(my_fe.get_user_courses("661889750"))
# print(my_fe.courses)
# my_comm.add_user("661889750", "8587400565")
# my_comm.add_rin("661889740", "8587400575")

# vals = my_comm.get_rins()
# print(vals)
# print(type(vals))

# print(my_comm.get_user("111111111"))
# cour = my_comm.get_courses()
# for i in cour:
#     print(i.get_id())



# my_comm.add_user_in_course("661889750", "ADMN-4400")
# my_usr = my_comm.get_user("661889750")
# print(my_usr.get_courses())