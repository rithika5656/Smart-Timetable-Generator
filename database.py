"""
Database connection manager.
"""
import sqlite3
from flask import g

DATABASE = 'scheduler.db'

def get_db():
    """Get the current database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    """Close the database connection at end of request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """Execute a query and return results."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_app(app):
    """Register database teardown context."""
    app.teardown_appcontext(close_connection)
