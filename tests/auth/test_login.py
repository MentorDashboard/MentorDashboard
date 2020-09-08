from tests.utils import add_user


def test_user_can_login(test_app, test_db):
    add_user('Test User', 'user@test.com', 'test1234')

    client = test_app.test_client()
    res = client.post('/login', data=dict(
        email='user@test.com',
        password='test1234',
    ))

    assert res.status_code == 201


def non_existent_user_can_not_login(test_app, test_db):
    client = test_app.test_client()
    res = client.post('/login', data=dict(
        email='user@test.com',
        password='test1234',
    ))

    assert res.status_code == 401


def user_can_not_login_with_incorrect_password(test_app, test_db):
    add_user('Test User', 'user@test.com', 'test1234')

    client = test_app.test_client()
    res = client.post('/login', data=dict(
        email='user@test.com',
        password='WRONG_PASSWORD',
    ))

    assert res.status_code == 201