import webapp.api.model as model
import unittest

class UserTests(unittest.TestCase):
    def testThatConstructorWork(self):
        model.User("login", "admin", "my name", "password")
        model.User("login", "customer", "my name", "password")

    def testThatTypeIsCorrect(self):
        self.assertRaises(
            ValueError, model.User, "login", "type", "fullname", "password")


class DatabaseTests(unittest.TestCase):
    def testInMemoryDatabase(self):
        db = model.Database()
        db.open("sqlite://")

        session = db.scoped_session()
        user = model.User("henrikn", "admin", "Henrik Nilsson", "password")
        session.add(user)
        session.commit()

if __name__ == '__main__':
    unittest.main()
