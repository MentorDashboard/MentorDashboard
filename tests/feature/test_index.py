from ..utils import login_user


def test_index(test_client):
    response = test_client.get("/")
    result = response.data.decode()

    assert response.status_code == 200
    assert "MentorDashboard" in result
    assert "New dashboard for Code Institute Mentors" in result


def test_logged_in_user_can_not_access_index(test_client, test_db):
    login_user(test_client)

    response = test_client.get("/")

    assert response.status_code == 302
