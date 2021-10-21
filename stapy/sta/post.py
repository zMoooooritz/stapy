import requests

from stapy.sta.query import Query
from stapy.sta.entity import Entity
from stapy.common.config import config
from stapy.sta.abstract_request import AbstractRequest
from stapy.sta.request import Request

class Post(AbstractRequest):
    """
    This static class allows to create new entities on a STA-Server by sending POST-Requests with according content
    """

    @staticmethod
    def datastream(name, description, unit_of_measurement, observation_type,
        thing_id, observed_property_id, sensor_id, properties=None):
        """
        Create a new Datastream with the given data filled in
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
        params = Post.cast_params(name=name, description=description, unitOfMeasurement=unit_of_measurement,
            observationType=observation_type, properties=properties, thing_id=thing_id,
            observed_property_id=observed_property_id, sensor_id=sensor_id)
        return Post.entity(Entity.Datastream, **params)

    @staticmethod
    def full_datastream(name, description, long_name, encoding_type, location, definition, unit, ob_type):
        """
        Create a new Datastream with all required and associated entities that contain the given data
        :param name: the name for the associated entities
        :param description: the description for the Datastream
        :param long_name: the description for the associated entities
        :param encoding_type: the encodingType for the Location and Sensor
        :param loc_type: the location according to the GeoJSON-Standard
        :param definition: the definition for the ObservedProperty
        :param unit: the unit in which the entries of the Datastream are taken
        :param ob_type: the type of observations for the Datastream
        :return: the ID of the newly created Datastream
        """
        l_id = Post.location(name, long_name, encoding_type, location)
        t_id = Post.thing(name, long_name, location_id=l_id)
        o_id = Post.observed_property(name, long_name, definition)
        s_id = Post.sensor(name, long_name, encoding_type)

        return Post.datastream(name, description, unit, ob_type, t_id, o_id, s_id)

    @staticmethod
    def feature_of_interest(name, description, encoding_type, feature, properties=None):
        """
        Create a new FeatureOfInterest with the given data filled in
        :param name: the name for the FeatureOfInterest
        :param description: the description for the FeatureOfInterest
        :param encoding_type: the encodingType for the FeatureOfInterest
        :param feature: the relevant feature for an observation
        :param properties: a dict of additional (meta-)data for the FeatureOfInterest
        :return: the ID of the newly created FeatureOfInterest
        """
        params = Post.cast_params(name=name, description=description, encodingType=encoding_type, feature=feature, properties=properties)
        return Post.entity(Entity.FeatureOfInterest, **params)

    @staticmethod
    def location(name, description, encoding_type, location, properties=None, thing_id=None):
        """
        Create a new Location with the given data filled in
        :param name: the name for the Location
        :param description: the description for the Location
        :param encoding_type: the encodingType for the Location
        :param location: the location of the Location
        :param properties: a dict of additional (meta-)data for the Location
        :param thing_id: the ID of the associated Thing
        :return: the ID of the newly created Location
        """
        params = Post.cast_params(name=name, description=description, encodingType=encoding_type, location=location,
            properties=properties, thing_id=thing_id)
        return Post.entity(Entity.Location, **params)

    @staticmethod
    def observation(phenomenon_time, result, result_quality=None, valid_time=None, parameters=None,
        datastream_id=None, feature_of_interest_id=None):
        """
        Create a new Observation with the given data filled in
        :param phenomenon_time: the time of the Observation
        :param result: the result of the Observation
        :param result_quality: the quality of the result for the Observation
        :param valid_time: the time interval in which the Observation is valid
        :param parameters: a dict of additional (meta-)data for the Observation
        :param datastream_id: the ID of the associated Datastream
        :param feature_of_interest_id: the ID of the associated FeatureOfInterest
        :return: the ID of the newly created Observation
        """
        params = Post.cast_params(phenomenonTime=phenomenon_time, result=result,
            resultQuality=result_quality, validTime=valid_time, parameters=parameters,
            datastream_id=datastream_id, feature_of_interest_id=feature_of_interest_id)
        return Post.entity(Entity.Observation, **params)

    @staticmethod
    def observations(results, times, d_id, keys=None, values=None):
        """
        Create new Observations with the given data filled in
        values has to contain a list of entries for each element in keys
        :param results: the results of value of the Observations
        :param times: the times of the Observation
        :param d_id: the ID of the associated Datastream
        :param keys: a list of keys that contain additional information of the Observation
        :param values: a list of list of values that contain additional information of the Observation
        :return: None
        """
        payload = {
            "Datastream": {
                "@iot.id": d_id
            },
            "components": [
                "phenomenonTime",
                "result"
            ],
            "dataArray": []
        }

        for idx in range(len(results)):
            arr = [times[idx], results[idx]]
            payload["dataArray"].append(arr)

        if keys is not None and values is not None:
            if not isinstance(keys, list):
                keys = [keys]
                values = [values]
            for idx, key in enumerate(keys):
                payload["components"].append("parameters")
                for v_idx, value in enumerate(values[idx]):
                    payload["dataArray"][v_idx].append({key: value})
        path = config.get("API_URL") + "CreateObservations"
        requests.post(path, json=[payload])

    @staticmethod
    def observed_property(name, description, definition, properties=None):
        """
        Create a new ObservedProperty with the given data filled in
        :param name: the name for the ObservedProperty
        :param description: the description for the ObservedProperty
        :param definition: the definition for the ObservedProperty
        :param properties: a dict of additional (meta-)data for the ObservedProperty
        :return: the ID of the newly created ObservedProperty
        """
        params = Post.cast_params(name=name, description=description, definition=definition,
            properties=properties)
        return Post.entity(Entity.ObservedProperty, **params)

    @staticmethod
    def sensor(name, description, encoding_type, metadata=None, properties=None):
        """
        Create a new Sensor with the given data filled in
        :param name: the name for the Sensor
        :param description: the description for the Sensor
        :param encoding_type: the encodingType of the Sensor
        :param metadata: the metadata of the Sensor
        :param properties: a dict of additional (meta-)data for the Sensor
        :return: the ID of the newly created Sensor
        """
        params = Post.cast_params(name=name, description=description, encodingType=encoding_type,
            metadata=metadata, properties=None)
        return Post.entity(Entity.Sensor, **params)

    @staticmethod
    def thing(name, description, properties=None, location_id=None, datastream_id=None):
        """
        Create a new Thing with the given data filled in
        :param name: the name for the Thing
        :param description: the description for the Thing
        :param properties: a dict of additional (meta-)data for the Thing
        :param location_id: the ID of the associated Location
        :param datastream_id: the ID of the associated Datastream
        :return: the ID of the newly created Thing
        """
        params= Post.cast_params(name=name, description=description, properties=properties,
            location_id=location_id, datastream_id=datastream_id)
        return Post.entity(Entity.Thing, **params)

    @staticmethod
    def entity(entity, **params):
        """
        Create a new Entity with the provided data
        :param entity: the type of entity to create
        :param params: kwargs of all attributes that should be set for the entity
        :return: the ID of the newly created Entity
        """
        ent = Post.get_entity(entity)(Request.POST)
        ent.set_param(**params)
        payload = ent.get_data()
        path = Query(entity).get_query()
        return Post.send_request(Request.POST, path, payload)
