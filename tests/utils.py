from src import db
from src.models.User import create_user
from src.models.Student import create_student


def add_user(name='Test User', email='user@test.com', password='test1234'):
    return create_user(name, email, password)


def login_user(client, email=None, password=None):
    if email is None and password is None:
        email = 'user@test.com'
        password = 'test1234'
        add_user('Test User', email, password)

    return client.post(
        '/login',
        data=dict(email=email, password=password)
    )


def add_student(user, name, email, course, stage):
    return create_student(name, email, course, stage, user.id)


def add_existing_student(user, name, email, course, stage, date):
    student = add_student(user, name, email, course, stage)
    student.last_contact = date
    db.session.commit()

    return student
