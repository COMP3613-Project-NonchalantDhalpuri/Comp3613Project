from flask import Blueprint, redirect, render_template, request, jsonify, flash, url_for
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    current_user
)
from jwt import ExpiredSignatureError

from App.controllers.student import (
    get_student_by_id,
    get_student_accolades,
    get_next_milestone,
)
from App.controllers.activity_history import get_activity_history_by_student
from App.controllers.request import create_request, get_requests_by_student

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student/home', methods=['GET', 'POST'])
def student_home_page():
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

    if request.method == 'POST':
        title = request.form.get('title')
        hours_raw = request.form.get('hours')
        description = request.form.get('description', '')

        try:
            hours = float(hours_raw)
            if hours <= 0:
                raise ValueError
        except (TypeError, ValueError):
            flash("Hours must be a positive number.", "error")
            return render_template(
                'student_home.html',
            )
        
        try:    
            new_request = create_request(
                student_id=student_id,
                hours=hours,
                title=title,
                description=description
            )
            flash("Request made successfully.", "success")
            return redirect(url_for("index_views.student_home_page"))
        except Exception as e:
            print(e)
            flash("Failed to create request. Please try again.", "error")
            return redirect(url_for("index_views.student_home_page"))
    
    requests = get_requests_by_student(student_id)
    approved_requests = [req for req in requests if req.status == 'approved']
    pending_requests = [req for req in requests if req.status == 'pending']
    denied_requests = [req for req in requests if req.status == 'denied']

    return render_template(
        'student_home.html',
        approved_requests=approved_requests,
        pending_requests=pending_requests,
        denied_requests=denied_requests, 
        active_tab='home'
    )

@student_views.route('/student/accolades', methods=['GET'])
def student_accolades_page():
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
    except ExpiredSignatureError:
        flash("Session has expired. Please log in again.", "error")
        return redirect(url_for('index_views.login_page'))
    except Exception:
        return redirect(url_for('index_views.login_page'))

    accolade_index = request.args.get("accolade_index", type=int)
    student = get_student_by_id(current_user.id)
    awarded_accolades = get_student_accolades(current_user.id)
    next_milestone = get_next_milestone(current_user.id)

    if next_milestone:
        progress_percent = (student.hoursAccumulated / next_milestone) * 100
        if progress_percent > 100:
            progress_percent = 100
    else:
        progress_percent = 100

    selected_milestone = awarded_accolades[accolade_index] if accolade_index is not None else None
    selected_milestone_hours = int(selected_milestone.split()[0]) if selected_milestone is not None else None

    return render_template(
        'student_accolades.html',
        student=student,
        next_milestone=next_milestone,
        progress_percent=progress_percent,
        selected_milestone=selected_milestone,
        awarded_accolades=awarded_accolades,
        selected_milestone_hours = selected_milestone_hours
    )

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
        activity_history = activity_history,
        active_tab='history'
    )