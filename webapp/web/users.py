import cherrypy
import webapp.web.template as template
import webapp.web.db as db
from formencode import Invalid
from genshi.filters import HTMLFormFiller
from webapp.api.model import User
from webapp.web.auth import require, member_of
from webapp.web.form import AddUserForm

class Users(object):
    """
    User administration of the system.
    """

    @cherrypy.expose
    @require(member_of("admin"))
    @template.output('users.html')
    def list(self):
        """
        Lists all available users on the system.
        """
        session = db.get()
        users = session.query(User)
        return template.render(users=users)

    @cherrypy.expose
    @require(member_of("admin"))
    @template.output('adduser.html')
    def add(self, **data):
        """
        Create a new user.
        """
        errors = {}
        if cherrypy.request.method == 'POST':
            form = AddUserForm()
            try:
                data = form.to_python(data)
                session = db.get()
                user = User(**data)
                session.add(user)
                session.commit()
                raise cherrypy.HTTPRedirect('/users/user/%s' % data["login"])
            except Invalid, error:
                errors = error.unpack_errors()
                print errors

        return template.render(errors=errors) | HTMLFormFiller(data=data)

    def delete(self, id):
        pass
