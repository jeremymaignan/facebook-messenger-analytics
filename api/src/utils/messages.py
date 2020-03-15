from utils.logger import log

from flask import jsonify

def message(payload, code=200, namespace="core-api", no_log=False):
    if not no_log:
        log.info("{} - Returning message {} : {}".format(namespace, code, payload))
    return (jsonify(payload), code)

def not_found(item=""):
    return error('Not found : {}'.format(item), code=404)

def bad_request(e=""):
    return error('Bad request : {}'.format(repr(e)), code=400)

def success(message_str, code=200, namespace="core-api"):
    log.info("{} - Returning message {} : {}".format(namespace, code, message_str))
    return message({'success': message_str}, code=code)

def unauthorized(e=""):
    return error('Unauthorized : {}'.format(e), code=401)

def internal_error(message_str="", namespace="core-api"):
    log.info("{} - Returning message {} : {}".format(namespace, 500, message_str))
    return error('An internal error occurred : {}'.format(message_str))

def validation_error(exc, code=400):
    errors = [{'subject': k, 'errors': d} for k, d in exc.messages.items()]
    return error('Invalid request', errors, code=code)

def not_authorized_error(e, code=401):
    return error('Not authorized : {}'.format(e), code=code)

def error(message_str, details=None, code=500):
    payload = {'error': message_str}
    if details:
        payload['details'] = details

    log.error(payload)
    return message(payload, code)
