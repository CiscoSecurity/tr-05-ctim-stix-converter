from http import HTTPStatus
from unittest.mock import patch, MagicMock

BODY = {'content': 'content'}
RESULT = {'type': 'bundle'}


def test_submit_call_success(client, authorization):
    with patch('api.utils.ThreatResponse') as tr_mock:
        tr_client_mock = MagicMock()
        tr_client_mock.private_intel.bundle.import_.post = MagicMock(
            return_value=RESULT
        )
        tr_mock.return_value = tr_client_mock

        response = client.post(
            '/submit', headers=authorization(), json=BODY
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json == RESULT
        tr_client_mock.private_intel.bundle.import_.post.assert_called_with(
            BODY
        )
