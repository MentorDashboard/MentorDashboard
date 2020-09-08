def test_user_can_register(test_app, test_db):
    client = test_app.test_client()
    res = client.post('/register', data=dict(
        name='Test User',
        email='user@test.com',
        password='test123',
        password_confirm='test123'
    ), follow_redirects=True)

    assert res.status_code == 201
