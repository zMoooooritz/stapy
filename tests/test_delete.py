import unittest
from unittest import mock

from stapy.sta.delete import Delete
from stapy.sta.entity import Entity
from stapy.common.config import config

def mocked_query_request(*args, **kwargs):
    return [1, 2, 15]

class TestDeleteMethods(unittest.TestCase):

    def setUp(self):
        self.API_URL = config.get("API_URL")

    @mock.patch("requests.delete")
    def test_entity(self, mocked_delete):
        Delete.entity(Entity.Datastream, "15")
        params, kparams = mocked_delete.call_args
        self.assertEqual(params[0], self.API_URL + "Datastreams(15)")
        Delete.entity(Entity.Datastream, 15)
        params, kparams = mocked_delete.call_args
        self.assertEqual(params[0], self.API_URL + "Datastreams(15)")
        Delete.entity(Entity.Datastream, [15, 16, 17])
        urls = [f'{self.API_URL}Datastreams({index})' for index in [15, 16, 17]]
        params, kparams = mocked_delete.call_args
        self.assertIn(params[0], urls)
        Delete.entity(Entity.Datastream, "abc")
        with self.assertRaises(Exception):
            Delete.entity("Datastream", 15)

    @mock.patch("stapy.sta.query.Query.get_data_sets", side_effect=mocked_query_request)
    @mock.patch("stapy.sta.delete.Delete.entity")
    def test_query(self, mocked_delete, mocked_query):
        Delete.query("/Datastream")
        params, kparams = mocked_delete.call_args
        self.assertEqual(params[0], Entity.Datastream)
        self.assertEqual(params[1:][0], [1, 2, 15])
        Delete.query("Datastream(15)/Observations")
        params, kparams = mocked_delete.call_args
        self.assertEqual(params[0], Entity.Observation)
        self.assertEqual(params[1:][0], [1, 2, 15])
        Delete.query("Datastream(15)/ObservedProperty?$top=10")
        params, kparams = mocked_delete.call_args
        self.assertEqual(params[0], Entity.ObservedProperty)
        Delete.query("Datastreams?$filter=id gt 10")
        params, kparams = mocked_delete.call_args
        self.assertEqual(params[0], Entity.Datastream)
        with self.assertRaises(Exception):
            Delete.query("(15)/Observations")
        with self.assertRaises(Exception):
            Delete.query("xyz(15)")


if __name__ == "__main__":
    unittest.main()
