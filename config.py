"""Encapsulate the different configuration details in this module"""
import os

class Config(object):
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adau fagkfa821b 32bdc^!$@sad'

    @staticmethod
    def init_app(app):
        pass

class Production(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YT\x89\xc9\xed\x88K>}\t\x01\xf0\xe6\xc94\\\xde\x85\x96H\x11\x88\xe7\x8b'

class Testing(Config):
    TESTING = True
    DEBUG = True


config = {
    'development': Config,
    'testing': Testing,
    'production': Production,
    'default': Testing
}