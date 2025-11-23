from App.database import db
from datetime import datetime

class ActivityHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=True)
    hours = db.Column(db.Float, nullable=False)
    action = db.Column(db.String(20), nullable=False, default='approved')
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable = True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, student_id, staff_id, title, hours, action='logged by staff', request_id=None, description=None):
        self.student_id = student_id
        self.staff_id = staff_id
        self.request_id = request_id
        self.hours = hours
        self.action = action
        self.title = title
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'hours': self.hours,
            'action': self.action,
            'title': self.title,
            'description': self.description,
            'timestamp':  self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }