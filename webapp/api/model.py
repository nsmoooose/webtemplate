"""
Specifies the database model to use for this application.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib

Base = declarative_base()

class User(Base):
    """
    A single user that can log in to the system. Object provides password
    verification.
    """

    __tablename__ = "users"
    userid = Column("id", Integer, primary_key=True)
    login = Column("login", String, unique=True)
    user_type = Column("type", String)
    fullname = Column("fullname", String)
    password = Column("password", String)

    user_types = ["admin", "customer"]

    def __init__(self, login, user_type, fullname, password):
        if not user_type in self.user_types:
            raise ValueError, "Incorrect user type: %s" % user_type
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
        self.meta_data = Base.metadata
        self.engine = None
        self.session = None
        self.scoped_session = None

    def open(self, filename, echo=True):
        """Opens the sqlite database for this program. Creates the
        database if it doesn exist yet.
        Returns a sessionmaker for easy session access."""

        self.engine = create_engine(filename, echo=echo)
        self.meta_data.create_all(self.engine)
        self.session = sessionmaker(
            bind=self.engine, autoflush=True, autocommit=False)
        self.scoped_session = scoped_session(self.session)
