from flask_login import current_user

from tests.utils import login_user


def test_user_can_logout(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    response = client.get("/logout", follow_redirects=True)
    result = response.data.decode()

    assert response.status_code == 200
    assert "You have been logged out" in result
    assert not current_user


def test_guest_can_not_logout(test_app, test_db):
    client = test_app.test_client()

    response = client.get("/logout", follow_redirects=True)
    result = response.data.decode()

    assert response.status_code == 200
    assert "You have been logged out" not in result
