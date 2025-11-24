from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize, get_student_by_id, get_student_accolades, get_next_milestone
from flask_jwt_extended import jwt_required, current_user


index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/student/home', methods=['GET'])
def student_home_page():
    return render_template('index.html')
    #CHANGE THIS TO APPROPRIATE HOME PAGE

@index_views.route('/staff/home', methods=['GET'])
def staff_home_page():
    return render_template('index.html')
    #CHANGE THIS TO APPROPRIATE HOME PAGE

@index_views.route('/student/accolades', methods=['GET'])
@jwt_required()
def student_accolades_page():
    student = get_student_by_id(current_user.id)
    recent = get_student_accolades(current_user.id)
    next_milestone = get_next_milestone(current_user.id)

    if next_milestone:
        progess_percentage = (student.hoursAccumulated / next_milestone) * 100
        if progess_percentage > 100:
            progess_percentage = 100
    else:
        progess_percentage = 100

    return render_template(
        'student_accolades.html',
        student=student,
        next_milestone=next_milestone,
        progress_percentage=progess_percentage
    )