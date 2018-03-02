from .users import Users


class Gear(object):
    """Defines a basic toolbox that holds the Users class manipulation behaviours"""

    @staticmethod
    def register_user(data):
        """:parameters: email, user_name, name, password:
        :returns: True if successfully registered, False otherwise"""
        user = Users(data['name'], data['user_name'], data['email'], data['password'])
        user.insert_user()
        this = Gear.load_user_by_user_name(user.user_name)
        return this

    @staticmethod
    def load_user_by_user_name(user_name):
        """:parameter: a string representing the username
        :returns the user object that is associated with the specified user_name"""
        return Users.query.filter_by(user_name = user_name).first()
    
    @staticmethod
    def modify_user_data(user_obj, email=None, password=None, plan=None):
        """:params: any changeable attribute of a user instance i.e. email, password, plan,"""
        if password is not None:
            user_obj.update_password(password)
        if email is not None:
            user_obj.update_email(email)
        if plan is not None:
            user_obj.update_plan(plan)
        return user_obj