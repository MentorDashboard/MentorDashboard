from tests.utils import add_user, add_admin, login_user


def test_admin_can_view_list_of_users(test_app, test_db):
    client = test_app.test_client()
    admin = add_admin("Test Admin", "admin@test.com", "test1234")
    user1 = add_user("Test User 1", "user1@test.com", "test1234")
    user2 = add_user("Test User 2", "user2@test.com", "test1234")
    login_user(client, "admin@test.com", "test1234")

    response = client.get("/users")
    result = response.data.decode()

    assert response.status_code == 200
    assert user1.name in result
    assert user2.email in result
    assert admin.name in result


def test_non_admin_cannot_view_list_of_users(test_app, test_db):
    client = test_app.test_client()
    user1 = add_user("Test User 1", "user1@test.com", "test1234")
    user2 = add_user("Test User 2", "user2@test.com", "test1234")
    login_user(client, "user1@test.com", "test1234")

    response = client.get("/users")
    result = response.data.decode()

    assert response.status_code == 403
    assert user1.name not in result
    assert user2.email not in result


def test_guest_cannot_view_list_of_users(test_app, test_db):
    client = test_app.test_client()
    user1 = add_user("Test User 1", "user1@test.com", "test1234")
    user2 = add_user("Test User 2", "user2@test.com", "test1234")

    response = client.get("/users")
    result = response.data.decode()

    assert response.status_code == 302
    assert user1.name not in result
    assert user2.email not in result
