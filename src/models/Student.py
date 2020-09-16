from datetime import datetime

from src import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True)
    course = db.Column(db.String(20))
    stage = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True, nullable=False)
    last_contact = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship("StudentNote", backref="student", lazy=True)
    sessions = db.relationship("StudentSession", backref="student", lazy=True)

    def __init__(self, name, email, course, stage, mentor_id):
        self.name = name
        self.email = email
        self.course = course
        self.stage = stage
        self.mentor_id = mentor_id


class StudentNote(db.Model):
    __tablename__ = "student_notes"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, student_id, note):
        self.student_id = student_id
        self.note = note


class StudentSession(db.Model):
    __tablename__ = "student_sessions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    session_type = db.Column(db.String(32), nullable=False)
    project = db.Column(db.String(32), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    progress = db.Column(db.String(32), nullable=False)
    concerns = db.Column(db.Text, nullable=True)
    personal_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(
        self,
        student_id,
        date,
        duration,
        session_type,
        project,
        summary,
        progress,
        concerns,
        personal_notes,
    ):
        self.student_id = student_id
        self.date = date
        self.duration = duration
        self.session_type = session_type
        self.project = project
        self.summary = summary
        self.progress = progress
        self.concerns = concerns
        self.personal_notes = personal_notes


def create_student(name, email, course, stage, mentor_id):
    student = Student(name, email, course, stage, mentor_id)
    db.session.add(student)
    db.session.commit()

    return student


def get_mentor_students(mentor_id):
    return (
        Student.query.filter_by(mentor_id=mentor_id).order_by(Student.name.asc()).all()
    )


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


def add_student_note(student_id, note):
    note = StudentNote(student_id, note)
    db.session.add(note)
    db.session.commit()

    return note


def update_contact_date(student_id):
    student = get_student_by_id(student_id)
    student.last_contact = datetime.utcnow()
    db.session.commit()

    return student


def create_student_session(
    student_id,
    date,
    duration,
    session_type,
    project,
    summary,
    progress,
    concerns,
    personal_notes,
):
    session = StudentSession(
        student_id,
        date,
        duration,
        session_type,
        project,
        summary,
        progress,
        concerns,
        personal_notes,
    )
    db.session.add(session)
    db.session.commit()

    update_contact_date(student_id)

    return session


def get_session_by_id(session_id):
    return StudentSession.query.get(session_id)


def update_student_session(
    student_id,
    session_id,
    date,
    duration,
    session_type,
    project,
    summary,
    progress,
    concerns,
    personal_notes,
):
    session = get_session_by_id(session_id)

    session.date = date
    session.duration = duration
    session.session_type = session_type
    session.project = project
    session.summary = summary
    session.progress = progress
    session.concerns = concerns
    session.personal_notes = personal_notes

    db.session.commit()

    update_contact_date(student_id)

    return session
