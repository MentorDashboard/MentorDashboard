from datetime import datetime

from ...utils import login_user, add_student, add_user, add_student_session


def test_user_can_edit_a_student_session(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student = add_student(user, "Test Student", "student@test.com", "2009FS-ON", "UCFD")
    session = add_student_session(student)
    now = datetime.utcnow().strftime("%Y-%m-%d")
    now_full = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    response = client.get(f"/students/{student.id}")
    result = response.data.decode()

    assert response.status_code is 200
    assert "Test Student" in result
    assert "inception" in result
    assert "UCFD" in result
    assert "45" in result
    assert "Last Contact: {date}".format(date=now) in result

    response = client.post(
        f"/students/{student.id}/sessions/{session.id}/edit",
        data=dict(
            date=now_full,
            duration=45,
            session_type="inception",
            project="IFD",
            summary="Booked as UCFD but was for IFD, went over students plans and pointed out some issues",
            progress="poor",
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
    assert "IFD" in result
    assert "45" in result
    assert "Last Contact: {date}".format(date=now) in result
    assert "Session successfully updated" in result
