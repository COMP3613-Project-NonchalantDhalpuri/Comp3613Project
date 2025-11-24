from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

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