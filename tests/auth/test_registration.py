from tests.utils import add_user


def test_user_can_register(test_app, test_db):
    client = test_app.test_client()

    response = client.post(
        "/register",
        data=dict(
            name="Test User",
            email="user@test.com",
            password="test1234",
            password_confirm="test1234",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code == 200
    assert "You have successfully registered. You can now login." in result


def test_user_can_not_register_with_a_duplicate_email(test_app, test_db):
    client = test_app.test_client()
    add_user("Test User", "user@test.com", "test1234")

    response = client.post(
        "/register",
        data=dict(
            name="Test User",
            email="user@test.com",
            password="test123",
            password_confirm="test123",
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert response.status_code == 400
    assert "A user already exists with that email address!" in result


def test_user_can_not_register_without_a_name(test_app, test_db):
    client = test_app.test_client()

    response = client.post(
        "/register",
        data=dict(
            email="user@test.com", password="test123", password_confirm="test123"
        ),
    )
    result = response.data.decode()

    assert "This field is required." in result


def test_user_can_not_register_without_an_email_address(test_app, test_db):
    client = test_app.test_client()

    response = client.post(
        "/register",
        data=dict(
            email="user@test.com", password="test123", password_confirm="test123"
        ),
        follow_redirects=True,
    )
    result = response.data.decode()

    assert "This field is required." in result
