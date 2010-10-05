"""
Specifies the database model to use for this application.
"""

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, scoped_session, sessionmaker
import hashlib

class User(object):
    """
    A single user that can log in to the system. Object provides password
    verification.
    """

    def __init__(self, login, user_type, fullname, password):
        self.user_type = user_type
        self.login = login
        self.fullname = fullname
        self.password = hashlib.md5(password).hexdigest()

    def verify_password(self, password):
        """Returns true if password is correct. If the password
        is incorrect we simply return false."""
        return hashlib.md5(password).hexdigest() == self.password

class Database(object):
    def __init__(self):
        self.meta_data = MetaData()

        users_table = Table("users", self.meta_data,
                            Column("id", Integer, primary_key=True),
                            Column("login", String, unique=True),
                            Column("user_type", String),
                            Column("fullname", String),
                            Column("password", String))
        mapper(User, users_table)

    def open(self, filename):
        """Opens the sqlite database for this program. Creates the
        database if it doesn exist yet.
        Returns a sessionmaker for easy session access."""

        self.engine = create_engine("sqlite:///%s" % filename, echo=True)
        self.meta_data.create_all(self.engine)
        self.session = sessionmaker(
            bind=self.engine, autoflush=True, autocommit=False)
        self.scoped_session = scoped_session(self.session)
