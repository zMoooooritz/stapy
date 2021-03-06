from enum import Enum
from thefuzz import fuzz

class Entity(Enum):
    """
    This class represents all available entities in the SensorThingsAPI (v1.1)
    """
    Datastream = "Datastreams"
    FeatureOfInterest = "FeaturesOfInterest"
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
        :return: a list of all entity values
        """
        return [entity.value for entity in Entity]

    @staticmethod
    def keys():
        """
        :return: a list of all entity names
        """
        return [entity.name for entity in Entity]

    @classmethod
    def remap(cls, entity):
        """
        This method remaps an Entity to the singular (string) version if needed,
        these are sometimes required in the STA (in case single elements are accesses)
        :param entity: the entity to remap
        :return: the remapped entity
        """
        if not isinstance(entity, Entity):
            raise Exception("invalid entity: " + entity)
        if entity in cls.__singular_map():
            return cls.__singular_map()[entity]
        return entity.value

    @classmethod
    def match(cls, entity, threshold=0.5):
        """
        This method takes a string entity and tries to find the Entity,
        whose value matches the provided string
        :param entity: the string to find the entity for
        :return: the entity or None
        """
        if not isinstance(entity, str):
            return None
        max_ele, max_val = max([(ent, fuzz.ratio(entity.lower(), ent.value.lower())) for ent in Entity], key=lambda x: x[1])
        return max_ele if max_val / 100 > threshold else None
