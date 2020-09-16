from tests.utils import login_user


def test_index(test_app):
    client = test_app.test_client()
    res = client.get("/")

    assert res.status_code == 200
    assert b"MentorDashboard" in res.data
    assert b"New dashboard for Code Institute Mentors" in res.data


def test_logged_in_user_can_not_access_index(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    res = client.get("/")

    assert res.status_code == 302
