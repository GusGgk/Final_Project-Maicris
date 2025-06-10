from flask import Blueprint, request, jsonify
from services.course_service import get_all_courses

course_controller = Blueprint('course_controller', __name__)

@course_controller.route('/courses', methods=['GET'])
def list_courses():
    courses = get_all_courses()
    return jsonify(courses)
