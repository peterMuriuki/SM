""" Launch Script"""
from flask_script import Manager, Shell
from app import create_app
import os


app = create_app(os.environ.get('CONFIGURATION') or 'default')
manager = Manager(app=app)


def make_shell_context():
    return dict(app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
