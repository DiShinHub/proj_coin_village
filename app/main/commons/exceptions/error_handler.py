from flask import jsonify
from app.main.commons.exceptions.exceptions import *


def error_handler(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            'err_code': 9000001,
            'message': "internal server error {0}".format(e)
        }), 500

    @app.errorhandler(InternalServerException)
    @app.errorhandler(InvalidPermitException)
    @app.errorhandler(RequiredException)
    @app.errorhandler(DuplicateException)
    @app.errorhandler(InvalidValueException)
    @app.errorhandler(NotFoundSuccessException)
    @app.errorhandler(NotFoundException)
    @app.errorhandler(DateException)
    @app.errorhandler(RuleException)
    @app.errorhandler(AuthException)
    def handle_exception(e):
        return jsonify({
            'status': e.status,
            'message': e.message
        }), e.status_code
