from ...utils import login_user, add_student, add_user


def test_a_user_can_view_one_of_their_students(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.get(f"/students/{student.id}")
    result = response.data.decode()

    assert response.status_code is 200
    assert "Test Student" in result
    assert "student@test.com" in result
    assert "2009FS-ON" in result


def test_a_user_can_not_view_student_of_another_user(test_app, test_db):
    client = test_app.test_client()
    add_user("Test User", "user@test.com", "test1234")
    other_user = add_user("Other User", "other@user.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(
        other_user, "Test Student", "student@test.com", "2009FS-ON", "UCFD"
    )

    response = client.get(f"/students/{student.id}")
    result = response.data.decode()

    assert response.status_code == 404
    assert "Test Student" not in result
    assert "student@test.com" not in result
    assert "2009FS-ON" not in result


def test_can_not_view_user_that_does_not_exist(test_app, test_db):
    client = test_app.test_client()
    add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")

    response = client.get("/students/1", follow_redirects=True)

    assert response.status_code == 404
