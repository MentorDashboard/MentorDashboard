from tests.utils import login_user, add_student, add_user


def test_a_user_can_view_one_of_their_students(test_app, test_db):
    client = test_app.test_client()
    user = add_user('Test User', 'user@test.com', 'test1234')
    login_user(client, 'user@test.com', 'test1234')
    student = add_student(user, 'Test Student', 'student@test.com', '2009FS-ON', 'UCFD')

    res = client.get(f'/students/{student.id}')

    assert res.status_code is 200
    assert b"Test Student" in res.data
    assert b"student@test.com" in res.data
    assert b"2009FS-ON" in res.data


# def test_guest_can_not_view_list_of_students(test_app, test_db):
#     client = test_app.test_client()
#     user = add_user('Test User', 'user@test.com', 'test1234')
#     add_student(user, 'Test Student', 'student@test.com', '2009FS-ON', 'UCFD')
#
#     res = client.get('/students', follow_redirects=True)
#
#     assert b"Test Student" not in res.data
#     assert b"Login" in res.data