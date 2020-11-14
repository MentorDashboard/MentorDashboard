import pytest

from app import create_app, db
from app.config import Config


class TestConfig(Config):
    FLASK_ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4


@pytest.fixture(scope="function")
def test_client():
    app = create_app(TestConfig)
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="function")
def test_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()
