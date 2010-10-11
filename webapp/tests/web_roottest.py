import cherrypy
import twill
import unittest
import webapp.web.root
from StringIO import StringIO

class RootTest(unittest.TestCase):
    def setUp(self):
        cherrypy.config.update({ "environment": "embedded" })
        wsgiApp = cherrypy.tree.mount(webapp.web.root.Root())
        cherrypy.server.start()
        twill.add_wsgi_intercept('localhost', 8080, lambda : wsgiApp)
        self.outp = StringIO()
        twill.set_output(self.outp)

    def tearDown(self):
        twill.remove_wsgi_intercept('localhost', 8080)
        cherrypy.server.stop()

    def testIndex(self):
        script = "find 'Start page'"
        twill.execute_string(script, initial_url='http://localhost:8080/')

    def testChangePasswordAndUnauthorizedAccess(self):
        # TODO dectect the redirect?
        # root = webapp.web.root.Root()
        # html = root.changepassword()
        # print(html)
        raise NotImplementedError

if __name__ == '__main__':
    unittest.main()
