"""
Provides access to a shared database.
"""
from webapp.api.model import Database

database = None

def get():
    """
    Returns a new database session.
    """
    return database._scoped_session()

def open_database(filename):
    """
    Opens the database and sets the global database to use. Use the `get`
    function to obtain a new session.
    """
    global database
    database = Database()
    database.open(filename)
