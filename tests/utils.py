from src.models.User import create_user


def add_user(name='Test User', email='user@test.com', password='test1234'):
    return create_user(name, email, password)
