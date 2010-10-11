import cherrypy
import twill
import unittest
import webapp.web.db
import webapp.web.root
from StringIO import StringIO

class RootTest(unittest.TestCase):
    def setUp(self):
        webapp.web.db.open_database("sqlite://")
        cherrypy.config.update(
            {
                "environment": "embedded",
                "global" : {
                    "tools.auth.on" : True,
                    "tools.sessions.on" : True,
                    }
                })
        wsgiApp = cherrypy.tree.mount(webapp.web.root.Root())
        cherrypy.server.start()
        twill.add_wsgi_intercept('localhost', 8080, lambda : wsgiApp)
        self.outp = StringIO()
        twill.set_output(self.outp)

    def tearDown(self):
        twill.remove_wsgi_intercept('localhost', 8080)
        cherrypy.server.stop()

    def test_index(self):
        script = "find 'Start page'"
        twill.execute_string(script, initial_url='http://localhost:8080/')

    def test_about(self):
        script = "find 'About this application'"
        twill.execute_string(script, initial_url='http://localhost:8080/about')

    def test_change_password_and_unauthorized_access(self):
        script = "find 'Enter login information'"
        twill.execute_string(script, initial_url='http://localhost:8080/changepassword')

if __name__ == '__main__':
    unittest.main()
