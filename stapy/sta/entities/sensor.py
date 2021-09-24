
from stapy.sta.abstract_entity import AbstractEntity

class Sensor(AbstractEntity):
    entry_map = {
        "name": (True, True, str),
        "description": (True, True, str),
        "encodingType": (True, True, str),
        "metadata": (True, True, object),
        "properties": (False, True, dict)
    }

    def check_entry(self, key, value):
        return True
