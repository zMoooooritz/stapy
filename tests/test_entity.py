from STAPy.sta.entity import Entity

import unittest

class TestSTAMethods(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_list(self):
        self.assertEqual(len(Entity.list()), len(Entity))
        self.assertEqual(Entity.list()[0], Entity.Datastream.value)

    def test_remap(self):
        self.assertEqual(Entity.remap(Entity.Datastream), Entity.Datastream.value)
        self.assertEqual(Entity.remap(Entity.Sensor), "Sensor")
        with self.assertRaises(Exception):
            Entity.remap("FooBar")
    
    def test_match(self):
        self.assertEqual(Entity.match("datastream"), Entity.Datastream)
        self.assertEqual(Entity.match("sens"), Entity.Sensor)
        self.assertEqual(Entity.match("ObservedPropertiess"), Entity.ObservedProperty)
        self.assertEqual(Entity.match("xyz"), None)


if __name__ == '__main__':
    unittest.main()