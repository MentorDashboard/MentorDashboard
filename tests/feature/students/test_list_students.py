from ...utils import login_user, add_student, add_user


def test_a_user_can_view_a_list_of_their_students(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    other_user = add_user("Other User", "other@user.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")
    add_student(user, "Another Student", "student@hello.com", "2007FS-ON", "IFD")
    add_student(user, "New Student", "student@new.com", "2003FS-ON", "DCD")
    add_student(other_user, "Other Student", "other@student.com", "2004FS-ON", "DCD")

    response = client.get("/students")
    result = response.data.decode()

    assert response.status_code is 200
    assert "Test Student" in result
    assert "student@hello.com" in result
    assert "2003FS-ON" in result
    assert "Other Student" not in result


def test_guest_can_not_view_list_of_students(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.get("/students", follow_redirects=True)
    result = response.data.decode()

    assert "Test Student" not in result
    assert "Login" in result
