from datetime import datetime

from ...utils import login_user, add_student, add_user


def test_user_can_add_a_session_to_a_student(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    response = client.post(
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
            send_feedback="no",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code is 200
    assert "Test Student" in result
    assert "inception" in result
    assert "UCFD" in result
    assert "45" in result
    assert "Last Contact: {date}".format(date=now) in result
