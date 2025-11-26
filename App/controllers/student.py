from App.database import db
from App.models import Student,ActivityHistory

def create_student(name,email,password):
    new_student=Student(name = name, email = email, password = password)
    db.session.add(new_student)
    db.session.commit()
    return new_student

def get_student_by_id(student_id):
    return db.session.get(Student, student_id)

def get_all_students():
    return db.session.scalars(db.select(Student)).all()

def calculate_accolades(student_id,staff_id=None):
    student = get_student_by_id(student_id)

    milestones = [10, 25, 50]
    new_accolades = []

    for milestone in milestones:
        if student.hoursAccumulated >= milestone and milestone not in student.accolades:
            title = f'{milestone} Hours Milestone'
            new_accolades.append(title)
            new_activity_log = ActivityHistory(student_id=student_id,staff_id=staff_id,hours=milestone,action="accolade",title=title)
            db.session.add(new_activity_log)

    student.accolades = new_accolades

    db.session.add(student)
    db.session.commit()

def get_leaderboard():
    return db.session.scalars(
        db.select(Student).order_by(Student.hoursAccumulated.desc())
    ).all()


def get_student_accolades(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return(f"Student with id {student_id} not found.")
    
    return student.accolades


def get_next_milestone(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return None
    
    milestones = [10, 25, 50]
    for milestone in milestones:
        if student.hoursAccumulated < milestone:
            return milestone
    return None
