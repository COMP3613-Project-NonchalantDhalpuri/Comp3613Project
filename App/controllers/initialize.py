from App.models import User, Student, Staff, Request
from App.database import db


def initialize_db(drop_first=True):
    """Initialize the database and seed sample data.

    Args:
        drop_first (bool): if True, drop all tables before creating them.

    Returns a dict with lists of created record IDs.
    """
    if drop_first:
        db.drop_all()
    db.create_all()

    # Sample students (username, email, password)
    students_data = [
        ("alice", "alice.smith@gmail.com", "password1"),
        ("bob", "bob.jones@hotmail.com", "password2"),
        ("charlie", "charlie.brown@gmail.com", "password3"),
        ("diana", "diana.lee@hotmail.com", "password4"),
        ("eve", "eve.patel@gmail.com", "password5"),
    ]

    # Sample staff (username, email, password)
    staff_data = [
        ("msmith", "mr.smith@gmail.com", "staffpass1"),
        ("mjohnson", "ms.johnson@hotmail.com", "staffpass2"),
        ("mlee", "mr.lee@gmail.com", "staffpass3"),
    ]

    students = []
    for name, email, pwd in students_data:
        s = Student(name=name, email=email, password=pwd)
        students.append(s)
        db.session.add(s)

    staff_members = []
    for name, email, pwd in staff_data:
        st = Staff(name=name, email=email, password=pwd)
        staff_members.append(st)
        db.session.add(st)

    db.session.commit()


    