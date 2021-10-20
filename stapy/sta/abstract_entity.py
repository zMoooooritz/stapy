import abc

from stapy.common.util import cast, un_cast, default
from stapy.sta.request import Request
from stapy.sta.entity import Entity

class AbstractEntity(metaclass=abc.ABCMeta):
    """
    This abstract class encapsulates some required functions for the classes inside the entities folder
    """

    entry_map = None
    """
    The attribute entry_map has to be overwritten by every Entity that inherits this class
    This dict is build up the following way:
    For each attribute of an entity in the STA it contains a key named the same way
    Each key has a triple as value
    The first value describes whether or not this value is mandatory for the respective entity
    The second value describes whether or not this value can be set from the outside
    And the last value defines the type of the value
    """
    json = None

    def __init__(self, request=None):
        """
        In case the passed request parameter is Post preinitialize json with mandatory data
        :param request: the type of request to send
        """
        self.json = {}
        if request == Request.POST:
            self.setup_json()

    def setup_json(self):
        """
        This method preinitializes the json with the mandatory data / fields
        """
        for k, (val_req, _, val_type) in self.entry_map.items():
            if not val_req:
                continue
            if isinstance(val_type, dict):
                self.json.update({k: {}})
            else:
                self.json.update({k: default(val_type)})

    def set_param(self, **data):
        """
        Update the json with the provided data
        :param data: the data to include in the json
        """
        self.json = self._update_json(self.entry_map, self.json, **data)

    def _update_json(self, template, res_json, **data):
        """
        This method does the core of the work to include the data in the global json dict
        It does include recursive calls to allow for multi-layered data in json
        :param template: defines the format of which the json has to be this is used to parse the data correct
        :param res_json: this parameter contains the current state of the json dict and where to change the data
        :param data: the data to be included in the json dict
        :return: the resulting json with all correct defined entries from data included
        """
        for k, (val_req, _, val_type) in template.items():

            ent = Entity.match(k, threshold=0.8)
            if ent is not None and k[0].isupper():
                val_is = data.get(ent.value)
                if val_is is None:
                    continue

                # singular
                if k != ent.value:
                    if isinstance(val_is, dict):
                        res_json.update({k: val_is})
                    else:
                        if isinstance(val_is, list):
                            val_is = int(val_is[0])
                        res_json.update({k: {"@iot.id": val_is}})
                # plural
                else:
                    if isinstance(val_is, dict):
                        res_json.update({k: val_is})
                    else:
                        if not isinstance(val_is, list):
                            val_is = [val_is]
                        ids = []
                        for value in val_is:
                            ids.append({"@iot.id": int(value)})
                        res_json.update({k: ids})
                continue

            if k not in data.keys():
                continue
            val_is = data.get(k)

            # base case
            if not isinstance(val_type, dict):
                # cast data
                if not isinstance(val_is, val_type):
                    try:
                        val_is = cast(val_type, val_is)
                    except TypeError:
                        raise ValueError("The provided value (" + str(val_is) + ") can not be casted to "
                            + str(val_type))

                if not self.check_entry(k, val_is):
                    raise ValueError("The provided value (" + str(val_is)
                        + ") does not satisfy the requirements")
                res_json.update({k: un_cast(val_is)})
            # recursion
            else:
                if not isinstance(val_is, dict):
                    try:
                        val_is = cast(dict, val_is)
                    except TypeError:
                        raise ValueError("The provided value (" + str(val_is) + ") can not be casted as dict")

                if not self.check_entry(k, val_is):
                    raise ValueError("The provided value (" + str(val_is)
                        + ") does not satisfy the requirements")

                if k in res_json.values():
                    res_json.update({k: self._update_json(val_type, res_json.get(k), **val_is)})
                else:
                    res_json.update({k: self._update_json(val_type, {}, **val_is)})
        return res_json

    @abc.abstractmethod
    def check_entry(self, key, value):
        """
        Abstract method that needs to be implemented in the concrete entities
        It checks whether a given value is of the correct format for a specific key
        """
        raise NotImplementedError
    
    def req_attributes(self):
        """
        Return all required attributes of the concrete entity
        """
        return [k for k, v in self.entry_map.items() if v[0] and v[1]]
    
    def opt_attributes(self):
        """
        Return all required attributes of the concrete entity
        """
        return [k for k, v in self.entry_map.items() if not v[0] and v[1]]

    def get_data(self):
        """
        Return the json data that can be used for POST and PATCH requests
        """
        return self.json
