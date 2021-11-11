from enum import Enum
import geojson
from thefuzz import fuzz

class GeoJSON(Enum):
    """
    This class represents all valid GeoJSON object for the SensorThingsAPI (v1.1)
    """
    Point = "Point"
    MultiPoint = "MultiPoint"
    LineString = "LineString"
    MultiLineString = "MultiLineString"
    Polygon = "Polygon"
    MultiPolygon = "MultiPolygon"

    @staticmethod
    def list():
        """
        :return: a list of all GeoJSON objects as strings
        """
        return [geo.value for geo in GeoJSON]

    @classmethod
    def is_valid(cls, obj, params):
        """
        :return: if the given obj and params build up a valid geojson object
        """
        if not isinstance(obj, GeoJSON):
            print("The given object is not a valid GeoJSON object: " + str(obj))
            return False

        switch = {
            GeoJSON.Point:            geojson.Point(params).is_valid,
            GeoJSON.MultiPoint:       geojson.MultiPoint(params).is_valid,
            GeoJSON.LineString:       geojson.LineString(params).is_valid,
            GeoJSON.MultiLineString:  geojson.MultiLineString(params).is_valid,
            GeoJSON.Polygon:          geojson.Polygon(params).is_valid,
            GeoJSON.MultiPolygon:     geojson.MultiPolygon(params).is_valid
        }
        return switch.get(obj, False)

    @classmethod
    def match(cls, obj, threshold=0.5):
        """
        This method takes a string obj and tries to find the GeoJSON object,
        whose value matches the provided string
        :param entity: the string to find the GeoJSON object for
        :return: the object or None
        """
        if not isinstance(obj, str):
            return None
        max_ele, max_val = max([(geo, fuzz.ratio(obj.lower(), geo.value.lower())) for geo in GeoJSON], key=lambda x: x[1])
        return max_ele if max_val / 100 > threshold else None
