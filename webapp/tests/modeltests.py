import webapp.api.model as model
import unittest

class UserTests(unittest.TestCase):
    def testThatConstructorWork(self):
        model.User("login", "admin", "my name", "password")
        model.User("login", "customer", "my name", "password")

    def testThatTypeIsCorrect(self):
        self.assertRaises(ValueError, model.User, "login", "type", "fullname", "password")

