from src.models.User import create_user


def add_user(name='Test User', email='user@test.com', password='test1234'):
    return create_user(name, email, password)


def login_user(client, email, password):
    return client.post(
        '/login',
        data=dict(email=email, password=password)
    )
