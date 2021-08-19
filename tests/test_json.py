#!/usr/bin/env python

from sta.entity import Entity
from sta.json import JSONExtract, JSONSelect

import unittest

class TestJSONMethods(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test(self):
        pass

    def test_select(self):
        self.assertEqual([], JSONSelect().get_selector())
        self.assertNotEqual(JSONSelect().attribute("X").attribute("Y").get_selector(),
                            JSONSelect().attribute("Y").attribute("X").get_selector())

    def test_select_entity(self):
        self.assertEqual([Entity.Datastreams.value], JSONSelect().entity(Entity.Datastreams.value).get_selector())
        self.assertEqual([Entity.Datastreams.value, "FooBar"],
                         JSONSelect().entity(Entity.Datastreams.value).attribute("FooBar").get_selector())
        with self.assertRaises(Exception):
            JSONSelect().entity("FooBar")

    def test_select_attribute(self):
        self.assertEqual(["FooBar"], JSONSelect().attribute("FooBar").get_selector())


if __name__ == '__main__':
    unittest.main()
