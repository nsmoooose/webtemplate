import cherrypy
import genshi
import sqlalchemy
import sqlite3
import sys
import webapp.web.template as template
from webapp.web.users import Users
from webapp.web.auth import AuthController, require

class Root(object):
    """
    Serves the root (http://www.my_domain.org/) url.
    """

    def __init__(self):
        self.users = Users()
        self.users.expose = True

        self.auth = AuthController()
        self.auth.expose = True

    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        """The default page."""
        return template.render()

    @cherrypy.expose
    @require()
    @template.output('changepassword.html')
    def changepassword(self):
        return template.render()

    @cherrypy.expose
    @template.output('about.html')
    def about(self):
        """
        Present some information about what tools this application was developed with.
        """
        versions = {
            "Python" : sys.version,
            "CherryPy" : cherrypy.__version__,
            "SQLAlchemy" : sqlalchemy.__version__,
            "FormEncode" : "Not exposed by package",
            "Genshi" : genshi.__version__,
            "sqlite" : sqlite3.version
            }
        return template.render(versions=versions)
