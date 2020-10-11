from ..utils import login_user


def test_an_authenticated_user_can_view_the_dashboard(test_client, test_db):
    login_user(test_client)

    response = test_client.get("/dashboard")
    result = response.data.decode()

    assert response.status_code == 200
    assert "Dashboard" in result
