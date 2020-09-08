from tests.utils import add_user, login_user


def test_an_authenticated_user_can_view_the_dashboard(test_app, test_db):
    client = test_app.test_client()
    add_user('Test User', 'user@test.com', 'test1234')
    login_user(client, 'user@test.com', 'test1234')

    res = client.get('/dashboard')

    assert res.status_code == 200
    assert b"Dashboard" in res.data
    assert b"Data Coming Soon" in res.data
