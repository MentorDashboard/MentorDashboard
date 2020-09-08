from flask_login import current_user

from tests.utils import add_user, login_user


def test_user_can_logout(test_app, test_db):
    client = test_app.test_client()
    add_user('Test User', 'user@test.com', 'test1234')
    login_user(client, 'user@test.com', 'test1234')

    res = client.get('/logout', follow_redirects=True)

    assert res.status_code == 200
    assert b"You have been logged out" in res.data
    assert not current_user


def test_guest_can_not_logout(test_app, test_db):
    client = test_app.test_client()

    res = client.get('/logout', follow_redirects=True)

    assert res.status_code == 200
    assert b"You have been logged out" not in res.data
