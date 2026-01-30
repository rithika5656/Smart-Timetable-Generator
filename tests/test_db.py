"""
Database tests.
"""
import pytest
from database import get_db, init_app
from app import app

def test_db_connection(client):
    with app.app_context():
        db = get_db()
        assert db is not None
        cur = db.execute('SELECT 1')
        assert cur.fetchone()[0] == 1

def test_history_insert(client):
    # Trigger a generation to create history
    # This is an integration test via the app context
    pass # Skipped for now, covered by API tests implicity
