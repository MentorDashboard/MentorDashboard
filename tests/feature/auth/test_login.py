from ...utils import add_user, login_user


def test_user_can_login(test_client, test_db):
    add_user("Test User", "user@test.com", "test1234")

    response = test_client.post(
        "/login",
        data=dict(
            email="user@test.com",
            password="test1234",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code == 200
    assert "You have been logged in" in result


def test_non_existent_user_can_not_login(test_client, test_db):
    response = test_client.post(
        "/login",
        data=dict(
            email="user@test.com",
            password="test1234",
        ),
    )
    result = response.data.decode()

    assert response.status_code == 401
    assert "Invalid email address or password" in result


def test_user_can_not_login_with_incorrect_password(test_client, test_db):
    add_user("Test User", "user@test.com", "test1234")

    response = test_client.post(
        "/login",
        data=dict(
            email="user@test.com",
            password="WRONG_PASSWORD",
        ),
    )
    result = response.data.decode()

    assert response.status_code == 401
    assert "Invalid email address or password" in result


def test_user_can_not_login_without_email_address(test_client, test_db):
    response = test_client.post(
        "/login",
        data=dict(
            password="WRONG_PASSWORD",
        ),
    )
    result = response.data.decode()

    assert "This field is required." in result


def test_logged_in_user_can_not_access_login_page(test_client, test_db):
    login_user(test_client)

    response = test_client.get("/login")

    assert response.status_code == 302
