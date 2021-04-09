class BaseTranslatorError(Exception):
    @property
    def json(self):
        return str(self)


class InvalidArgumentError(BaseTranslatorError):
    def __init__(self, error):
        super().__init__(error)


class NoObservablesFoundError(BaseTranslatorError):
    def __init__(self, file_name):
        super().__init__(f'No observables found in {file_name}')


class CredentialsNotSetError(BaseTranslatorError):
    def __init__(self, *args):
        super().__init__(
            'Authorization failed: Missing credentials.'
        )


class InvalidRegionError(BaseTranslatorError):
    def __init__(self, *args):
        super().__init__(
            'Authorization failed: Invalid region.'
        )


class FailedToReadFileError(BaseTranslatorError):
    def __init__(self, error):
        super().__init__(
            f'Failed to read file: {str(error)}'
        )


class BundleBuilderError(BaseTranslatorError):
    def __init__(self, error):
        super().__init__(f'Error occurred while constructing bundle: {error}')


class TRError(BaseTranslatorError):
    def __init__(self, error):
        message = ''
        if getattr(error, 'response') is not None:
            if self.is_authentication_error(error.response):
                message = (
                    'Make sure that your API credentials'
                    ' (CTR_CLIENT and CTR_PASSWORD) are valid.'
                )
            elif self.is_scope_missing(error.response):
                message = (
                    'Missing scope: inspect:read.'
                    ' Make sure that your API client'
                    ' has correct scope settings.'
                )

            message = message + str(error.response.text)

        super().__init__(
            'Unexpected response from Cisco SecureX Threat Response:'
            f' {message or str(error)}'
        )

    @staticmethod
    def is_authentication_error(response):
        return (
            response.status_code == 400
            and response.json().get('error') in (
                'invalid_client', 'wrong_client_creds'
            )
        )

    @staticmethod
    def is_scope_missing(response):
        return (
            response.status_code == 403
            and response.json().get("error") == "missing_scope"
        )
