import abc

from stapy.common.defaults import default
from stapy.sta.request import Request

class AbstractEntity(metaclass=abc.ABCMeta):

    entry_map = {}
    json = {}

    def __init__(self, request=None):
        if isinstance(request, Request) and request == Request.POST:
            self.setup_json()

    def setup_json(self):
        for k, v in self.entry_map.items():
            if not v[0]:
                continue
            if isinstance(v[1], dict):
                self.json.update({k: {}})
            else:
                self.json.update({k: default.get(v[1])})

    def set_param(self, **data):
        self.json = self.update_json(self.entry_map, self.json, **data)

    def update_json(self, template, json, **data):
        for k, v in template.items():
            value = v[1]
            if k not in data.keys():
                continue

            # base case
            if not isinstance(value, dict):
                if isinstance(data.get(k), value):
                    if not self.check_entry(k, data.get(k)):
                        print("The provided value (" + str(data.get(k))
                            + ") does not satisfy the requirements ignoring value")
                        continue
                    json.update({k: data.get(k)})
                else:
                    print("The provided value (" + str(data.get(k)) + ") is not of type "
                        + str(v) + " ignoring value")
            # recursion
            else:
                if not isinstance(data.get(k), dict):
                    print("The data for (" + k + ") needs to be a dict ignoring data")
                    continue

                if not self.check_entry(k, data.get(k)):
                    print("The provided value (" + str(data.get(k))
                        + ") does not satisfy the requirements ignoring value")
                    continue
                json.update({k: self.check_set_json(value, json.get(k), **data.get(k))})
        return json

    @abc.abstractmethod
    def check_entry(self, **kwargs):
        raise NotImplementedError
    
    def req_attributes(self):
        return [k for k, v in self.entry_map.items() if v[0]]
    
    def opt_attributes(self):
        return [k for k, v in self.entry_map.items() if not v[0]]

    def get_data(self):
        return self.json
