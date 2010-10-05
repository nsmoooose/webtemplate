"""
This is a excellent page describing this module:
http://tools.cherrypy.org/wiki/AuthenticationAndAccessRestrictions
"""

import cherrypy
import urllib
import webapp.api.model as model
import webapp.web.db as db
import webapp.web.template as template

SESSION_KEY = '_cp_username'

def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure"""
    session = db.get()

    # This is a check that there always is an administrator
    # account. If the administrator is missing or has been
    # deleted it will be recreated here.
    admin = session.query(model.User).filter_by(login="admin").first()
    if admin is None:
        print("No admin account present in database. " +
              "Creating with default password")
        admin = model.User("admin", "admin", "Administrator", "password")
        session.add(admin)
        session.commit()

    user = session.query(model.User).filter_by(login=username).first()
    if user is None or user.verify_password(password) is False:
        return "Incorrect username or password."
    return None

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as alist of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    # format GET params
    get_params = urllib.quote(cherrypy.request.request_line.split()[1])
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true orfalse
                if not condition():
                    # Send old page as from_page parameter
                    raise cherrypy.HTTPRedirect(
                        "/auth/login?from_page=%s" % get_params)
        else:
            # Send old page as from_page parameter
            raise cherrypy.HTTPRedirect("/auth/login?from_page=%s" %get_params)


cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(func):
        if not hasattr(func, '_cp_config'):
            func._cp_config = dict()
        if 'auth.require' not in func._cp_config:
            func._cp_config['auth.require'] = []
        func._cp_config['auth.require'].extend(conditions)
        return func
    return decorate

def member_of(groupname):
    """
    Returns a callable object that checks if the current user is member of the
    specified user group.
    """
    def check():
        # We don't have user groups currently. Only
        # type of users. But a type is almost the same
        # thing.
        session = db.get()
        user = session.query(model.User).filter_by(
            login=cherrypy.request.login).first()
        if user is None:
            return False
        return groupname == user.user_type

    return check

def name_is(reqd_username):
    """
    Condition that returns true if current user is the same as reqd_username.
    The return value is a callable object.
    """
    return lambda: reqd_username == cherrypy.request.login

def any_of(*conditions):
    """
    Returns True if any of the conditions match. All conditions must be callable
    objects.
    """
    def check():
        for condition in conditions:
            if condition():
                return True
        return False
    return check

def all_of(*conditions):
    """
    Returns True if all of the conditions match. All conditions must be callable
    objects.
    """
    def check():
        for condition in conditions:
            if not condition():
                return False
        return True
    return check

class AuthController(object):
    """Controller to provide login and logout actions"""

    def on_login(self, username):
        """Called on successful login"""

    def on_logout(self, username):
        """Called on logout"""

    def get_loginform(
        self, username, msg="Enter login information", from_page="/"):
        return {
            "from_page" :from_page,
            "msg" : msg,
            "username" : username
            }

    @cherrypy.expose
    @template.output("login.html")
    def login(self, username=None, password=None, from_page="/"):
        """Login page where you can enter username and password."""

        if username is None or password is None:
            return template.render(
                **self.get_loginform("", from_page=from_page))

        error_msg = check_credentials(username, password)
        if error_msg:
            return template.render(
                **self.get_loginform(username, error_msg, from_page))
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    def logout(self, from_page="/"):
        """
        Logout page that will terminate your session and redirect you
        to the index page unless set.
        """
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")
