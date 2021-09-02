import requests
import re

from stapy.sta.query import Query
from stapy.sta.entity import Entity
from stapy.common.config import config

class Delete(object):
    """
    This static class allows to delete existing entities on a STA-Server by sending DELETE-Requests
    """

    @staticmethod
    def entity(entity, ids):
        """
        Delete the entities defined by the entity type and the according ids
        :param entity: the type of entities to delete
        :param ids: a list of entities to delete
        """
        if not isinstance(ids, list):
            ids = [ids]
        for e_id in ids:
            if str(e_id).isdigit():
                try:
                    requests.delete(Query(entity).entity_id(int(e_id)).get_query())
                except Exception:
                    raise Exception("the supplied API_URL \"" + config.get("API_URL") + "\" is not valid")

    @staticmethod
    def query(path):
        """
        Delete the entities by the query path
        :param path: defines all the entities that are supposed to be deleted
        """
        ent = re.split(r"/|\(", path)[0]
        entity = Entity.match(ent)
        if entity is None:
            raise Exception("invalid path: " + path)
        if path.find("(") != -1 and path.find("(") < path.find("/"):
            ent = re.split(r"/|$", path.split("/")[1])[0]
            entity = Entity.match(ent) if Entity.match(ent) is not None else entity

        ids = Query(entity).select("@iot.id").get_data_sets()
        Delete.entity(entity, ids)
