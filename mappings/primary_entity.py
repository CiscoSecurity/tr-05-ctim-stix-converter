from abc import ABC

from constants import (
    NONE_CONFIDENCE,
    LOW_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    HIGH_CONFIDENCE
)
from mappings.bundled_entity import BundledEntityMapping


class PrimaryEntityMapping(BundledEntityMapping, ABC):
    def _tlp(self):
        for ref in self.stix_object.get('object_marking_refs', []):
            marking = self.bundle.find_by_ref(ref)
            if marking['definition_type'] == 'tlp':
                return marking['definition']['tlp']

    @staticmethod
    def _confidence(stix_value):
        # ToDo: validate if not presented
        #  - not add the field at all or return Unknown
        if not stix_value:
            return 'Unknown'

        try:
            stix_value = int(stix_value)
            assert 0 <= stix_value <= 100
        except (TypeError, ValueError, AssertionError):
            pass  # Add warning
            return None

        segments = [
            (0, NONE_CONFIDENCE),
            (29, LOW_CONFIDENCE),
            (69, MEDIUM_CONFIDENCE),
            (100, HIGH_CONFIDENCE)
        ]

        for bound, result in segments:
            if stix_value <= bound:
                return result

    @staticmethod
    def external_ids(external_references):
        external_references = external_references or []
        return [ref['id'] for ref in external_references]
