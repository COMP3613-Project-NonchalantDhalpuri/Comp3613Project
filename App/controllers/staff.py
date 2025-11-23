from App.database import db
from App.models import User,Staff,Student,Request

def create_staff(name,email,password): #registers a new staff member
    new_student=Staff(name = name, email = email, password = password)
    db.session.add(new_student)
    db.session.commit()
    return new_student

def get_staff_by_id(staff_id):
    return db.session.get(Staff, staff_id)

def get_all_staff():
    return db.session.scalars(db.select(Staff)).all()

