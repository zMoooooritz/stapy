#!/usr/bin/env python

from enum import Enum

class Entity(Enum):
    """
    This class represents all available entities in the SensorThingsAPI (v1.1)
    """
    Datastreams = "Datastreams"
    MultiDatastreams = "MultiDatastreams"
    FeaturesOfInterest = "FeaturesOfInterest"
    HistoricalLocations = "HistoricalLocations"
    Locations = "Locations"
    Observations = "Observations"
    ObservedProperties = "ObservedProperties"
    Sensors = "Sensors"
    Things = "Things"

    @staticmethod
    def list():
        """
        :return: a list of all entities as strings
        """
        return list(map(lambda e: e.value, Entity))

    @staticmethod
    def remap(entity):
        """
        This method remaps an entity to the singular version if needed,
        these are sometimes required in the STA (in case single elements are accesses)
        :param entity: the entity to possible remap
        :return: the remapped entity
        """
        if entity not in Entity.list():
            raise Exception("invalid entity: " + entity)
        singular_map = {
            "FeaturesOfInterest": "FeatureOfInterest",
            "ObservedProperties": "ObservedProperty",
            "Sensors": "Sensor",
            "Things": "Thing"
        }
        if entity in singular_map:
            return singular_map[entity]
        return entity

    @staticmethod
    def get(entity):
        switch = {
            "datastream": Entity.Datastreams.value,
            "location": Entity.Locations.value,
            "observation": Entity.Observations.value,
            "observedproperty": Entity.ObservedProperties.value,
            "sensor": Entity.Sensors.value,
            "things": Entity.Things.value
        }
        ent = entity.lower()
        for key, value in switch.items():
            if key == ent:
                return Entity(value)
        return None