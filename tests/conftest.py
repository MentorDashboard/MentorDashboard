import pytest

from app import create_app, db
from config import Config


class TestConfig(Config):
    FLASK_ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4


@pytest.fixture(scope="function")
def test_app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def test_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
