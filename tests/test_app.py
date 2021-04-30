from collections import namedtuple
from http import HTTPStatus

from pytest import fixture

Call = namedtuple('Call', ('method', 'route', 'expected_status_code'))


def calls():
    yield Call('POST', '/post', HTTPStatus.NOT_FOUND)
    yield Call('GET', '/get', HTTPStatus.NOT_FOUND)
    yield Call('PUT', '/put', HTTPStatus.NOT_FOUND)
    yield Call('DELETE', '/delete', HTTPStatus.NOT_FOUND)

    yield Call('GET', '/translate', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('GET', '/submit', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('PUT', '/', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('PUT', '/translate', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('PUT', '/submit', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('PUT', '/authorize', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('DELETE', '/', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('DELETE', '/translate', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('DELETE', '/submit', HTTPStatus.METHOD_NOT_ALLOWED)
    yield Call('DELETE', '/authorize', HTTPStatus.METHOD_NOT_ALLOWED)


@fixture(scope='module',
         params=calls(),
         ids=lambda call: f'{call.method} {call.route}')
def call(request):
    return request.param


def test_non_defined_call_failure(call, client):
    response = client.open(call.route, method=call.method)
    assert response.status_code == call.expected_status_code
