
from stapy.sta.abstract_entity import AbstractEntity

class Observation(AbstractEntity):
    entry_map = {
        "phenomenonTime": (True, str),
        "result": (True, object),
        "resultTime": (False, str),
        "resultQuality": (False, dict),
        "validTime": (False, str),
        "parameters": (False, dict),
        "Datastream": (True, {
            "@iot.id": (True, int)
        }),
        "FeatureOfInterest": (False, {
            "@iot.id": (True, int)
        })
    }

    def check_entry(self, key, value):
        return True
