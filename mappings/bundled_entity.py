from abc import ABC

from mappings.mapping import Mapping


class BundledEntityMapping(Mapping, ABC):
    def __init__(self, stix_object, bundle):
        super().__init__(stix_object)
        self.bundle = bundle
