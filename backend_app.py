"""Import Flask, Flask CORS, and FeCommunicator"""
from threading import Lock
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from feCommunicator import FeCommunicator

# Facade design pattern:
# All communication from the front-end passes through the feCommunicator
# which then gets passed to the appropriate object

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

MY_FE = FeCommunicator("GCmate.db")
MY_FE.populate()

@app.route('/api/rin', methods=['POST'])
def valid_rin():
    """Checks whether the RIN is already in the database or not"""
    data = request.get_json()
    if MY_FE.available_rin(data['RIN']):
        return {"valid": "true"}
    return {"valid": "false"}

@app.route('/api/phoneRIN', methods=['POST'])
def create_new_user():
    """Stores RIN and Phone number in database as a new user"""
    data = request.get_json()
    MY_FE.new_user(data['RIN'], data['PHONE'])
    return {"valid": "true"}

@app.route('/api/subj', methods=['GET'])
def get_subjects():
    """Get list of course subjects"""
    return jsonify(MY_FE.get_subjects())

@app.route('/api/coursebysubj', methods=['POST'])
def get_cour_by_subject():
    """Get list of courses from a subject"""
    data = request.get_json()
    return jsonify(MY_FE.get_courses_by_subject(data['SUBJECT']))

@app.route('/api/ucupdate', methods=['POST'])
@app.errorhandler(500)
def update_user_course():
    """Update a user's course list with one course"""
    data = request.get_json()
    bool_val = MY_FE.update_user_course(data['RIN'], data['COURSEID'])
    # Duplicate course chosen
    if not bool_val:
        return 500
    user_courses = MY_FE.get_user_courses(data['RIN'])
    return {"courses": user_courses}

@app.route('/api/chatMembersList', methods=['POST'])
def get_chat_members():
    """Returns the members of a group chat"""
    data = request.get_json()
    members = MY_FE.get_chat_members(data['COURSEID'])
    return {"members": members}

@app.route('/api/addUserChat', methods=['POST'])
def update_user_chat():
    """Adds a user to a chat's member list"""
    data = request.get_json()
    MY_FE.update_user_chat(data['RIN'], data['COURSEID'])
    chat_members = MY_FE.get_chat_members(data['COURSEID'])
    return {"users": chat_members}

@app.route('/api/removeUserChat', methods=['POST'])
def remove_user_chat():
    """Removes a user from a chat's member list"""
    data = request.get_json()
    MY_FE.remove_user_chat(data['RIN'], data['COURSEID'])
    chat_members = MY_FE.get_chat_members(data['COURSEID'])
    return {"users": chat_members}

@app.route('/api/ucremove', methods=['POST'])
def rem_user_course():
    """Remove a user from course"""
    data = request.get_json()
    MY_FE.remove_user_course(data['RIN'], data['COURSEID'])
    user_courses = MY_FE.get_user_courses(data['RIN'])
    return {"courses": user_courses}

@app.route('/api/userCourses', methods=['POST'])
def send_user_courses():
    """Returns a user's registered courses"""
    data = request.get_json()
    user_courses = MY_FE.get_user_courses(data['RIN'])
    return {"courses": user_courses}

if __name__ == "__main__":
    app.run(debug=True)
