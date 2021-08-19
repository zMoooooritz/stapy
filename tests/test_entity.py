#!/usr/bin/env python

from sta.entity import Entity

import unittest

class TestSTAMethods(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_list(self):
        self.assertEqual(len(Entity.list()), 9)
        self.assertEqual(Entity.list()[0], Entity.Datastreams.value)

    def test_remap(self):
        self.assertEqual(Entity.remap(Entity.Datastreams.value), Entity.Datastreams.value)
        self.assertEqual(Entity.remap(Entity.Sensors.value), "Sensor")
        with self.assertRaises(Exception):
            Entity.remap("FooBar")


if __name__ == '__main__':
    unittest.main()
