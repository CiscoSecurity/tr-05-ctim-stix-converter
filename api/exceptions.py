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
            'Authorization failed: Missing credentials.'
        )


class InvalidRegionError(BaseTranslatorError, BadRequest):
    def __init__(self, *args):
        super().__init__(
            'Authorization failed: Invalid region.'
        )


class NoObservablesFoundError(BaseTranslatorError, UnprocessableEntity):
    def __init__(self, file_name):
        super().__init__(f'No observables found in {file_name}')


# ToDo deprecate
class FailedToReadFileError(BaseTranslatorError, UnprocessableEntity):
    def __init__(self, error):
        super().__init__(
            f'Failed to read file: {str(error)}'
        )


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
