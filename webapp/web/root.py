"""
Serves the web server root pages.
"""

import cherrypy
import coverage
import genshi
import gettext
import nose
import os.path
import sphinx
import sqlalchemy
import sqlite3
import sys
import twill
import webapp.api.model as model
import webapp.web.db as db
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
        session = db.get()
        articles = session.query(model.NewsArticle)
        return template.render(articles=articles)

    @cherrypy.expose
    def set_language(self, language):
        locale_dir = os.path.join(os.path.dirname(__file__), "localedir")
        domain = "messages"
        codeset = "utf-8"
        gettext.bindtextdomain(domain, locale_dir)
        gettext.textdomain(domain)
        raise cherrypy.HTTPRedirect('/')

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
            "Nose" : nose.__version__,
            "sqlite" : sqlite3.version,
            "Sphinx" : sphinx.__version__,
            "Twill" : twill.__version__,
            "Coverage" : coverage.__version__
            }
        return template.render(versions=versions)
