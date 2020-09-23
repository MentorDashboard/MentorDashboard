from ...utils import add_user, add_admin, login_user


def test_user_can_view_their_profile(test_app, test_db):
    client = test_app.test_client()
    user1 = add_user("Test User 1", "user1@test.com", "test1234")
    login_user(client, "user1@test.com", "test1234")

    response = client.get("/users/1")
    result = response.data.decode()

    assert response.status_code == 200
    assert user1.name in result
    assert user1.email in result


def test_admin_can_not_view_profile_if_user_does_not_exist(test_app, test_db):
    client = test_app.test_client()
    add_admin("Test Admin", "admin@test.com", "test1234")
    login_user(client, "admin@test.com", "test1234")

    response = client.get("/users/2")

    assert response.status_code == 404


def test_non_admin_can_not_view_another_users_profile(test_app, test_db):
    client = test_app.test_client()
    user1 = add_user("Test User 1", "user1@test.com", "test1234")
    user2 = add_user("Test User 2", "user2@test.com", "test1234")
    login_user(client, "user1@test.com", "test1234")

    response = client.get("/users/2")
    result = response.data.decode()

    assert response.status_code == 403
    assert user2.name not in result
    assert user2.email not in result


def test_admin_can_view_another_users_profile(test_app, test_db):
    client = test_app.test_client()
    user1 = add_user("Test User 1", "user1@test.com", "test1234")
    add_admin("Test Admin", "admin@test.com", "test1234")
    login_user(client, "admin@test.com", "test1234")

    response = client.get("/users/1")
    result = response.data.decode()

    assert response.status_code == 200
    assert user1.name in result
    assert user1.email in result
