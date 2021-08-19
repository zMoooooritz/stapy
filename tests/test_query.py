#!/usr/bin/env python

from sta.query import Query, Expand
from sta.entity import Entity
from common.constants import API_URL

import unittest

class TestQueryMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.query = Query(Entity.Datastreams.value)
        self.query_alt = Query(Entity.Datastreams.value)
        self.da = Entity.Datastreams.value

    def test_entities(self):
        self.assertEqual(self.query.get_query(), API_URL + "Datastreams")

        with self.assertRaises(Exception):
            Query("Foo").get_query()

    def test_select(self):
        self.assertEqual(self.query.select("id").get_query(), API_URL + "Datastreams?$select=id")

    def test_multi_select(self):
        self.assertEqual(self.query.select("id").get_query(),
                         self.query_alt.multi_select(["id"]).get_query())
        self.assertEqual(Query(self.da).select(["pi"]).get_query(),
                         Query(self.da).multi_select(["pi", "e"]).get_query())
        with self.assertRaises(Exception):
            Query(Entity.Datastreams.value).multi_select("id").get_query()

    def test_filter(self):
        self.assertEqual(self.query.filter("id eq 0").get_query(), API_URL + "Datastreams?$filter=id%20eq%200")

    def test_expand(self):
        with self.assertRaises(Exception):
            Expand().get_expand()
        with self.assertRaises(Exception):
            Expand("FooBar").get_expand()
        exp = Expand(Entity.Observations.value).get_expand()
        self.assertEqual(self.query.expand(exp).get_query(), API_URL + "Datastreams?$expand=Observations")

    def test_order(self):
        self.assertEqual(self.query.order("id").get_query(), API_URL + "Datastreams?$orderby=id%20asc")

    def test_limit(self):
        self.assertEqual(self.query.limit().get_query(), API_URL + "Datastreams?$top=10")
        self.assertEqual(self.query_alt.limit(500).get_query(), API_URL + "Datastreams?$top=500")

    def test_max(self):
        self.assertEqual(self.query.limit(1000).get_query(), self.query_alt.max().get_query())

    def test_offset(self):
        self.assertEqual(self.query.offset(10).get_query(), API_URL + "Datastreams?$skip=10")

    def test_sub_entity(self):
        self.assertEqual(self.query.sub_entity(Entity.Observations.value).get_query(), API_URL + "Datastreams")
        with self.assertRaises(Exception):
            self.query_alt.sub_entity("Bar").get_query()

    def test_entity_id(self):
        self.assertEqual(self.query.entity_id(1).get_query(), API_URL + "Datastreams(1)")
        self.assertEqual(self.query_alt.sub_entity(Entity.Observations.value).entity_id(10).get_query(),
                         API_URL + "Datastreams(10)/Observations")


if __name__ == '__main__':
    unittest.main()
