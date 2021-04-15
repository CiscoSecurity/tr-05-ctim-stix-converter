from flask import Flask, jsonify
from requests import HTTPError

from api.exceptions import TRError
from api.submit import submit_api
from api.translate import translate_api

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config.from_object('config.Config')

app.register_blueprint(translate_api)
app.register_blueprint(submit_api)


@app.errorhandler(HTTPError)
def handle_http_error(exception):
    app.logger.error(exception)
    return handle_error(TRError(exception))


@app.errorhandler(Exception)
def handle_error(exception):
    app.logger.error(exception)
    code = getattr(exception, 'code', 500)
    message = getattr(exception, 'description', str(exception))
    reason = '.'.join([
        exception.__class__.__module__,
        exception.__class__.__name__,
    ])

    response = jsonify(code=code, message=message, reason=reason)
    return response, code


if __name__ == '__main__':
    app.run()
