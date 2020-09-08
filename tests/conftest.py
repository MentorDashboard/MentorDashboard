import pytest

from src import create_app
from config import Config


@pytest.fixture(scope='module')
def test_app():
    app = create_app(Config)
    with app.app_context():
        yield app
