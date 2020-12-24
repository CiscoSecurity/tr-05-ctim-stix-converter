from bundlebuilder.models.primary import Indicator as CTIMIndicator
from bundlebuilder.models.secondary import (
    ValidTime as CTIMValidTime, KillChainPhase as CTIMKillChainPhase
)

from constants import INDICATOR_LABEL_MAP
from mappings.mapping_result import CTIMMappingResult
from mappings.primary_entity import PrimaryEntityMapping


class Indicator(PrimaryEntityMapping):
    @classmethod
    def type(cls):
        return 'indicator'

    def map_to_ctim(self):
        input_ = self.stix_object
        created_by = self.bundle.find_by_ref(input_.get('created_by'))

        result = {
            'producer': created_by['name'] if created_by else 'Anonymous',
            'valid_time': self._valid_time(input_),
            # 'composite_indicator_expression': '',
            'confidence': self._confidence(input_.get('confidence')),
            'description': input_.get('description'),
            'external_ids': [
                *self.external_ids(input_.get('external_references')),
                input_['id']
            ],
            'external_references': input_.get('external_references'),
            'indicator_type':
                self._indicator_type(input_.get('indicator_types')),
            'kill_chain_phases': [CTIMKillChainPhase(**kchf) for kchf in
                                  input_.get('kill_chain_phases', [])],
            'language': input_.get('lang'),
            # 'likely_impact': '',
            # 'negate': '',
            # 'revision': '',
            # 'severity': '',
            # 'short_description': '',
            'source': 'STIX',  # ToDo verify
            # 'source_uri': '',
            # 'specification': '',
            'tags': input_.get('labels'),
            # 'test_mechanisms': '',
            'timestamp': (
                    input_.get('modified') or input_['created']
            ),
            'title': input_.get('name'),
            'tlp': self._tlp()
        }

        result = {k: v for k, v in result.items() if v is not None}

        return CTIMMappingResult(CTIMIndicator(**result))

    @staticmethod
    def _indicator_type(stix_value):
        if not stix_value:
            return []

        # ToDo: Indicator_type vocab in STIX is open while
        #  CTIM is not - filter/ignore/add warnings??
        indicator_types = []

        for v in stix_value:
            mapped_type = INDICATOR_LABEL_MAP.get(v)
            if mapped_type:
                indicator_types.append(mapped_type)
            else:
                pass  # ToDo: add warning
        return indicator_types

    @staticmethod
    def _valid_time(stix_indicator):
        time = {'start_time': stix_indicator['valid_from']}
        end = stix_indicator.get('valid_until')
        if end:
            time['end_time'] = end
        return CTIMValidTime(**time)
