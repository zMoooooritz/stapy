
from stapy.sta.abstract_entity import AbstractEntity

class ObservedProperty(AbstractEntity):
    entry_map = {
        "name": (True, str),
        "description": (True, str),
        "definition": (True, str),
        "properties": (False, dict)
    }

    def check_entry(self, key, value):
        return True
