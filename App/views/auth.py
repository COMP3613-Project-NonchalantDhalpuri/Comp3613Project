from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from.index import index_views

from App.controllers import (
    jwt_authenticate,
    get_user_by_name
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


@auth_views.route('/login/staff', methods=['POST'])
def login_staff():
    data = request.form
    user = get_user_by_name(data['name'])

    if user and user.role != 'staff':
        flash('Bad username or password given'), 401
        return redirect(url_for('index_views.login_page'))

    token = jwt_authenticate(data['name'], data['password'])
    if not token:
        flash('Bad username or password given'), 401
        response = redirect(url_for('index_views.login_page'))
    else:
        flash('Login Successful')
        response = redirect(url_for('index_views.staff_home_page'))
        set_access_cookies(response, token) 
    return response

@auth_views.route('/login/student', methods=['POST'])
def login_student():
    data = request.form
    user = get_user_by_name(data['name'])

    if user and user.role != 'student':
        flash('Bad username or password given'), 401
        return redirect(url_for('index_views.login_page'))
    
    token = jwt_authenticate(data['name'], data['password'])
    response = redirect(request.referrer)
    if not token:
        flash('Bad username or password given'), 401
        response = redirect(url_for('index_views.login_page'))
    else:
        flash('Login Successful')
        response = redirect(url_for('index_views.student_home_page'))
        set_access_cookies(response, token) 
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('index_views.login_page')) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response