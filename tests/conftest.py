
import pytest
from app import app
from database import get_db, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

@pytest.fixture
def runner():
    return app.test_cli_runner()
