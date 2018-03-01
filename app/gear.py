from .users import Users


class Gear(object):
    """Defines a basic toolbox that holds the Users class manipulation behaviours"""

    @staticmethod
    def register_user(data):
        """:parameters: email, user_name, name, password:
        :returns: True if successfully registered, False otherwise"""
        user = Users(data['name'], data['user_name'], data['email'], data['password'])
        user.insert_user
        return user

    @staticmethod
    def load_user_by_user_name(user_name):
        """:parameter: a string representing the username
        :returns the user object that is associated with the specified user_name"""
        return Users.query.filter_by(user_name = user_name).first()