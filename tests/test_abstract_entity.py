import unittest
import json

import stapy.sta.entities as ent
from stapy.sta.request import Request
from stapy.sta.patch import Patch
from stapy.sta.geo import GeoJSON

class TestAbstractEntityMethods(unittest.TestCase):

    loc = None

    def setUp(self):
        self.loc = {"type": "Point", "coordinates": [1, 2, 3]}

    def test_init(self):
        obprop = ent.ObservedProperty(Request.PATCH)
        self.assertEqual(obprop.get_data(), {})
        obprop = ent.ObservedProperty(Request.POST)
        data = obprop.get_data()
        self.assertIn("name", data)
        self.assertIn("description", data)
        self.assertIn("definition", data)
        self.assertNotIn("properties", data)

    def test_attributes(self):
        obprop = ent.ObservedProperty(Request.PATCH)
        self.assertIn("name", obprop.req_attributes())
        self.assertIn("description", obprop.req_attributes())
        self.assertIn("definition", obprop.req_attributes())
        self.assertNotIn("properties", obprop.req_attributes())
        self.assertIn("properties", obprop.opt_attributes())

    def test_datastream(self):
        datastream = ent.Datastream(Request.PATCH)
        datastream.set_param(name="TestName", properties={"key": "value"},
            Things=123, Observations=[123, 456])
        data = datastream.get_data()
        self.assertEqual(data["name"], "TestName")
        self.assertEqual(data["properties"]["key"], "value")
        self.assertEqual(data["Thing"]["@iot.id"], 123)
        self.assertEqual(data["Observations"], [{"@iot.id": 123},{"@iot.id": 456}])

    def test_featureofinterest(self):
        foi = ent.FeatureOfInterest(Request.POST)
        foi.set_param(encodingType="enc_type")
        foi.set_param(location=self.loc)
        data = foi.get_data()
        self.assertEqual(data["encodingType"], "enc_type")
        self.assertEqual(data["location"], self.loc)

    def test_location(self):
        location = ent.Location(Request.PATCH)
        location.set_param(location=self.loc)
        self.assertEqual(location.get_data()["location"], self.loc)
        location = ent.Location(Request.PATCH)
        location.set_param(locaton={"type": "xyz", "coordinates": [1, 2, 3]})
        self.assertIsNone(location.get_data().get("location"))

    def test_observation(self):
        observation = ent.Observation(Request.POST)
        observation.set_param(Datastreams=[1, 2, 3])
        self.assertEqual(observation.get_data()["Datastream"], {"@iot.id": 1})
        stream = {"@iot.id": [1, 2, 3]}
        observation = ent.Observation(Request.PATCH)
        observation.set_param(Datastreams=stream)
        self.assertEqual(observation.get_data()["Datastream"], stream)

    def test_observedproperty(self):
        obprop = ent.ObservedProperty(Request.PATCH)
        obprop.set_param(name="123")
        self.assertEqual(obprop.get_data()["name"], "123")
        self.assertEqual(len(obprop.get_data()), 1)
        obprop.set_param(properties={"test": "test"})
        self.assertEqual(len(obprop.get_data()), 2)

    def test_sensor(self):
        sensor = ent.Sensor(Request.POST)
        self.assertEqual(len(sensor.get_data()), 4)
        dict_data = {"desc": "description"}
        sensor.set_param(description=dict_data)
        self.assertEqual(json.loads(sensor.get_data()["description"].replace("\'", "\"")), dict_data)

    def test_thing(self):
        thing = ent.Thing(Request.PATCH)
        props = {"xzy": 123, "abc": 987}
        thing.set_param(properties=json.dumps(props))
        self.assertEqual(thing.get_data()["properties"], props)


if __name__ == '__main__':
    unittest.main()
