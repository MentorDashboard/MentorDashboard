from tests.utils import login_user


def test_a_user_can_create_a_new_student(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    res = client.post('/students/new', data=dict(
        name='Test User',
        email='user@test.com',
        course='2009FS-ON',
        stage='UCFD'
    ), follow_redirects=True)

    assert res.status_code is 200
    assert b"New student saved" in res.data
    assert b"Student Management" in res.data


def test_a_guest_can_not_create_a_new_student(test_app, test_db):
    client = test_app.test_client()

    res = client.post('/students/new', data=dict(
        name='Test User',
        email='user@test.com',
        course='2009FS-ON',
        stage='UCFD'
    ), follow_redirects=True)

    assert b"Login" in res.data
    assert b"New student saved" not in res.data
    assert b"Student Management" not in res.data


def test_create_student_form_renders_for_a_user(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    res = client.get('/students/new')

    assert res.status_code is 200
    assert b"Add New Student" in res.data
    assert b"Name" in res.data
    assert b"Email" in res.data
    assert b"Course" in res.data
    assert b"Stage" in res.data
    assert b"Add Student" in res.data


def test_guest_can_not_view_create_new_student_form(test_app, test_db):
    client = test_app.test_client()

    res = client.get('/students/new', follow_redirects=True)

    assert res.status_code is 200
    assert b"Add New Student" not in res.data
    assert b"Name" not in res.data
    assert b"Course" not in res.data
    assert b"Stage" not in res.data
    assert b"Add Student" not in res.data
