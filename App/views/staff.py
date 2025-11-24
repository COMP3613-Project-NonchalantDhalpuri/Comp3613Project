from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from jwt import ExpiredSignatureError

from App.controllers.request import get_all_requests, approve_request, process_request_denial         

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

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