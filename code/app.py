from flask import Flask, jsonify, request, flash, redirect, url_for
from requests import HTTPError

from api.exceptions import TRError
from api.submit import submit_api
from api.convert import convert_api
from api.ui import ui
from flask_bootstrap import Bootstrap5


app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.url_map.strict_slashes = False
app.config.from_object('config.Config')

app.register_blueprint(convert_api)
app.register_blueprint(submit_api)
app.register_blueprint(ui)


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

    if request.blueprint == 'ui':
        flash(message)
        return redirect(url_for(request.endpoint))

    response = jsonify(code=code, message=message, reason=reason)
    return response, code


if __name__ == '__main__':
    app.run()
