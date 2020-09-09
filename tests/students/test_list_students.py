from tests.utils import login_user, add_student, add_user


def test_a_user_can_view_a_list_of_their_students(test_app, test_db):
    client = test_app.test_client()
    user = add_user('Test User', 'user@test.com', 'test1234')
    other_user = add_user('Other User', 'other@user.com', 'test1234')
    login_user(client, 'user@test.com', 'test1234')
    add_student(user, 'Test Student', 'student@test.com', '2009FS-ON', 'UCFD')
    add_student(user, 'Another Student', 'student@hello.com', '2007FS-ON', 'IFD')
    add_student(user, 'New Student', 'student@new.com', '2003FS-ON', 'DCD')
    add_student(other_user, 'Other Student', 'other@student.com', '2004FS-ON', 'DCD')

    res = client.get('/students')

    assert res.status_code is 200
    assert b"Test Student" in res.data
    assert b"student@hello.com" in res.data
    assert b"2003FS-ON" in res.data
    assert b"Other Student" not in res.data
