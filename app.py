from flask import Flask, jsonify

from api.exceptions import BaseTranslatorError
from api.translate import translate_api

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config.from_object('config.Config')

app.register_blueprint(translate_api)


@app.errorhandler(BaseTranslatorError)
def handle_translator_error(error):
    app.logger.error(error.json)
    return error.json


@app.errorhandler(Exception)
def handle_error(exception):
    app.logger.error(exception)
    code = getattr(exception, 'code', 500)
    message = getattr(exception, 'description', 'Something went wrong.')
    reason = '.'.join([
        exception.__class__.__module__,
        exception.__class__.__name__,
    ])

    response = jsonify(code=code, message=message, reason=reason)
    return response, code


if __name__ == '__main__':
    app.run()
