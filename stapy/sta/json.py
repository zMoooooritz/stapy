from stapy.sta.entity import Entity
from stapy.common.retry import retry

import json
import urllib.request
import logging

logger = logging.getLogger('root')

class JSONExtract(object):
    """
    Given a path to an entity in a FROST-Server this class extracts all / count many
    entries according to the defined selector and returns the data as list or tuple of lists
    """

    _path = None
    _count = None
    _selectors = None

    def __init__(self, path, count=0):
        """
        The constructor of the JSONExtract class
        :param path: the STA-Path to retrieve data from
        :param count: restricts the number of elements per list if greater than 0
        """
        self._path = path
        self._count = count
        self._selectors = []

    def select(self, selector):
        """
        Given a string of list of string this method adds the selector for later extraction of data
        :param selector: a string or list of string
        :return: self to allow command-chaining
        """
        if isinstance(selector, list):
            self._selectors.append(selector)
        else:
            self._selectors.append([selector])
        return self

    def multi_select(self, *selectors):
        """
        Given a tuple of lists of strings this method adds the selectors for later extraction of data
        :param selectors: a tuple of lists of strings
        :return: self to allow command-chaining
        """
        for selector in selectors:
            self.select(selector)
        return self

    @retry(urllib.error.HTTPError, tries=5, delay=1, backoff=2, logger=logger)
    def urlopen_with_retry(self, path):
        """
        This method retries to fetch data from the specified path according to the retry parameters
        """
        return urllib.request.urlopen(path)

    def get_data_sets(self):
        """
        This method extracts all data defined by the different given selectors from the data specified by the path
        Each definded selector results in one list in the tuple of lists
        :return: tuple of lists of required data
        """
        if len(self._selectors) == 0:
            return []
        data_sets = [[] for _ in range(len(self._selectors))]
        count = 0
        finished = False
        is_list = True
        while True:
            url = self.urlopen_with_retry(self._path)
            data = json.loads(url.read().decode())
            try:
                payload = data["value"]
            except KeyError:
                payload = data
                is_list = False

            if is_list:
                for value in payload:
                    for idx, selector in enumerate(self._selectors):
                        val = value
                        for sel in selector:
                            try:
                                val = val[sel]
                            except KeyError:
                                val = ""
                                break
                        data_sets[idx].append(val)
                    count += 1
                    if count == self._count:
                        finished = True
                        break

                if finished or "@iot.nextLink" not in data:
                    break
                else:
                    self._path = data["@iot.nextLink"]
            else:
                for idx, selector in enumerate(self._selectors):
                    val = payload
                    for sel in selector:
                        try:
                            val = val[sel]
                        except KeyError:
                            val = ""
                            break
                    data_sets[idx].append(val)
                break

        if len(self._selectors) == 1:
            return data_sets[0]
        else:
            return tuple(data_sets)


class JSONSelect(object):
    """
    This class defines a selector for JSON data,
    each selector represents one property of the json data
    """

    _selectors = None

    def __init__(self):
        """
        Initialize JSONSelect
        """
        self._selectors = []

    def entity(self, entity):
        """
        Select an entity that contains the relevant data for this selector
        :param entity:
        :return: self to allow command-chaining
        """
        if entity not in Entity:
            raise Exception("Invalid entity: " + entity.value)
        self._selectors.append(Entity.remap(entity))
        return self

    def attribute(self, attr):
        """
        Select an attribute that contains the relevant data for this selector
        :param attr:
        :return: self to allow command-chaining
        """
        self._selectors.append(attr)
        return self

    def get_selector(self):
        """
        Returns the final selector formatted as list of strings and numbers
        :return: list of strings and numbers
        """
        return self._selectors
