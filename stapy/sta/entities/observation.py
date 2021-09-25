from stapy.sta.time import Time
from stapy.sta.abstract_entity import AbstractEntity

# TODO resultQuality DQ_Element
class Observation(AbstractEntity):
    entry_map = {
        "phenomenonTime": (True, True, Time),
        "result": (True, True, object),
        "resultTime": (False, True, Time),
        "resultQuality": (False, True, dict),
        "validTime": (False, True, Time),
        "parameters": (False, True, dict),
        "Datastream": (True, True, dict),
        "FeatureOfInterest": (False, True, dict)
    }

    def check_entry(self, key, value):
        return True
