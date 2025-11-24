from App.database import db
from App.models.commands import LogHoursCommand
from .student import get_student_by_id
from .staff import get_staff_by_id

def get_activity_history_by_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    return student.activity_history

def filter_student_history_by_action(student_id, action):
    student = get_student_by_id(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    return [entry for entry in student.activity_history if entry.action == action]

def log_hours(staff_id, student_id, hours, title, activity_description=None):
    staff = get_staff_by_id(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    
    student = get_student_by_id(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    # Pass the STUDENT OBJECT, not the id string
    log_command = LogHoursCommand(
        student=student,
        staff_id=staff_id,
        title=title,
        hours=hours,
        description=activity_description
    )
    log_entry = log_command.execute()
    return log_entry

