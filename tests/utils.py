from datetime import date, timedelta

from src import db
from src.models.User import create_user
from src.models.Student import create_student, create_student_session


def add_user(name="Test User", email="user@test.com", password="test1234"):
    return create_user(name, email, password)


def login_user(client, email=None, password=None):
    if email is None and password is None:
        email = "user@test.com"
        password = "test1234"
        add_user("Test User", email, password)

    return client.post("/login", data=dict(email=email, password=password))


def add_student(user, name, email, course, stage):
    student = create_student(name, email, course, stage, user.id)
    student.last_contact = date.today() - timedelta(days=1)
    db.session.commit()

    return student


def add_student_session(student):
    session = create_student_session(
        student.id,
        date.today(),
        45,
        "inception",
        "UCFD",
        "This was an intro call for UCFD",
        "average",
        "",
        "",
    )

    db.session.add(session)
    db.session.commit()

    return session
