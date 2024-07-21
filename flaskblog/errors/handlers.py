from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)




@errors.app_errorhandler(404)     # handling the 404, basically creating a custom route for the specified error
def error_404(error):
    return render_template('errors/404.html'), 404      # creating errors subdirectory in templates folder


@errors.app_errorhandler(403)     # handling the 403, basically creating a custom route for the specified error
def error_403(error):
    return render_template('errors/403.html'), 403      # creating errors subdirectory in templates folder


@errors.app_errorhandler(500)     # handling the 500, basically creating a custom route for the specified error
def error_500(error):
    return render_template('errors/500.html'), 500      # creating errors subdirectory in templates folder