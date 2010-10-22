"""
Provides access to a shared database.
"""
import cherrypy
from webapp.api.model import Database

database = None

def open_database(filename):
    """
    Opens the database and sets the global database to use. Use the `get`
    function to obtain a new session.
    """
    global database
    database = Database()
    database.open(filename)

def close_database():
    database.close()

def get():
    """
    Returns a new database session.
    """
    if cherrypy.session.has_key("db"):
        return cherrypy.session["db"]

    def db_close_hook():
        del cherrypy.session["db"]

    s = database._scoped_session()
    cherrypy.session["db"] = s
    cherrypy.request.hooks.attach("on_end_request", db_close_hook)
    return s
