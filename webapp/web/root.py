import cherrypy
import genshi
import sqlalchemy
import sqlite3
import sys
import template
from users import Users
from auth import AuthController, require, member_of, name_is

class Root(object):
    def __init__(self):
        self.users = Users()
        self.users.expose = True

        self.auth = AuthController()
        self.auth.expose = True

    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        return template.render()

    @cherrypy.expose
    @require()
    @template.output('changepassword.html')
    def changepassword(self):
        return template.render()

    @cherrypy.expose
    @template.output('about.html')
    def about(self):
        versions = {
            "Python" : sys.version,
            "CherryPy" : cherrypy.__version__,
            "SQLAlchemy" : sqlalchemy.__version__,
            "FormEncode" : "Not exposed by package",
            "Genshi" : genshi.__version__,
            "sqlite" : sqlite3.version
            }
        return template.render(versions=versions)
