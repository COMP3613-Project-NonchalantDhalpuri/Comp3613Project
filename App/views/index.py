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
        denied_requests=denied_requests, 
        active_tab='home'
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


@index_views.route('/student/accolades', methods=['GET'])
@jwt_required()
def student_accolades_page():
    student = get_student_by_id(current_user.id)
    recent_milestones = get_student_accolades(current_user.id)
    next_milestone = get_next_milestone(current_user.id)

    if next_milestone:
        progress_percent = (student.hoursAccumulated / next_milestone) * 100
        if progress_percent > 100:
            progress_percent = 100
    else:
        progress_percent = 100

    selected_milestone = recent_milestones[0] if recent_milestones else None
    awarded_accolades = recent_milestones

    return render_template(
        'student_accolades.html',
        student=student,
        recent_milestones=recent_milestones,
        next_milestone=next_milestone,
        progress_percent=progress_percent,
        selected_milestone=selected_milestone,
        awarded_accolades=awarded_accolades,
    )

@index_views.route('/staff/student-hours', methods=['GET'])
def staff_student_hours_page():
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

    search_id = request.args.get('search_id', '').strip()
    search_name = request.args.get('search_name', '').strip()
    min_hours_raw = request.args.get('min_hours', '').strip()

    students = get_all_students()

    if search_id:
        students = [s for s in students if str(s.id) == search_id]

    if search_name:
        q = search_name.lower()
        students = [s for s in students if q in s.name.lower()]

    if min_hours_raw:
        try:
            min_hours = float(min_hours_raw)
            students = [s for s in students if s.hoursAccumulated >= min_hours]
        except ValueError:
            flash("Hours filter must be a valid number.", "error")

    pending_counts = {}
    for s in students:
        reqs = get_requests_by_student(s.id)
        pending_counts[s.id] = len([r for r in reqs if r.status == 'pending'])

    return render_template(
        'staff_student_hours.html',
        active_tab='student_hours',
        students=students,
        pending_counts=pending_counts,
        search_id=search_id,
        search_name=search_name,
        min_hours=min_hours_raw
    )

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

