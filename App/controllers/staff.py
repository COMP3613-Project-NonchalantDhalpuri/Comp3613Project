from App.database import db
from App.models import Staff

def create_staff(name,email,password): #registers a new staff member
    new_staff=Staff(name = name, email = email, password = password)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff

def get_staff_by_id(staff_id):
    return db.session.get(Staff, staff_id)

def get_all_staff():
    return db.session.scalars(db.select(Staff)).all()

