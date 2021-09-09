
from stapy.sta.geo import GeoJSON
from stapy.sta.abstract_entity import AbstractEntity

class Location(AbstractEntity):
    entry_map = {
        "name": (True, str),
        "description": (True, str),
        "encodingType": (True, str),
        "location": (True, {
            "type": (True, GeoJSON),
            "coordinates": (True, list)
        }),
        "properties": (False, dict),
        "Things": (False, {
            "@iot.id": (True, int)
        }),
        "HistoricalLocations": (False, {
            "@iot.id": (True, int)
        })
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
