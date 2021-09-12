from stapy.sta.request import Request
from stapy.sta.query import Query
from stapy.sta.entity import Entity
from stapy.sta.abstract_request import AbstractRequest

class Patch(AbstractRequest):
    """
    This static class allows to patch entities on a STA-Server by sending PATCH-Requests with according content
    """

    @staticmethod
    def datastream(entity_id, name=None, description=None, unit_of_measurement=None, observation_type=None,
        properties=None, thing_id=None, observed_property_id=None, sensor_id=None):
        """
        Update a Datastream with the given data
        :param entity_id: the ID of the Datastream to patch
        :param name: the name for the Datastream
        :param description: the description for the Datastream
        :param unit_of_measurement: the unit in which the entries of the Datastream are taken
        :param observation_type: the type of observations for the Datastream
        :param thing_id: the ID of the associated Thing
        :param observed_property_id: the ID of the associated ObservedProperty
        :param sensor_id: the ID of the associated Sensor
        :param properties: a dict of additional (meta-)data for the Datastream
        :return: the ID of the newly created Datastream
        """
        params = Patch.cast_params(description=description, name=name, unitOfMeasurement=unit_of_measurement,
            observationType=observation_type, properties=properties, thing_id=thing_id,
            observed_property_id=observed_property_id, sensor_id=sensor_id)
        return Patch.entity(Entity.Datastream, entity_id, **params)

    @staticmethod
    def feature_of_interest(entity_id, name=None, description=None, encoding_type=None, feature=None, properties=None):
        """
        Update a FeatureOfInterest with the given data
        :param entity_id: the ID of the FeatureOfInterest to patch
        :param name: the name for the FeatureOfInterest
        :param description: the description for the FeatureOfInterest
        :param encoding_type: the encodingType for the FeatureOfInterest
        :param feature: the relevant feature for an observation
        :param properties: a dict of additional (meta-)data for the FeatureOfInterest
        :return: the ID of the newly created FeatureOfInterest
        """
        params = Patch.cast_params(name=name, description=description, encodingType=encoding_type, feature=feature, properties=properties)
        return Patch.entity(Entity.FeatureOfInterest, entity_id, **params)

    @staticmethod
    def location(entity_id, name=None, description=None, encoding_type=None, location=None,
        properties=None, thing_id=None):
        """
        Update a Location with the given data
        :param entity_id: the ID of the Location to patch
        :param name: the name for the Location
        :param description: the description for the Location
        :param encoding_type: the encodingType for the Location
        :param location: the location of the Location
        :param properties: a dict of additional (meta-)data for the Location
        :param thing_id: the ID of the associated Thing
        :return: the ID of the newly created Location
        """
        params = Patch.cast_params(name=name, description=description, encodingType=encoding_type, location=location,
            properties=properties, thing_id=thing_id)
        return Patch.entity(Entity.Location, entity_id, **params)

    @staticmethod
    def observation(entity_id, phenomenon_time=None, result=None, result_quality=None, valid_time=None,
        parameters=None, datastream_id=None, feature_of_interest_id=None):
        """
        Update a Observation with the given data
        :param entity_id: the ID of the Observation to patch
        :param phenomenon_time: the time of the Observation
        :param result: the result of the Observation
        :param result_quality: the quality of the result for the Observation
        :param valid_time: the time interval in which the Observation is valid
        :param parameters: a dict of additional (meta-)data for the Observation
        :param datastream_id: the ID of the associated Datastream
        :param feature_of_interest_id: the ID of the associated FeatureOfInterest
        :return: the ID of the newly created Observation
        """
        params = Patch.cast_params(phenomenonTime=phenomenon_time, result=result,
            resultQuality=result_quality, validTime=valid_time, parameters=parameters,
            datastream_id=datastream_id, feature_of_interest_id=feature_of_interest_id)
        return Patch.entity(Entity.Observation, entity_id, **params)

    @staticmethod
    def observed_property(entity_id, name=None, description=None, definition=None, properties=None):
        """
        Update a ObservedProperty with the given data
        :param entity_id: the ID of the ObservedProperty to patch
        :param name: the name for the ObservedProperty
        :param description: the description for the ObservedProperty
        :param definition: the definition for the ObservedProperty
        :param properties: a dict of additional (meta-)data for the ObservedProperty
        :return: the ID of the newly created ObservedProperty
        """
        params = Patch.cast_params(name=name, description=description, definition=definition, properties=properties)
        return Patch.entity(Entity.ObservedProperty, entity_id, **params)

    @staticmethod
    def sensor(entity_id, name=None, description=None, encoding_type=None, metadata=None, properties=None):
        """
        Update a Sensor with the given data
        :param entity_id: the ID of the Sensor to patch
        :param name: the name for the Sensor
        :param description: the description for the Sensor
        :param encoding_type: the encodingType of the Sensor
        :param metadata: the metadata of the Sensor
        :param properties: a dict of additional (meta-)data for the Sensor
        :return: the ID of the newly created Sensor
        """
        params = Patch.cast_params(name=name, description=description, encodingType=encoding_type, metadata=metadata, properties=properties)
        return Patch.entity(Entity.Sensor, entity_id, **params)

    @staticmethod
    def thing(entity_id, name=None, description=None, properties=None, location_id=None, datastream_id=None):
        """
        Update a Thing with the given data
        :param entity_id: the ID of the Thing to patch
        :param name: the name for the Thing
        :param description: the description for the Thing
        :param properties: a dict of additional (meta-)data for the Thing
        :param location_id: the ID of the associated Location
        :param datastream_id: the ID of the associated Datastream
        :return: the ID of the newly created Thing
        """
        params= Patch.cast_params(name=name, description=description, properties=properties, location_id=location_id, datastream_id=datastream_id)
        return Patch.entity(Entity.Thing, entity_id, **params)

    @staticmethod
    def entity(entity, entity_id, **params):
        """
        Update a Entity with the given data
        :param entity_id: the ID of the Entity to patch
        :param entity: the type of entity to create
        :param params: kwargs of all attributes that should be set for the entity
        :return: the ID of the newly created Entity
        """
        ent = Patch.get_entity(entity)(Request.PATCH)
        ent.set_param(**params)
        payload = ent.get_data()
        path = Query(entity).entity_id(entity_id).get_query()
        return Patch.send_request(Request.PATCH, path, payload)
