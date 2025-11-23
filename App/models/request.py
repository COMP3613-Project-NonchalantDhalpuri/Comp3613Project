from App.database import db
from datetime import datetime

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable = True)
    hours = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    title = db.Colum(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = True)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                             onupdate=db.func.current_timestamp())

    def __init__(self, student_id, hours, title,  status='pending', staff_id = None, description = None):
        self.student_id = student_id
        self.staff_id = staff_id
        self.hours = hours
        self.status = status
        self.title = title
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'hours': self.hours,
            'status': self.status,
            'date_created': self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'date_updated': self.date_updated.strftime("%Y-%m-%d %H:%M:%S")
        }