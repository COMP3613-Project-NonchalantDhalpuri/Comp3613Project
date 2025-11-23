from App.database import db
from App.models import Staff,Student,Request
from App.models.commands import ApproveRequestCommand, DenyRequestCommand
from .student import get_student_by_id
from .staff import get_staff_by_id

def create_request(student_id,hours,title,description=None): 
    student = get_student_by_id(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    new_request = Request(
        student_id=student_id,
        hours=hours,
        title=title,
        description=description
    )

    db.session.add(new_request)
    db.session.commit()

    return new_request

def get_all_requests():
    return db.session.scalars(db.select(Request)).all()

def get_request_by_id(request_id):
    return db.session.get(Request, request_id)

def get_requests_by_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    return student.requests

def delete_request(request_id):
    request = get_request_by_id(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    db.session.delete(request)
    db.session.commit()

def update_request(request_id, hours=None, title=None, description=None):
    request = get_request_by_id(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    if hours is not None:
        request.hours = hours
    if title is not None:
        request.title = title
    if description is not None:
        request.description = description

    db.session.add(request)
    db.session.commit()

def approve_request(staff_id, request_id): #staff approves a student's hours request
    staff = get_staff_by_id(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    
    request = get_request_by_id(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    student = get_student_by_id(request.student_id)

    approval = ApproveRequestCommand(request, student)
    approval.execute()

def process_request_denial(staff_id, request_id): 
    staff = get_staff_by_id(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    
    request = get_request_by_id(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    student = get_student_by_id(request.student_id)

    denial = DenyRequestCommand(request, student)
    denial.execute()
