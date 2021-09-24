from stapy.sta.geo import GeoJSON

from stapy.sta.abstract_entity import AbstractEntity

# TODO other encodingTypes
class FeatureOfInterest(AbstractEntity):
    entry_map = {
        "name": (True, True, str),
        "description": (True, True, str),
        "encodingType": (True, True, str),
        "feature": (True, True, dict),
        "properties": (False, True, dict)
    }

    def check_entry(self, key, value):
        if key == "feature":
            geo = value.get("type")
            coords = value.get("coordinates")

            if not isinstance(geo, GeoJSON):
                geo = GeoJSON.match(geo)
            if not GeoJSON.is_valid(geo, coords):
                return False

        return True
