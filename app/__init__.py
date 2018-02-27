"""  declare the application factory (create_app method)"""
from flask import Flask
from config import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
db = SQLAlchemy()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(configuration_name):
    app = Flask(__name__)
    configuration_list = ['development', 'testing', 'production', 'default']
    if configuration_name not in configuration_list:
        raise ValueError('Unknown configuration argument')
    app.config.from_object(config[configuration_name])
    config[configuration_name].init_app(app)

    login_manager.init_app()
    db.init_app()

    from .main.views import main
    app.register_blueprint(main)
    from .auth.views import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
