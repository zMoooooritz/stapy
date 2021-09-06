
from stapy.sta.abstract_entity import AbstractEntity

class ObservedProperty(AbstractEntity):
    entry_map = {
        "name": (True, str),
        "description": (True, str),
        "definition": (True, str)
    }

    def check_entry(self, key, value):
        return True