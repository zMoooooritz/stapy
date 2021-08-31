from stapy.sta.query import Query
from stapy.sta.entity import Entity
from stapy.sta.geo import GeoJSON
from stapy.common.config import config

import requests

class Post(object):
    """
    This static class allows to create new entities on a STA-Server by sending POST-Requests with according content
    """

    @staticmethod
    def datastream(name, description, observation_type, unit, op_id, s_id, t_id, key=None, value=None):
        """
        Create a new Datastream with the given data filled in
        key and value have to be of the same length and will be handled as map afterwards
        :param name: the name for the Datastream
        :param description: the description for the Datastream
        :param observation_type: the type of observations for the Datastream
        :param unit: the unit in which the entries of the Datastream are taken
        :param op_id: the ID of the associated ObservedProperty
        :param s_id: the ID of the associated Sensor
        :param t_id: the ID of the associated Thing
        :param key: a list of keys that contain additional information of the Datastream
        :param value: a list of values that contain additional information of the Datastream
        :return: the ID of the newly created Datastream
        """
        payload = {
            "name": name,
            "description": description,
            "observationType": observation_type,
            "unitOfMeasurement": unit,
            "ObservedProperty": {
                "@iot.id": op_id
            },
            "Sensor": {
                "@iot.id": s_id
            },
            "Thing": {
                "@iot.id": t_id
            }
        }
        payload = Post.append_props(payload, "properties", key, value)
        path = Query(Entity.Datastream).get_query()
        return Post.send_request(path, payload), True

    @staticmethod
    def full_datastream(name, description, long_name, obv_type, unit, ob_prop, loc_type, loc_coords, key=None, value=None):
        """
        Create a new Datastream with all required and associated entities that contain the given data
        key and value have to be of the same length and will be handled as map afterwards
        :param description: the description for the Datastream
        :param name: the name for the associated entities
        :param long_name: the description for the associated entities
        :param ob_prop: the name and definition of the ObservedProperty
        :param loc_type: the type of location according to the GeoJSON-Standard
        :param loc_coords: coordinates formatted according to the defined type in loc_type
        :param key: a list of keys that contain additional information of the Datastream
        :param value: a list of values that contain additional information of the Datastream
        :return: the ID of the newly created Datastream
        """
        l_id, err = Post.location(name, long_name, loc_type, loc_coords)
        if err != True:
            return -1, False
        t_id, err = Post.thing(name, long_name, l_id)
        if err != True:
            return -1, False
        o_id, err = Post.observed_property(ob_prop, ob_prop, ob_prop)
        if err != True:
            return -1, False
        s_id, err = Post.sensor(name, long_name)
        if err != True:
            return -1, False

        return Post.datastream(name, description, obv_type, unit, o_id, s_id, t_id, key, value), True

    @staticmethod
    def feature_of_interest(name, description="", encodingType="", feature=""):
        """
        Create a new FeatureOfInterest with the given data filled in
        :param name: the name for the FeatureOfInterest
        :param description: the description for the FeatureOfInterest
        :param encodingType: the encodingType for the FeatureOfInterest
        :param feature: the relevant feature for an observation
        :return: the ID of the newly created FeatureOfInterest
        """
        payload = {
            "name": name,
            "description": description,
            "encodingType": encodingType,
            "feature": feature
        }
        path = Query(Entity.FeatureOfInterest).get_query()
        return Post.send_request(path, payload), True

    @staticmethod
    def observation(result, time, d_id, key=None, value=None):
        """
        Create a new Observation with the given data filled in
        key and value have to be of the same length and will be handled as map afterwards
        :param result: the result of the Observation
        :param time: the time of the Observation
        :param d_id: the ID of the associated Datastream
        :param key: a list of keys that contain additional information of the Observation
        :param value: a list of values that contain additional information of the Observation
        :return: the ID of the newly created Observation
        """
        payload = {
            "result": result,
            "phenomenonTime": time,
            "resultTime": time,
            "Datastream": {
                "@iot.id": d_id
            }
        }
        payload = Post.append_props(payload, "parameters", key, value)
        path = Query(Entity.Observation).get_query()
        return Post.send_request(path, payload), True

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
    def sensor(name, description="", encodingType="", metadata=""):
        """
        Create a new Sensor with the given data filled in
        :param name: the name for the Sensor
        :param description: the description for the Sensor
        :param encodingType: the encodingType of the Sensor
        :param metadata: the metadata of the Sensor
        :return: the ID of the newly created Sensor
        """
        payload = {
            "name": name,
            "description": description,
            "encodingType": encodingType,
            "metadata": metadata
        }
        path = Query(Entity.Sensor).get_query()
        return Post.send_request(path, payload), True

    @staticmethod
    def observed_property(name, description, definition):
        """
        Create a new ObservedProperty with the given data filled in
        :param name: the name for the ObservedProperty
        :param definition: the definition for the ObservedProperty
        :return: the ID of the newly created ObservedProperty
        """
        payload = {
            "name": name,
            "description": description,
            "definition": definition,
        }
        path = Query(Entity.ObservedProperty).get_query()
        return Post.send_request(path, payload), True

    @staticmethod
    def location(name, description, loc_type, loc_coords, encodingType=""):
        """
        Create a new Location with the given data filled in
        :param name: the name for the Location
        :param description: the description for the Location
        :param loc_type: the type of location according to the GeoJSON-Standard
        :param loc_coords: coordinates formatted according to the defined type in loc_type
        :return: the ID of the newly created Location
        """
        if not GeoJSON.is_valid(loc_type, loc_coords):
            return -1, False

        payload = {
            "name": name,
            "description": description,
            "encodingType": encodingType,
            "location": {
                "type": loc_type,
                "coordinates": loc_coords
            }
        }
        path = Query(Entity.Location).get_query()
        return Post.send_request(path, payload), True

    @staticmethod
    def thing(name, description, loc_id):
        """
        Create a new Thing with the given data filled in
        :param name: the name for the Thing
        :param description: the description for the Thing
        :param loc_id: the ID of the associated Location
        :return: the ID of the newly created Thing
        """
        payload = {
            "name": name,
            "description": description,
            "Locations": [
                {
                    "@iot.id": loc_id
                }
            ]
        }
        path = Query(Entity.Thing).get_query()
        return Post.send_request(path, payload), True

    @staticmethod
    def get_entity_method(entity):
        switch = {
            Entity.Datastream: Post.datastream,
            Entity.FeatureOfInterest: Post.feature_of_interest,
            Entity.Location: Post.location,
            Entity.Observation: Post.observation,
            Entity.ObservedProperty: Post.observed_property,
            Entity.Sensor: Post.sensor,
            Entity.Thing: Post.thing
        }
        return switch.get(entity)
   
    @staticmethod
    def entity(entity, *args):
        return Post.get_entity_method(entity)(*args)

    @staticmethod
    def append_props(payload, name, key=None, value=None):
        """
        This class takes a dict and adds a key-value pairs in the attribute name in the dict
        :param payload: the dict with the base data
        :param name: the attribute which contains the key-value data
        :param key: a list of keys
        :param value: a list of values for the given keys
        :return: the dict that is extended by the defined data
        """
        if key is None and value is None:
            return payload
        if not isinstance(key, list) and not isinstance(value, list):
            key = [key]
            value = [value]
        payload[name] = {}
        for k, v in zip(key, value):
            payload[name][k] = v
        return payload

    @staticmethod
    def send_request(path, payload):
        """
        Given a path and payload this method creates a HTTP-Post with the given data
        :param path: the SensorThingsAPI-URL to add the data to
        :param payload: the content of the message
        :return: the ID of the created entity
        """
        resp = requests.post(path, json=payload)
        loc = resp.headers["location"]
        entity_id = int(loc[loc.find("(")+1:loc.find(")")])
        return entity_id