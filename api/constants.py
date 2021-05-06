from datetime import timedelta

DEFAULT_REGION = 'us'

DEFAULT_SOURCE_URI = (
    'https://github.com/CiscoSecurity/tr-05-ctim-stix-translator'
)
DEFAULT_SOURCE = 'CTIM-STIX Converter'
DEFAULT_EXTERNAL_ID_PREFIX = 'ctim-stix-converter'

DEFAULT_PRODUCER = DEFAULT_SOURCE
DEFAULT_TITLE = 'Generated with CTIM-STIX Converter'
DEFAULT_CONFIDENCE = 'High'
DEFAULT_INTERNAL = False
DEFAULT_COUNT = 1

INDICATOR_VALIDITY_INTERVAL = timedelta(30)
