from datetime import timedelta

DEFAULT_REGION = 'us'

DEFAULT_SOURCE = 'CTIM-STIX Translator'
DEFAULT_SOURCE_URI = (
    'https://github.com/CiscoSecurity/tr-05-ctim-stix-translator'
)
DEFAULT_EXTERNAL_ID_PREFIX = 'ctim-stix-translator'

DEFAULT_TITLE = 'Generated with CTIM-STIX Translator'
DEFAULT_CONFIDENCE = 'High'

SIGHTING_DEFAULTS = {
    'confidence': DEFAULT_CONFIDENCE,
    'count': 1,
    'title': DEFAULT_TITLE,
    'internal': False
}

INDICATOR_DEFAULTS = {
    'producer': DEFAULT_SOURCE,
    'confidence': DEFAULT_CONFIDENCE,
    'title': DEFAULT_TITLE
}
INDICATOR_VALIDITY_INTERVAL = timedelta(30)

NON_CUSTOMIZABLE_FIELDS = ('observed_time', 'observables', 'valid_time')
