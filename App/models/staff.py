from App.database import db
from .user import User

class Staff(User):
    __tablename__ = "staff"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    activity_history = db.relationship('ActivityHistory', backref='staff', lazy=True, cascade="all, delete-orphan")   
    
    __mapper_args__ = {
        "polymorphic_identity": "staff"
    }

    def __init__(self, name, email, password):
       super().__init__(name, email, password, role="staff")

    def __repr__(self):
        return f"[Staff ID= {str(self.staff_id):<3} Name= {self.username:<10} Email= {self.email}]"
    
    def get_json(self):
        return{
            'staff_id': self.staff_id,
            'username': self.username,
            'email': self.email
        }
    
    