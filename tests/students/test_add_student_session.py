from datetime import datetime

from tests.utils import login_user, add_student, add_user


def test_user_can_add_a_session_to_a_student(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    res = client.post(
        f"/students/{student.id}/sessions",
        data=dict(
            date=now,
            duration=45,
            session_type="inception",
            project="UCFD",
            summary="This was a session",
            progress="average",
            concerns="There are some concerns",
            personal_notes="These are my personal notes",
        ),
        follow_redirects=True,
    )

    assert res.status_code is 200
    assert b"Test Student" in res.data
    assert b"inception" in res.data
    assert b"UCFD" in res.data
    assert b"45" in res.data
    assert "Last Contact: {date}".format(date=now).encode() in res.data
