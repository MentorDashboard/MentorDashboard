from tests.utils import login_user, add_student, add_user, add_student_session


def test_user_can_view_student_sessions_report(test_app, test_db):
    client = test_app.test_client()
    user = add_user("Test User", "user@test.com", "test1234")
    login_user(client, "user@test.com", "test1234")
    student1 = add_student(
        user, "Test Student", "student@test.com", "2009FS-ON", "UCFD"
    )
    student2 = add_student(
        user, "Test Student", "student@test.com", "2009FS-ON", "UCFD"
    )
    student3 = add_student(
        user, "Test Student", "student@test.com", "2009FS-ON", "UCFD"
    )
    session1 = add_student_session(student1)
    session2 = add_student_session(student2)
    session3 = add_student_session(student3)
    session4 = add_student_session(student1)

    rv = client.get("/reports/sessions-report")
    res = rv.data.decode()

    assert rv.status_code == 200
    assert session1.project in res
    assert session2.student.name in res
    assert str(session3.duration) in res
    assert session4.session_type in res
    assert "4 Student Sessions" in res
