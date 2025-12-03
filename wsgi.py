import pytest, sys
from flask.cli import  AppGroup
from App.database import get_migrate
from App.main import create_app
from App.controllers.student import *
from App.controllers.staff import *
from flask import jsonify

# from App.controllers.app_controller import *
from App.controllers import (initialize_db )


'''APP COMMANDS(TESTING PURPOSES)'''

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

@app.route('/init')
def init_db_route():
    initialize_db()
    return jsonify({"message": "db initialized!"})


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize_db()
    print('database intialized')

# '''
# Test Commands
# '''

test = AppGroup('test', help='Testing commands') 

@test.command("unit", help="Run all unit tests")
def unit_tests_command():
    sys.exit(pytest.main(["-k", "UserUnitTests or StudentUnitTests or StaffUnitTests"]))
    
@test.command("int", help='Run all integration tests')
def integration_tests_command():
    sys.exit(pytest.main(["-k", "TestUserIntegrationTests or TestStudentIntegrationTests or TestStaffIntegrationTests or TestActivityHistoryIntegrationTests or TestRequestIntegrationTests or TestCommandIntegrationTests"]))

app.cli.add_command(test)