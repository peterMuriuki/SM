from .views import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found(e):
    """http error code 404: Page not found"""
    return render_template('error/404.html')


@main.app_errorhandler(500)
def internal_server_error(e):
    """http error code 500: Internal Server Error"""
    return render_template('error/500.html')