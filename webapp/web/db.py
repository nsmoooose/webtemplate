import cherrypy
from webapp.api.model import Database
from sys import exc_info

database = None

def Get():
    return database.ScopedSession()

def OpenDatabase(filename):
    global database
    database = Database()
    database.Open(filename)
