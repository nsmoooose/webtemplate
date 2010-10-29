"""
Specifies the database model to use for this application.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib

Base = declarative_base()

class ApplicationSettings(Base):
    """
    Settings for the application like the application name.
    """
    __tablename__ = "application_settings"
    application_id = Column("id", Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

class NewsArticle(Base):
    """
    A news article that can be displayed on the frontpage of the application.
    """

    __tablename__ = "newsarticle"
    articleid = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    text = Column("text", String)
    author = Column("author", String)

    def __init__(self, title, text, author):
        self.title = title
        self.text = text
        self.author = author

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
    """
    Object that handles the database.

    New database sessions are available through the `scoped_session`
    member.
    """

    def __init__(self):
        self._meta_data = Base.metadata
        self._engine = None
        self._session = None
        self._scoped_session = None

    def open(self, filename, echo=True):
        """
        Opens the database for this program. Creates the database if it doesnt
        exist yet. Also makes sure that there is an ApplicationSettings object
        present in the database.
        """

        self._engine = create_engine(filename, echo=echo)
        self._meta_data.create_all(self._engine)
        self._session = sessionmaker(
            bind=self._engine, autoflush=True, autocommit=False)
        self._scoped_session = scoped_session(self._session)

        # Make sure that there is a application settings object
        session = self.new_session()
        rows = session.query(ApplicationSettings).all()
        if len(rows) == 0:
            session.add(ApplicationSettings("Template application"))
        session.commit()

    def new_session(self):
        """
        Returns a new scoped session.
        """
        return self._scoped_session()
