from datetime import datetime

from bundlebuilder.models import (
    Sighting as CTIMSighting,
    ObservedTime as CTIMObservedTime
)

from mappings.primary_entity import PrimaryEntityMapping
from mappings.mapping_result import CTIMMappingResult
from utils import ctim_time_format


class Sighting(PrimaryEntityMapping):
    @classmethod
    def type(cls):
        return 'sighting'

    def map_to_ctim(self):
        input_ = self.stix_object
        created_by = self.bundle.find_by_ref(input_.get('created_by'))
        result = {
            'confidence': self._confidence(input_.get('confidence')),
            'count': input_.get('count') or 0,
            'observed_time': self.observed_time(input_),
            # 'data': '',
            'description': input_.get('description'),
            'external_ids': [
                *self.external_ids(input_.get('external_references')),
                input_['id']
            ],
            'external_references': input_.get('external_references'),
            # 'internal': '',
            'language': input_.get('lang'),
            # 'observables': '',
            # 'relations': '',
            # 'resolution': '',
            # 'revision': '',
            # 'sensor': '',
            # 'sensor_coordinates': '',
            # 'severity': '',
            # 'short_description': '',
            'source': created_by['name'] if created_by else 'Anonymous',
            # 'source_uri': '',
            # 'targets': '',
            'timestamp': (
                    input_.get('modified') or input_['created']
            ),
            # 'title': '',
            'tlp': self._tlp()
        }

        result = {k: v for k, v in result.items() if v is not None}

        return CTIMMappingResult(CTIMSighting(**result))

    @staticmethod
    def observed_time(input_):
        # ToDo validate what to do if not presented (required in CTIM)
        start_time = (
                input_.get('first_seen')
                or ctim_time_format(datetime.now())
        )

        end_time = input_.get('last_seen') or start_time

        return CTIMObservedTime(start_time=start_time, end_time=end_time)
