from tests.utils import login_user


def test_index(test_app):
    client = test_app.test_client()
    response = client.get("/")
    result = response.data.decode()

    assert response.status_code == 200
    assert "MentorDashboard" in result
    assert "New dashboard for Code Institute Mentors" in result


def test_logged_in_user_can_not_access_index(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    response = client.get("/")

    assert response.status_code == 302
