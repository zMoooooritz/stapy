import unittest
import logging
from unittest import mock

from stapy.sta.post import Post
from stapy.sta.entity import Entity
from stapy.common.config import config

logging.disable(logging.CRITICAL)

def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.ok = status_code < 400
            self.headers = {"location": "(1)"}

        def json(self):
            return self.json_data

    data = kwargs.get("json")
        
    if "name" in data.keys() and data.get("name") == "invalid":
        return MockResponse(kwargs, 404)

    if any(x in args[0] for x in Entity.list()):
        return MockResponse(kwargs, 200)
    return MockResponse({}, 404)

class TestPostMethods(unittest.TestCase):

    def setUp(self):
        self.STA_URL = config.get("STA_URL")

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_datastream(self, mocked_post):
        self.assertEqual(Post.datastream("Test", "Test", {}, "Test", 1, 1, 1), 1)
        self.assertEqual(Post.datastream("invalid", "Test", {}, "Test", 1, 1, 1), -1)
        with self.assertRaises(Exception):
            Post.datastream("Test", "Test", "Test", "Test", 1, 1, 1)

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_full_datastream(self, mocked_post):
        self.assertEqual(Post.full_datastream("Test", "Test", "Test", "Test", {"type": "Point", "coordinates": [1, 2, 3]}, "Test", {}, "Test"), 1)
        with self.assertRaises(Exception):
            self.assertEqual(Post.full_datastream("Test", "Test", "Test", "Test", {"type": "Point", "coordinates": [1, 2, 3]}, "Test", "Test", "Test"), 1)
    
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_featureofinterest(self, mocked_post):
        self.assertEqual(Post.feature_of_interest("Test", "Test", "Test", {"type": "Point", "coordinates": [1, 2, 3]}), 1)
        with self.assertRaises(Exception):
            Post.feature_of_interest("Test", "Test")

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_location(self, mocked_post):
        self.assertEqual(Post.location("Test", "Test", "Test", {"type": "Point", "coordinates": [1, 2, 3]}), 1)
        with self.assertRaises(Exception):
            Post.location("Test", "Test", "Test", {"type": "xyz", "coordinates": [1, 2, 3]})

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_observation(self, mocked_post):
        self.assertEqual(Post.observation("Test", "Test"), 1)
        self.assertEqual(Post.observation("Test", None), 1)
        with self.assertRaises(Exception):
            Post.observation("Test", "Test", result="Tester")

    @mock.patch("requests.post")
    def test_observations(self, mocked_post):
        Post.observations([], [], 1)
        params, kparams = mocked_post.call_args
        self.assertEqual(params[0], self.STA_URL + "CreateObservations")
        self.assertEqual(kparams, {"json": [{"Datastream": {"@iot.id": 1}, "components": ["phenomenonTime", "result"], "dataArray": []}]})
        Post.observations([1, 2, 5], [5, 2, 1], 1)
        params, kparams = mocked_post.call_args
        self.assertEqual(params[0], self.STA_URL + "CreateObservations")
        self.assertEqual(kparams, {"json": [{"Datastream": {"@iot.id": 1}, "components": ["phenomenonTime", "result"], "dataArray": [[5, 1], [2, 2], [1, 5]]}]})
        Post.observations([1, 2, 5], [5, 2, 1], 1, ["key1", "key2"], [["value1", "value2", "value3"], [5, 2, 1]])
        params, kparams = mocked_post.call_args
        self.assertEqual(params[0], self.STA_URL + "CreateObservations")
        self.assertEqual(kparams, {"json": [{"Datastream": {"@iot.id": 1}, "components": ["phenomenonTime", "result", "parameters", "parameters"],
            "dataArray": [[5, 1, {"key1": "value1"}, {"key2": 5}], [2, 2, {"key1": "value2"}, {"key2": 2}], [1, 5, {"key1": "value3"}, {"key2": 1}]]}]})

        Post.observations([1, 2, 5], [5, 2, 1], 1, "key", ["value1", "value2", "value3"])
        params, kparams = mocked_post.call_args
        self.assertEqual(params[0], self.STA_URL + "CreateObservations")
        self.assertEqual(kparams, {"json": [{"Datastream": {"@iot.id": 1}, "components": ["phenomenonTime", "result", "parameters"],
            "dataArray": [[5, 1, {"key": "value1"}], [2, 2, {"key": "value2"}], [1, 5, {"key": "value3"}]]}]})

        with self.assertRaises(Exception):
            Post.observations([], [], 1, ["key1"], [1, 5])

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_observed_property(self, mocked_post):
        self.assertEqual(Post.observed_property("Test", "Test", "Test"), 1)
        self.assertEqual(Post.observed_property("invalid", "Test", "Test"), -1)
        with self.assertRaises(Exception):
            Post.observed_property("invalid", "Test", "Test", "Test")

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_sensor(self, mocked_post):
        self.assertEqual(Post.sensor("Test", "Test", "Test"), 1)
        with self.assertRaises(Exception):
            Post.sensor("Test")

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_thing(self, mocked_post):
        self.assertEqual(Post.thing("Test", "Test"), 1)
        self.assertEqual(Post.thing("invalid", "Test"), -1)
        with self.assertRaises(Exception):
            Post.thing("Test", "Test", location_id="Test")

if __name__ == "__main__":
    unittest.main()
