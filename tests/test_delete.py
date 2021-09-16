import unittest
from unittest import mock

from stapy.sta.delete import Delete
from stapy.sta.entity import Entity

def mocked_delete_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return 1

class TestDeleteMethods(unittest.TestCase):

    @mock.patch("requests.delete", side_effect=mocked_delete_request)
    def test_entity(self, mock_delete):
        Delete.entity(Entity.Datastream, "15")
        Delete.entity(Entity.Datastream, 15)
        Delete.entity(Entity.Datastream, [15, 16, 17])
        with self.assertRaises(Exception):
            Delete.entity("Datastream", 15)

    @mock.patch("requests.delete", side_effect=mocked_delete_request)
    def test_query(self, mock_delete):
        pass
        # Delete.query("Datastream")
        # with self.assertRaises(Exception):
        #     Delete.query("/Datastream(15)")
        # with self.assertRaises(Exception):
        #     Delete.query("xyz(15)")
