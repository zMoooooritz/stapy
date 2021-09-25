
from stapy.sta.geo import GeoJSON
from stapy.sta.abstract_entity import AbstractEntity

class Location(AbstractEntity):
    entry_map = {
        "name": (True, True, str),
        "description": (True, True, str),
        "encodingType": (True, True, str),
        "location": (True, True, {
            "type": (True, True, GeoJSON),
            "coordinates": (True, True, list)
        }),
        "properties": (False, True, dict),
        "Things": (False, True, dict),
        "HistoricalLocations": (False, True, dict)
    }

    def check_entry(self, key, value):
        if key == "location":
            geo = value.get("type")
            coords = value.get("coordinates")

            if not isinstance(geo, GeoJSON):
                geo = GeoJSON.match(geo)
            if not GeoJSON.is_valid(geo, coords):
                return False

        return True
