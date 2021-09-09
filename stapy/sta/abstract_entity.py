import abc

from stapy.common.util import cast, un_cast, default
from stapy.sta.request import Request
from stapy.sta.entity import Entity

class AbstractEntity(metaclass=abc.ABCMeta):

    entry_map = None
    json = None

    def __init__(self, request=None):
        self.json = {}
        if request == Request.POST:
            self.setup_json()

    def setup_json(self):
        for k, (val_req, val_type) in self.entry_map.items():
            if not val_req:
                continue
            if isinstance(val_type, dict):
                self.json.update({k: {}})
            else:
                self.json.update({k: default(val_type)})

    def set_param(self, **data):
        self.json = self._update_json(self.entry_map, self.json, **data)

    def _update_json(self, template, result, **data):
        for k, (val_req, val_type) in template.items():

            ent = Entity.match(k, threshold=0.5) # 0.8 too big?!
            if ent is not None and k[0].isupper():
                val_is = data.get(ent.value)
                if val_is is None:
                    continue

                # singular
                if k != ent.value:
                    if isinstance(val_is, dict):
                        result.update({k: val_is})
                    else:
                        if isinstance(val_is, list):
                            val_is = val_is[0]
                        result.update({k: {"@iot.id": val_is}})
                # plural
                else:
                    if isinstance(val_is, dict):
                        result.update({k: val_is})
                    else:
                        if not isinstance(val_is, list):
                            val_is = [val_is]
                        ids = []
                        for value in val_is:
                            ids.append({"@iot.id": value})
                        result.update({k: ids})
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
                    except Exception:
                        print("The provided value (" + str(val_is) + ") is not of type "
                            + str(val_type) + " ignoring value")
                        continue

                if not self.check_entry(k, val_is):
                    print("The provided value (" + str(val_is)
                        + ") does not satisfy the requirements ignoring value")
                    continue
                result.update({k: un_cast(val_is)})
            # recursion
            else:
                if not isinstance(val_is, dict):
                    print("The data for (" + k + ") needs to be a dict ignoring data")
                    continue

                if not self.check_entry(k, val_is):
                    print("The provided value (" + str(val_is)
                        + ") does not satisfy the requirements ignoring value")
                    continue

                if k in result.values():
                    result.update({k: self._update_json(val_type, result.get(k), **data.get(k))})
                else:
                    result.update({k: self._update_json(val_type, {}, **data.get(k))})
        return result

    @abc.abstractmethod
    def check_entry(self, key, value):
        raise NotImplementedError
    
    def req_attributes(self):
        return [k for k, v in self.entry_map.items() if v[0]]
    
    def opt_attributes(self):
        return [k for k, v in self.entry_map.items() if not v[0]]

    def get_data(self):
        return self.json
