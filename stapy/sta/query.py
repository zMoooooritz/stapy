import json
import urllib.request

from stapy.sta.entity import Entity
from stapy.common.config import config
from stapy.common.retry import retry

class Query(object):
    """
    This class allows to create queries for the SensorThings API
    """
    _selectors = None
    _params = None
    _sel_entity = None
    _entity_id = None
    _sub_entity = None
    _expands = None
    _data_sets = None

    def __init__(self, entity):
        """
        Construct the base query with the relevant entity
        :param entity: entity that contains the relevant information
        """
        if entity not in Entity:
            raise ValueError("Invalid entity: " + str(entity))
        self._sel_entity = entity.value
        self._selectors = []
        self._params = []
        self._expands = []

    def select(self, *selectors):
        """
        Select a list of attributes that contain the relevant data
        :param selectors: a tuple strings that can contain "." where the first part of each string is the top-level attribute
        :return: self to allow command-chaining
        """
        if len(selectors) == 0:
            raise Exception("no selectors provided")

        sels = []
        for selector in selectors:
            if not isinstance(selector, str):
                raise Exception("invalid selector")
            if "@iot.id" == selector:
                sel_split = [selector]
            else:
                sel_split = selector.split(".")
            sel = sel_split[0]
            if not sel in sels:
                sels.append(sel)
            self._selectors.append(sel_split)
        self._params.append(_build_selpand("select", list(sels)))
        return self

    def filter(self, statement):
        """
        Filter the entity with the given statement
        :param statement: the filter statement
        :return: self to allow command-chaining
        """
        self._params.append("filter=" + statement)
        return self

    def expand(self, expand):
        """
        Expand the entity with another entity
        :param expand: the entity to expand with
        :return: self to allow command-chaining
        """
        self._expands.append(expand)
        return self

    def order(self, attribute, asc=True):
        """
        Sort the resulting data by attribute in the given order
        :param attribute: the attribute to filter by
        :param asc: whether or not to sort ascending
        :return: self to allow command-chaining
        """
        self._params.append("orderby=" + str(attribute) + " " + ("asc" if asc else "desc"))
        return self

    def limit(self, count=10):
        """
        Limit the number entities in the response
        :param count: the number of required entities
        :return: self to allow command-chaining
        """
        self._params.append("top=" + str(count))
        return self

    def max(self):
        """
        Get all available entities
        :return: self to allow command-chaining
        """
        return self.limit(1000)

    def offset(self, count=10):
        """
        Skip over the first count entities in the response
        :param count: the number of entities to skip over
        :return: self to allow command-chaining
        """
        self._params.append("skip=" + str(count))
        return self

    def entity_id(self, entity_id):
        """
        Select a specific entity with the given ID
        :param entity_id: the ID of the relevant entity
        :return: self to allow command-chaining
        """
        self._entity_id = str(entity_id)
        return self

    def sub_entity(self, entity):
        """
        Select a specific sub-entity of a given entity
        This only takes effect if an entity_id is selected
        :param entity: the sub-entity to select
        :return: self to allow command-chaining
        """
        if entity not in Entity:
            raise ValueError("Invalid entity: " + str(entity))
        self._sub_entity = entity.value
        return self

    def get_query(self):
        """
        This method builds the final query defined by all previous calls
        :return: the final query
        """
        entity = self._build_entity()
        expand = "$" + self._build_expands()
        selector = _build_selector(self._params, "&")
        query = config.get("API_URL") + entity
        if len(self._expands) > 0 and len(self._params) > 0:
            query += "?" + expand + "&" + selector
        elif len(self._expands) > 0:
            query += "?" + expand
        elif len(self._params) > 0:
            query += "?" + selector
        return query

    @retry(urllib.error.HTTPError, tries=5, delay=1, backoff=2)
    def urlopen_with_retry(self, path):
        """
        This method retries to fetch data from the specified path according to the retry parameters
        """
        return urllib.request.urlopen(path)

    def get_data_sets(self, count=0):
        """
        This method extracts all data defined by the different given selectors from the data specified by the path
        Each defined selector results in one list in the tuple of lists
        :return: tuple of lists of required data
        """
        if len(self._selectors) == 0:
            return []
        self._data_sets = [[] for _ in range(len(self._selectors))]
        path = self.get_query()
        cnt = 0
        finished = False
        is_list = True
        while True:
            url = self.urlopen_with_retry(path)
            data = json.loads(url.read().decode())
            try:
                payload = data["value"]
            except KeyError:
                payload = data
                is_list = False

            if is_list:
                for value in payload:
                    self.extract_data(value)
                    cnt += 1
                    if cnt == count:
                        finished = True
                        break

                if finished or "@iot.nextLink" not in data:
                    break
                else:
                    path = data["@iot.nextLink"]
            else:
                self.extract_data(payload)
                break

        # TODO this conversion could be non intuitive and therefore result in confusion
        #       as it changes from lists to elements if the lists only contain one element
        if cnt <= 1:
            self._data_sets = [data[0] for data in self._data_sets]
        return self._data_sets[0] if len(self._selectors) == 1 else tuple(self._data_sets)

    def extract_data(self, data):
        """
        This method extracts all data defined by the different selectors from the supplied data
        """
        for idx, selector in enumerate(self._selectors):
            val = data
            for sel in selector:
                try:
                    val = val[sel]
                except (KeyError, TypeError):
                    val = ""
                    break
            self._data_sets[idx].append(val)
    
    def _build_entity(self):
        """
        Build the entity string for the query with the defined entity and possible entity_id and sub_entity
        :return: the entity string
        """
        entity = self._sel_entity
        if self._entity_id is not None:
            entity += "(" + self._entity_id + ")"
            if self._sub_entity is not None:
                entity += "/" + self._sub_entity
        return entity

    def _build_expands(self):
        """
        Build the expand term for the defined expands
        :return: the resulting expand term
        """
        return _build_selpand("expand", self._expands)


