from tests.utils import add_user, login_user


def test_user_can_login(test_app, test_db):
    client = test_app.test_client()
    add_user('Test User', 'user@test.com', 'test1234')

    res = client.post('/login', data=dict(
        email='user@test.com',
        password='test1234',
    ), follow_redirects=True)

    assert res.status_code == 200
    assert b"You have been logged in" in res.data


def test_non_existent_user_can_not_login(test_app, test_db):
    client = test_app.test_client()

    res = client.post('/login', data=dict(
        email='user@test.com',
        password='test1234',
    ))

    assert res.status_code == 401


def test_user_can_not_login_with_incorrect_password(test_app, test_db):
    client = test_app.test_client()
    add_user('Test User', 'user@test.com', 'test1234')

    res = client.post('/login', data=dict(
        email='user@test.com',
        password='WRONG_PASSWORD',
    ))

    assert res.status_code == 401
    assert b"Invalid email address or password" in res.data


def test_user_can_not_login_without_email_address(test_app, test_db):
    client = test_app.test_client()

    res = client.post('/login', data=dict(
        password='WRONG_PASSWORD',
    ))

    assert b"This field is required." in res.data


def test_logged_in_user_can_not_access_login_page(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    res = client.get('/login')

    assert res.status_code == 302
