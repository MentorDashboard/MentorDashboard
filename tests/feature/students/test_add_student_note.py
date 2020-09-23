from datetime import datetime

from ...utils import login_user, add_student, add_user


def test_user_can_add_a_note_to_a_student(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.post(
        f"/students/{student.id}/notes",
        data=dict(
            note="This is a test note",
            update_contact_date="no",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code is 200
    assert "Test Student" in result
    assert "This is a test note" in result


def test_user_can_add_a_note_to_a_student_and_update_last_contact_date(
    test_app, test_db
):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.post(
        f"/students/{student.id}/notes",
        data=dict(
            note="This is a test note",
            update_contact_date="yes",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code is 200
    assert "Test Student" in result
    assert "This is a test note" in result
    assert (
        "Last Contact: {date}".format(date=datetime.utcnow().strftime("%Y-%m-%d"))
        in result
    )


def test_user_gets_an_error_if_note_not_added(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    response = client.post(
        f"/students/{student.id}/notes",
        data=dict(
            update_contact_date="no",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code is 200
    assert (
        "There was a problem adding this note, make sure you actually add a note"
        in result
    )
