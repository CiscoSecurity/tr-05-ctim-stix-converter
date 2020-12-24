from mappings.bundled_entity import BundledEntityMapping
from mappings.mapping import Mapping
from mappings.mapping_result import CTIMMappingResult


class Bundle(Mapping):
    @classmethod
    def type(cls):
        return 'bundle'

    def __init__(self, stix_object):
        self.bundle_index = {
            ob['id']: ob for ob in stix_object['objects']
        }
        super().__init__(stix_object)

    def find_by_ref(self, ref_id):
        return self.bundle_index.get(ref_id)

    def map_to_ctim(self):
        mapping_result = CTIMMappingResult()
        for inner_object in self.stix_object['objects']:
            mapping = BundledEntityMapping.for_(inner_object, self)
            if mapping:
                mapping_result.merge(mapping.map_to_ctim())
            else:
                pass  # todo add warning
        return mapping_result
