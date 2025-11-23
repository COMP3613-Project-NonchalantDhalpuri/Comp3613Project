from App.database import db
from .user import User

class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    hoursAccumulated = db.Column(db.Integer, default = 0)
    accolades = db.Column(db.JSON, default = list)

    activity_history = db.relationship('ActivityHistory', backref='student', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Request', backref='student', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "student"
    }
    
    def __init__(self, name, email, password):
        super().__init__(name, email, password, role="student")
       
    
    
    def get_json(self):
        return{
            'student_id': self.student_id,
            'username': self.username,
            'email': self.email
        }
    
    # Method to calculate total approved hours and accolades
    # To be moved to controllers later
    def accolades(self):
        milestones = [10, 25, 50]

        new_accolades = []

        for milestone in milestones:
            if self.hoursAccumulated >= milestone and milestone not in self.accolades:
                new_accolades.append(f'{milestone} Hours Milestone')

        self.accolades = new_accolades