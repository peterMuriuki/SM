"""  declare the application factory (create_app method)"""
from flask import Flask
from config import config


def create_app(configuration_name):
    app = Flask(__name__)
    configuration_list = ['development', 'testing', 'production', 'default']
    if configuration_name not in configuration_list:
        raise ValueError('Unknown configuration argument')
    app.config.from_object(config[configuration_name])
    config[configuration_name].init_app(app)

    from .main.views import main
    app.register_blueprint(main)

    return app
