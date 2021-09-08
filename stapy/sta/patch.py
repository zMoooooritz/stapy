from stapy.sta.request import Request
from stapy.sta.query import Query
from stapy.sta.entity import Entity
from stapy.sta.abstract_request import AbstractRequest

class Patch(AbstractRequest):

    @staticmethod
    def datastream(entity_id, name=None, description=None, unit_of_measurement=None, observation_type=None,
        properties=None, thing_id=None, observed_property_id=None, sensor_id=None):
        params = Patch.cast_params(description=description, name=name, unit_of_measurement=unit_of_measurement,
            observation_type=observation_type, properties=properties, thing_id=thing_id,
            observed_property_id=observed_property_id, sensor_id=sensor_id)
        Patch.entity(Entity.Datastream, entity_id, **params)

    @staticmethod
    def feature_of_interest(entity_id, name=None, description=None, encoding_type=None, feature=None, properties=None):
        params = Patch.cast_params(name=name, description=description, encoding_type=encoding_type, feature=feature, properties=properties)
        Patch.entity(Entity.FeatureOfInterest, entity_id, **params)

    @staticmethod
    def location(entity_id, name=None, description=None, encoding_type=None, location=None,
        properties=None, thing_id=None):
        params = Patch.cast_params(name=name, description=description, encoding_type=encoding_type, location=location,
            properties=properties, thing_id=thing_id)
        Patch.entity(Entity.Location, entity_id, **params)

    @staticmethod
    def observation(entity_id, phenomenon_time=None, result=None, result_quality=None, valid_time=None,
        parameters=None, datastream_id=None, feature_of_interest_id=None):
        params = Patch.cast_params(phenomenon_time=phenomenon_time, result=result,
            result_quality=result_quality, valid_time=valid_time, parameters=parameters,
            datastream_id=datastream_id, feature_of_interest_id=feature_of_interest_id)
        Patch.entity(Entity.Observation, entity_id, **params)

    @staticmethod
    def observed_property(entity_id, name=None, description=None, definition=None, properties=None):
        params = Patch.cast_params(name=name, description=description, definition=definition, properties=properties)
        Patch.entity(Entity.ObservedProperty, entity_id, **params)

    def sensor(entity_id, name=None, description=None, encoding_type=None, metadata=None, properties=None):
        params = Patch.cast_params(name=name, description=description, encoding_type=encoding_type, metadata=metadata, properties=properties)
        Patch.entity(Entity.Sensor, entity_id, **params)

    @staticmethod
    def thing(entity_id, name=None, description=None, properties=None, location_id=None, datastream_id=None):
        params= Patch.cast_params(name=name, description=description, properties=properties, location_id=location_id, datastream_id=datastream_id)
        Patch.entity(Entity.Thing, entity_id, **params)

    @staticmethod
    def entity(entity, entity_id, **params):
        ent = Patch.get_entity(entity)(Request.PATCH)
        ent.set_param(**params)
        payload = ent.get_data()
        path = Query(entity).entity_id(entity_id).get_query()
        Patch.send_request(Request.PATCH, path, payload)
