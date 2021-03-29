import os
from unittest.mock import patch

from pytest import raises, mark
from requests.exceptions import (
    ConnectionError,
    Timeout as TimeoutError,
    HTTPError
)
from threatresponse.exceptions import RegionError

from exceptions import (
    TRError,
    CredentialsNotSetError,
    InvalidRegionError
)
from translator import get_tr_client, DEFAULT_REGION

CTR_CLIENT = 'CTR_CLIENT'
CTR_PASSWORD = 'CTR_PASSWORD'
CTR_REGION = 'CTR_REGION'


@patch.dict(
    os.environ,
    {
        CTR_CLIENT: CTR_CLIENT, CTR_PASSWORD: CTR_PASSWORD,
        CTR_REGION: CTR_REGION
    }
)
def test_get_tr_client():
    with patch('translator.ThreatResponse') as tr_mock:
        get_tr_client()

        tr_mock.assert_called_with(
            client_id=CTR_CLIENT, client_password=CTR_PASSWORD,
            region=CTR_REGION
        )


@patch.dict(os.environ, {})
def test_get_tr_client_no_credentials_set():
    with raises(CredentialsNotSetError):
        get_tr_client()


@patch.dict(
    os.environ,
    {CTR_CLIENT: CTR_CLIENT, CTR_PASSWORD: CTR_PASSWORD, CTR_REGION: 'wrong'}
)
def test_get_tr_client_invalid_region():
    with patch('translator.ThreatResponse') as tr_mock:
        tr_mock.side_effect = RegionError()

        with raises(InvalidRegionError):
            get_tr_client()

        tr_mock.assert_called_with(
            client_id=CTR_CLIENT, client_password=CTR_PASSWORD,
            region='wrong'
        )


@patch.dict(
    os.environ, {CTR_CLIENT: CTR_CLIENT, CTR_PASSWORD: CTR_PASSWORD}
)
@mark.parametrize(
    'error', (TimeoutError, ConnectionError, HTTPError), ids=str(),
)
def test_get_tr_client_tr_communication_failed(error):
    with patch('translator.ThreatResponse') as tr_mock:
        tr_mock.side_effect = error()

        with raises(TRError):
            get_tr_client()

        tr_mock.assert_called_with(
            client_id=CTR_CLIENT, client_password=CTR_PASSWORD,
            region=DEFAULT_REGION
        )
