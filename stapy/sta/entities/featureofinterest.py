
from stapy.sta.abstract_entity import AbstractEntity

class FeatureOfInterest(AbstractEntity):
    entry_map = {
        "name": (True, str),
        "description": (True, str),
        "encodingType": (True, str),
        "location": (True, dict)
    }

    def check_entry(self, key, value):
        return True