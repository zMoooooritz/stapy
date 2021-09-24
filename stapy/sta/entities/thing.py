
from stapy.sta.abstract_entity import AbstractEntity

# TODO HistoricalLocations
class Thing(AbstractEntity):
    entry_map = {
        "name": (True, True, str),
        "description": (True, True, str),
        "properties": (False, True, dict),
        "Locations": (False, True, dict),
        "HistoricalLocations": (False, True, dict),
        "Datastreams": (False, True, dict)
    }

    def check_entry(self, key, value):
        return True
