from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    current_user
)
from jwt import ExpiredSignatureError

from App.controllers import create_user, initialize
from App.controllers.student import (
    get_student_by_id,
    get_student_accolades,
    get_next_milestone,
    get_all_students
)
from App.controllers.activity_history import get_activity_history_by_student
from App.controllers.request import create_request, get_requests_by_student

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student/history', methods=['GET'])
def student_history_page():
    student_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity is not None:
            student_id = int(identity)
    except ExpiredSignatureError:
        flash("Session has expired. Please log in again.", "error")
        return redirect(url_for('index_views.login_page'))
    except Exception:
        student_id = None
        return redirect(url_for('index_views.login_page'))
    
    activity_history = get_activity_history_by_student(student_id)

    return render_template(
        'student_history.html',
        activity_history = activity_history
    )