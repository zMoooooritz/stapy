import abc
import logging
import requests

from stapy.common.config import config
from stapy.sta.entity import Entity
from stapy.sta.request import Request
import stapy.sta.entities as ent

class AbstractRequest(metaclass=abc.ABCMeta):
    """
    This abstract class encapsulates some required functions for the POST and PATCH requests
    """

    @staticmethod
    def get_entity(entity):
        """
        Return the according concrete entity for an entry of Entity
        :param entity: the entity that needs to 'translated'
        :return: the concrete entity
        """
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
        """
        This method received a dictionary of named arguments modifies them slightly and returns one dictionary
        :param params: the dictionary of named arguments to modify
        :return: the resulting dict containing the elements
        """
        final_params = {}
        for k, v in params.items():
            if v is None:
                continue

            if "_id" in k:
                entity = Entity.match(k.split("_")[0]).value
                final_params.update({entity: v})
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

        if request == Request.POST:
            request_method = requests.post
        elif request == Request.PATCH:
            request_method = requests.patch
        else:
            raise Exception("Invalid request type")

        api_usr = config.get("STA_USR")
        api_pwd = config.get("STA_PWD")
        if api_usr != "" and api_pwd != "":
            response = request_method(path, json=payload, auth=requests.auth.HTTPBasicAuth(api_usr, api_pwd))
        else:
            response = request_method(path, json=payload)

        if not response.ok:
            if "message" in response.json():
                logging.info("Request was not successful (" + response.json().get("message") + ")")
                return -1
            else:
                logging.warning("An error occurred, request failed")
                return -1
        elif request == Request.POST:
            loc = response.headers["location"]
            return int(loc[loc.find("(")+1:loc.find(")")])
        elif request == Request.PATCH:
            return int(path[path.find("(")+1:path.find(")")])
