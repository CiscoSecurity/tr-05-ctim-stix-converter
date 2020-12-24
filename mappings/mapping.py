from abc import ABC, abstractmethod

from mappings.mapping_result import MappingResult
from utils import all_subclasses


class Mapping(ABC):
    def __init__(self, stix_object):
        self.stix_object = stix_object

    @classmethod
    @abstractmethod
    def type(cls):
        pass

    @abstractmethod
    def map_to_ctim(self, *args, **kwargs) -> MappingResult:
        pass

    @classmethod
    def for_(cls, stix_object, *args, **kwargs):
        """Return an instance of `Mapping` for the specified type."""

        for subcls in all_subclasses(Mapping):
            if subcls.type() == stix_object['type']:
                return subcls(stix_object,  *args, **kwargs)

        return None
