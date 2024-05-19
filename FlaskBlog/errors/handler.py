from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(e):
    return render_template('errors/404_error.html'), 404
