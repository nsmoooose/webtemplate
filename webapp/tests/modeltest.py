import webapp.api.model as model
import unittest

class UserTests(unittest.TestCase):
    def testThatConstructorWork(self):
        usera = model.User("login", "admin", "my name", "password")
        self.assertEqual(usera.login, "login")
        self.assertEqual(usera.user_type, "admin")
        self.assertEqual(usera.fullname, "my name")
        self.assertTrue(usera.password != "password")

        model.User("login", "customer", "my name", "password")

    def testThatTypeIsCorrect(self):
        self.assertRaises(
            ValueError, model.User, "login", "type", "fullname", "password")

    def testPasswordVerification(self):
        user = model.User("login", "admin", "my name", "password")
        self.assertTrue(user.verify_password("password"))
        self.assertFalse(user.verify_password("Password"))

class DatabaseTests(unittest.TestCase):
    def testInMemoryDatabase(self):
        db = model.Database()
        db.open("sqlite://")

        session = db.new_session()
        user = model.User("henrikn", "admin", "Henrik Nilsson", "password")
        session.add(user)
        session.commit()

    def testCreateANewSession(self):
        db = model.Database()
        db.open("sqlite://")

        session = db.new_session()
        self.assertFalse(session is None)

if __name__ == '__main__':
    unittest.main()
