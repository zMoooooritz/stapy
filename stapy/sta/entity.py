from enum import Enum

class Entity(Enum):
    """
    This class represents all available entities in the SensorThingsAPI (v1.1)
    """
    Datastream = "Datastreams"
    MultiDatastream = "MultiDatastreams"
    FeatureOfInterest = "FeaturesOfInterest"
    HistoricalLocation = "HistoricalLocations"
    Location = "Locations"
    Observation = "Observations"
    ObservedProperty = "ObservedProperties"
    Sensor = "Sensors"
    Thing = "Things"

    @staticmethod
    def __singular_map():
        return {
            Entity.FeatureOfInterest: "FeatureOfInterest",
            Entity.ObservedProperty: "ObservedProperty",
            Entity.Sensor: "Sensor",
            Entity.Thing: "Thing"
        }

    @staticmethod
    def list():
        """
        :return: a list of all entities as strings
        """
        return list(map(lambda e: e.value, Entity))

    @classmethod
    def remap(cls, entity):
        """
        This method remaps an Entity to the singular (string) version if needed,
        these are sometimes required in the STA (in case single elements are accesses)
        :param entity: the entity to remap
        :return: the remapped entity
        """
        if entity not in Entity:
            raise Exception("invalid entity: " + entity.value)
        if entity in cls.__singular_map():
            return cls.__singular_map()[entity]
        return entity.value

    @classmethod
    def match(cls, entity):
        """
        This method takes a string entity and tries to find the Entity,
        whose value matches the provided string
        :param entity: the string to find the entity for
        :return: the entity or None
        """
        ent_search = entity.lower()
        for entity in Entity:
            ent_is = entity.value.lower()
            if ent_is in ent_search or ent_search in ent_is:
                return entity
        for entity, ent_val in cls.__singular_map().items():
            ent_is = ent_val.lower()
            if ent_is in ent_search or ent_search in ent_is:
                return entity
        return None