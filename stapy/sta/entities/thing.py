
from stapy.sta.abstract_entity import AbstractEntity

class Thing(AbstractEntity):
    entry_map = {
        "name": (True, str),
        "description": (True, str),
        "properties": (False, dict),
        "Locations": (False, {
            "@iot.id": (True, int)
        }),
        "HistoricalLocations": (False, {
            "@iot.id": (True, int)
        }),
        "Datastreams": (False, {
            "@iot.id": (True, int)
        })
    }

    def check_entry(self, key, value):
        return True
