from datetime import datetime

from src import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True)
    course = db.Column(db.String(20))
    stage = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True, nullable=False)
    last_contact = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, course, stage, mentor_id):
        self.name = name
        self.email = email
        self.course = course
        self.stage = stage
        self.mentor_id = mentor_id


def create_student(name, email, course, stage, mentor_id):
    student = Student(name, email, course, stage, mentor_id)
    db.session.add(student)
    db.session.commit()

    return student


def get_mentor_students(mentor_id):
    return Student.query.filter_by(mentor_id=mentor_id).order_by(Student.name.asc()).all()


def get_student_by_id(student_id):
    return Student.query.get(student_id)


def update_student(student_id, name, email, course, stage, active, mentor_id):
    student = get_student_by_id(student_id)

    if student.mentor_id is not mentor_id:
        return False

    student.name = name
    student.email = email
    student.course = course
    student.stage = stage
    student.active = active

    db.session.commit()
    return True
