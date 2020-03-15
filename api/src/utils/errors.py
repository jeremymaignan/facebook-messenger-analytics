import peewee
from flask import request
from marshmallow.exceptions import ValidationError

from utils import messages
from utils.logger import log


def setup(app):
    app.register_error_handler(Exception, error_handler)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(404, not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(peewee.IntegrityError, bad_request)
    app.register_error_handler(peewee.DoesNotExist, bad_request)
    app.register_error_handler(peewee.OperationalError, db_access_error)
    app.register_error_handler(ValidationError, validation_error)

def error_handler(e):
    try:
        log.exception("An error occurred during a request. {} {} Err: {}".format(request.method, request.full_path, repr(e)))
        message = "{} {} Err: {}".format(request.method, request.full_path, repr(e))
    except:
        log.exception("An error occurred during a request: {}".format(repr(e)))
        message = repr(e)
    return messages.internal_error(message)

def db_access_error(e):
    log.exception('Peewee.OperationalError occurred during a request.')
    log.exception(e)
    return messages.message(repr(e), code=500)

def not_found(e):
    return messages.not_found(e)

def method_not_allowed(e):
    return messages.error("Method not allowed", code=405)

def bad_request(e):
    return messages.bad_request(e)

def unauthorized(e):
    return messages.unauthorized(e)

def validation_error(e):
    return messages.validation_error(e)
