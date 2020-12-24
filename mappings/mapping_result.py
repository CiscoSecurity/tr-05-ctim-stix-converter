from abc import ABC, abstractmethod

from bundlebuilder.models.primary import (
    Bundle as CTIMBundle,
    Indicator as CTIMIndicator,
    Sighting as CTIMSighting,
    Judgement as CTIMJudgement,
    Verdict as CTIMVerdict,
    Relationship as CTIMRelationship
)


class MappingResult(ABC):
    def __init__(self, *args):
        self._objects = list(args)

    def add(self, item):
        self._objects.append(item)

    def merge(self, other):
        self._objects.extend(other._objects)

    @abstractmethod
    def json(self):
        pass


class CTIMMappingResult(MappingResult):
    def bundle(self):
        result = CTIMBundle()
        add_method_map = {
            CTIMIndicator: result.add_indicator,
            CTIMSighting: result.add_sighting,
            CTIMJudgement: result.add_judgement,
            CTIMVerdict: result.add_verdict,
            CTIMRelationship: result.add_relationship
        }
        for ob in self._objects:
            add_method_map[type(ob)](ob)
        return result

    def json(self):
        return self.bundle().json
