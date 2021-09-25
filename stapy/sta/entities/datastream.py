
from stapy.sta.abstract_entity import AbstractEntity
from stapy.sta.time import Time

class Datastream(AbstractEntity):
    entry_map = {
        "name": (True, True, str),
        "description": (True, True, str),
        "unitOfMeasurement": (True, True, {
            "name": (True, True, str),
            "symbol": (True, True, str),
            "definition": (True, True, str)
        }),
        "observationType": (True, True, str),
        "observedArea": (False, False, dict),
        "phenomenonTime": (False, False, Time),
        "resultTime": (False, False, Time),
        "properties": (False, True, dict),
        "Thing": (True, True, dict),
        "ObservedProperty": (True, True, dict),
        "Sensor": (True, True, dict),
        "Observations": (False, True, dict)
    }

    def check_entry(self, key, value):
        return True
