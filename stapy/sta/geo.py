from enum import Enum
import geojson
import Levenshtein as lev

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
        max_obj = max(GeoJSON, key=lambda x: lev.ratio(obj.lower(), x.value.lower()))
        return max_obj if lev.ratio(obj.lower(), max_obj.value.lower()) > threshold else None
