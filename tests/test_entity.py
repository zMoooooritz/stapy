import unittest
import logging

from stapy.sta.entity import Entity

logging.disable(logging.CRITICAL)

class TestSTAMethods(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_list(self):
        self.assertEqual(len(Entity.list()), len(Entity))
        self.assertIn(Entity.Datastream.value, Entity.list())

    def test_remap(self):
        self.assertEqual(Entity.remap(Entity.Datastream), Entity.Datastream.value)
        self.assertEqual(Entity.remap(Entity.Sensor), "Sensor")
        with self.assertRaises(Exception):
            Entity.remap("FooBar")
    
    def test_match(self):
        self.assertEqual(Entity.match("datastream"), Entity.Datastream)
        self.assertEqual(Entity.match("sens"), Entity.Sensor)
        self.assertEqual(Entity.match("ObservedPropertiess"), Entity.ObservedProperty)
        self.assertIsNone(Entity.match(123))
        self.assertIsNone(Entity.match("xyz"))

if __name__ == "__main__":
    unittest.main()
