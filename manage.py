""" Launch Script"""
from flask_script import Manager, Shell, Server
from app import create_app
import os
from app.users import Users
from app import db


app = create_app(os.environ.get('CONFIGURATION') or 'default')
manager = Manager(app=app)


def make_shell_context():
    return dict(app=app, Users=Users)


# manager.add_command('runserver', Server(host='0.0.0.0', port='9000')) use when developing on codeanywhere
manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def deploy():
    """Define all the deploy operations once and in a encapsulated manner """
    # create the tables
    db.drop_all()
    db.create_all()

    if os.environ['CONFIGURATION'] == 'production' or os.environ['CONFIGURATION'] == 'heroku':
        Users.insert_admin() # will wok for all application configurations
    else:
        Users.insert_test_admin()

if __name__ == '__main__':
    manager.run()
