from http import HTTPStatus
from unittest.mock import patch, MagicMock

from pytest import fixture
from requests import HTTPError
from threatresponse.exceptions import RegionError


def routes():
    yield '/translate'
    yield '/submit'


@fixture(scope='module', params=routes())
def route(request):
    return request.param


def test_call_no_authorization(route, client, error_response):
    response = client.post(
        route, headers={}, json={'content': 'content'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == error_response(
        'Bad Request: Missing credentials.', 'CredentialsNotSetError'
    )


def test_call_no_credentials(
        route, client, authorization, error_response
):
    response = client.post(
        route, headers=authorization(password=''), json={'content': 'content'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == error_response(
        'Bad Request: Missing credentials.', 'CredentialsNotSetError'
    )


def test_call_region_error(
        route, client, authorization,  error_response
):
    with patch('api.utils.ThreatResponse') as tr_mock:
        tr_mock.side_effect = RegionError()

        response = client.post(
            route, headers=authorization(), json={'content': 'content'}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == error_response(
            'Bad Request: Invalid region.', 'InvalidRegionError'
        )


def test_call_http_error(
        route, client, authorization, error_response
):
    with patch('api.utils.ThreatResponse') as tr_mock:
        tr_mock.side_effect = HTTPError(response=MagicMock(status_code=400))

        response = client.post(
            route, headers=authorization(), json={'content': 'content'}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == error_response(
            'Unexpected response from Cisco SecureX Threat Response: ',
            'TRError'
        )
