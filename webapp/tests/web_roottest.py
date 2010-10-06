import webapp.web.root
import unittest

class RootTest(unittest.TestCase):
    def testIndex(self):
        root = webapp.web.root.Root()
        html = root.index()
        raise NotImplementedError

    def testChangePasswordAndUnauthorizedAccess(self):
        # TODO dectect the redirect?
        root = webapp.web.root.Root()
        html = root.changepassword()
        print(html)
        self.assertTrue(html.find(""))
        raise NotImplementedError

if __name__ == '__main__':
    unittest.main()
