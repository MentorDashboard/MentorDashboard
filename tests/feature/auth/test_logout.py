from flask_login import current_user

from ...utils import login_user


def test_user_can_logout(test_client, test_db):
    login_user(test_client)

    response = test_client.get("/logout", follow_redirects=True)
    result = response.data.decode()

    assert response.status_code == 200
    assert "You have been logged out" in result


def test_guest_can_not_logout(test_client, test_db):
    response = test_client.get("/logout", follow_redirects=True)
    result = response.data.decode()

    assert response.status_code == 200
    assert "You have been logged out" not in result
