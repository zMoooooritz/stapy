import unittest
from unittest import mock

from stapy.sta.patch import Patch
from stapy.sta.entity import Entity

def mocked_requests_patch(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.ok = status_code < 400

        def json(self):
            return self.json_data

    data = kwargs.get("json")
        
    if "name" in data.keys() and data.get("name") == "invalid":
        return MockResponse(kwargs, 404)

    if any(x in args[0] for x in Entity.list()):
        return MockResponse(kwargs, 200)
    return MockResponse({}, 404)

class TestPatchMethods(unittest.TestCase):

    @mock.patch("requests.patch", side_effect=mocked_requests_patch)
    def test_datastream(self, mock_patch):
        self.assertEqual(Patch.datastream(2, name="Test", description="Test", unit_of_measurement={}), 2)
        self.assertEqual(Patch.datastream(1, name="invalid"), -1)
        self.assertEqual(Patch.datastream(1, observation_type="Test", properties={}), 1)
        self.assertEqual(Patch.datastream(1, thing_id=2, observed_property_id=3, sensor_id=4), 1)
        with self.assertRaises(Exception):
            Patch.datastream()

    @mock.patch("requests.patch", side_effect=mocked_requests_patch)
    def test_featureofinterest(self, mock_patch):
        self.assertEqual(Patch.feature_of_interest(1, "Test", "Test", "Test", {"type": "Point", "coordinates": [1, 2, 3]}), 1)
        with self.assertRaises(Exception):
            Patch.feature_of_interest(1, "Test", test="Test")

    @mock.patch("requests.patch", side_effect=mocked_requests_patch)
    def test_location(self, mock_patch):
        self.assertEqual(Patch.location(1, "Test", "Test", "Test", {"type": "Point", "coordinates": [1, 2, 3]}), 1)
        with self.assertRaises(Exception):
            Patch.location(1, "Test", "Test", "Test", {"type": "xyz", "coordinates": [1, 2, 3]})

    @mock.patch("requests.patch", side_effect=mocked_requests_patch)
    def test_observation(self, mock_patch):
        self.assertEqual(Patch.observation(1, "Test", "Test"), 1)
        self.assertEqual(Patch.observation(1, "Test", None), 1)
        with self.assertRaises(Exception):
            Patch.observation(1, "Test", "Test", result="Tester")

    @mock.patch("requests.patch", side_effect=mocked_requests_patch)
    def test_observed_property(self, mock_patch):
        self.assertEqual(Patch.observed_property(1, "Test", "Test", "Test"), 1)
        self.assertEqual(Patch.observed_property(1, "invalid", "Test", "Test"), -1)
        with self.assertRaises(Exception):
            Patch.observed_property(1, "invalid", "Test", "Test", "Test")

    @mock.patch("requests.patch", side_effect=mocked_requests_patch)
    def test_sensor(self, mock_patch):
        self.assertEqual(Patch.sensor(1, "Test", "Test", "Test"), 1)
        with self.assertRaises(Exception):
            Patch.sensor(1, "Test", name="Test")

    @mock.patch("requests.patch", side_effect=mocked_requests_patch)
    def test_thing(self, mock_patch):
        self.assertEqual(Patch.thing(1, "Test", "Test"), 1)
        self.assertEqual(Patch.thing(1, "invalid", "Test"), -1)
        with self.assertRaises(Exception):
            Patch.thing(1, "Test", "Test", location_id="Test")

if __name__ == '__main__':
    unittest.main()
