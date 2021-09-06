
from stapy.sta.abstract_entity import AbstractEntity

class Datastream(AbstractEntity):
    entry_map = {
        "name": (True, str),
        "description": (True, str),
        "unitOfMeasurement": (True, dict),
        "observationType": (True, str),
        "observedArea": (False, object),
        "phenomenonTime": (False, str),
        "resultTime": (False, str),
        "Thing": (True, {
            "@iot.id": (True, int)
        }),
        "ObservedProperty": (True, {
            "@iot.id": (True, int)
        }),
        "Sensor": (True, {
            "@iot.id": (True, int)
        }),
        "Observations": (False, {
            "@iot.id": (True, int)
        })
    }

    def check_entry(self, key, value):
        return True