class Expand(object):
    """
    This class is similar to the Query but reduced in functionality as it only builds expands for an query
    An expand adds the data of a related entity and can be sel/fil/ord as the other entities
    But this has to be a separate class to avoid not allowed stacking of expands
    """
    _entity = None
    _options = None

    def __init__(self, entity):
        """
        Construct the base expand with the relevant entity
        :param entity: entity that contains the relevant information
        """
        if entity not in Entity:
            raise ValueError("Invalid entity: " + str(entity))
        self._entity = Entity.remap(entity)
        self._options = []

    def select(self, attributes):
        """
        Select a list of attributes that contain the relevant data
        :param attributes: a list of strings each select a top-level attribute in the entity
        :return: self to allow command-chaining
        """
        self._options.append(_build_selpand("select", attributes))
        return self

    def limit(self, count=10):
        """
        Limit the number entities in the response
        :param count: the number of required entities
        :return: self to allow command-chaining
        """
        self._options.append("top=" + str(count))
        return self

    def order(self, attribute, asc=True):
        """
        Sort the resulting data by attribute in the given order
        :param attribute: the attribute to filter by
        :param asc: whether or not to sort ascending
        :return: self to allow command-chaining
        """
        self._options.append("orderBy=" + str(attribute) + " " + ("asc" if asc else "desc"))
        return self

    def filter(self, statement):
        """
        Filter the entity with the given statement
        :param statement: the filter statement
        :return: self to allow command-chaining
        """
        self._options.append("filter=" + str(statement))
        return self

    def expand(self, expand):
        """
        Expand the entity with another entity
        :param expand: the entity to expand with
        :return: self to allow command-chaining
        """
        self._options.append("expand=" + str(expand))
        return self

    def get_expand(self):
        """
        This method builds the final expand defined by all previous calls
        :return: the final expand
        """
        expand = self._entity
        if len(self._options) > 0:
            expand += "(" + _build_selector(self._options, ";") + ")"
        return expand


def _build_selpand(item, attributes):
    """
    This method builds an expand or select term for an STA Query
    :param item: string either expand or select
    :param attributes: a list of strings that has to be expanded / selected
    :return: the resulting select or expand-term
    """
    selector = item + "="
    if not isinstance(attributes, list):
        attributes = [attributes]
    for i, attribute in enumerate(attributes):
        if i != 0:
            selector += ","
        selector += str(attribute)
    return selector

def _build_selector(selectors, separator):
    """
    Build a selector defined by the selector and separator
    :param selectors: a list of strings that are selector
    :param separator: the char that separates the different selectors
    :return: the resulting selector
    """
    selector = ""
    for i, sel in enumerate(selectors):
        if i != 0:
            selector += separator
        selector += "$" + sel.replace(" ", "%20")
    return selector
