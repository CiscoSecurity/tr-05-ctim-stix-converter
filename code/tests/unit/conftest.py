import base64
from http import HTTPStatus

from pytest import fixture

from app import app


@fixture(scope='session')
def client():
    app.testing = True

    with app.test_client() as client:
        yield client


@fixture(scope='session')
def authorization():
    def make_authorization(user='testuser', password='testpassword'):
        return {
            "Authorization":
                "Basic " +
                base64.b64encode(
                    bytes(f"{user}:{password}", "utf-8")
                ).decode("utf-8")
        }

    return make_authorization


@fixture(scope='session')
def error_response():
    def make_response(message, reason, status_code=HTTPStatus.BAD_REQUEST):
        return {
            'code': status_code,
            'message': message,
            'reason': 'api.exceptions.' + reason
        }

    return make_response
