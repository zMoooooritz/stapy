import abc
import requests

from stapy.common.config import config
from stapy.sta.entity import Entity
from stapy.sta.request import Request
import stapy.sta.entities as ent

class AbstractRequest(metaclass=abc.ABCMeta):

    @staticmethod
    def get_entity(entity):
        switch = {
            Entity.Datastream: ent.Datastream,
            Entity.FeatureOfInterest: ent.FeatureOfInterest,
            Entity.Location: ent.Location,
            Entity.Observation: ent.Observation,
            Entity.ObservedProperty: ent.ObservedProperty,
            Entity.Sensor: ent.Sensor,
            Entity.Thing: ent.Thing
        }
        return switch.get(entity)

    @staticmethod
    def cast_params(**params):
        final_params = {}
        for k, v in params:
            if v is None:
                continue
            if "_id" in k:
                entity = Entity.match(k.split("_")[0]).value
                if isinstance(v, dict):
                    final_params.update({entity: v})
                    continue
                if not isinstance(v, list):
                    final_params.update({entity: {"@iot.id": v}})
                else:
                    ids = []
                    for value in v:
                        ids.append({"@iot.id": value})
                    final_params.update({entity: ids})
            else:
                final_params.update({k: v})
        return final_params

    @staticmethod
    def send_request(request, path, payload):
        """
        Given a path and payload this method creates a HTTP-Request with the given data
        :param request: the type of request to create
        :param path: the SensorThingsAPI-URL for the request
        :param payload: the content of the message
        :return: the ID of the created or edited entity
        """
        try:
            if request == Request.POST:
                resp = requests.post(path, json=payload)
            elif request == Request.PATCH:
                resp = requests.patch(path, json=payload)
        except Exception:
            raise Exception("the supplied API_URL \"" + config.get("API_URL") + "\" is not valid")
        if request == Request.POST:
            loc = resp.headers["location"]
            entity_id = int(loc[loc.find("(")+1:loc.find(")")])
            return entity_id
