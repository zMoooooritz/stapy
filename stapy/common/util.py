import json
from datetime import date

from stapy.sta.geo import GeoJSON
from stapy.sta.time import Time

def default(typ):
    switch = {
        str: "",
        int: 0,
        float: 0.0,
        dict: {},
        list: [],
        object: None,
        Time: date.today().isoformat(),
    }
    return switch.get(typ, None)

def cast(typ, value):
    switch = {
        str: str,
        int: int,
        float: float,
        dict: json.loads,
        GeoJSON: GeoJSON.match,
        Time: Time,
    }
    return switch.get(typ)(value)

def un_cast(value):
    if isinstance(value, GeoJSON):
        return value.value
    if isinstance(value, Time):
        return str(value)
    return value
