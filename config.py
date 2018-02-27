"""Encapsulate the different configuration details in this module"""
import os
database_base_uri = os.path.join(os.path.dirname(__file__), 'app', 'files', 'db')

class Config(object):
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adau fagkfa821b 32bdc^!$@sad'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class Production(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YT\x89\xc9\xed\x88K>}\t\x01\xf0\xe6\xc94\\\xde\x85\x96H\x11\x88\xe7\x8b'
    SQLALCHEMY_DATABASE_URI = ''

class Testing(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.path.join(database_base_uri, 'test.db')

class Heroku(Config):
    """Different settings for heroku deployable application"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': Config,
    'heroku': Heroku,
    'testing': Testing,
    'production': Production,
    'default': Testing
}