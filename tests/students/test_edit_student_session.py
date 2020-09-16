from datetime import datetime

from tests.utils import login_user, add_student, add_user, add_student_session


def test_user_can_edit_a_student_session(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")
    session = add_student_session(student)
    now = datetime.utcnow().strftime("%Y-%m-%d")
    now_full = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    res = client.get(f"/students/{student.id}")

    assert res.status_code is 200
    assert b"Test Student" in res.data
    assert b"inception" in res.data
    assert b"UCFD" in res.data
    assert b"45" in res.data
    assert "Last Contact: {date}".format(date=now).encode() in res.data

    res = client.post(
        f"/students/{student.id}/sessions/{session.id}",
        data=dict(
            date=now_full,
            duration=45,
            session_type="inception",
            project="IFD",
            summary="Booked as UCFD but was for IFD, went over students plans and pointed out some issues",
            progress="poor",
            concerns="There are some concerns",
            personal_notes="These are my personal notes",
        ),
        follow_redirects=True,
    )

    assert res.status_code is 200
    assert b"Test Student" in res.data
    assert b"inception" in res.data
    assert b"IFD" in res.data
    assert b"45" in res.data
    assert "Last Contact: {date}".format(date=now).encode() in res.data
    assert b"Session successfully updated" in res.data
