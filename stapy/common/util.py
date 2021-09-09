import json

from stapy.sta.geo import GeoJSON

def default(typ):
    switch = {
        str: "",
        int: 0,
        float: 0.0,
        dict: {},
        list: [],
        object: None
    }
    return switch.get(typ, None)

def cast(typ, value):
    switch = {
        str: str,
        int: int,
        float: float,
        dict: json.loads,
        GeoJSON: GeoJSON.match
    }
    return switch.get(typ)(value)

def un_cast(value):
    if isinstance(value, GeoJSON):
        return value.value
    return value
