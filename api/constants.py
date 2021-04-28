from datetime import timedelta

DEFAULT_REGION = 'us'

DEFAULT_SOURCE_URI = (
    'https://github.com/CiscoSecurity/tr-05-ctim-stix-translator'
)
DEFAULT_SOURCE = 'CTIM-STIX Translator'
DEFAULT_EXTERNAL_ID_PREFIX = 'ctim-stix-translator'

DEFAULT_PRODUCER = DEFAULT_SOURCE
DEFAULT_TITLE = 'Generated with CTIM-STIX Translator'
DEFAULT_CONFIDENCE = 'High'

INDICATOR_VALIDITY_INTERVAL = timedelta(30)
