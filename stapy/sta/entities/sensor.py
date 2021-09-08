
from stapy.sta.abstract_entity import AbstractEntity

class Sensor(AbstractEntity):
    entry_map = {
        "name": (True, str),
        "description": (True, str),
        "encodingType": (True, str),
        "metadata": (True, object),
        "properties": (False, dict)
    }

    def check_entry(self, key, value):
        return True
