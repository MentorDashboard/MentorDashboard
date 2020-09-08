from tests.utils import add_user


def test_user_can_login(test_app, test_db):
    add_user('Test User', 'user@test.com', 'test1234')

    client = test_app.test_client()
    res = client.post('/login', data=dict(
        email='user@test.com',
        password='test1234',
    ))

    assert res.status_code == 201
