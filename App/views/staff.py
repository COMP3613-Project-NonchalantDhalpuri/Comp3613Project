from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required
from jwt import ExpiredSignatureError

from App.controllers.request import get_all_requests, approve_request, process_request_denial, get_requests_by_student   
from App.controllers.student import get_student_by_id, get_all_students
    

from App.controllers.activity_history import log_hours     

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/home', methods=['GET', 'POST'])
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


@staff_views.route('/staff/pending' , methods=['GET', 'POST'])
def staff_pending_requests_page():
    staff_id = None
    action = request.args.get("action")
    reqId = request.args.get("request_id")
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
        return redirect(url_for('index_views.login_page'))
    
    requests = get_all_requests()
    pending_requests = [req for req in requests if req.status == 'pending']
    
    if request.method == 'POST':
        if action == 'approve_request':
            try:
                approve_request(staff_id=staff_id, request_id=reqId)
                flash("Request approved successfully.", "success")
            except Exception as e:
                print(e)
                flash("Failed to approve request. Please try again.", "error")
        elif action == 'deny_request':
            try:
                process_request_denial(staff_id=staff_id, request_id=reqId)
                flash("Request denied successfully.", "success")
            except Exception as e:
                print(e)
                flash("Failed to deny request. Please try again.", "error")
        elif action == 'approve_all':
            try:
                for req in pending_requests:
                    approve_request(staff_id=staff_id, request_id=req.id)
                flash("All requests approved successfully.", "success")
            except Exception as e:
                print(e)
                flash("Failed to approve all requests. Please try again later", "error")
        elif action == 'deny_all':
            try:
                for req in pending_requests:
                    process_request_denial(staff_id=staff_id, request_id=req.id)
                flash("All requests denied successfully.", "success")
            except Exception as e:
                print(e)
                flash("Failed to deny all requests. Please try again later", "error")
        
        return redirect(url_for('staff_views.staff_pending_requests_page'))


    return render_template(
        'staff_pending_requests.html',
        pending_requests=pending_requests,
        num_pending=len(pending_requests)
    )

@staff_views.route('/staff/student-hours', methods=['GET'])
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
        return redirect(url_for('index_views.login_page'))

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