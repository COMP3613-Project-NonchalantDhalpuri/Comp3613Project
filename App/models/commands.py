from abc import ABC, abstractmethod
from App.database import db
from .activity_history import ActivityHistory


class Command(ABC):
    @abstractmethod
    def execute(self):
        """Execute the command"""
        pass


class ApproveRequestCommand(Command):
    def __init__(self, request, student):
        self.request = request
        self.student = student

    def execute(self):
        self.request.status = 'approved'
        self.student.hoursAccumulated += self.request.hours

        activity = ActivityHistory(
            student_id=self.student.id,
            staff_id=self.request.staff_id,
            request_id = self.request.id,
            title=self.request.title,
            hours=self.request.hours,
            action='approved',
            description=self.request.description
        )

        db.session.add(activity)
        db.session.commit()

class DenyRequestCommand(Command):
    def __init__(self, request, student):
        self.request = request
        self.student = student

    def execute(self):
        self.request.status = 'denied'

        activity = ActivityHistory(
            student_id=self.student.id,
            staff_id=self.request.staff_id,
            request_id = self.request.id,
            title=self.request.title,
            hours=self.request.hours,
            action='denied',
            description=self.request.description
        )
        
        db.session.add(activity)
        db.session.commit()

class LogHoursCommand(Command):
    def __init__(self, student, staff_id, title, hours, description=None):
        self.student = student
        self.staff_id = staff_id
        self.title = title
        self.hours = hours
        self.description = description

    def execute(self):
        self.student.hoursAccumulated += self.hours
        activity = ActivityHistory(
            student_id=self.student.id,
            staff_id=self.staff_id,
            title=self.title,
            hours=self.hours,
            action='logged',
            description=self.description
        )
        db.session.add(activity)
        db.session.commit()

        return activity 