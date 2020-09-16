from datetime import date, timedelta

from tests.utils import login_user, add_student, add_user, add_existing_student


def test_user_can_add_a_note_to_a_student(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    res = client.post(
        f"/students/{student.id}/notes",
        data=dict(
            note="This is a test note",
            update_contact_date="no",
        ),
        follow_redirects=True,
    )

    assert res.status_code is 200
    assert b"Test Student" in res.data
    assert b"This is a test note" in res.data


def test_user_can_add_a_note_to_a_student_and_update_last_contact_date(
    test_app, test_db
):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    today = date.today()
    yesterday = today - timedelta(days=1)
    student = add_existing_student(
        user, "Test Student", "student@test.com", "2009FS-ON", "UCFD", yesterday
    )

    res = client.post(
        f"/students/{student.id}/notes",
        data=dict(
            note="This is a test note",
            update_contact_date="yes",
        ),
        follow_redirects=True,
    )

    assert res.status_code is 200
    assert b"Test Student" in res.data
    assert b"This is a test note" in res.data
    assert (
        "Last Contact: {date}".format(date=today.strftime("%Y-%m-%d")).encode()
        in res.data
    )


def test_user_gets_an_error_if_note_not_added(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")

    res = client.post(
        f"/students/{student.id}/notes",
        data=dict(
            update_contact_date="no",
        ),
        follow_redirects=True,
    )

    assert res.status_code is 200
    assert (
        b"There was a problem adding this note, make sure you actually add a note"
        in res.data
    )
