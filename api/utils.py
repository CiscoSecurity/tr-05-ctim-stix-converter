from flask import request
from requests import HTTPError
from threatresponse import ThreatResponse
from threatresponse.exceptions import RegionError

from api.constants import DEFAULT_REGION
from api.exceptions import (
    CredentialsNotSetError,
    InvalidRegionError,
    TRError,
    InvalidArgumentError
)


def get_json(schema):
    """
    Parse the incoming request's data as JSON.
    Validate and deserialize it with specified schema.
    """

    data = request.get_json(force=True, silent=True, cache=False)

    message = schema.validate(data)
    if message:
        raise InvalidArgumentError(message)

    return schema.load(data)


def get_tr_client(client, password, region=DEFAULT_REGION):
    try:
        assert client and password

        return ThreatResponse(
            client_id=client, client_password=password, region=region
        )

    except AssertionError as error:
        raise CredentialsNotSetError(error)

    except RegionError as error:
        raise InvalidRegionError(error)

    except (TimeoutError, ConnectionError, HTTPError) as error:
        raise TRError(error)
