from formencode import Schema, validators

class AddUserForm(Schema):
    login = validators.UnicodeString(not_empty=True)
    fullname = validators.UnicodeString(not_empty=True)
    password = validators.UnicodeString(not_empty=True)
    user_type = validators.UnicodeString(not_empty=True)
