from ...utils import login_user, add_student, add_user


def test_user_can_edit_their_student(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.post(
        f"/students/{student.id}/edit",
        data=dict(
            name="Updated Student",
            email="student@test.com",
            course="2009FS-ON",
            stage="IFD",
            active="1",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code is 200
    assert "Updated Student" in result
    assert "IFD" in result
    assert "Student Successfully Updated" in result


def test_updating_status_causes_status_to_be_updated(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.post(
        f"/students/{student.id}/edit",
        data=dict(
            name="Updated Student",
            email="student@test.com",
            course="2009FS-ON",
            stage="IFD",
            active="0",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code is 200
    assert "Updated Student" in result
    assert "IFD" in result
    assert "InActive" in result
    assert "Student Successfully Updated" in result


def test_a_user_can_not_update_another_users_student(test_app, test_db):
    client = test_app.test_client()
    add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    other_user = add_user("Other User", "other@user.com", "test1234")
    student = add_student(
        other_user, "TestR Student", "student@test.com", "2009FS-ON", "UCFD"
    )

    response = client.post(
        f"/students/{student.id}/edit",
        data=dict(
            name="Updated Student",
            email="student@test.com",
            course="2009FS-ON",
            stage="IFD",
            active="1",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 403


def test_edit_student_form_renders(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.get(f"/students/{student.id}/edit")
    result = response.data.decode()

    assert response.status_code == 200
    assert "Test Student" in result
    assert "student@test.com" in result
    assert "2009FS-ON" in result
    assert "User Centric Frontend Development" in result
