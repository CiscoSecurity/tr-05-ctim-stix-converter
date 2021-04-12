from flask import request
from requests.exceptions import HTTPError
from threatresponse import ThreatResponse
from threatresponse.exceptions import RegionError

from api.exceptions import (
    CredentialsNotSetError,
    InvalidRegionError,
    InvalidArgumentError, TRError
)


def get_json(schema=None):
    """
    Parse the incoming request's data as JSON.
    Validate and deserialize it with specified schema if specified.
    """

    data = request.get_json(force=True, silent=True, cache=False)

    if schema is None:
        return data

    message = schema.validate(data)
    if message:
        raise InvalidArgumentError(message)

    return schema.load(data)


def get_tr_client():
    try:
        client_id = request.authorization.username
        client_password = request.authorization.password
        assert client_id and client_password

        return ThreatResponse(
            client_id=client_id,
            client_password=client_password,
            region=request.args.get('region')
        )

    except AssertionError as error:
        raise CredentialsNotSetError(error)

    except RegionError as error:
        raise InvalidRegionError(error)

    except HTTPError as error:
        raise TRError(error)