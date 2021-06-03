from abc import ABC, abstractmethod
from typing import Any, Dict

JSON = Dict[str, Any]

CTIM_DEFAULTS = {
    'schema_version': '1.1.6',
}


class Mapping(ABC):

    @classmethod
    @abstractmethod
    def map(cls, *args, **kwargs) -> JSON:
        pass


class Indicator(Mapping):
    DEFAULTS = {
        'type': 'indicator',
        **CTIM_DEFAULTS
    }

    @classmethod
    def map(cls, indicator_data) -> JSON:
        indicator: JSON = cls.DEFAULTS.copy()

        indicator['id'] = indicator_data['id']

        indicator['valid_time'] = {
            'start_time': indicator_data['start_time'],
        }

        indicator['producer'] = indicator_data['producer']

        indicator['description'] = indicator_data['description']

        indicator['title'] = indicator_data['title']

        indicator['confidence'] = indicator_data['confidence']

        indicator['indicator_type'] = indicator_data['indicator_type']

        return indicator
