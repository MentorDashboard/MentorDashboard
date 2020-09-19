from tests.utils import login_user


def test_a_user_can_create_a_new_student(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    response = client.post(
        "/students/new",
        data=dict(
            name="Test User", email="user@test.com", course="2009FS-ON", stage="UCFD"
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code is 200
    assert "New student saved" in result
    assert "Student Management" in result


def test_a_guest_can_not_create_a_new_student(test_app, test_db):
    client = test_app.test_client()

    response = client.post(
        "/students/new",
        data=dict(
            name="Test User", email="user@test.com", course="2009FS-ON", stage="UCFD"
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert "Login" in result
    assert "New student saved" not in result
    assert "Student Management" not in result


def test_create_student_form_renders_for_a_user(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    response = client.get("/students/new")
    result = response.data.decode()

    assert response.status_code is 200
    assert "Add New Student" in result
    assert "Name" in result
    assert "Email" in result
    assert "Course" in result
    assert "Stage" in result
    assert "Add Student" in result


def test_guest_can_not_view_create_new_student_form(test_app, test_db):
    client = test_app.test_client()

    response = client.get("/students/new", follow_redirects=True)
    result = response.data.decode()

    assert response.status_code is 200
    assert "Add New Student" not in result
    assert "Name" not in result
    assert "Course" not in result
    assert "Stage" not in result
    assert "Add Student" not in result
