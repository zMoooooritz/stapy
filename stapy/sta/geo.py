from enum import Enum

import geojson

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
        return list(map(lambda e: e.value, GeoJSON))

    @classmethod
    def is_valid(cls, obj, params):
        """
        :return: if the given obj and params build up a valid geojson object
        """
        if not cls.__is_valid_obj(obj):
            print("The given object is not a valid GeoJSON object: " + str(obj))
            return False
        if not cls.__has_valid_params(obj, params):
            print("The given params \"" + str(params) + "\" are not valid for the GeoJSON object: " + str(obj))
            return False
        return True

    @staticmethod
    def __is_valid_obj(obj):
        """
        :return: if the specified obj ist a valid geojson object
        """
        if obj not in GeoJSON.list():
            return False
        return True

    @staticmethod
    def __has_valid_params(obj, params):
        """
        :return: if the given obj and params build up a valid geojson object
        """                        
        switch = {
            "Point":            geojson.Point(params).is_valid,
            "MultiPoint":       geojson.MultiPoint(params).is_valid,
            "LineString":       geojson.LineString(params).is_valid,
            "MultiLineString":  geojson.MultiLineString(params).is_valid,
            "Polygon":          geojson.Polygon(params).is_valid,
            "MultiPolygon":     geojson.MultiPolygon(params).is_valid
        }
        return switch.get(obj, False)