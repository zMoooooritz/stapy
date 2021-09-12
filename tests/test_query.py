from stapy.sta.query import Query, Expand
from stapy.sta.entity import Entity
from stapy.common.config import config

import unittest

class TestQueryMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.query = Query(Entity.Datastream)
        self.query_alt = Query(Entity.Datastream)
        self.da = Entity.Datastream
        self.API_URL = config.get("API_URL")

    def test_entities(self):
        self.assertEqual(self.query.get_query(), self.API_URL + "Datastreams")

        with self.assertRaises(Exception):
            Query("Foo").get_query()

    def test_select1(self):
        self.assertEqual(self.query.select("id").get_query(), self.API_URL + "Datastreams?$select=id")
        self.assertEqual(self.query_alt.select("id").get_query(), self.API_URL + "Datastreams?$select=id")
        with self.assertRaises(Exception):
            Query(Entity.Datastream).select().get_query()

    def test_select2(self):
        self.assertEqual(self.query.select("id.pi").get_query(), self.API_URL + "Datastreams?$select=id")
        self.assertEqual(self.query_alt.select("id", "pi").get_query(), self.API_URL + "Datastreams?$select=id,pi")
        with self.assertRaises(Exception):
            Query(Entity.Datastream).select(1).get_query()

    def test_filter(self):
        self.assertEqual(self.query.filter("id eq 0").get_query(), self.API_URL + "Datastreams?$filter=id%20eq%200")

    def test_expand(self):
        with self.assertRaises(Exception):
            Expand().get_expand()
        with self.assertRaises(Exception):
            Expand("FooBar").get_expand()
        exp = Expand(Entity.Observation).get_expand()
        self.assertEqual(self.query.expand(exp).get_query(), self.API_URL + "Datastreams?$expand=Observations")

    def test_order(self):
        self.assertEqual(self.query.order("id").get_query(), self.API_URL + "Datastreams?$orderby=id%20asc")

    def test_limit(self):
        self.assertEqual(self.query.limit().get_query(), self.API_URL + "Datastreams?$top=10")
        self.assertEqual(self.query_alt.limit(500).get_query(), self.API_URL + "Datastreams?$top=500")

    def test_max(self):
        self.assertEqual(self.query.limit(1000).get_query(), self.query_alt.max().get_query())

    def test_offset(self):
        self.assertEqual(self.query.offset(10).get_query(), self.API_URL + "Datastreams?$skip=10")

    def test_sub_entity(self):
        self.assertEqual(self.query.sub_entity(Entity.Observation).get_query(), self.API_URL + "Datastreams")
        with self.assertRaises(Exception):
            self.query_alt.sub_entity("Bar").get_query()

    def test_entity_id(self):
        self.assertEqual(self.query.entity_id(1).get_query(), self.API_URL + "Datastreams(1)")
        self.assertEqual(self.query_alt.sub_entity(Entity.Observation).entity_id(10).get_query(),
                         self.API_URL + "Datastreams(10)/Observations")

class TestExpandMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.expand = Expand(Entity.Observation)

        self.API_URL = config.get("API_URL")

    def test_entities(self):
        self.assertEqual(self.expand.get_expand(), "Observations")

        with self.assertRaises(Exception):
            Expand("Foo").get_expand()

    def test_select(self):
        self.assertEqual(self.expand.select("@iot.id").get_expand(), "Observations($select=@iot.id)")
        with self.assertRaises(Exception):
            Expand(Entity.Observation).select("@iot.id", "result").get_expand()

    def test_limit(self):
        self.assertEqual(self.expand.limit().get_expand(), "Observations($top=10)")
        self.assertEqual(Expand(Entity.Observation).limit(100).get_expand(), "Observations($top=100)")

    def test_order(self):
        self.assertEqual(self.expand.order("@iot.id").get_expand(), "Observations($orderBy=@iot.id%20asc)")
        with self.assertRaises(Exception):
            self.expand.order().get_expand()

    def test_filter(self):
        self.assertEqual(self.expand.filter("@iot.id gt 100").get_expand(), "Observations($filter=@iot.id%20gt%20100)")
        with self.assertRaises(Exception):
            Expand(Entity.Observation).filter().get_expand()

    def test_expand(self):
        expand = Expand(Entity.Datastream).get_expand()
        self.assertEqual(self.expand.get_expand(), "Observations")

        self.assertEqual(self.expand.expand(expand).get_expand(), "Observations($expand=Datastreams)")
        with self.assertRaises(Exception):
            Expand(Entity.Observation).expand().get_expand()


if __name__ == '__main__':
    unittest.main()