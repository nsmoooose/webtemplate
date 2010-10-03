from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, scoped_session, sessionmaker
import sha

class User(object):
    def __init__(self, login, type, fullname, password):
        self.type = type
        self.login = login
        self.fullname = fullname

        # Create a sha hash of the password to improve
        # security. We don't want to store any passwords
        # in clear text.
        self.password = sha.new(password).hexdigest()

    def VerifyPassword(self, password):
        """Returns true if password is correct. If the password
        is incorrect we simply return false."""
        return sha.new(password).hexdigest() == self.password

class Database(object):
    MetaData = None
    Engine = None
    Session = None
    ScopedSession = None
    
    def __init__(self):
        self.MetaData = MetaData()

        users_table = Table("users", self.MetaData, 
                            Column("id", Integer, primary_key=True),
                            Column("login", String, unique=True),
                            Column("type", String),
                            Column("fullname", String),
                            Column("password", String))
        mapper(User, users_table)

    def Open(self, filename):
        """Opens the sqlite database for this program. Creates the
        database if it doesn exist yet. 
        Returns a sessionmaker for easy session access."""
        
        self.Engine = create_engine("sqlite:///%s" % filename, echo=True)
        self.MetaData.create_all(self.Engine)
        self.Session = sessionmaker(bind=self.Engine, autoflush=True, autocommit=False)
        self.ScopedSession = scoped_session(self.Session)
