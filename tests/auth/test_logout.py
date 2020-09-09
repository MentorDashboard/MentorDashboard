from flask_login import current_user

from tests.utils import login_user


def test_user_can_logout(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    res = client.get('/logout', follow_redirects=True)

    assert res.status_code == 200
    assert b"You have been logged out" in res.data
    assert not current_user


def test_guest_can_not_logout(test_app, test_db):
    client = test_app.test_client()

    res = client.get('/logout', follow_redirects=True)

    assert res.status_code == 200
    assert b"You have been logged out" not in res.data
