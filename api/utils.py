from flask import request
from threatresponse import ThreatResponse
from threatresponse.exceptions import RegionError

from api.exceptions import (
    CredentialsNotSetError,
    InvalidRegionError,
    InvalidArgumentError
)


def get_json(schema=None):
    """
    Parse the incoming request's data as JSON.
    Validate and deserialize it with schema if specified.
    """

    data = request.get_json(force=True, silent=True, cache=False)

    if schema is None:
        return data

    message = schema.validate(data)
    if message:
        raise InvalidArgumentError(message)

    return schema.load(data)


def get_form_data(schema=None, data=None):
    """
    Parse the incoming request's data as JSON.
    Validate and deserialize it with schema if specified.
    """

    data = data or dict(request.form)

    if schema is None:
        return data

    message = schema.validate(data)
    if message:
        raise InvalidArgumentError(message)

    return schema.load(data)


def get_tr_client(session_=None):
    try:
        if session_:
            client_id = session_.get('client_id')
            client_password = session_.get('client_password')
            region = session_.get('region')
        else:
            assert request.authorization
            client_id = request.authorization.username
            client_password = request.authorization.password
            region = request.args.get('region')
            assert client_id and client_password

        return ThreatResponse(
            client_id=client_id,
            client_password=client_password,
            region=region
        )

    except AssertionError as error:
        raise CredentialsNotSetError(error)

    except RegionError as error:
        raise InvalidRegionError(error)
