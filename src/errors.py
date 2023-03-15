from collections import namedtuple

from flask import jsonify


def handle_generic_error(e):
    return jsonify(code=str(e.code), error=str(e.description)), e.code


Handler = namedtuple("Handler", "code handler_function")

error_handlers = [
    Handler(400, handle_generic_error),
    Handler(401, handle_generic_error),
]
