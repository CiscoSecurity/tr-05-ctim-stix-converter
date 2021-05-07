from werkzeug.exceptions import BadRequest, UnprocessableEntity


class InvalidArgumentError(BadRequest):
    def __init__(self, error):
        super().__init__(error)


class CredentialsNotSetError(BadRequest):
    def __init__(self, *args):
        super().__init__(
            'Bad Request: Missing credentials.'
        )


class InvalidRegionError(BadRequest):
    def __init__(self, *args):
        super().__init__(
            'Bad Request: Invalid region.'
        )


class NoObservablesFoundError(UnprocessableEntity):
    def __init__(self):
        super().__init__('No observables found.')


class BundleBuilderError(UnprocessableEntity):
    def __init__(self, error):
        super().__init__(f'Error occurred while constructing bundle: {error}')


class TRError(Exception):
    def __init__(self, error):
        if getattr(error, 'response') is not None:
            self.code = error.response.status_code
        self.description = (
            'Unexpected response from Cisco SecureX Threat Response:'
            f' {str(error)}'
        )
