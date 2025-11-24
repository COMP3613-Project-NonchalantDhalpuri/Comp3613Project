from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from jwt import ExpiredSignatureError

from App.controllers import create_user, initialize            
from App.controllers.student import get_student_by_id          
from App.controllers.activity_history import log_hours
from App.controllers.request import create_request, get_requests_by_student         

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/student/home', methods=['GET', 'POST'])
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
        denied_requests=denied_requests
    )


# IMPORTANT: no endpoint= here, so endpoint is index_views.staff_home_page
@index_views.route('/staff/home', methods=['GET', 'POST'])
def staff_home_page():
    # ----- get staff id from JWT (no models here, just JWT helpers) -----
    staff_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity is not None:
            staff_id = int(identity)
    except ExpiredSignatureError:
        flash("Session has expired. Please log in again.", "error")
        return redirect(url_for('index_views.login_page'))
    except Exception:
        staff_id = None

    selected_student = None
    student_id = request.values.get('student_id')  

    
    if student_id:
        selected_student = get_student_by_id(student_id)
        if not selected_student:
            flash(f"No student found with ID {student_id}.", "error")

    
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
                'staff_home.html',
                active_tab='home',
                selected_student=selected_student
            )

        if not staff_id:
            flash("You must be logged in as staff to log hours.", "error")
        elif not selected_student:
            flash("Please select a valid student first.", "error")
        else:
            try:
                log_hours(
                    staff_id=staff_id,
                    student_id=student_id,
                    hours=hours,
                    title=title,
                    activity_description=description
                )
                flash("Hours logged successfully.", "success")
                selected_student = get_student_by_id(student_id)
                return redirect(url_for("index_views.staff_home_page"))
            except Exception as e:
                print(e)
                flash("Failed to log hours. Please try again.", "error")
                return redirect(url_for("index_views.staff_home_page"))

    return render_template(
        'staff_home.html',
        active_tab='home',
        selected_student=selected_student
    )
