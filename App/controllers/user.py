from App.models import User
from App.database import db

def create_user(name, password, email, role):
    newuser = User(name=name, password=password, email=email, role=role)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_name(name):
    result = db.session.execute(db.select(User).filter_by(name=name))
    return result.scalar_one_or_none()

def get_user_by_id(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def update_user(id, username=None, email=None, password=None):
    user = get_user_by_id(id)
    if user:
        user.name = username if username else user.name
        user.email = email if email else user.email
        user.set_password(password) if password else None
        db.session.commit()
        return True
    return None
