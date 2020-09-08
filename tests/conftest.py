import pytest

from src import create_app
from config import Config


class TestConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True


@pytest.fixture(scope='module')
def test_app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app
