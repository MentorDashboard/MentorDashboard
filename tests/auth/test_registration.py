from tests.utils import add_user


def test_user_can_register(test_app, test_db):
    client = test_app.test_client()
    res = client.post('/register', data=dict(
        name='Test User',
        email='user@test.com',
        password='test1234',
        password_confirm='test1234'
    ), follow_redirects=True)

    assert res.status_code == 201


def test_user_can_not_register_with_a_duplicate_email(test_app, test_db):
    add_user('Test User', 'user@test.com', 'test1234')

    client = test_app.test_client()
    res = client.post('/register', data=dict(
        name='Test User',
        email='user@test.com',
        password='test123',
        password_confirm='test123'
    ), follow_redirects=True)

    assert res.status_code == 400
    assert b"A user already exists with that email address!" in res.data


def test_user_can_not_register_without_a_name(test_app, test_db):
    client = test_app.test_client()
    res = client.post('/register', data=dict(
        email='user@test.com',
        password='test123',
        password_confirm='test123'
    ))

    assert b"This field is required." in res.data


def test_user_can_not_register_without_an_email_address(test_app, test_db):
    client = test_app.test_client()
    res = client.post('/register', data=dict(
        email='user@test.com',
        password='test123',
        password_confirm='test123'
    ), follow_redirects=True)

    assert b"This field is required." in res.data
