from ..utils import login_user


def test_an_authenticated_user_can_view_the_dashboard(test_app, test_db):
    client = test_app.test_client()
    login_user(client)

    response = client.get("/dashboard")
    result = response.data.decode()

    assert response.status_code == 200
    assert "Dashboard" in result
