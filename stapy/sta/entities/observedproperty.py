
from stapy.sta.abstract_entity import AbstractEntity

# TODO defintion URI
class ObservedProperty(AbstractEntity):
    entry_map = {
        "name": (True, True, str),
        "description": (True, True, str),
        "definition": (True, True, str),
        "properties": (False, True, dict)
    }

    def check_entry(self, key, value):
        return True
