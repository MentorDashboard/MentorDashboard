from tests.utils import login_user


def test_an_authenticated_user_can_view_the_dashboard(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    res = client.get("/dashboard")

    assert res.status_code == 200
    assert b"Dashboard" in res.data
