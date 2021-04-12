from werkzeug.exceptions import BadRequest, UnprocessableEntity


class BaseTranslatorError(Exception):
    @property
    def json(self):
        return str(self)


class InvalidArgumentError(BaseTranslatorError, BadRequest):
    def __init__(self, error):
        super().__init__(error)


class CredentialsNotSetError(BaseTranslatorError, BadRequest):
    def __init__(self, *args):
        super().__init__(
            'Bad Request: Missing credentials.'
        )


class InvalidRegionError(BaseTranslatorError, BadRequest):
    def __init__(self, *args):
        super().__init__(
            'Bad Request: Invalid region.'
        )


class NoObservablesFoundError(BaseTranslatorError, UnprocessableEntity):
    def __init__(self):
        super().__init__('No observables found.')


class BundleBuilderError(BaseTranslatorError, UnprocessableEntity):
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
