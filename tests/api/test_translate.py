from http import HTTPStatus
from unittest.mock import patch, MagicMock

from pytest import mark

from api.exceptions import BundleBuilderError

ROUT = '/translate'
BODY = {'content': 'content'}


def test_translate_success(client, authorization):
    with patch('api.translator.translate') as translate_mock, \
            patch('api.utils.ThreatResponse') as tr_mock:
        translate_mock.return_value = MagicMock(json={'type': 'bundle'})
        tr_mock.return_value = MagicMock()

        response = client.post(ROUT, headers=authorization(), json=BODY)

        assert response.status_code == HTTPStatus.OK
        assert response.json == {'type': 'bundle'}


@mark.parametrize(
    'request_body, expected_message',
    (
            ({'content': 'content', 'indicator': {'title': ''}},
             {'indicator': {'title': ['Field may not be blank.']}}),
            ({'content': 'content', 'source': ''},
             {'source': ['Field may not be blank.']}),
            ({},
             {'content': ['Missing data for required field.']})

    ),
    ids=str
)
def test_translate_bad_request(
        client, authorization, request_body, expected_message, error_response
):
    response = client.post(ROUT, headers=authorization(), json=request_body)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == error_response(
        expected_message, 'InvalidArgumentError'
    )


def test_translate_bundle_builder_error(client, authorization, error_response):
    with patch('api.translator.translate') as translate_mock, \
            patch('api.utils.ThreatResponse') as tr_mock:
        translate_mock.side_effect = BundleBuilderError(Exception())
        tr_mock.return_value = MagicMock()

        response = client.post(ROUT, headers=authorization(), json=BODY)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json == error_response(
            'Error occurred while constructing bundle: ',
            'BundleBuilderError', HTTPStatus.UNPROCESSABLE_ENTITY
        )
