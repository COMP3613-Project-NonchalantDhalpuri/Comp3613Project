from flask import Blueprint, redirect, render_template, flash, url_for
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
)
from jwt import ExpiredSignatureError

from App.controllers.student import (
    get_student_by_id,
    get_all_students
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/leaderboard', methods=['GET'])
def leaderboard_page():
    viewer_student = None
    viewer_type = None
    
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()

        if identity is not None:
            try:
                viewer_student = get_student_by_id(identity)
                viewer_type = "student"     
            except Exception:
                viewer_student = None
                viewer_type = "staff"      
        else:
            viewer_type = "staff"           

    except ExpiredSignatureError:
        flash("Session has expired. Please log in again.", "error")
        return redirect(url_for('index_views.login_page'))
    except Exception:
        viewer_student = None
        viewer_type = "staff"                

    students = get_all_students() or []

    
    for i in range(len(students)):
        max_index = i
        for j in range(i + 1, len(students)):
            if students[j].hoursAccumulated > students[max_index].hoursAccumulated:
                max_index = j
        students[i], students[max_index] = students[max_index], students[i]
    

    user_rank = None
    user_hours = None

    if viewer_student:
        
        id_list = []
        for s in students:
            id_list.append(s.id)

        
        for i in range(len(id_list)):
            if viewer_student.id == id_list[i]:
                user_rank = i + 1
                break

        user_hours = viewer_student.hoursAccumulated

    return render_template(
        'leaderboard.html',
        leaders=students,
        viewer_is_student=viewer_student is not None,
        viewer_type=viewer_type,
        user_rank=user_rank,
        user_hours=user_hours,
        active_tab='leaderboards'
    )

