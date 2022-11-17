# from dbCommunicator import DbCommunicator
from user_v2 import User
from course_v2 import Course
from chat import Chat
from feCommunicator import FeCommunicator

from threading import Lock
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import json


app = Flask(__name__)
CORS(app, supports_credentials = True)
app.config['CORS_HEADERS'] = 'Content-Type'

my_fe = FeCommunicator("GCmate.db")
my_fe.populate()


# Sending data from front -> back
@app.route('/api/rin', methods=['POST'])
def valid_rin():
    data = request.get_json() 
    # print("{}, {}".format(data['RIN'], available_rin(data['RIN'])))
    if my_fe.available_rin(data['RIN']):
        return {"valid": "true"}
    else: return {"valid": "false"}

# Storing RIN and Phone number in database as a new user  
@app.route('/api/phoneRIN', methods=['POST'])
def create_new_user():
    data = request.get_json() 
    # print("{}, {}".format(data['RIN'], data['PHONE']))
    return my_fe.new_user(data['RIN'], data['PHONE'])
    # return {"valid": available_phone(data['PHONE'])}

# get list of course subjects
@app.route('/api/subj', methods=['GET'])
def get_subjects():
   return jsonify(my_fe.get_subjects())

# get list of course from subject
@app.route('/api/coursebysubj', methods=['POST'])
def get_cour_by_subject():
   data = request.get_json()  
   return jsonify(my_fe.get_courses_by_subject(data['SUBJECT']))

# Update a user's course list with one course 
@app.route('/api/ucupdate', methods=['POST'])
@app.errorhandler(500)
def update_user_course():
    data = request.get_json()  
    bool_val = my_fe.update_user_course(data['RIN'],data['COURSEID'])
    # Duplicate course chosen 
    if not bool_val: 
        return 500
    else: 
        user_courses = my_fe.get_user_courses(data['RIN'])

        return {"courses": user_courses}

# remove user from course
@app.route('/api/ucremove', methods=['POST'])
def rem_user_course():
    data = request.get_json()  
    result = my_fe.remove_user_course(data['RIN'],data['COURSEID'])
    user_courses = my_fe.get_user_courses(data['RIN'])

    return {"courses": user_courses}

# Returns a user's registered courses 
@app.route('/api/userCourses', methods=['POST'])
def send_user_courses(): 
    data = request.get_json() 
    user_courses = my_fe.get_user_courses(data['RIN'])
    
    return {"courses": user_courses}
    
if __name__ == "__main__": 
    app.run(debug=True)