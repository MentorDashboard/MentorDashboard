def test_index(test_app):
    client = test_app.test_client()
    res = client.get('/')

    assert res.status_code == 200
    assert b"MentorDashboard" in res.data
    assert b"New dashboard for Code Institute Mentors" in res.data
